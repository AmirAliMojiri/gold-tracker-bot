from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database import db_service
from tgju_service import tgju_service
from chart_service import chart_service
from states import HoldingStates
from keyboards import (
    get_tools_menu_keyboard,
    get_cancel_keyboard,
    get_back_to_main_keyboard
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

SWAP_ASSET_NAMES = {
    'gold_18k': ('طلای ۱۸ عیار', 'گرم', 'gold'),
    'silver_999': ('نقره ۹۹۹', 'گرم', 'silver'),
    'coin_emami': ('سکه امامی', 'عدد', 'coins'),
    'coin_bahar': ('تمام بهار آزادی', 'عدد', 'coins'),
    'coin_half_new': ('نیم سکه', 'عدد', 'coins'),
    'coin_rob_new': ('ربع سکه', 'عدد', 'coins'),
    'coin_grami': ('سکه گرمی', 'عدد', 'coins'),
    'currency_usd': ('دلار آمریکا', 'دلار', 'currencies'),
    'currency_usdt': ('تتر', 'تتر', 'currencies'),
}

# منوی اصلی ابزارها
@router.callback_query(F.data == "btn_tools_menu")
async def cb_tools_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    text = (
        "🧮 **ابزارهای هوشمند تحلیلی و محاسباتی:**\n\n"
        "• 📊 **نمودار دایره‌ای سبد:** مشاهده بصری درصد وزنی طلا، نقره، سکه و ارزها\n"
        "• 🔄 **تبدیل دارایی‌ها (Swapper):** محاسبه معادل‌سازی و ارزش تعویض دارایی‌ها\n"
        "• 📈 **خرید پله‌ای و میانگین‌گیری (DCA):** محاسبه بهای تمام‌شده جدید با خریدهای بعدی"
    )
    try:
        await call.message.edit_text(text, reply_markup=get_tools_menu_keyboard(), parse_mode="Markdown")
    except Exception:
        await call.message.answer(text, reply_markup=get_tools_menu_keyboard(), parse_mode="Markdown")
    await call.answer()

# ۱. رسم نمودار دایره‌ای توزیع سبد
@router.callback_query(F.data == "tool_pie_chart")
async def cb_tool_pie_chart(call: CallbackQuery):
    await call.answer("در حال تولید نمودار تصویری سبد دارایی شما...")
    
    holdings = await db_service.get_holdings(call.from_user.id)
    main_h = holdings['main']
    parsian_h = holdings['parsian']

    prices = await tgju_service.get_all_prices()
    gold_p = prices.get('gold', {})
    silver_p = prices.get('silver', {})
    coin_p = prices.get('coins', {})
    curr_p = prices.get('currencies', {})
    parsian_p = prices.get('parsian', {})

    # محاسبه تجمیعی ارزش هر دسته‌بندی
    cat_vals = {
        'Gold (طلا)': 0.0,
        'Silver (نقره)': 0.0,
        'Coins (سکه)': 0.0,
        'Currencies (ارز)': 0.0,
        'Parsian (پارسیان)': 0.0,
    }

    # طلا
    for k in ['gold_18k', 'gold_24k', 'gold_used', 'gold_melted']:
        amt = main_h.get(k, 0.0)
        if amt > 0:
            cat_vals['Gold (طلا)'] += amt * gold_p.get(k, {}).get('toman', 0)

    # نقره
    for k in ['silver_999', 'silver_925']:
        amt = main_h.get(k, 0.0)
        if amt > 0:
            cat_vals['Silver (نقره)'] += amt * silver_p.get(k, {}).get('toman', 0)

    # سکه
    for k in ['coin_emami', 'coin_bahar', 'coin_half_new', 'coin_half_old', 'coin_rob_new', 'coin_rob_old', 'coin_grami']:
        amt = main_h.get(k, 0.0)
        if amt > 0:
            cat_vals['Coins (سکه)'] += amt * coin_p.get(k, {}).get('toman', 0)

    # ارز
    for k in ['currency_usd', 'currency_usdt', 'currency_eur', 'currency_aed', 'currency_gbp', 'currency_try', 'currency_cad', 'currency_aud', 'currency_iqd']:
        amt = main_h.get(k, 0.0)
        if amt > 0:
            cat_vals['Currencies (ارز)'] += amt * curr_p.get(k, {}).get('toman', 0)

    # پارسیان
    for p in parsian_h:
        w = p['weight']
        q = p['quantity']
        if q > 0:
            unit_p = parsian_p.get(f"{w:.3f}", {}).get('toman', 0) or tgju_service.estimate_parsian_price(w, prices)
            cat_vals['Parsian (پارسیان)'] += q * unit_p

    total_val = sum(cat_vals.values())
    if total_val <= 0:
        await call.message.answer(
            "⚠️ سبد دارایی شما در حال حاضر خالی است! ابتدا دارایی‌های خود را ثبت کنید.",
            reply_markup=get_back_to_main_keyboard()
        )
        return

    # تولید تصویر با matplotlib
    buf = chart_service.generate_portfolio_pie_chart(cat_vals, total_val)
    if buf:
        photo = BufferedInputFile(buf.getvalue(), filename="portfolio_chart.png")
        caption = (
            f"📊 **نمودار توزیع وزنی سبد دارایی شما:**\n\n"
            f"💰 **ارزش کل سبد:** `{format_price(total_val)}`\n"
            f"🕒 تاریخ محاسبه: `{prices.get('updated_at', '')}`"
        )
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 بازگشت به ابزارها", callback_data="btn_tools_menu")]
        ])
        await call.message.answer_photo(photo=photo, caption=caption, parse_mode="Markdown", reply_markup=kb)

