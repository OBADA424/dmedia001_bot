import asyncio
import aiohttp
import aiofiles
import yt_dlp
import instaloader
import os
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import re
from datetime import datetime
import hashlib

class MediaDownloader:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.session: Optional[aiohttp.ClientSession] = None
        self.insta_loader = instaloader.Instaloader(
            download_videos=True,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False,
            max_connection_attempts=3
        )
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to be filesystem safe."""
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'[^\w\s-.]', '_', filename)
        return filename.strip()[:100]  # Limit length
    
    def _generate_caption(self, metadata: Dict[str, Any], platform: str) -> str:
        """Generate custom caption from metadata."""
        caption_parts = []
        
        if self.config.get('captions.include_platform', True):
            caption_parts.append(f"📱 {platform.title()}")
        
        if self.config.get('captions.include_username', True) and metadata.get('uploader'):
            caption_parts.append(f"👤 @{metadata['uploader']}")
        
        if self.config.get('captions.include_date', True) and metadata.get('upload_date'):
            try:
                date_obj = datetime.strptime(metadata['upload_date'], '%Y%m%d')
                caption_parts.append(f"📅 {date_obj.strftime('%Y-%m-%d')}")
            except:
                pass
        
        if metadata.get('title'):
            title = metadata['title'][:100] + "..." if len(metadata['title']) > 100 else metadata['title']
            caption_parts.append(f"📝 {title}")
        
        caption = "\n".join(caption_parts)
        max_length = self.config.get('captions.max_length', 200)
        
        return caption[:max_length] if len(caption) > max_length else caption
    
    async def download_tiktok(self, url: str) -> Tuple[List[str], Dict[str, Any]]:
        """Download TikTok video/slideshow."""
        try:
            ydl_opts = {
                'format': f"{self.config.get('tiktok.quality', 'best')}[ext={self.config.get('tiktok.format', 'mp4')}]",
                'outtmpl': os.path.join(self.config.temp_dir, '%(title)s_%(id)s.%(ext)s'),
                'writesubtitles': False,
                'writeautomaticsub': False,
                'extractaudio': self.config.get('tiktok.extract_audio', False),
                'noplaylist': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info first
                info = ydl.extract_info(url, download=False)
                
                # Check file size
                if info.get('filesize') and info['filesize'] > self.config.max_file_size_mb * 1024 * 1024:
                    raise ValueError(f"File too large: {info['filesize']} bytes")
                
                # Download
                ydl.download([url])
                
                # Find downloaded files
                downloaded_files = []
                temp_path = Path(self.config.temp_dir)
                
                # Handle slideshow (multiple images)
                if info.get('_type') == 'playlist':
                    for entry in info['entries']:
                        filename_pattern = f"*{entry['id']}*"
                        matching_files = list(temp_path.glob(filename_pattern))
                        downloaded_files.extend([str(f) for f in matching_files])
                else:
                    # Single video
                    filename_pattern = f"*{info['id']}*"
                    matching_files = list(temp_path.glob(filename_pattern))
                    downloaded_files.extend([str(f) for f in matching_files])
                
                metadata = {
                    'title': info.get('title', 'TikTok Video'),
                    'uploader': info.get('uploader', ''),
                    'upload_date': info.get('upload_date', ''),
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                    'like_count': info.get('like_count', 0),
                    'platform': 'tiktok'
                }
                
                self.logger.info(f"Successfully downloaded TikTok content: {len(downloaded_files)} files")
                return downloaded_files, metadata
                
        except Exception as e:
            self.logger.error(f"Error downloading TikTok video: {e}")
            raise
    
    async def download_instagram(self, url: str) -> Tuple[List[str], Dict[str, Any]]:
        """Download Instagram content."""
        try:
            # Extract shortcode from URL
            shortcode_match = re.search(r'/(?:p|reel|tv)/([A-Za-z0-9_-]+)', url)
            if not shortcode_match:
                raise ValueError("Could not extract Instagram shortcode from URL")
            
            shortcode = shortcode_match.group(1)
            
            # Get post info
            post = instaloader.Post.from_shortcode(self.insta_loader.context, shortcode)
            
            downloaded_files = []
            temp_path = Path(self.config.temp_dir)
            
            # Download main content
            if post.is_video:
                video_url = post.video_url
                filename = f"instagram_{shortcode}.mp4"
                filepath = temp_path / filename
                
                async with self.session.get(video_url) as response:
                    if response.status == 200:
                        async with aiofiles.open(filepath, 'wb') as f:
                            async for chunk in response.content.iter_chunked(8192):
                                await f.write(chunk)
                        downloaded_files.append(str(filepath))
            else:
                # Handle image or slideshow
                if post.mediacount > 1:
                    # Slideshow
                    for i, node in enumerate(post.get_sidecar_nodes()):
                        if node.is_video:
                            media_url = node.video_url
                            ext = 'mp4'
                        else:
                            media_url = node.display_url
                            ext = 'jpg'
                        
                        filename = f"instagram_{shortcode}_{i+1}.{ext}"
                        filepath = temp_path / filename
                        
                        async with self.session.get(media_url) as response:
                            if response.status == 200:
                                async with aiofiles.open(filepath, 'wb') as f:
                                    async for chunk in response.content.iter_chunked(8192):
                                        await f.write(chunk)
                                downloaded_files.append(str(filepath))
                else:
                    # Single image
                    image_url = post.url
                    filename = f"instagram_{shortcode}.jpg"
                    filepath = temp_path / filename
                    
                    async with self.session.get(image_url) as response:
                        if response.status == 200:
                            async with aiofiles.open(filepath, 'wb') as f:
                                async for chunk in response.content.iter_chunked(8192):
                                    await f.write(chunk)
                            downloaded_files.append(str(filepath))
            
            metadata = {
                'title': post.caption[:100] if post.caption else 'Instagram Post',
                'uploader': post.owner_username,
                'upload_date': post.date_utc.strftime('%Y%m%d'),
                'like_count': post.likes,
                'view_count': post.video_view_count if post.is_video else 0,
                'platform': 'instagram'
            }
            
            self.logger.info(f"Successfully downloaded Instagram content: {len(downloaded_files)} files")
            return downloaded_files, metadata
            
        except Exception as e:
            self.logger.error(f"Error downloading Instagram content: {e}")
            raise
    
    async def download_media(self, url: str, platform: str) -> Tuple[List[str], Dict[str, Any], str]:
        """Download media from supported platforms."""
        try:
            if platform == 'tiktok':
                files, metadata = await self.download_tiktok(url)
            elif platform == 'instagram':
                files, metadata = await self.download_instagram(url)
            else:
                raise ValueError(f"Unsupported platform: {platform}")
            
            # Generate caption
            caption = self._generate_caption(metadata, platform)
            
            # Check file sizes
            valid_files = []
            max_size = self.config.max_file_size_mb * 1024 * 1024
            
            for file_path in files:
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    if file_size <= max_size:
                        valid_files.append(file_path)
                    else:
                        self.logger.warning(f"File too large, skipping: {file_path} ({file_size} bytes)")
                        os.remove(file_path)
            
            return valid_files, metadata, caption
            
        except Exception as e:
            self.logger.error(f"Error in download_media: {e}")
            raise
    
    def cleanup_temp_files(self, file_paths: List[str]):
        """Clean up temporary files."""
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.logger.debug(f"Cleaned up temp file: {file_path}")
            except Exception as e:
                self.logger.warning(f"Could not clean up temp file {file_path}: {e}")