from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from tgju_service import tgju_service

router = Router()

def format_price(toman: int) -> str:
    return f"{toman:,.0f} تومان"

async def render_live_prices_text() -> str:
    prices = await tgju_service.get_all_prices()
    gold_data = prices.get('gold', {})
    silver_data = prices.get('silver', {})
    coins_data = prices.get('coins', {})
    currencies_data = prices.get('currencies', {})
    parsian_data = prices.get('parsian', {})
    updated_at = prices.get('updated_at', '')

    lines = ["📈 **تابلوی نرخ‌های لحظه‌ای بازار (منبع: TGJU.org)**\n"]

    # طلا و آبشده
    lines.append("✨ **طلا و آبشده:**")
    if 'gold_18k' in gold_data:
        lines.append(f"• طلای ۱۸ عیار: `{format_price(gold_data['gold_18k']['toman'])}` (هر گرم)")
    if 'gold_24k' in gold_data:
        lines.append(f"• طلای ۲۴ عیار: `{format_price(gold_data['gold_24k']['toman'])}` (هر گرم)")
    if 'gold_used' in gold_data:
        lines.append(f"• طلای دست دوم: `{format_price(gold_data['gold_used']['toman'])}`")
    if 'mesghal' in gold_data:
        lines.append(f"• مثقال طلا: `{format_price(gold_data['mesghal']['toman'])}`")
    if 'gold_melted' in gold_data:
        lines.append(f"• طلای آبشده: `{format_price(gold_data['gold_melted']['toman'])}`")

    # نقره
    if silver_data:
        lines.append("\n⚪️ **انواع نقره:**")
        if 'silver_999' in silver_data:
            lines.append(f"• گرم نقره ۹۹۹ (شمش/ساچمه): `{format_price(silver_data['silver_999']['toman'])}`")
        if 'silver_925' in silver_data:
            lines.append(f"• گرم نقره ۹۲۵ (استرلینگ): `{format_price(silver_data['silver_925']['toman'])}`")

    # سکه‌های بانکی
    lines.append("\n🪙 **سکه‌های طرح جدید (بانکی):**")
    if 'coin_emami' in coins_data:
        lines.append(f"• سکه امامی (طرح جدید): `{format_price(coins_data['coin_emami']['toman'])}`")
    if 'coin_bahar' in coins_data:
        lines.append(f"• تمام بهار آزادی: `{format_price(coins_data['coin_bahar']['toman'])}`")
    if 'coin_half_new' in coins_data:
        lines.append(f"• نیم سکه (طرح جدید): `{format_price(coins_data['coin_half_new']['toman'])}`")
    if 'coin_rob_new' in coins_data:
        lines.append(f"• ربع سکه (طرح جدید): `{format_price(coins_data['coin_rob_new']['toman'])}`")
    if 'coin_grami' in coins_data:
        lines.append(f"• سکه گرمی: `{format_price(coins_data['coin_grami']['toman'])}`")

    # سکه‌های طرح قدیم
    lines.append("\n🏛 **سکه‌های طرح قدیم (قبل ۸۶):**")
    if 'coin_emami_old' in coins_data:
        lines.append(f"• تمام سکه طرح قدیم: `{format_price(coins_data['coin_emami_old']['toman'])}`")
    if 'coin_half_old' in coins_data:
        lines.append(f"• نیم سکه طرح قدیم: `{format_price(coins_data['coin_half_old']['toman'])}`")
    if 'coin_rob_old' in coins_data:
        lines.append(f"• ربع سکه طرح قدیم: `{format_price(coins_data['coin_rob_old']['toman'])}`")

    # ارزها و تتر
    if currencies_data:
        lines.append("\n💵 **ارزها و تتر:**")
        if 'currency_usd' in currencies_data:
            lines.append(f"• دلار آمریکا: `{format_price(currencies_data['currency_usd']['toman'])}`")
        if 'currency_usdt' in currencies_data:
            lines.append(f"• تتر (USDT): `{format_price(currencies_data['currency_usdt']['toman'])}`")
        if 'currency_eur' in currencies_data:
            lines.append(f"• یورو: `{format_price(currencies_data['currency_eur']['toman'])}`")
        if 'currency_aed' in currencies_data:
            lines.append(f"• درهم امارات: `{format_price(currencies_data['currency_aed']['toman'])}`")
        if 'currency_gbp' in currencies_data:
            lines.append(f"• پوند انگلیس: `{format_price(currencies_data['currency_gbp']['toman'])}`")
        if 'currency_try' in currencies_data:
            lines.append(f"• لیر ترکیه: `{format_price(currencies_data['currency_try']['toman'])}`")
        if 'currency_cad' in currencies_data:
            lines.append(f"• دلار کانادا: `{format_price(currencies_data['currency_cad']['toman'])}`")
        if 'currency_aud' in currencies_data:
            lines.append(f"• دلار استرالیا: `{format_price(currencies_data['currency_aud']['toman'])}`")
        if 'currency_iqd' in currencies_data:
            lines.append(f"• ۱۰۰ دینار عراق: `{format_price(currencies_data['currency_iqd']['toman'])}`")

    # پارسیان
    if parsian_data:
        lines.append("\n🎖 **گزیده‌ای از سکه‌های پارسیان:**")
        sample_weights = ["0.100", "0.200", "0.500", "1.000", "1.500"]
        for sw in sample_weights:
            if sw in parsian_data:
                lines.append(f"• پارسیان {parsian_data[sw]['weight']:g} گرم: `{format_price(parsian_data[sw]['toman'])}`")

    if updated_at:
        lines.append(f"\n🕒 آخرین بروزرسانی: `{updated_at}`")

    return "\n".join(lines)

@router.message(Command("prices"))
@router.message(F.text == "📈 نرخ‌های لحظه‌ای بازار")
async def cmd_live_prices(message: Message):
    text = await render_live_prices_text()
    await message.answer(text, parse_mode="Markdown")

@router.callback_query(F.data == "btn_live_prices")
async def cb_live_prices(call: CallbackQuery):
    await call.answer("در حال استعلام نرخ‌ها...")
    text = await render_live_prices_text()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu")]
    ])
    try:
        await call.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    except Exception:
        await call.message.answer(text, reply_markup=kb, parse_mode="Markdown")
