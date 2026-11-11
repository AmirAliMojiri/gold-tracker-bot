from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database import db_service
from tgju_service import tgju_service
from states import HoldingStates
from keyboards import (
    get_alerts_menu_keyboard,
    get_alert_items_keyboard,
    get_cancel_keyboard
)

router = Router()

def clean_input_number(text: str) -> str:
    persian_digits = '۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩'
    english_digits = '01234567890123456789'
    table = str.maketrans(persian_digits, english_digits)
    text = text.translate(table)
    text = text.replace('٫', '.').replace('/', '.').replace(',', '').strip()
    return text

def format_price(toman: float) -> str:
    return f"{int(round(toman)):,d} تومان"

ALERT_ITEM_NAMES = {
    'gold_18k': 'طلای ۱۸ عیار',
    'gold_melted': 'طلای آب‌شده',
    'coin_emami': 'سکه تمام امامی',
    'coin_bahar': 'تمام بهار آزادی',
    'coin_half_new': 'نیم سکه',
    'coin_rob_new': 'ربع سکه',
    'currency_usd': 'دلار آمریکا',
    'currency_usdt': 'تتر (USDT)',
    'silver_999': 'نقره ۹۹۹',
}

async def render_alerts_menu(user_id: int) -> tuple[str, InlineKeyboardMarkup]:
    settings = await db_service.get_user_settings(user_id)
    daily_en = bool(settings.get('daily_digest', 1))

    text = (
        "🔔 **مرکز مدیریت هشدارهای هوشمند و اطلاع‌رسانی:**\n\n"
        "در این بخش می‌توانید تارگت‌های قیمتی برای خرید و فروش تنظیم کنید، وضعیت حباب سکه‌ها را رصد کرده و گزارش‌های خودکار شبانه را مدیریت نمایید."
    )
    return text, get_alerts_menu_keyboard(daily_en)

@router.message(Command("alerts"))
@router.message(F.text == "🔔 هشدارهای قیمت")
async def cmd_alerts_menu(message: Message, state: FSMContext):
    await state.clear()
    text, kb = await render_alerts_menu(message.from_user.id)
    await message.answer(text, reply_markup=kb, parse_mode="Markdown")

@router.callback_query(F.data == "btn_alerts_menu")
async def cb_alerts_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    text, kb = await render_alerts_menu(call.from_user.id)
    try:
        await call.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    except Exception:
        await call.message.answer(text, reply_markup=kb, parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "toggle_daily_digest")
async def cb_toggle_daily_digest(call: CallbackQuery):
    new_val = await db_service.toggle_setting(call.from_user.id, 'daily_digest')
    daily_en = bool(new_val)
    status_str = "فعال شد ✅" if daily_en else "غیرفعال شد ❌"
    await call.answer(f"گزارش شبانه (ساعت ۲۱:۰۰) {status_str}")

    text, kb = await render_alerts_menu(call.from_user.id)
    await call.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")

@router.callback_query(F.data == "alert_bubble_radar")
async def cb_bubble_radar(call: CallbackQuery):
    await call.answer("در حال محاسبه حباب‌های بازار...")
    prices = await tgju_service.get_all_prices()
    bubbles = prices.get('bubbles', {})
    coins = prices.get('coins', {})

    lines = [
        "🎈 **رادار تحلیل حباب سکه‌ها (منبع: TGJU.org):**\n",
        "حباب نشان‌دهنده اختلاف قیمت بازار با ارزش طلای سکه است:\n"
    ]

    bubble_map = [
        ('coin_emami', 'bubble_emami', 'سکه امامی'),
        ('coin_bahar', 'bubble_bahar', 'بهار آزادی'),
        ('coin_half_new', 'bubble_nim', 'نیم سکه'),
        ('coin_rob_new', 'bubble_rob', 'ربع سکه'),
        ('coin_grami', 'bubble_grami', 'سکه گرمی'),
    ]

    for c_key, b_key, c_name in bubble_map:
        if b_key in bubbles and c_key in coins:
            b_val = bubbles[b_key]['toman']
            pct = bubbles[b_key].get('percentage', 0.0)
            c_val = coins[c_key]['toman']
            
            status_icon = "🟢 حباب کم" if pct < 15 else ("🟡 حباب متوسط" if pct < 25 else "🔴 حباب بسیار بالا")
            lines.append(
                f"• **{c_name}**:\n"
                f"  ↳ قیمت کل: `{format_price(c_val)}`\n"
                f"  ↳ مقدار حباب: `{format_price(b_val)}` (`{pct}%` از قیمت) - {status_icon}\n"
            )

    lines.append(
        "💡 **توصیه استراتژیک:**\n"
        "هرگاه حباب ربع سکه یا نیم سکه به زیر ۱۵٪ کاهش یابد، بهترین زمان خرید سکه است. در حباب‌های بالاتر، خرید طلای آبشده یا نقره ریسک بسیار کمتری دارد."
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 بازگشت به بخش هشدارها", callback_data="btn_alerts_menu"),
            InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu"),
        ]
    ])
    await call.message.edit_text("\n".join(lines), reply_markup=kb, parse_mode="Markdown")

