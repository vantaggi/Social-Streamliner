import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# === Google Sheets ===
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME")
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")

# === Telegram Bot ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# === Google Gemini AI ===
GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

# === YouTube API ===
YOUTUBE_CLIENT_SECRETS_FILE = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE")

# === Publisher APIs ===
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")

# === Scheduler ===
PUBLISH_SCHEDULE = os.getenv("PUBLISH_SCHEDULE", "09:00,18:00")
