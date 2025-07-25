# TikTok/Instagram Media Downloader Telegram Bot

A powerful, production-ready Telegram bot that downloads TikTok videos (without watermarks) and Instagram content (posts, reels, stories) and sends them directly to users.

## 🚀 Features

### Core Functionality
- ✅ **TikTok Downloads**: Videos and photo slideshows without watermarks
- ✅ **Instagram Downloads**: Posts, Reels, Stories, and IGTV content
- ✅ **Smart URL Detection**: Auto-detects and parses URLs from messages
- ✅ **Custom Captions**: Generates rich captions with metadata (username, date, likes, etc.)
- ✅ **Error Handling**: Graceful handling of invalid URLs, private content, and network issues

### Performance & Reliability
- ✅ **Async Downloads**: Concurrent downloads with configurable rate limiting
- ✅ **File Size Management**: Respects Telegram's file size limits
- ✅ **Comprehensive Logging**: Rotating logs with multiple levels
- ✅ **Modular Architecture**: Clean, maintainable code structure

### Telegram Integration
- ✅ **Rich UI**: Inline keyboards with quick actions
- ✅ **Media Groups**: Handles slideshows and multiple files
- ✅ **Admin Commands**: Statistics and management commands
- ✅ **User-Friendly**: Clear error messages and progress updates

## 📋 Requirements

- Python 3.8+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Required Python packages (see `requirements.txt`)

## 🔧 Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd tiktok-instagram-telegram-bot
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure the bot**:
   - Copy `config.yaml` and update with your settings
   - Add your Telegram Bot Token
   - Set your admin user ID for management commands

4. **Run the bot**:
```bash
python main.py
```

## ⚙️ Configuration

Edit `config.yaml` to customize the bot behavior:

```yaml
bot:
  token: "YOUR_BOT_TOKEN_HERE"
  admin_user_id: 123456789

downloads:
  output_dir: "./downloads"
  temp_dir: "./temp"
  max_file_size_mb: 50
  concurrent_downloads: 3
  cleanup_after_hours: 24

tiktok:
  quality: "best"
  format: "mp4"
  extract_audio: false

instagram:
  quality: "best"
  download_stories: true
  download_reels: true
  download_posts: true

logging:
  level: "INFO"
  file: "bot.log"
  max_file_size_mb: 10
  backup_count: 5

captions:
  include_username: true
  include_date: true
  include_platform: true
  max_length: 200
```

## 🎯 Usage

### For Users
1. Start a chat with your bot
2. Send `/start` to see the welcome message
3. Send any TikTok or Instagram URL
4. Wait for the bot to download and send the media

### Supported URL Formats
- **TikTok**: 
  - `https://tiktok.com/@username/video/1234567890`
  - `https://vm.tiktok.com/ABC123`
  - `https://tiktok.com/t/ABC123`
- **Instagram**:
  - `https://instagram.com/p/ABC123/`
  - `https://instagram.com/reel/ABC123/`
  - `https://instagram.com/stories/username/1234567890/`

### Commands
- `/start` - Welcome message and instructions
- `/help` - Detailed help and supported formats
- `/stats` - Bot statistics (admin only)

## 🏗️ Architecture

The bot is built with a modular architecture:

```
src/
├── config.py          # Configuration management
├── logger.py          # Logging setup and utilities
├── url_detector.py    # URL detection and parsing
├── downloader.py      # Media download logic
└── telegram_bot.py    # Telegram bot interface

main.py                # Application entry point
config.yaml           # Configuration file
requirements.txt      # Python dependencies
```

### Key Components

1. **Config**: YAML-based configuration with validation
2. **Logger**: Rotating file logs with console output
3. **URLDetector**: Pattern matching for supported platforms
4. **MediaDownloader**: Async downloads using yt-dlp and instaloader
5. **TelegramBot**: Bot interface with rich UI features

## 🔒 Security Features

- **Rate Limiting**: Prevents abuse with concurrent download limits
- **File Size Validation**: Respects Telegram's limitations
- **Error Isolation**: Prevents crashes from individual download failures
- **Admin Controls**: Management commands restricted to admin users
- **Clean URLs**: Removes tracking parameters

## 🚦 Error Handling

The bot handles various error scenarios gracefully:

- **Invalid URLs**: Clear error messages with format examples
- **Private Content**: Informative messages about access restrictions
- **Network Issues**: Retry logic and timeout handling
- **File Size Limits**: Automatic validation and user notification
- **Platform Changes**: Robust parsing with fallback options

## 📊 Logging

Comprehensive logging includes:

- **Download Activity**: Success/failure rates and performance metrics
- **Error Tracking**: Detailed error logs with context
- **User Activity**: Usage patterns and popular content
- **System Health**: Resource usage and performance monitoring

## 🔧 Development

### Adding New Platforms

1. Add URL patterns to `URLDetector`
2. Implement download logic in `MediaDownloader`
3. Update configuration schema
4. Add tests for new functionality

### Customizing UI

- Modify `_create_inline_keyboard()` for different button layouts
- Update caption generation in `_generate_caption()`
- Customize error messages in message handlers

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## 📞 Support

For issues and questions:
- Check the logs in `bot.log`
- Review the configuration settings
- Ensure all dependencies are installed
- Verify your bot token and permissions

## ⚠️ Disclaimer

This bot is for educational and personal use only. Users are responsible for complying with the terms of service of TikTok, Instagram, and Telegram. Respect content creators' rights and platform policies.

## 🔄 Updates

The bot includes robust error handling for platform changes, but regular updates may be needed as social media platforms evolve. Check for updates regularly to ensure continued functionality.