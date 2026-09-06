import re
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database import db_service
from tgju_service import tgju_service
from states import HoldingStates
from keyboards import (
    get_categories_keyboard,
    get_gold_items_keyboard,
    get_silver_items_keyboard,
    get_new_coins_keyboard,
    get_old_coins_keyboard,
    get_currency_items_keyboard,
    get_parsian_keyboard,
    get_cancel_keyboard,
    get_skip_buy_price_keyboard,
    get_clear_confirmation_keyboard
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

def format_pl(current_val: float, buy_cost: float) -> str:
    if buy_cost <= 0:
        return ""
    diff = current_val - buy_cost
    pct = (diff / buy_cost) * 100
    if diff > 0:
        return f"\n  ↳ 🟢 سود: `+{format_price(diff)}` (`+{pct:.1f}%`)"
    elif diff < 0:
        return f"\n  ↳ 🔴 زیان: `-{format_price(abs(diff))}` (`{pct:.1f}%`)"
    else:
        return "\n  ↳ ⚪️ سربه‌سر (`0.0%`)"

ITEM_METADATA = {
    # طلا
    'gold_18k': ('طلای ۱۸ عیار', 'گرم', 'gold', '23,000,000'),
    'gold_24k': ('طلای ۲۴ عیار', 'گرم', 'gold', '30,000,000'),
    'gold_used': ('طلای دست دوم', 'گرم', 'gold', '22,500,000'),
    'gold_melted': ('طلای آب‌شده', 'گرم', 'gold', '100,000,000'),
    # نقره
    'silver_999': ('گرم نقره ۹۹۹ (خالص)', 'گرم', 'silver', '500,000'),
    'silver_925': ('گرم نقره ۹۲۵ (استرلینگ)', 'گرم', 'silver', '460,000'),
    # سکه‌های بانکی
    'coin_emami': ('سکه تمام امامی (طرح جدید)', 'عدد', 'coin', '230,000,000'),
    'coin_bahar': ('سکه تمام بهار آزادی', 'عدد', 'coin', '225,000,000'),
    'coin_half_new': ('نیم سکه (طرح جدید)', 'عدد', 'coin', '118,000,000'),
    'coin_rob_new': ('ربع سکه (طرح جدید)', 'عدد', 'coin', '64,000,000'),
    'coin_grami': ('سکه گرمی (بانکی)', 'عدد', 'coin', '35,000,000'),
    # سکه‌های طرح قدیم (قبل ۸۶)
    'coin_emami_old': ('تمام سکه طرح قدیم (قبل ۸۶)', 'عدد', 'coin', '230,000,000'),
    'coin_half_old': ('نیم سکه طرح قدیم (قبل ۸۶)', 'عدد', 'coin', '114,000,000'),
    'coin_rob_old': ('ربع سکه طرح قدیم (قبل ۸۶)', 'عدد', 'coin', '57,000,000'),
    # ارزها
    'currency_usd': ('دلار آمریکا', 'دلار', 'currency', '220,000'),
    'currency_usdt': ('تتر (USDT)', 'تتر', 'currency', '222,000'),
    'currency_eur': ('یورو', 'یورو', 'currency', '255,000'),
    'currency_aed': ('درهم امارات', 'درهم', 'currency', '60,000'),
    'currency_gbp': ('پوند انگلیس', 'پوند', 'currency', '295,000'),
    'currency_try': ('لیر ترکیه', 'لیر', 'currency', '4,500'),
    'currency_cad': ('دلار کانادا', 'دلار', 'currency', '160,000'),
    'currency_aud': ('دلار استرالیا', 'دلار', 'currency', '158,000'),
    'currency_iqd': ('۱۰۰ دینار عراق', 'دینار', 'currency', '160'),
}

async def render_portfolio_summary(user_id: int) -> str:
    holdings_data = await db_service.get_holdings(user_id)
    main_h = holdings_data['main']
    parsian_h = holdings_data['parsian']

    prices = await tgju_service.get_all_prices()
    gold_prices = prices.get('gold', {})
    silver_prices = prices.get('silver', {})
    coin_prices = prices.get('coins', {})
    currency_prices = prices.get('currencies', {})
    parsian_prices = prices.get('parsian', {})

    total_current_value = 0.0
    total_invested_cost = 0.0
    has_any_buy_price = False

    items_output = []

    # طلا
    gold_lines = []
    for field in ['gold_18k', 'gold_24k', 'gold_used', 'gold_melted']:
        amount = main_h.get(field, 0.0)
        if amount and amount > 0:
            buy_price = main_h.get(f"{field}_buy", 0.0)
            unit_price = gold_prices.get(field, {}).get('toman', 0)
            item_val = amount * unit_price
            total_current_value += item_val
            
            title = ITEM_METADATA[field][0]
            line = f"• **{title}**: `{amount:g} گرم` (نرخ روز: `{format_price(unit_price)}`)\n  ↳ ارزش روز: `{format_price(item_val)}`"
            if buy_price > 0:
                has_any_buy_price = True
                cost = amount * buy_price
                total_invested_cost += cost
                line += format_pl(item_val, cost)
            gold_lines.append(line)

    if gold_lines:
        items_output.append("✨ **طلا و آبشده:**\n" + "\n".join(gold_lines))

    # نقره
    silver_lines = []
    for field in ['silver_999', 'silver_925']:
        amount = main_h.get(field, 0.0)
        if amount and amount > 0:
            buy_price = main_h.get(f"{field}_buy", 0.0)
            unit_price = silver_prices.get(field, {}).get('toman', 0)
            item_val = amount * unit_price
            total_current_value += item_val
            
            title = ITEM_METADATA[field][0]
            line = f"• **{title}**: `{amount:g} گرم` (نرخ روز: `{format_price(unit_price)}`)\n  ↳ ارزش روز: `{format_price(item_val)}`"
            if buy_price > 0:
                has_any_buy_price = True
                cost = amount * buy_price
                total_invested_cost += cost
                line += format_pl(item_val, cost)
            silver_lines.append(line)

    if silver_lines:
        items_output.append("⚪️ **انواع نقره:**\n" + "\n".join(silver_lines))

    # سکه‌های بانکی و قدیم
    coin_lines = []
    coin_fields = [
        'coin_emami', 'coin_bahar', 'coin_half_new', 'coin_rob_new', 'coin_grami',
        'coin_emami_old', 'coin_half_old', 'coin_rob_old'
    ]
    for field in coin_fields:
        qty = main_h.get(field, 0.0)
        if qty and qty > 0:
            buy_price = main_h.get(f"{field}_buy", 0.0)
            unit_price = coin_prices.get(field, {}).get('toman', 0)
            item_val = qty * unit_price
            total_current_value += item_val
            
            title = ITEM_METADATA[field][0]
            line = f"• **{title}**: `{int(qty)} عدد` (نرخ روز: `{format_price(unit_price)}`)\n  ↳ ارزش روز: `{format_price(item_val)}`"
            if buy_price > 0:
                has_any_buy_price = True
                cost = qty * buy_price
                total_invested_cost += cost
                line += format_pl(item_val, cost)
            coin_lines.append(line)

    if coin_lines:
        items_output.append("🪙 **انواع سکه‌های بانکی و طرح قدیم:**\n" + "\n".join(coin_lines))

    # ارزها
    curr_lines = []
    currency_fields = [
        'currency_usd', 'currency_usdt', 'currency_eur', 'currency_aed',
        'currency_gbp', 'currency_try', 'currency_cad', 'currency_aud', 'currency_iqd'
    ]
    for field in currency_fields:
        amount = main_h.get(field, 0.0)
        if amount and amount > 0:
            buy_price = main_h.get(f"{field}_buy", 0.0)
            unit_price = currency_prices.get(field, {}).get('toman', 0)
            item_val = amount * unit_price
            total_current_value += item_val
            
            title, unit, _, _ = ITEM_METADATA[field]
            line = f"• **{title}**: `{amount:g} {unit}` (نرخ روز: `{format_price(unit_price)}`)\n  ↳ ارزش روز: `{format_price(item_val)}`"
            if buy_price > 0:
                has_any_buy_price = True
                cost = amount * buy_price
                total_invested_cost += cost
                line += format_pl(item_val, cost)
            curr_lines.append(line)

    if curr_lines:
        items_output.append("💵 **ارزها و تتر:**\n" + "\n".join(curr_lines))

    # پارسیان
    parsian_lines = []
    for p in parsian_h:
        w = p['weight']
        q = p['quantity']
        buy_p = p.get('buy_price', 0.0)
        if q > 0:
            w_key = f"{w:.3f}"
            if w_key in parsian_prices:
                unit_price = parsian_prices[w_key]['toman']
            else:
                unit_price = tgju_service.estimate_parsian_price(w, prices)

            item_val = q * unit_price
            total_current_value += item_val
            
            line = f"• **پارسیان {w:g} گرم**: `{q} عدد` (نرخ روز: `{format_price(unit_price)}`)\n  ↳ ارزش روز: `{format_price(item_val)}`"
            if buy_p > 0:
                has_any_buy_price = True
                cost = q * buy_p
                total_invested_cost += cost
                line += format_pl(item_val, cost)
            parsian_lines.append(line)

    if parsian_lines:
        items_output.append("🎖 **سکه‌های پارسیان:**\n" + "\n".join(parsian_lines))

    if not items_output:
        return (
            "💼 **سبد دارایی‌های شما در حال حاضر خالی است!**\n\n"
            "برای ثبت دارایی‌های خود، از منوی زیر روی دکمه «➕ **ثبت و ویرایش دارایی**» کلیک فرمایید."
        )

    header = "💼 **گزارش لحظه‌ای دارایی‌های من (پرتفوی هوشمند):**\n"
    body = "\n\n".join(items_output)
    
    summary_lines = [
        "\n\n━━━━━━━━━━━━━━━━━━━━",
        "💰 **خلاصه وضعیت کل سرمایه‌گذاری شما:**",
        f"🔹 **ارزش روز کل دارایی:** `{format_price(total_current_value)}`\n   ↳ `{int(total_current_value * 10):,d} ریال`"
    ]

    if has_any_buy_price and total_invested_cost > 0:
        total_diff = total_current_value - total_invested_cost
        total_pct = (total_diff / total_invested_cost) * 100
        summary_lines.append(f"🔹 **کل مبلغ خرید (بهای تمام‌شده):** `{format_price(total_invested_cost)}`")
        if total_diff > 0:
            summary_lines.append(f"📈 **مجموع سود خالص شما:** `+{format_price(total_diff)}` (`+{total_pct:.1f}%` 🟢)")
        elif total_diff < 0:
            summary_lines.append(f"📉 **مجموع زیان شما:** `-{format_price(abs(total_diff))}` (`{total_pct:.1f}%` 🔴)")
        else:
            summary_lines.append("⚪️ **وضعیت بازدهی:** سربه‌سر (`0.0%`)")

    summary_lines.append(f"🕒 زمان استعلام نرخ TGJU: `{prices.get('updated_at', '')}`")
    return header + "\n" + body + "\n".join(summary_lines)

# نمایش دارایی من
@router.message(Command("portfolio"))
@router.message(F.text == "💼 دارایی‌های من (پرتفوی)")
async def cmd_portfolio(message: Message, state: FSMContext):
    await state.clear()
    msg = await render_portfolio_summary(message.from_user.id)
    await message.answer(msg, parse_mode="Markdown")

@router.callback_query(F.data == "btn_portfolio_summary")
async def cb_portfolio_summary(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer("در حال استخراج ارزش دارایی‌ها...")
    msg = await render_portfolio_summary(call.from_user.id)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu"),
        ]
    ])
    try:
        await call.message.edit_text(msg, reply_markup=kb, parse_mode="Markdown")
    except Exception:
        await call.message.answer(msg, reply_markup=kb, parse_mode="Markdown")

