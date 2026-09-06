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
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config import BOT_TOKEN, PROXY_URL, WEBHOOK_URL
from database import db_service
from handlers import main_router
from scheduler import AlertScheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("GoldBot")

async def health_check(request):
    return web.Response(text="TGJU Gold & Coin Bot is running healthy 🚀", status=200)

async def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        logger.error("❌ خطای توکن: متغیر BOT_TOKEN یافت نشد!")
        print("\n" + "="*60)
        print("⚠️ خطا: لطفاً توکن ربات تلگرام خود را در متغیرهای محیطی Render وارد نمایید.")
        print("="*60 + "\n")
        # برای اینکه وب‌سرور بالا بماند و وضعیت خطا را نمایش دهد
        app = web.Application()
        app.router.add_get("/", lambda r: web.Response(text="Error: BOT_TOKEN is missing! Please set BOT_TOKEN in Render Environment Variables.", status=400))
        port = int(os.getenv("PORT", 10000))
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        while True:
            await asyncio.sleep(3600)

    token_preview = f"{BOT_TOKEN[:6]}...{BOT_TOKEN[-4:]}" if len(BOT_TOKEN) > 10 else "VALID"
    logger.info(f"🔑 Bot Token loaded successfully: {token_preview}")

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

    logger.info("🗄 در حال آماده‌سازی پایگاه داده...")
    await db_service.init_db()

    scheduler = AlertScheduler(bot)
    scheduler_task = asyncio.create_task(scheduler.start())

    port = int(os.getenv("PORT", 10000))
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)

    # اگر روی سرور رندر با دامنه اختصاصی هستیم از وبهوک استفاده می‌شود که سریع‌تر و پایدارتر است
    if WEBHOOK_URL:
        clean_base = WEBHOOK_URL.rstrip("/")
        if not clean_base.startswith("http"):
            clean_base = f"https://{clean_base}"
        webhook_path = "/webhook"
        full_webhook_url = f"{clean_base}{webhook_path}"
        logger.info(f"🌐 حالت وب‌هوک فعال شد: {full_webhook_url}")

        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
        )
        webhook_requests_handler.register(app, path=webhook_path)
        setup_application(app, dp, bot=bot)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()

        await bot.set_webhook(url=full_webhook_url, drop_pending_updates=True)
        logger.info(f"🚀 ربات در حالت Webhook با موفقیت روی پورت {port} راه‌اندازی شد...")

        try:
            while True:
                await asyncio.sleep(3600)
        finally:
            scheduler.stop()
            scheduler_task.cancel()
            await bot.delete_webhook()
            await runner.cleanup()
            await bot.session.close()

    else:
        # حالت لانگ پولینگ (برای اجرای محلی روی سیستم یا سرورهای معمولی)
        logger.info("📡 حالت Long Polling فعال شد...")
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()

        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("🚀 ربات در حالت Polling آماده دریافت پیام است...")

        try:
            await dp.start_polling(bot)
        finally:
            scheduler.stop()
            scheduler_task.cancel()
            await runner.cleanup()
            await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("ربات متوقف شد.")
