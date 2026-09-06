import asyncio
import logging
from datetime import datetime
import pytz
from aiogram import Bot
from database import db_service
from tgju_service import tgju_service

logger = logging.getLogger("Scheduler")

class AlertScheduler:
    def __init__(self, bot: Bot):
        self.bot = bot
        self._is_running = False
        self._last_digest_date = ""

    def _get_current_price_for_key(self, item_key: str, prices: dict) -> float:
        # جستجو در دسته‌های طلا، نقره، سکه، ارز
        for cat in ['gold', 'silver', 'coins', 'currencies']:
            if item_key in prices.get(cat, {}):
                return float(prices[cat][item_key].get('toman', 0))
        return 0.0

    async def check_price_alerts(self, prices: dict):
        try:
            alerts = await db_service.get_active_alerts()
            for al in alerts:
                alert_id = al['id']
                user_id = al['user_id']
                item_key = al['item_key']
                item_title = al['item_title']
                target = al['target_price']
                direction = al['direction']

                curr_p = self._get_current_price_for_key(item_key, prices)
                if curr_p <= 0:
                    continue

                triggered = False
                if direction == 'above' and curr_p >= target:
                    triggered = True
                elif direction == 'below' and curr_p <= target:
                    triggered = True

                if triggered:
                    dir_str = "بیشتر یا مساوی با" if direction == "above" else "کمتر یا مساوی با"
                    icon = "📈" if direction == "above" else "📉"
                    msg = (
                        f"🚨 **هشدار قیمت فعال شد!** {icon}\n\n"
                        f"📌 **دارایی:** {item_title}\n"
                        f"🎯 **تارگت شما:** `{target:,.0f} تومان` ({dir_str})\n"
                        f"💰 **قیمت لحظه‌ای بازار:** `{curr_p:,.0f} تومان`\n"
                        f"🕒 زمان: `{prices.get('updated_at', '')}`"
                    )
                    try:
                        await self.bot.send_message(chat_id=user_id, text=msg, parse_mode="Markdown")
                        await db_service.deactivate_alert(alert_id)
                        logger.info(f"Alert {alert_id} triggered for user {user_id}")
                    except Exception as e:
                        logger.warning(f"Failed to send alert to user {user_id}: {e}")
        except Exception as e:
            logger.error(f"Error checking price alerts: {e}")

    async def check_daily_digest(self, prices: dict):
        try:
            tehran_tz = pytz.timezone('Asia/Tehran')
            now_tehran = datetime.now(tehran_tz)
            today_str = now_tehran.strftime("%Y-%m-%d")

            # هر روز ساعت ۲۱:۰۰
            if now_tehran.hour == 21 and self._last_digest_date != today_str:
                self._last_digest_date = today_str
                users = await db_service.get_all_digest_users()
                logger.info(f"Sending daily digest to {len(users)} users...")

                for uid in users:
                    try:
                        h = await db_service.get_holdings(uid)
                        main_h = h['main']
                        parsian_h = h['parsian']

                        tot_val = 0.0
                        for field, val in main_h.items():
                            if not field.endswith('_buy') and val > 0:
                                p = self._get_current_price_for_key(field, prices)
                                tot_val += val * p

                        for p in parsian_h:
                            w = p['weight']
                            q = p['quantity']
                            if q > 0:
                                p_price = prices.get('parsian', {}).get(f"{w:.3f}", {}).get('toman', 0) or tgju_service.estimate_parsian_price(w, prices)
                                tot_val += q * p_price

                        if tot_val > 0:
                            digest_msg = (
                                "🌙 **گزارش شبانگاهی وضعیت دارایی شما (Daily Digest):**\n\n"
                                f"💰 **ارزش کل سبد:** `{tot_val:,.0f} تومان`\n"
                                f"🕒 تاریخ و ساعت: `{now_tehran.strftime('%Y/%m/%d - %H:%M')}`\n\n"
                                "برای مشاهده جزئیات کامل و سود/زیان هر دارایی، ربات را باز کنید."
                            )
                            await self.bot.send_message(chat_id=uid, text=digest_msg, parse_mode="Markdown")
                    except Exception as e:
                        logger.warning(f"Failed sending daily digest to {uid}: {e}")
        except Exception as e:
            logger.error(f"Error checking daily digest: {e}")

    async def start(self):
        self._is_running = True
        logger.info("AlertScheduler background task started.")
        while self._is_running:
            try:
                prices = await tgju_service.get_all_prices()
                await self.check_price_alerts(prices)
                await self.check_daily_digest(prices)
            except Exception as e:
                logger.error(f"Scheduler loop error: {e}")
            await asyncio.sleep(60)

    def stop(self):
        self._is_running = False