# ثبت و ویرایش دارایی
@router.message(Command("manage"))
@router.message(F.text == "➕ ثبت و ویرایش دارایی")
async def cmd_manage(message: Message, state: FSMContext):
    await state.clear()
    text = "📁 **دسته‌بندی دارایی مورد نظر برای ثبت یا ویرایش را انتخاب کنید:**"
    await message.answer(text, reply_markup=get_categories_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "btn_manage_holdings")
async def cb_manage_holdings(call: CallbackQuery, state: FSMContext):
    await state.clear()
    text = "📁 **دسته‌بندی دارایی مورد نظر برای ثبت یا ویرایش را انتخاب کنید:**"
    try:
        await call.message.edit_text(text, reply_markup=get_categories_keyboard(), parse_mode="Markdown")
    except Exception:
        await call.message.answer(text, reply_markup=get_categories_keyboard(), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "cat_gold")
async def cb_cat_gold(call: CallbackQuery):
    text = "✨ **نوع طلا را جهت ثبت یا ویرایش وزن انتخاب کنید:**"
    await call.message.edit_text(text, reply_markup=get_gold_items_keyboard(), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "cat_silver")
async def cb_cat_silver(call: CallbackQuery):
    text = "⚪️ **نوع نقره را جهت ثبت یا ویرایش انتخاب کنید:**"
    await call.message.edit_text(text, reply_markup=get_silver_items_keyboard(), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "cat_coins_new")