# ۲. ماشین‌حساب تبدیل دارایی‌ها (Asset Swapper)
@router.callback_query(F.data == "tool_swapper")
async def cb_tool_swapper(call: CallbackQuery):
    text = "🔄 **انتخاب دارایی مبدا جهت تبدیل:**\nکدام دارایی را قصد دارید معادل‌سازی کنید؟"
    buttons = [
        [
            InlineKeyboardButton(text="🪙 ربع سکه", callback_data="swapfrom_coin_rob_new"),
            InlineKeyboardButton(text="🪙 نیم سکه", callback_data="swapfrom_coin_half_new"),
        ],
        [
            InlineKeyboardButton(text="🪙 سکه امامی", callback_data="swapfrom_coin_emami"),
            InlineKeyboardButton(text="✨ طلای ۱۸ عیار", callback_data="swapfrom_gold_18k"),
        ],
        [
            InlineKeyboardButton(text="💵 دلار آمریکا", callback_data="swapfrom_currency_usd"),
            InlineKeyboardButton(text="⚪️ نقره ۹۹۹", callback_data="swapfrom_silver_999"),
        ],
        [InlineKeyboardButton(text="🔙 بازگشت", callback_data="btn_tools_menu")]
    ]
    await call.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data.startswith("swapfrom_"))
async def cb_swap_from_select(call: CallbackQuery, state: FSMContext):
    source_key = call.data.replace("swapfrom_", "")
    title, unit, _ = SWAP_ASSET_NAMES.get(source_key, ('دارایی', 'واحد', ''))

    await state.set_state(HoldingStates.waiting_for_swapper_amount)
    await state.update_data(source_key=source_key, source_title=title, source_unit=unit)

    prompt = (
        f"🔄 **معادل‌سازی {title}:**\n\n"
        f"لطفاً **مقدار موجودی** را بر حسب **{unit}** وارد فرمایید (مثال: `2`):"
    )
    await call.message.edit_text(prompt, reply_markup=get_cancel_keyboard("tool_swapper"), parse_mode="Markdown")
    await call.answer()

