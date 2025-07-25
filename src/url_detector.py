import re
from typing import Optional, Dict, Any
from urllib.parse import urlparse, parse_qs

class URLDetector:
    def __init__(self):
        self.patterns = {
            'tiktok': [
                r'https?://(?:www\.)?tiktok\.com/@[\w.-]+/video/(\d+)',
                r'https?://(?:www\.)?tiktok\.com/t/(\w+)',
                r'https?://vm\.tiktok\.com/(\w+)',
                r'https?://(?:www\.)?tiktok\.com/@[\w.-]+/photo/(\d+)',
            ],
            'instagram': [
                r'https?://(?:www\.)?instagram\.com/p/([A-Za-z0-9_-]+)',
                r'https?://(?:www\.)?instagram\.com/reel/([A-Za-z0-9_-]+)',
                r'https?://(?:www\.)?instagram\.com/stories/[\w.-]+/(\d+)',
                r'https?://(?:www\.)?instagram\.com/tv/([A-Za-z0-9_-]+)',
            ]
        }
    
    def detect_platform(self, url: str) -> Optional[str]:
        """Detect which platform the URL belongs to."""
        for platform, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, url, re.IGNORECASE):
                    return platform
        return None
    
    def extract_video_id(self, url: str, platform: str) -> Optional[str]:
        """Extract video/post ID from URL."""
        if platform not in self.patterns:
            return None
            
        for pattern in self.patterns[platform]:
            match = re.search(pattern, url, re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    def clean_url(self, url: str) -> str:
        """Clean URL by removing tracking parameters."""
        parsed = urlparse(url)
        # Remove common tracking parameters
        query_params = parse_qs(parsed.query)
        cleaned_params = {k: v for k, v in query_params.items() 
                         if k not in ['utm_source', 'utm_medium', 'utm_campaign', 'fbclid']}
        
        # Reconstruct URL
        if cleaned_params:
            query_string = '&'.join(f"{k}={v[0]}" for k, v in cleaned_params.items())
            return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{query_string}"
        else:
            return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid and supported."""
        return self.detect_platform(url) is not None