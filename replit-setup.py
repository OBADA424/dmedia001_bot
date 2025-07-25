#!/usr/bin/env python3
"""
Replit setup script for Telegram bot
This script configures the bot for Replit hosting
"""

import os
import sys
import subprocess

def setup_replit():
    """Setup the bot for Replit hosting"""
    print("🚀 Setting up Telegram Bot for Replit...")
    
    # Create .replit file
    replit_config = """
language = "python3"
run = "python main.py"

[nix]
channel = "stable-22_11"

[deployment]
run = ["sh", "-c", "python main.py"]
"""
    
    with open('.replit', 'w') as f:
        f.write(replit_config)
    print("✅ Created .replit configuration")
    
    # Create pyproject.toml for Poetry
    pyproject_content = """
[tool.poetry]
name = "telegram-media-bot"
version = "1.0.0"
description = "TikTok/Instagram Media Downloader Bot"
author = "Bot Developer"

[tool.poetry.dependencies]
python = "^3.8"
yt-dlp = "^2024.1.0"
python-telegram-bot = "^20.0"
instaloader = "^4.10"
aiohttp = "^3.8.0"
aiofiles = "^23.0.0"
python-dotenv = "^0.19.0"
pyyaml = "^6.0"
pillow = "^9.0.0"
requests = "^2.28.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""
    
    with open('pyproject.toml', 'w') as f:
        f.write(pyproject_content)
    print("✅ Created pyproject.toml for Poetry")
    
    # Create keep_alive.py for 24/7 running
    keep_alive_content = """
from flask import Flask
from threading import Thread
import time

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
"""
    
    with open('keep_alive.py', 'w') as f:
        f.write(keep_alive_content)
    print("✅ Created keep_alive.py for 24/7 running")
    
    # Update main.py to include keep_alive
    print("✅ Bot is ready for Replit!")
    print("\n📋 Next steps:")
    print("1. Upload this project to Replit")
    print("2. Set environment variables in Replit:")
    print("   - TELEGRAM_BOT_TOKEN: 8434259985:AAFFJ-EEj2x5HzysYvK4Ag0t8yJHz0Hy4o8")
    print("   - ADMIN_USER_ID: 933343496")
    print("3. Click 'Run' button")
    print("4. Your bot will be live 24/7!")

if __name__ == "__main__":
    setup_replit()