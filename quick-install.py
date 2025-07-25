#!/usr/bin/env python3
"""
Quick installation script for the Media Downloader Bot
This script tries multiple installation methods to handle network issues
"""

import subprocess
import sys
import time

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Media Downloader Bot - Quick Installation")
    print("=" * 50)
    
    # Update pip
    run_command("python -m pip install --upgrade pip", "Updating pip")
    
    # Method 1: Try with specific versions
    print("\n📦 Method 1: Installing with specific versions...")
    if run_command("pip install -r requirements.txt", "Installing requirements"):
        print("🎉 Installation completed successfully!")
        return
    
    # Method 2: Try with minimal versions
    print("\n📦 Method 2: Installing with minimal versions...")
    if run_command("pip install -r requirements-minimal.txt", "Installing minimal requirements"):
        print("🎉 Installation completed successfully!")
        return
    
    # Method 3: Install packages individually
    print("\n📦 Method 3: Installing packages individually...")
    packages = [
        "yt-dlp",
        "python-telegram-bot",
        "instaloader",
        "aiohttp",
        "aiofiles",
        "python-dotenv",
        "pyyaml",
        "pillow",
        "requests"
    ]
    
    failed_packages = []
    for package in packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            failed_packages.append(package)
            # Wait a bit before trying next package
            time.sleep(2)
    
    if failed_packages:
        print(f"\n⚠️ Some packages failed to install: {', '.join(failed_packages)}")
        print("You may need to install them manually or check your internet connection.")
    else:
        print("\n🎉 All packages installed successfully!")
    
    print("\n🤖 You can now run the bot with: python main.py")

if __name__ == "__main__":
    main()