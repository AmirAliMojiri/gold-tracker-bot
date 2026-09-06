import os
from pathlib import Path
from dotenv import load_dotenv

# بارگذاری تنظیمات از فایل .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
PROXY_URL = os.getenv("PROXY_URL", "").strip() or None
DB_PATH = os.getenv("DB_PATH", "gold_bot.db").strip()

if not DB_PATH.startswith("/") and not (len(DB_PATH) > 2 and DB_PATH[1] == ":"):
    DB_PATH = str(BASE_DIR / DB_PATH)
