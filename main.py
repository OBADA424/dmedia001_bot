#!/usr/bin/env python3
"""
TikTok/Instagram Media Downloader Telegram Bot

A powerful, production-ready bot that downloads TikTok and Instagram content
and sends it via Telegram.

Features:
- Download TikTok videos and slideshows without watermarks
- Download Instagram posts, reels, and stories
- Auto-detect URLs and platforms
- Generate custom captions with metadata
- Concurrent downloads with rate limiting
- Comprehensive error handling and logging
- Modular architecture for easy maintenance

Author: Generated for production use
License: MIT
"""

import asyncio
import sys
import signal
import os
from pathlib import Path

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config import Config
from src.logger import Logger
from src.telegram_bot import TelegramBot

class MediaDownloaderBotApp:
    def __init__(self):
        self.config = None
        self.logger = None
        self.bot = None
        self.shutdown_event = asyncio.Event()
    
    async def initialize(self):
        """Initialize the application components."""
        try:
            # Load configuration
            self.config = Config()
            
            # Setup logging
            self.logger = Logger(self.config)
            self.logger.info("Starting Media Downloader Bot...")
            
            # Initialize Telegram bot
            self.bot = TelegramBot(self.config, self.logger)
            
            self.logger.info("Application initialized successfully")
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to initialize application: {e}")
            else:
                print(f"Failed to initialize application: {e}")
            sys.exit(1)
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            self.logger.info(f"Received signal {signum}, initiating shutdown...")
            asyncio.create_task(self.shutdown())
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def shutdown(self):
        """Graceful shutdown procedure."""
        self.logger.info("Shutting down bot...")
        self.shutdown_event.set()
    
    async def run(self):
        """Main application runner."""
        await self.initialize()
        self.setup_signal_handlers()
        
        try:
            # Start the bot
            bot_task = asyncio.create_task(self.bot.run())
            shutdown_task = asyncio.create_task(self.shutdown_event.wait())
            
            # Wait for either bot completion or shutdown signal
            done, pending = await asyncio.wait(
                [bot_task, shutdown_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancel pending tasks
            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            
        except Exception as e:
            self.logger.error(f"Application error: {e}")
            sys.exit(1)
        finally:
            self.logger.info("Application shutdown complete")

def main():
    """Main entry point."""
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    # Create and run the application
    app = MediaDownloaderBotApp()
    
    try:
        # Run the async application
        asyncio.run(app.run())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()