@router.callback_query(F.data == "alert_new_select")
async def cb_alert_new_select(call: CallbackQuery):
    text = "🎯 **دارایی مورد نظر را برای تنظیم هشدار قیمت انتخاب کنید:**"
    await call.message.edit_text(text, reply_markup=get_alert_items_keyboard(), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data.startswith("setalert_"))
async def cb_setalert_item(call: CallbackQuery, state: FSMContext):
    item_key = call.data.replace("setalert_", "")
    item_title = ALERT_ITEM_NAMES.get(item_key, item_key)

    prices = await tgju_service.get_all_prices()
    curr_p = 0.0
    for cat in ['gold', 'silver', 'coins', 'currencies']:
        if item_key in prices.get(cat, {}):
            curr_p = prices[cat][item_key].get('toman', 0)
            break

    await state.set_state(HoldingStates.waiting_for_alert_price)
    await state.update_data(item_key=item_key, item_title=item_title, current_price=curr_p)

    prompt = (
        f"🎯 **تنظیم هشدار قیمت برای {item_title}:**\n\n"
        f"💰 قیمت فعلی بازار: `{format_price(curr_p)}`\n\n"
        f"لطفاً **قیمت هدف (تارگت)** مدنظر خود را به **تومان** وارد فرمایید.\n"
        f"🔹 مثال: `{int(curr_p * 1.05):,d}`"
    )
    await call.message.edit_text(prompt, reply_markup=get_cancel_keyboard("btn_alerts_menu"), parse_mode="Markdown")
    await call.answer()

@router.message(HoldingStates.waiting_for_alert_price)
async def process_alert_target(message: Message, state: FSMContext):
    data = await state.get_data()
    item_key = data.get('item_key')
    item_title = data.get('item_title')
    curr_p = data.get('current_price', 0.0)

    raw_text = clean_input_number(message.text)
    try:
        target_price = float(raw_text)
        if target_price <= 0:
            raise ValueError()
    except Exception:
        await message.answer(
            "❌ لطفاً یک مبلغ معتبر به تومان وارد کنید:",
            reply_markup=get_cancel_keyboard("btn_alerts_menu")
        )
        return

    direction = 'above' if target_price > curr_p else 'below'
    dir_str = "رسیدن یا عبور به بالای" if direction == 'above' else "رسیدن یا افت به زیرِ"

    await db_service.add_price_alert(
        user_id=message.from_user.id,
        item_key=item_key,
        item_title=item_title,
        target_price=target_price,
        direction=direction
    )
    await state.clear()

    ans = (
        f"✅ **هشدار قیمت با موفقیت ثبت شد!**\n\n"
        f"📌 **دارایی:** {item_title}\n"
        f"🎯 **شرط فعال‌سازی:** {dir_str} `{format_price(target_price)}`\n"
        f"💰 **قیمت فعلی:** `{format_price(curr_p)}`\n\n"
        f"به محض رسیدن بازار به این رقم، ربات در تلگرام به شما پیام هشدار خواهد داد."
    )
    await message.answer(ans, parse_mode="Markdown")

@router.callback_query(F.data == "alert_my_list")
async def cb_my_alerts(call: CallbackQuery):
    alerts = await db_service.get_user_alerts(call.from_user.id)
    if not alerts:
        text = "📋 **شما در حال حاضر هیچ هشدار قیمت فعالی ندارید.**"
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎯 ثبت هشدار جدید", callback_data="alert_new_select")],
            [
                InlineKeyboardButton(text="🔙 بازگشت", callback_data="btn_alerts_menu"),
                InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu"),
            ]
        ])
        await call.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
        await call.answer()
        return

    text = "📋 **لیست هشدارهای قیمت فعال شما:**\n\nبرای حذف هر هشدار، روی دکمه ضربدر کلیک کنید:\n"
    buttons = []
    for al in alerts:
        dir_icon = "📈" if al['direction'] == 'above' else "📉"
        dir_text = "بالای" if al['direction'] == 'above' else "زیر"
        btn_text = f"❌ حذف: {al['item_title']} ({dir_icon} {dir_text} {format_price(al['target_price'])})"
        buttons.append([InlineKeyboardButton(text=btn_text, callback_data=f"delalert_{al['id']}")])

    buttons.append([InlineKeyboardButton(text="➕ ثبت هشدار جدید", callback_data="alert_new_select")])
    buttons.append([
        InlineKeyboardButton(text="🔙 بازگشت به بخش هشدارها", callback_data="btn_alerts_menu"),
        InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu"),
    ])

    await call.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data.startswith("delalert_"))
async def cb_delete_alert(call: CallbackQuery):
    alert_id = int(call.data.replace("delalert_", ""))
    await db_service.delete_alert(alert_id, call.from_user.id)
    await call.answer("هشدار با موفقیت حذف شد.")
    await cb_my_alerts(call)
