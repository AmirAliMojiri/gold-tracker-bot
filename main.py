import asyncio
import logging
import os
import sys
from aiohttp import web
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

# سرور بررسی سلامت برای سازگاری کامل با Web Service های Render و هاست‌های ابری
async def health_handler(request):
    return web.Response(text="TGJU Gold Tracker Bot is running healthy 🚀", status=200)

async def start_health_server(port: int):
    try:
        app = web.Application()
        app.router.add_get("/", health_handler)
        app.router.add_get("/health", health_handler)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        logger.info(f"🌐 Health server started on port {port}")
        return runner
    except Exception as e:
        logger.warning(f"Could not start health server on port {port}: {e}")
        return None

async def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        logger.error("❌ توکن ربات تنظیم نشده است! لطفاً فایل .env یا Environment Variables در Render را با BOT_TOKEN مقداردهی کنید.")
        print("\n" + "="*60)
        print("⚠️ خطا: لطفاً توکن ربات تلگرام خود را در متغیرهای محیطی Render وارد نمایید.")
        print("="*60 + "\n")
        return

    # پورت Render برای پینگ سلامت سرور
    port = int(os.getenv("PORT", 10000))
    runner = await start_health_server(port)

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
        if scheduler:
            scheduler.stop()
        if scheduler_task:
            scheduler_task.cancel()
        if runner:
            await runner.cleanup()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("ربات متوقف شد.")
