from flask import Flask
from threading import Thread
import time

app = Flask('')

@app.route('/')
def home():
    return """
    <h1>🤖 Telegram Media Downloader Bot</h1>
    <p>✅ Bot is running successfully!</p>
    <p>📊 Status: Active</p>
    <p>🔗 Send TikTok or Instagram URLs to the bot</p>
    """

@app.route('/health')
def health():
    return {"status": "healthy", "bot": "running"}

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    """Keep the bot alive on Replit"""
    t = Thread(target=run)
    t.daemon = True
    t.start()
    print("🌐 Keep-alive server started on port 8080")