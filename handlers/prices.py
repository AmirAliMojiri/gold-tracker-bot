from typing import List
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from tgju_service import tgju_service
from keyboards import get_prices_view_keyboard

router = Router()

def format_price(toman: int | float) -> str:
    if not toman:
        return "۰ تومان"
    return f"{int(round(toman)):,d} تومان"

def format_change(change_str: str) -> str:
    if not change_str:
        return "-"
    return change_str.strip()

async def render_live_prices_summary() -> str:
    prices = await tgju_service.get_all_prices()
    gold_data = prices.get('gold', {})
    silver_data = prices.get('silver', {})
    coins_data = prices.get('coins', {})
    currencies_data = prices.get('currencies', {})
    parsian_data = prices.get('parsian', {})
    macro_data = prices.get('macro', {})
    updated_at = prices.get('updated_at', '')

    lines = [
        "📈 **تابلوی نرخ‌های لحظه‌ای بازار (منبع: TGJU.org)**\n",
        "💡 *برای مشاهده سقف و کف روزانه هر بخش، از دکمه‌های زیر پیام استفاده کنید:*\n"
    ]

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

    # شاخص‌های کلان
    if macro_data:
        lines.append("\n🌐 **شاخص‌های بین‌المللی:**")
        if 'ons_gold' in macro_data:
            lines.append(f"• انس طلای جهانی: `${macro_data['ons_gold']:,.2f}`")
        if 'ons_silver' in macro_data:
            lines.append(f"• انس نقره جهانی: `${macro_data['ons_silver']:,.2f}`")
        if 'gold_silver_ratio' in macro_data:
            lines.append(f"• نسبت طلا به نقره (GSR): `{macro_data['gold_silver_ratio']}`")

    if updated_at:
        lines.append(f"\n🕒 آخرین بروزرسانی: `{updated_at}`")

    return "\n".join(lines)

def render_category_range_block(category_name: str, items_dict: dict, icon: str = "✨") -> List[str]:
    lines = [f"\n{icon} **{category_name}:**"]
    for k, item in items_dict.items():
        title = item.get('title', k)
        cur_p = item.get('toman', 0)
        low_p = item.get('low_toman', cur_p)
        high_p = item.get('high_toman', cur_p)
        chg = item.get('change', '')
        t_str = item.get('time', '')
        
        lines.append(
            f"• **{title}:**\n"
            f"  💰 نرخ زنده: `{format_price(cur_p)}`\n"
            f"  📈 بالاترین (سقف روز): `{format_price(high_p)}`\n"
            f"  📉 پایین‌ترین (کف روز): `{format_price(low_p)}`\n"
            f"  🔄 نوسان روزانه: `{format_change(chg)}`" + (f" | 🕒 `{t_str}`" if t_str else "")
        )
    return lines

async def render_daily_range_view(category: str = "all") -> str:
    prices = await tgju_service.get_all_prices()
    gold_data = prices.get('gold', {})
    silver_data = prices.get('silver', {})
    coins_data = prices.get('coins', {})
    currencies_data = prices.get('currencies', {})
    updated_at = prices.get('updated_at', '')

    lines = ["📊 **گزارش جامع دامنه نوسان و سقف/کف روزانه (منبع: TGJU.org)**\n"]

    if category in ["all", "gold"] and gold_data:
        lines.extend(render_category_range_block("طلا و آبشده", gold_data, "✨"))

    if category in ["all", "silver"] and silver_data:
        lines.extend(render_category_range_block("انواع نقره", silver_data, "⚪️"))

    if category in ["all", "coins"] and coins_data:
        lines.extend(render_category_range_block("مسکوکات طلا (بانکی و قدیم)", coins_data, "🪙"))

    if category in ["all", "currencies"] and currencies_data:
        lines.extend(render_category_range_block("ارزها و تتر", currencies_data, "💵"))

    if updated_at:
        lines.append(f"\n🕒 آخرین بروزرسانی مارکت: `{updated_at}`")

    return "\n".join(lines)

@router.message(Command("prices"))
@router.message(F.text == "📈 نرخ‌های لحظه‌ای بازار")
async def cmd_live_prices(message: Message):
    text = await render_live_prices_summary()
    await message.answer(text, reply_markup=get_prices_view_keyboard("summary"), parse_mode="Markdown")

@router.callback_query(F.data == "btn_live_prices")
@router.callback_query(F.data == "priceview_summary")
async def cb_live_prices_summary(call: CallbackQuery):
    await call.answer("در حال دریافت تابلوی نرخ‌ها...")
    text = await render_live_prices_summary()
    try:
        await call.message.edit_text(text, reply_markup=get_prices_view_keyboard("summary"), parse_mode="Markdown")
    except Exception:
        await call.message.answer(text, reply_markup=get_prices_view_keyboard("summary"), parse_mode="Markdown")

@router.callback_query(F.data.startswith("priceview_range_"))
async def cb_price_range_view(call: CallbackQuery):
    cat = call.data.replace("priceview_range_", "")
    await call.answer("در حال استخراج سقف و کف روزانه...")
    text = await render_daily_range_view(cat)
    try:
        await call.message.edit_text(text, reply_markup=get_prices_view_keyboard(f"range_{cat}"), parse_mode="Markdown")
    except Exception:
        await call.message.answer(text, reply_markup=get_prices_view_keyboard(f"range_{cat}"), parse_mode="Markdown")