@router.message(HoldingStates.waiting_for_swapper_amount)
async def process_swapper_calc(message: Message, state: FSMContext):
    data = await state.get_data()
    s_key = data.get('source_key')
    s_title = data.get('source_title')
    s_unit = data.get('source_unit')

    raw_text = clean_input_number(message.text)
    try:
        amount = float(raw_text)
        if amount <= 0:
            raise ValueError()
    except Exception:
        await message.answer("❌ لطفاً یک عدد معتبر وارد کنید:", reply_markup=get_cancel_keyboard("tool_swapper"))
        return

    await state.clear()
    prices = await tgju_service.get_all_prices()

    # یافتن نرخ واحد دارایی مبدا
    source_price = 0.0
    for cat in ['gold', 'silver', 'coins', 'currencies']:
        if s_key in prices.get(cat, {}):
            source_price = prices[cat][s_key].get('toman', 0)
            break

    total_toman_val = amount * source_price
    if total_toman_val <= 0:
        await message.answer("❌ خطا در دریافت نرخ بازار.", reply_markup=get_back_to_main_keyboard())
        return

    # معادل‌سازی در برابر سایر دارایی‌ها
    p_18k = prices.get('gold', {}).get('gold_18k', {}).get('toman', 1)
    p_sil = prices.get('silver', {}).get('silver_999', {}).get('toman', 1)
    p_usd = prices.get('currencies', {}).get('currency_usd', {}).get('toman', 1)
    p_emami = prices.get('coins', {}).get('coin_emami', {}).get('toman', 1)
    p_rob = prices.get('coins', {}).get('coin_rob_new', {}).get('toman', 1)

    lines = [
        f"🔄 **نتیجه معادل‌سازی آنلاین (نرخ روز TGJU):**\n",
        f"📦 **دارایی شما:** `{amount:g} {s_unit} {s_title}`",
        f"💰 **ارزش کل تومانی:** `{format_price(total_toman_val)}`\n",
        "⚖️ **با این مبلغ می‌توانید دارایی‌های زیر را خریداری کنید:**",
        f"• ✨ **طلای ۱۸ عیار:** `{total_toman_val / p_18k:.2f} گرم`",
        f"• ⚪️ **گرم نقره ۹۹۹:** `{total_toman_val / p_sil:.1f} گرم`",
        f"• 💵 **دلار آمریکا:** `{total_toman_val / p_usd:.1f} دلار`",
        f"• 🪙 **سکه تمام امامی:** `{total_toman_val / p_emami:.2f} عدد`",
        f"• 🪙 **ربع سکه:** `{total_toman_val / p_rob:.2f} عدد`",
    ]

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 تبدیل مجدد", callback_data="tool_swapper")],
        [InlineKeyboardButton(text="🔙 بازگشت به ابزارها", callback_data="btn_tools_menu")]
    ])
    await message.answer("\n".join(lines), reply_markup=kb, parse_mode="Markdown")

# ۳. ماشین‌حساب خرید پله‌ای و میانگین‌گیری (DCA)
@router.callback_query(F.data == "tool_dca")
async def cb_tool_dca_start(call: CallbackQuery, state: FSMContext):
    await state.set_state(HoldingStates.waiting_for_dca_old_amount)
    prompt = (
        "📈 **ماشین‌حساب خرید پله‌ای و میانگین‌گیری بهای تمام‌شده (DCA):**\n\n"
        "این ابزار میانگین قیمت خرید جدید شما را پس از خرید پله دوم محاسبه می‌کند.\n\n"
        "گام ۱ از ۴: لطفاً **مقدار موجودی قبلی** را وارد فرمایید (مثال: `10` گرم یا عدد):"
    )
    await call.message.edit_text(prompt, reply_markup=get_cancel_keyboard("btn_tools_menu"), parse_mode="Markdown")
    await call.answer()

@router.message(HoldingStates.waiting_for_dca_old_amount)
async def process_dca_1(message: Message, state: FSMContext):
    raw_text = clean_input_number(message.text)
    try:
        val = float(raw_text)
        if val <= 0:
            raise ValueError()
    except Exception:
        await message.answer("❌ لطفاً یک مقدار معتبر وارد کنید:", reply_markup=get_cancel_keyboard("btn_tools_menu"))
        return

    await state.update_data(old_amount=val)
    await state.set_state(HoldingStates.waiting_for_dca_old_price)
    await message.answer(
        f"گام ۲ از ۴: **میانگین قیمت خرید قبلی** (به ازای هر واحد به تومان) چقدر بوده است؟\n🔹 مثال: `21000000`",
        reply_markup=get_cancel_keyboard("btn_tools_menu"),
        parse_mode="Markdown"
    )

