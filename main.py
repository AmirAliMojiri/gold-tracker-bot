import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from aiohttp import web

from config import BOT_TOKEN, PROXY_URL, WEBHOOK_URL
from database import db_service
from tgju_service import tgju_service
from chart_service import chart_service
from advisor import advisor_service

# مسیر دایرکتوری پایه و فایل‌های استاتیک داشبورد
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("TalaNamaApp")

# ==========================================
# مسیرهای وب‌اپلیکیشن داشبورد طلانما
# ==========================================

async def index_handler(request):
    """ارائه صفحه اصلی داشبورد وب‌اپلیکیشن طلانما"""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return web.FileResponse(index_file)
    return web.Response(text="داشبورد وب طلانما: فایل index.html یافت نشد.", status=404, content_type="text/plain; charset=utf-8")

async def styles_handler(request):
    """ارائه استایل‌های اختصاصی داشبورد"""
    css_file = STATIC_DIR / "styles.css"
    if css_file.exists():
        return web.FileResponse(css_file)
    return web.Response(text="/* styles.css not found */", status=404, content_type="text/css")

async def app_js_handler(request):
    """ارائه اسکریپت جاوااسکریپت داشبورد"""
    js_file = STATIC_DIR / "app.js"
    if js_file.exists():
        return web.FileResponse(js_file)
    return web.Response(text="// app.js not found", status=404, content_type="application/javascript")

async def api_prices_handler(request):
    """API دریافت کلیه نرخ‌های زنده TGJU شامل طلا، سکه، نقره، حباب‌ها، سقف و کف روزانه و شاخص‌های کلان"""
    try:
        force = request.query.get("force", "").lower() in ["true", "1", "yes"]
        prices = await tgju_service.get_all_prices(force_refresh=force)
        return web.json_response(prices)
    except Exception as e:
        logger.error(f"Error fetching prices: {e}")
        return web.json_response({"error": str(e)}, status=500)

async def get_current_user(request):
    auth_header = request.headers.get("Authorization", "")
    token = ""
    if auth_header.startswith("Bearer "):
        token = auth_header[7:].strip()
    elif "token" in request.query:
        token = request.query.get("token", "").strip()
    if not token:
        return None, None
    user = await db_service.get_web_user_by_token(token)
    return user, token

async def api_register_handler(request):
    try:
        body = await request.json()
        username = body.get("username", "")
        password = body.get("password", "")
        display_name = body.get("display_name", "")
        res = await db_service.register_web_user(username, password, display_name)
        status = 200 if res.get("success") else 400
        return web.json_response(res, status=status)
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)

async def api_login_handler(request):
    try:
        body = await request.json()
        username = body.get("username", "")
        password = body.get("password", "")
        res = await db_service.login_web_user(username, password)
        status = 200 if res.get("success") else 400
        return web.json_response(res, status=status)
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)

async def api_me_handler(request):
    user, token = await get_current_user(request)
    if not user:
        return web.json_response({"authenticated": False}, status=401)
    portfolio = await db_service.get_web_user_portfolio(user["id"])
    return web.json_response({
        "authenticated": True,
        "user": user,
        "portfolio": portfolio
    })

async def api_logout_handler(request):
    user, token = await get_current_user(request)
    if token:
        await db_service.logout_web_user(token)
    return web.json_response({"success": True})

async def api_get_portfolio_handler(request):
    user, _ = await get_current_user(request)
    if not user:
        return web.json_response({"error": "Unauthorized"}, status=401)
    portfolio = await db_service.get_web_user_portfolio(user["id"])
    return web.json_response({"portfolio": portfolio})

async def api_save_portfolio_handler(request):
    user, _ = await get_current_user(request)
    if not user:
        return web.json_response({"error": "Unauthorized"}, status=401)
    body = await request.json()
    portfolio = body.get("portfolio", [])
    if isinstance(portfolio, list):
        await db_service.save_web_user_portfolio(user["id"], portfolio)
        return web.json_response({"success": True})
    return web.json_response({"error": "Invalid portfolio format"}, status=400)

