#!/bin/bash

echo "🚀 Installing Media Downloader Bot dependencies..."

# Update pip first
echo "📦 Updating pip..."
pip install --upgrade pip

# Try installing with different methods
echo "🔄 Attempting installation method 1: Standard install"
if pip install -r requirements.txt; then
    echo "✅ Installation successful!"
    exit 0
fi

echo "⚠️ Method 1 failed, trying method 2: Minimal versions"
if pip install -r requirements-minimal.txt; then
    echo "✅ Installation successful with minimal versions!"
    exit 0
fi

echo "⚠️ Method 2 failed, trying method 3: Individual packages"
packages=(
    "yt-dlp"
    "python-telegram-bot"
    "instaloader"
    "aiohttp"
    "aiofiles"
    "python-dotenv"
    "pyyaml"
    "pillow"
    "requests"
)

for package in "${packages[@]}"; do
    echo "📦 Installing $package..."
    pip install "$package" --no-deps --force-reinstall
done

echo "✅ Installation completed!"
echo "🤖 You can now run: python main.py"