@router.message(HoldingStates.waiting_for_dca_old_price)
async def process_dca_2(message: Message, state: FSMContext):
    raw_text = clean_input_number(message.text)
    try:
        val = float(raw_text)
        if val <= 0:
            raise ValueError()
    except Exception:
        await message.answer("❌ لطفاً یک مبلغ معتبر وارد کنید:", reply_markup=get_cancel_keyboard("btn_tools_menu"))
        return

    await state.update_data(old_price=val)
    await state.set_state(HoldingStates.waiting_for_dca_new_amount)
    await message.answer(
        f"گام ۳ از ۴: **مقدار خرید جدید (پله دوم)** چقدر است؟\n🔹 مثال: `5`",
        reply_markup=get_cancel_keyboard("btn_tools_menu"),
        parse_mode="Markdown"
    )

@router.message(HoldingStates.waiting_for_dca_new_amount)
async def process_dca_3(message: Message, state: FSMContext):
    raw_text = clean_input_number(message.text)
    try:
        val = float(raw_text)
        if val <= 0:
            raise ValueError()
    except Exception:
        await message.answer("❌ لطفاً یک مقدار معتبر وارد کنید:", reply_markup=get_cancel_keyboard("btn_tools_menu"))
        return

    await state.update_data(new_amount=val)
    await state.set_state(HoldingStates.waiting_for_dca_new_price)
    await message.answer(
        f"گام ۴ از ۴: **قیمت خرید پله جدید** (به ازای هر واحد به تومان) چقدر است؟\n🔹 مثال: `23500000`",
        reply_markup=get_cancel_keyboard("btn_tools_menu"),
        parse_mode="Markdown"
    )

@router.message(HoldingStates.waiting_for_dca_new_price)
async def process_dca_4(message: Message, state: FSMContext):
    data = await state.get_data()
    old_amt = data.get('old_amount')
    old_prc = data.get('old_price')
    new_amt = data.get('new_amount')

    raw_text = clean_input_number(message.text)
    try:
        new_prc = float(raw_text)
        if new_prc <= 0:
            raise ValueError()
    except Exception:
        await message.answer("❌ لطفاً یک مبلغ معتبر وارد کنید:", reply_markup=get_cancel_keyboard("btn_tools_menu"))
        return

    await state.clear()

    # محاسبات میانگین وزنی
    total_qty = old_amt + new_amt
    total_cost = (old_amt * old_prc) + (new_amt * new_prc)
    weighted_avg_price = total_cost / total_qty
    diff = weighted_avg_price - old_prc
    diff_pct = (diff / old_prc) * 100

    change_str = f"+{format_price(diff)} (+{diff_pct:.1f}%)" if diff > 0 else f"-{format_price(abs(diff))} ({diff_pct:.1f}%)"

    lines = [
        "📊 **نتیجه محاسبه خرید پله‌ای و میانگین بهای تمام‌شده:**\n",
        f"• پله اول: `{old_amt:g} واحد` با نرخ `{format_price(old_prc)}`",
        f"• پله دوم: `{new_amt:g} واحد` با نرخ `{format_price(new_prc)}`\n",
        "━━━━━━━━━━━━━━━━━━━━",
        f"🔹 **مجموع کل موجودی جدید:** `{total_qty:g} واحد`",
        f"🔹 **کل سرمایه‌گذاری:** `{format_price(total_cost)}`",
        f"🎯 **میانگین قیمت خرید جدید شما:** `{format_price(weighted_avg_price)}`",
        f"📈 تغییر میانگین خرید: `{change_str}`"
    ]

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧮 محاسبه مجدد", callback_data="tool_dca")],
        [InlineKeyboardButton(text="🔙 بازگشت به ابزارها", callback_data="btn_tools_menu")]
    ])
    await message.answer("\n".join(lines), reply_markup=kb, parse_mode="Markdown")