async def api_chart_history_handler(request):
    """API تولید سری زمانی و اندیکاتورهای تکنیکال بر اساس آخرین نرخ بازار"""
    try:
        market = request.query.get("market", "iran")
        period = request.query.get("period", "6M")
        prices = await tgju_service.get_all_prices()

        if market == "iran":
            current_price = prices.get("gold", {}).get("gold_18k", {}).get("toman", 0) or 7450000
        elif market == "global":
            current_price = prices.get("macro", {}).get("ons_gold", 0.0) or 2900.0
        elif market == "usd":
            current_price = prices.get("currencies", {}).get("currency_usd", {}).get("toman", 0) or 93500
        elif market == "silver":
            current_price = prices.get("silver", {}).get("silver_999", {}).get("toman", 0) or 110000
        else:
            current_price = 7450000

        data = chart_service.get_market_history(market, period, float(current_price))
        return web.json_response(data)
    except Exception as e:
        logger.error(f"Error in chart history API: {e}")
        return web.json_response({"error": str(e)}, status=500)

async def api_advisor_handler(request):
    """API مشاوره تخصصی مدیریت پورتفولیو، وزن‌دهی بهینه سبد، نسبت طلا به نقره و استراتژی پله‌ای DCA"""
    try:
        budget = 50000000.0
        if request.method == "POST":
            try:
                body = await request.json()
                if isinstance(body, dict) and "budget" in body:
                    budget = float(body["budget"])
            except Exception:
                pass
        else:
            budget_str = request.query.get("budget", "50000000")
            budget = float(budget_str)

        prices = await tgju_service.get_all_prices()
        report = advisor_service.analyze_macro_portfolio(budget, prices)
        return web.json_response(report)
    except Exception as e:
        logger.error(f"Error in advisor API: {e}")
        return web.json_response({"error": str(e)}, status=500)

async def health_check(request):
    """بررسی سلامت سرور و وضعیت استقرار"""
    has_bot = bool(BOT_TOKEN and BOT_TOKEN != "YOUR_TELEGRAM_BOT_TOKEN_HERE")
    return web.json_response({
        "status": "healthy",
        "app": "طلانما | داشبورد هوشمند بازار طلا، سکه، نقره و ارز",
        "service": "running",
        "bot_active": has_bot,
        "mode": "standalone_webapp"
    })

async def setup_bot_commands(bot):
    """تنظیم لیست دستورات رسمی تلگرام در صورت فعال بودن ربات"""
    from aiogram.types import BotCommand
    commands = [
        BotCommand(command="home", description="🏠 خانه و منوی اصلی"),
        BotCommand(command="portfolio", description="💼 دارایی‌های من (پرتفوی)"),
        BotCommand(command="manage", description="➕ ثبت و ویرایش دارایی"),
        BotCommand(command="prices", description="📈 نرخ‌های لحظه‌ای بازار"),
        BotCommand(command="advisor", description="💡 پیشنهاد خرید با بودجه"),
        BotCommand(command="alerts", description="🔔 هشدارهای قیمت"),
        BotCommand(command="help", description="ℹ️ راهنمای ربات"),
    ]
    try:
        await bot.set_my_commands(commands)
        logger.info("✅ منوی دستورات تلگرام با موفقیت ثبت شد.")
    except Exception as e:
        logger.warning(f"ثبت دستورات تلگرام مقدور نشد: {e}")

# ==========================================
# تابع اصلی راه‌اندازی (Web Server + Optional Bot)
# ==========================================

