import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

from config import BOT_TOKEN, PROXY_URL
from database import db_service
from handlers import main_router
from scheduler import AlertScheduler

# تنظیم لاگ‌ها
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("GoldBot")

async def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        logger.error("❌ توکن ربات تنظیم نشده است! لطفاً فایل .env را ویرایش کرده و BOT_TOKEN را وارد کنید.")
        print("\n" + "="*60)
        print("⚠️ خطا: لطفاً توکن ربات تلگرام خود را در فایل d:\\gemini\\.env وارد نمایید.")
        print("="*60 + "\n")
        return

    session = None
    if PROXY_URL:
        logger.info(f"🌐 استفاده از پروکسی: {PROXY_URL}")
        session = AiohttpSession(proxy=PROXY_URL)

    bot = Bot(
        token=BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(main_router)

    logger.info("🗄 در حال بررسی و آماده‌سازی پایگاه داده...")
    await db_service.init_db()

    # راه‌اندازی تسک پس‌زمینه بررسی هشدارها و گزارش شبانگاهی
    scheduler = AlertScheduler(bot)
    scheduler_task = asyncio.create_task(scheduler.start())

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("🚀 ربات با موفقیت راه‌اندازی شد و آماده دریافت پیام است...")

    try:
        await dp.start_polling(bot)
    finally:
        scheduler.stop()
        scheduler_task.cancel()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("ربات متوقف شد.")