async def cb_cat_coins_new(call: CallbackQuery):
    text = "🪙 **نوع سکه بانکی (طرح جدید) را انتخاب کنید:**"
    await call.message.edit_text(text, reply_markup=get_new_coins_keyboard(), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "cat_coins_old")
async def cb_cat_coins_old(call: CallbackQuery):
    text = "🏛 **نوع سکه طرح قدیم (قبل از سال ۸۶) را انتخاب کنید:**"
    await call.message.edit_text(text, reply_markup=get_old_coins_keyboard(), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "cat_currency")
async def cb_cat_currency(call: CallbackQuery):
    text = "💵 **ارز مورد نظر خود را جهت ثبت یا ویرایش انتخاب کنید:**"
    await call.message.edit_text(text, reply_markup=get_currency_items_keyboard(), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "cat_parsian")
async def cb_cat_parsian(call: CallbackQuery):
    text = "🎖 **وزن سکه پارسیان را انتخاب نمایید:**"
    await call.message.edit_text(text, reply_markup=get_parsian_keyboard(), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data.startswith("item_"))
async def cb_select_item(call: CallbackQuery, state: FSMContext):
    field_name = call.data.replace("item_", "")
    if field_name not in ITEM_METADATA:
        await call.answer("آیتم نامعتبر است.")
        return

    title, unit, itype, sample_buy = ITEM_METADATA[field_name]
    await state.set_state(HoldingStates.waiting_for_main_value)
    await state.update_data(field_name=field_name, title=title, unit=unit, itype=itype, sample_buy=sample_buy)

    example = "12.5" if unit == "گرم" else ("1000" if unit in ["دلار", "تتر", "یورو", "درهم", "لیر", "پوند", "دینار"] else "2")
    prompt = (
        f"📝 **ثبت موجودی {title}:**\n\n"
        f"لطفاً مقدار موجودی خود را بر حسب **{unit}** وارد کنید.\n"
        f"🔹 مثال: `{example}`\n"
        f"🔹 برای حذف این دارایی از سبد، عدد `0` را ارسال کنید."
    )
    await call.message.edit_text(prompt, reply_markup=get_cancel_keyboard(), parse_mode="Markdown")
    await call.answer()