async def main():
    logger.info("🌟 در حال راه‌اندازی سرور جامع طلانما (Web Application + Services)...")

    # راه‌اندازی پایگاه داده محلی
    try:
        await db_service.init_db()
        logger.info("🗄 پایگاه داده آماده‌سازی شد.")
    except Exception as e:
        logger.warning(f"خطا در آماده‌سازی پایگاه داده: {e}")

    # ایجاد برنامه وب aiohttp
    app = web.Application()

    # روت‌های فرانت‌اند وب‌اپلیکیشن
    app.router.add_get("/", index_handler)
    app.router.add_get("/styles.css", styles_handler)
    app.router.add_get("/app.js", app_js_handler)
    if STATIC_DIR.exists():
        app.router.add_static("/static", path=str(STATIC_DIR))

    # روت‌های REST API
    app.router.add_get("/api/prices", api_prices_handler)
    app.router.add_get("/api/chart-history", api_chart_history_handler)
    app.router.add_get("/api/advisor", api_advisor_handler)
    app.router.add_post("/api/advisor", api_advisor_handler)
    app.router.add_get("/health", health_check)
    app.router.add_get("/api/health", health_check)

    # روت‌های حساب کاربری وب و پرتفوی ابری
    app.router.add_post("/api/auth/register", api_register_handler)
    app.router.add_post("/api/auth/login", api_login_handler)
    app.router.add_get("/api/auth/me", api_me_handler)
    app.router.add_post("/api/auth/logout", api_logout_handler)
    app.router.add_get("/api/portfolio", api_get_portfolio_handler)
    app.router.add_post("/api/portfolio", api_save_portfolio_handler)

    # راه‌اندازی ربات تلگرام (اختیاری؛ در پس‌زمینه در صورت موجود بودن توکن)
    bot = None
    dp = None
    scheduler = None
    scheduler_task = None
    has_valid_bot_token = bool(BOT_TOKEN and BOT_TOKEN != "YOUR_TELEGRAM_BOT_TOKEN_HERE")

    if has_valid_bot_token:
        try:
            from aiogram import Bot, Dispatcher
            from aiogram.enums import ParseMode
            from aiogram.fsm.storage.memory import MemoryStorage
            from aiogram.client.default import DefaultBotProperties
            from aiogram.client.session.aiohttp import AiohttpSession
            from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
            from handlers import main_router
            from scheduler import AlertScheduler

            token_preview = f"{BOT_TOKEN[:6]}...{BOT_TOKEN[-4:]}" if len(BOT_TOKEN) > 10 else "VALID"
            logger.info(f"🔑 توکن ربات تلگرام شناسایی شد: {token_preview}")

            session = None
            if PROXY_URL:
                logger.info(f"🌐 اتصال ربات تلگرام با پروکسی: {PROXY_URL}")
                session = AiohttpSession(proxy=PROXY_URL)

            bot = Bot(
                token=BOT_TOKEN,
                session=session,
                default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
            )

            dp = Dispatcher(storage=MemoryStorage())
            dp.include_router(main_router)

            await setup_bot_commands(bot)

            scheduler = AlertScheduler(bot)
            scheduler_task = asyncio.create_task(scheduler.start())

            if WEBHOOK_URL:
                clean_base = WEBHOOK_URL.rstrip("/")
                if not clean_base.startswith("http"):
                    clean_base = f"https://{clean_base}"
                webhook_path = "/webhook"
                full_webhook_url = f"{clean_base}{webhook_path}"
                logger.info(f"🌐 ربات در حالت Webhook: {full_webhook_url}")

                webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
                webhook_requests_handler.register(app, path=webhook_path)
                setup_application(app, dp, bot=bot)

                async def register_webhook_on_start(app_inst):
                    try:
                        await bot.set_webhook(url=full_webhook_url, drop_pending_updates=True)
                        logger.info("🚀 وب‌هوک تلگرام ثبت گردید.")
                    except Exception as err:
                        logger.warning(f"خطا در ثبت وب‌هوک: {err}")

                app.on_startup.append(register_webhook_on_start)
            else:
                # Polling در تسک پس‌زمینه بدون مسدودسازی وب سرور
                async def run_bot_polling():
                    try:
                        await bot.delete_webhook(drop_pending_updates=True)
                        logger.info("📡 ربات در حالت Polling آماده به کار است...")
                        await dp.start_polling(bot)
                    except Exception as err:
                        logger.warning(f"خطای Polling تلگرام (وب سرور بدون مشکل فعال است): {err}")

                asyncio.create_task(run_bot_polling())

        except Exception as e:
            logger.warning(f"⚠️ راه‌اندازی ربات تلگرام انجام نشد: {e} (وب‌اپلیکیشن به صورت کامل در دسترس است)")
    else:
        logger.info("ℹ️ توکن ربات تلگرام تنظیم نشده است. وب‌اپلیکیشن طلانما به صورت ۱۰۰٪ مستقل در حال ارائه خدمات است.")

    # اجرای وب سرور روی پورت تعیین‌شده توسط محیط (Render یا لوکال)
    port = int(os.getenv("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"✨ داشبورد وب طلانما با موفقیت روی آدرس http://0.0.0.0:{port} در دسترس است!")

    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        if scheduler:
            scheduler.stop()
        if scheduler_task:
            scheduler_task.cancel()
        if bot and bot.session:
            await bot.session.close()
        await runner.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("سرور طلانما متوقف شد.")
