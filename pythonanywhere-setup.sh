#!/bin/bash

echo "🐍 Setting up bot for PythonAnywhere..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3.10 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing requirements..."
pip install -r requirements.txt

# Create startup script
cat > start_bot.py << 'EOF'
#!/usr/bin/env python3
"""
PythonAnywhere startup script
"""
import os
import sys
import subprocess
import time

def start_bot():
    """Start the bot with proper error handling"""
    while True:
        try:
            print("🤖 Starting Telegram bot...")
            subprocess.run([sys.executable, "main.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Bot crashed with error: {e}")
            print("🔄 Restarting in 10 seconds...")
            time.sleep(10)
        except KeyboardInterrupt:
            print("🛑 Bot stopped by user")
            break

if __name__ == "__main__":
    start_bot()
EOF

chmod +x start_bot.py

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps for PythonAnywhere:"
echo "1. Upload all files to your PythonAnywhere account"
echo "2. Open a Bash console"
echo "3. Run: chmod +x pythonanywhere-setup.sh && ./pythonanywhere-setup.sh"
echo "4. Run: python3.10 start_bot.py"
echo "5. Your bot will be running!"
echo ""
echo "💡 To run 24/7, set up a scheduled task in PythonAnywhere dashboard"