@router.message(HoldingStates.waiting_for_main_value)
async def process_main_value(message: Message, state: FSMContext):
    data = await state.get_data()
    field_name = data.get('field_name')
    title = data.get('title')
    unit = data.get('unit')
    sample_buy = data.get('sample_buy', '1,000,000')

    raw_text = clean_input_number(message.text)
    try:
        value = float(raw_text)
        if value < 0:
            raise ValueError()
    except Exception:
        await message.answer(
            f"❌ لطفاً یک مقدار معتبر و مثبت برای **{unit}** وارد کنید (مثال: {'5.4' if unit == 'گرم' else '2'}).",
            reply_markup=get_cancel_keyboard()
        )
        return

    if value == 0:
        await db_service.update_main_holding(message.from_user.id, field_name, 0.0, 0.0)
        await state.clear()
        ans = f"✅ **{title}** با موفقیت از سبد دارایی شما حذف شد."
        await message.answer(ans, parse_mode="Markdown")
        return

    await state.update_data(amount=value)
    await state.set_state(HoldingStates.waiting_for_main_buy_price)

    prompt = (
        f"💰 **ثبت میانگین قیمت خرید (جهت محاسبه سود/زیان):**\n\n"
        f"موجودی ثبت‌شده: `{value:g} {unit}`\n\n"
        f"لطفاً **میانگین قیمت خرید به ازای هر {unit}** را به **تومان** وارد کنید.\n"
        f"🔹 مثال: `{sample_buy}`\n\n"
        f"💡 در صورت عدم تمایل به محاسبه سود/زیان، دکمه زیر را بزنید:"
    )
    await message.answer(prompt, reply_markup=get_skip_buy_price_keyboard("skip_main_buy_price"), parse_mode="Markdown")

