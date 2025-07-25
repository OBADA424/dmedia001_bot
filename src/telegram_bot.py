import asyncio
import os
from typing import List, Dict, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from telegram.constants import ParseMode
from telegram.error import TelegramError

from .url_detector import URLDetector
from .downloader import MediaDownloader

class TelegramBot:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.url_detector = URLDetector()
        self.app = Application.builder().token(config.bot_token).build()
        self.download_semaphore = asyncio.Semaphore(config.concurrent_downloads)
        
        self._register_handlers()
    
    def _register_handlers(self):
        """Register bot command and message handlers."""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("stats", self.stats_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.app.add_handler(CallbackQueryHandler(self.handle_callback_query))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome_message = (
            "🎬 **Media Downloader Bot**\n\n"
            "Send me TikTok or Instagram URLs and I'll download them for you!\n\n"
            "**Supported platforms:**\n"
            "🎵 TikTok (videos and slideshows)\n"
            "📸 Instagram (posts, reels, stories)\n\n"
            "Just paste a URL and I'll handle the rest! ✨\n\n"
            "Use /help for more commands."
        )
        
        await update.message.reply_text(
            welcome_message,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_message = (
            "📋 **Available Commands:**\n\n"
            "/start - Welcome message\n"
            "/help - Show this help message\n"
            "/stats - Bot statistics (admin only)\n\n"
            "**How to use:**\n"
            "1. Copy a TikTok or Instagram URL\n"
            "2. Send it to this bot\n"
            "3. Wait for the download to complete\n"
            "4. Enjoy your media! 🎉\n\n"
            "**Supported formats:**\n"
            "• TikTok videos and photo slideshows\n"
            "• Instagram posts (single/multiple photos)\n"
            "• Instagram Reels\n"
            "• Instagram Stories (public only)\n"
            "• Instagram TV (IGTV)\n\n"
            "**Note:** Files larger than 50MB cannot be sent through Telegram."
        )
        
        await update.message.reply_text(
            help_message,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command (admin only)."""
        if update.effective_user.id != self.config.admin_user_id:
            await update.message.reply_text("❌ This command is only available to administrators.")
            return
        
        # Basic stats - you can expand this
        stats_message = (
            "📊 **Bot Statistics**\n\n"
            f"🤖 Bot is running\n"
            f"📁 Temp directory: {self.config.temp_dir}\n"
            f"💾 Output directory: {self.config.output_dir}\n"
            f"🔄 Max concurrent downloads: {self.config.concurrent_downloads}\n"
            f"📏 Max file size: {self.config.max_file_size_mb}MB\n"
        )
        
        await update.message.reply_text(
            stats_message,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages containing URLs."""
        message_text = update.message.text.strip()
        
        # Check if message contains a URL
        if not self.url_detector.is_valid_url(message_text):
            await update.message.reply_text(
                "❌ Please send a valid TikTok or Instagram URL.\n\n"
                "Supported formats:\n"
                "• TikTok: tiktok.com/@username/video/...\n"
                "• Instagram: instagram.com/p/... or /reel/...",
                disable_web_page_preview=True
            )
            return
        
        # Clean and detect platform
        clean_url = self.url_detector.clean_url(message_text)
        platform = self.url_detector.detect_platform(clean_url)
        
        if not platform:
            await update.message.reply_text(
                "❌ Unsupported URL format. Please check the URL and try again."
            )
            return
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            f"🔄 Processing {platform.title()} URL...\n"
            "This may take a few moments.",
            disable_web_page_preview=True
        )
        
        try:
            # Download media with semaphore for rate limiting
            async with self.download_semaphore:
                async with MediaDownloader(self.config, self.logger) as downloader:
                    files, metadata, caption = await downloader.download_media(clean_url, platform)
                    
                    if not files:
                        await processing_msg.edit_text("❌ No files were downloaded. The content might be private or deleted.")
                        return
                    
                    # Update processing message
                    await processing_msg.edit_text(
                        f"📤 Uploading {len(files)} file(s)...",
                        disable_web_page_preview=True
                    )
                    
                    # Send files
                    await self._send_media_files(update, files, caption, metadata, platform)
                    
                    # Clean up temp files
                    downloader.cleanup_temp_files(files)
                    
                    # Delete processing message
                    await processing_msg.delete()
                    
        except Exception as e:
            self.logger.error(f"Error processing URL {clean_url}: {e}")
            await processing_msg.edit_text(
                f"❌ Error downloading content: {str(e)}\n\n"
                "This could be due to:\n"
                "• Private/deleted content\n"
                "• Unsupported format\n"
                "• Network issues\n"
                "• Platform restrictions"
            )
    
    async def _send_media_files(self, update: Update, files: List[str], caption: str, metadata: Dict[str, Any], platform: str):
        """Send media files to user."""
        try:
            if len(files) == 1:
                # Send single file
                file_path = files[0]
                file_ext = os.path.splitext(file_path)[1].lower()
                
                # Create inline keyboard
                keyboard = self._create_inline_keyboard(metadata, platform)
                
                if file_ext in ['.mp4', '.mov', '.avi']:
                    await update.message.reply_video(
                        video=open(file_path, 'rb'),
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=keyboard
                    )
                else:
                    await update.message.reply_photo(
                        photo=open(file_path, 'rb'),
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=keyboard
                    )
            
            elif len(files) <= 10:  # Telegram limit for media groups
                # Send as media group
                media_group = []
                
                for i, file_path in enumerate(files):
                    file_ext = os.path.splitext(file_path)[1].lower()
                    
                    if file_ext in ['.mp4', '.mov', '.avi']:
                        media_item = InputMediaVideo(
                            media=open(file_path, 'rb'),
                            caption=caption if i == 0 else None,
                            parse_mode=ParseMode.MARKDOWN if i == 0 else None
                        )
                    else:
                        media_item = InputMediaPhoto(
                            media=open(file_path, 'rb'),
                            caption=caption if i == 0 else None,
                            parse_mode=ParseMode.MARKDOWN if i == 0 else None
                        )
                    
                    media_group.append(media_item)
                
                await update.message.reply_media_group(media=media_group)
                
                # Send keyboard separately for media groups
                keyboard = self._create_inline_keyboard(metadata, platform)
                await update.message.reply_text(
                    "⚡ Quick actions:",
                    reply_markup=keyboard
                )
            
            else:
                # Too many files, send individually with progress
                for i, file_path in enumerate(files, 1):
                    file_ext = os.path.splitext(file_path)[1].lower()
                    file_caption = f"{caption}\n\n📁 File {i}/{len(files)}"
                    
                    if file_ext in ['.mp4', '.mov', '.avi']:
                        await update.message.reply_video(
                            video=open(file_path, 'rb'),
                            caption=file_caption,
                            parse_mode=ParseMode.MARKDOWN
                        )
                    else:
                        await update.message.reply_photo(
                            photo=open(file_path, 'rb'),
                            caption=file_caption,
                            parse_mode=ParseMode.MARKDOWN
                        )
        
        except TelegramError as e:
            self.logger.error(f"Telegram error sending files: {e}")
            await update.message.reply_text(
                f"❌ Error sending files: {str(e)}\n"
                "File might be too large or in unsupported format."
            )
        except Exception as e:
            self.logger.error(f"Unexpected error sending files: {e}")
            await update.message.reply_text("❌ Unexpected error occurred while sending files.")
    
    def _create_inline_keyboard(self, metadata: Dict[str, Any], platform: str) -> InlineKeyboardMarkup:
        """Create inline keyboard with quick actions."""
        keyboard = []
        
        # Platform-specific buttons
        if platform == 'tiktok':
            if metadata.get('uploader'):
                keyboard.append([
                    InlineKeyboardButton(
                        f"👤 @{metadata['uploader']}", 
                        url=f"https://tiktok.com/@{metadata['uploader']}"
                    )
                ])
        elif platform == 'instagram':
            if metadata.get('uploader'):
                keyboard.append([
                    InlineKeyboardButton(
                        f"👤 @{metadata['uploader']}", 
                        url=f"https://instagram.com/{metadata['uploader']}"
                    )
                ])
        
        # Additional info button
        info_text = f"Platform: {platform.title()}"
        if metadata.get('like_count'):
            info_text += f"\\nLikes: {metadata['like_count']:,}"
        if metadata.get('view_count'):
            info_text += f"\\nViews: {metadata['view_count']:,}"
        
        keyboard.append([
            InlineKeyboardButton("ℹ️ Info", callback_data=f"info_{platform}")
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard button presses."""
        query = update.callback_query
        await query.answer()
        
        if query.data.startswith("info_"):
            platform = query.data.split("_")[1]
            info_message = (
                f"ℹ️ **{platform.title()} Download Info**\\n\\n"
                f"✅ Successfully downloaded from {platform.title()}\\n"
                f"🤖 Processed by Media Downloader Bot\\n\\n"
                f"Send me more URLs to download! 🎬"
            )
            
            await query.edit_message_text(
                info_message,
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def run(self):
        """Start the bot."""
        self.logger.info("Starting Telegram bot...")
        
        # Initialize and start the bot
        await self.app.initialize()
        await self.app.start()
        
        self.logger.info("Bot started successfully!")
        
        # Keep the bot running
        await self.app.updater.start_polling()
        
        # Wait until the bot is stopped
        await self.app.updater.idle()
        
        # Clean shutdown
        await self.app.stop()
        self.logger.info("Bot stopped.")