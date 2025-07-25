import yaml
import os
from pathlib import Path
from typing import Dict, Any
import logging

class Config:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self._config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                
            # Validate required fields
            required_fields = ['bot.token']
            for field in required_fields:
                if not self._get_nested_value(config, field):
                    raise ValueError(f"Missing required config field: {field}")
                    
            # Create directories
            os.makedirs(config['downloads']['output_dir'], exist_ok=True)
            os.makedirs(config['downloads']['temp_dir'], exist_ok=True)
            
            return config
            
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            raise
    
    def _get_nested_value(self, data: Dict, key: str) -> Any:
        keys = key.split('.')
        value = data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        return value
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._get_nested_value(self._config, key) or default
    
    @property
    def bot_token(self) -> str:
        return self.get('bot.token')
    
    @property
    def admin_user_id(self) -> int:
        return self.get('bot.admin_user_id')
    
    @property
    def output_dir(self) -> str:
        return self.get('downloads.output_dir')
    
    @property
    def temp_dir(self) -> str:
        return self.get('downloads.temp_dir')
    
    @property
    def max_file_size_mb(self) -> int:
        return self.get('downloads.max_file_size_mb', 50)
    
    @property
    def concurrent_downloads(self) -> int:
        return self.get('downloads.concurrent_downloads', 3)