@router.callback_query(F.data == "skip_main_buy_price")
async def cb_skip_main_buy_price(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    field_name = data.get('field_name')
    title = data.get('title')
    unit = data.get('unit')
    amount = data.get('amount', 0.0)

    await db_service.update_main_holding(call.from_user.id, field_name, amount, 0.0)
    await state.clear()

    ans = f"✅ موجودی **{title}** به مقدار `{amount:g} {unit}` (بدون قیمت خرید) ثبت و ذخیره شد."
    await call.message.edit_text(ans, parse_mode="Markdown")
    await call.answer("دارایی ثبت شد.")

@router.message(HoldingStates.waiting_for_main_buy_price)
async def process_main_buy_price(message: Message, state: FSMContext):
    data = await state.get_data()
    field_name = data.get('field_name')
    title = data.get('title')
    unit = data.get('unit')
    amount = data.get('amount', 0.0)

    raw_text = clean_input_number(message.text)
    try:
        buy_price = float(raw_text)
        if buy_price < 0:
            raise ValueError()
    except Exception:
        await message.answer(
            "❌ لطفاً یک مبلغ معتبر به تومان وارد کنید (یا دکمه رد شدن را بزنید):",
            reply_markup=get_skip_buy_price_keyboard("skip_main_buy_price")
        )
        return

    await db_service.update_main_holding(message.from_user.id, field_name, amount, buy_price)
    await state.clear()

    ans = (
        f"✅ موجودی **{title}** با موفقیت در دیتابیس شما ذخیره شد:\n"
        f"🔹 مقدار: `{amount:g} {unit}`\n"
        f"🔹 قیمت خرید واحد: `{format_price(buy_price)}`"
    )
    await message.answer(ans, parse_mode="Markdown")

# پارسیان
@router.callback_query(F.data.startswith("parsian_"))
async def cb_select_parsian(call: CallbackQuery, state: FSMContext):
    val = call.data.replace("parsian_", "")
    
    if val == "custom":
        await state.set_state(HoldingStates.waiting_for_parsian_weight)
        prompt = (
            "⚖️ **ثبت سکه پارسیان با وزن دلخواه:**\n\n"
            "لطفاً وزن سکه پارسیان را بر حسب **گرم** ارسال کنید.\n"
            "🔹 مثال: `0.350` یا `1.75`"
        )
        await call.message.edit_text(prompt, reply_markup=get_cancel_keyboard("cat_parsian"), parse_mode="Markdown")
        await call.answer()
        return

    try:
        weight = float(val)
    except ValueError:
        await call.answer("وزن نامعتبر است.")
        return

    await state.set_state(HoldingStates.waiting_for_parsian_quantity)
    await state.update_data(parsian_weight=weight)
    prompt = (
        f"🎖 **ثبت سکه پارسیان {weight:g} گرمی:**\n\n"
        f"لطفاً **تعداد** این سکه را به عدد وارد کنید.\n"
        f"🔹 مثال: `3`\n"
        f"🔹 برای حذف، عدد `0` را ارسال فرمایید."
    )
    await call.message.edit_text(prompt, reply_markup=get_cancel_keyboard("cat_parsian"), parse_mode="Markdown")
    await call.answer()

@router.message(HoldingStates.waiting_for_parsian_weight)
async def process_parsian_weight(message: Message, state: FSMContext):
    raw_text = clean_input_number(message.text)
    try:
        weight = float(raw_text)
        if weight <= 0 or weight > 100:
            raise ValueError()
    except Exception:
        await message.answer(
            "❌ لطفاً یک وزن معتبر و مثبت به گرم وارد کنید (مثال: `0.450` یا `1.2`):",
            reply_markup=get_cancel_keyboard("cat_parsian")
        )
        return

    await state.set_state(HoldingStates.waiting_for_parsian_quantity)
    await state.update_data(parsian_weight=weight)
    prompt = (
        f"🎖 **سکه پارسیان {weight:g} گرمی:**\n\n"
        f"اکنون لطفاً **تعداد** این سکه را به عدد وارد فرمایید (مثال: `2`):"
    )
    await message.answer(prompt, reply_markup=get_cancel_keyboard("cat_parsian"), parse_mode="Markdown")

@router.message(HoldingStates.waiting_for_parsian_quantity)
async def process_parsian_quantity(message: Message, state: FSMContext):
    data = await state.get_data()
    weight = data.get('parsian_weight', 0.0)

    raw_text = clean_input_number(message.text)
    try:
        qty = int(float(raw_text))
        if qty < 0:
            raise ValueError()
    except Exception:
        await message.answer(
            "❌ لطفاً تعداد معتبر وارد کنید (مثال: `2` یا `0` برای حذف):",
            reply_markup=get_cancel_keyboard("cat_parsian")
        )
        return

    if qty == 0:
        await db_service.update_parsian_holding(message.from_user.id, weight, 0, 0.0)
        await state.clear()
        ans = f"✅ سکه پارسیان `{weight:g} گرمی` از دارایی‌های شما حذف شد."
        await message.answer(ans, parse_mode="Markdown")
        return

    await state.update_data(parsian_qty=qty)
    await state.set_state(HoldingStates.waiting_for_parsian_buy_price)

    prompt = (
        f"💰 **ثبت میانگین قیمت خرید سکه پارسیان {weight:g} گرمی:**\n\n"
        f"تعداد: `{qty} عدد`\n\n"
        f"لطفاً **قیمت خرید هر یک عدد از این سکه** را به **تومان** وارد کنید (مثال: `12,000,000`):\n"
        f"💡 در صورت عدم تمایل به محاسبه سود/زیان، دکمه رد شدن را بزنید:"
    )
    await message.answer(prompt, reply_markup=get_skip_buy_price_keyboard("skip_parsian_buy_price"), parse_mode="Markdown")

@router.callback_query(F.data == "skip_parsian_buy_price")
async def cb_skip_parsian_buy_price(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    weight = data.get('parsian_weight', 0.0)
    qty = data.get('parsian_qty', 0)

    await db_service.update_parsian_holding(call.from_user.id, weight, qty, 0.0)
    await state.clear()

    ans = f"✅ تعداد `{qty} عدد` سکه پارسیان `{weight:g} گرمی` با موفقیت ذخیره شد."
    await call.message.edit_text(ans, parse_mode="Markdown")
    await call.answer("پارسیان ثبت شد.")

@router.message(HoldingStates.waiting_for_parsian_buy_price)
async def process_parsian_buy_price(message: Message, state: FSMContext):
    data = await state.get_data()
    weight = data.get('parsian_weight', 0.0)
    qty = data.get('parsian_qty', 0)

    raw_text = clean_input_number(message.text)
    try:
        buy_price = float(raw_text)
        if buy_price < 0:
            raise ValueError()
    except Exception:
        await message.answer(
            "❌ لطفاً قیمت معتبر به تومان وارد کنید:",
            reply_markup=get_skip_buy_price_keyboard("skip_parsian_buy_price")
        )
        return

    await db_service.update_parsian_holding(message.from_user.id, weight, qty, buy_price)
    await state.clear()

    ans = (
        f"✅ سکه پارسیان `{weight:g} گرمی` با موفقیت ذخیره گردید:\n"
        f"🔹 تعداد: `{qty} عدد`\n"
        f"🔹 قیمت خرید واحد: `{format_price(buy_price)}`"
    )
    await message.answer(ans, parse_mode="Markdown")
