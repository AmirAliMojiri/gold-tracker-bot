from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from tgju_service import tgju_service
from advisor import advisor_service
from states import HoldingStates
from keyboards import (
    get_quick_budget_keyboard,
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

async def generate_advisor_response(budget_toman: float) -> str:
    prices = await tgju_service.get_all_prices()
    report = advisor_service.analyze_macro_portfolio(budget_toman, prices)

    allocations = report['allocations']
    dca = report['dca_tranches']
    macro = report['macro_metrics']

    lines = [
        "📊 **استراتژی تخصصی و سبدگردانی هوشمند اقتصاد کلان**",
        f"💵 سرمایه در دسترس: `{format_price(budget_toman)}`\n",
        "━━━━━━━━━━━━━━━━━━━━",
        "🌐 **شاخص‌های کلیدی اقتصاد کلان و متغیرهای بازار:**"
    ]

    # شاخص‌های جهانی
    if macro.get('ons_gold') or macro.get('ons_silver'):
        g_str = f"${macro['ons_gold']:,.2f}" if macro.get('ons_gold') else "-"
        s_str = f"${macro['ons_silver']:,.2f}" if macro.get('ons_silver') else "-"
        lines.append(f"• 🥇 **انس طلای جهانی:** `{g_str}` | 🥈 **انس نقره:** `{s_str}`")

    if macro.get('gsr'):
        gsr_val = macro['gsr']
        gsr_comment = "ارزندگی تاریخی نقره نسبت به طلا در مقیاس جهانی (GSR بالای ۶۵)" if gsr_val >= 65 else "تعادل نسبی در برابری طلا و نقره"
        lines.append(f"• ⚖️ **نسبت طلا به نقره (GSR):** `{gsr_val}` (↳ *{gsr_comment}*)")

    # حباب سکه
    if macro.get('bubble_emami_pct') is not None and macro.get('bubble_emami_val'):
        b_pct = macro['bubble_emami_pct']
        b_val = macro['bubble_emami_val']
        intr = macro.get('intrinsic_emami', 0)
        intr_str = f" | ارزش ذاتی طلا: `{format_price(intr)}`" if intr else ""
        lines.append(f"• 🪙 **حباب سکه امامی:** `{format_price(b_val)}` (`{b_pct}%`){intr_str}")

    lines.append("\n━━━━━━━━━━━━━━━━━━━━")
    lines.append("🎯 **ماتریس بهینه تخصیص دارایی (Portfolio Allocation):**\n")

    for idx, item in enumerate(allocations, 1):
        lines.append(
            f"**{idx}. {item['name']} ({item['weight_pct']}٪ وزن سبد):**\n"
            f"  🔹 بودجه تخصیصی: `{format_price(item['budget_share'])}` (مقدار هدف: `{item['target_units']}`)\n"
            f"  🔹 منطق تحلیلی: {item['role']}\n"
            f"  🔹 سطح ریسک: `{item['risk']}`\n"
        )

    lines.append("━━━━━━━━━━━━━━━━━━━━")
    lines.append("📈 **استراتژی اجرای ورود پله‌ای (DCA Tranches):**\n")

    for tranche in dca:
        lines.append(
            f"• **{tranche['tranche']}** — سهم: `{tranche['pct']}` (`{format_price(tranche['amount'])}`)\n"
            f"  ↳ {tranche['action']}\n"
        )

    lines.append(
        "━━━━━━━━━━━━━━━━━━━━\n"
        "⏱ **افق سرمایه‌گذاری و مدیریت ریسک:**\n"
        "• **افق زمانی:** میان‌مدت (۳ الی ۶ ماهه)\n"
        "• **نسبت پاداش به ریسک (R/R):** برآورد بالای ۲.۵ بر پایه روندهای انقباضی نقدینگی و تورم ساختاری\n"
        "• **نکته کلیدی تریدرها:** به هیچ عنوان تمام نقدینگی را در یک سفارش تک‌پله‌ای وارد نکنید و پله‌های حمایتی را رعایت فرمایید."
    )

    return "\n".join(lines)

@router.message(Command("advisor"))
@router.message(F.text == "💡 پیشنهاد خرید با بودجه")
async def cmd_smart_advisor(message: Message, state: FSMContext):
    await state.clear()
    prompt = (
        "💡 **مشاور هوشمند تخصیص سرمایه و خرید دارایی:**\n\n"
        "این سیستم بر اساس **روند قیمتی گذشته**، **میزان حباب**، **کارمزدها** و **نرخ‌های زنده TGJU** بهترین گزینه‌ها را متناسب با بودجه شما پیشنهاد می‌دهد.\n\n"
        "لطفاً مبلغ سرمایه خود را انتخاب یا ارسال فرمایید:"
    )
    await message.answer(prompt, reply_markup=get_quick_budget_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "btn_smart_advisor")
async def cb_smart_advisor(call: CallbackQuery, state: FSMContext):
    await state.clear()
    prompt = (
        "💡 **مشاور هوشمند تخصیص سرمایه و خرید دارایی:**\n\n"
        "لطفاً مبلغ سرمایه در دسترس خود را انتخاب یا ارسال نمایید:"
    )
    try:
        await call.message.edit_text(prompt, reply_markup=get_quick_budget_keyboard(), parse_mode="Markdown")
    except Exception:
        await call.message.answer(prompt, reply_markup=get_quick_budget_keyboard(), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data.startswith("budget_"))
async def cb_select_budget(call: CallbackQuery, state: FSMContext):
    val = call.data.replace("budget_", "")
    
    if val == "custom":
        await state.set_state(HoldingStates.waiting_for_advisor_budget)
        prompt = (
            "✏️ **لطفاً مبلغ بودجه خود را به تومان ارسال فرمایید:**\n"
            "🔹 مثال: `15000000` (برای ۱۵ میلیون تومان)"
        )
        await call.message.edit_text(prompt, reply_markup=get_cancel_keyboard("btn_smart_advisor"), parse_mode="Markdown")
        await call.answer()
        return

    try:
        budget = float(val)
    except ValueError:
        await call.answer("مبلغ نامعتبر است.")
        return

    await call.answer("در حال آنالیز بازار...")
    response_text = await generate_advisor_response(budget)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu"),
        ]
    ])
    await call.message.edit_text(response_text, reply_markup=kb, parse_mode="Markdown")

@router.message(HoldingStates.waiting_for_advisor_budget)
async def process_custom_budget(message: Message, state: FSMContext):
    raw_text = clean_input_number(message.text)
    try:
        budget = float(raw_text)
        if budget < 500_000:
            raise ValueError()
    except Exception:
        await message.answer(
            "❌ لطفاً یک مبلغ معتبر به تومان وارد کنید (حداقل ۵۰۰,۰۰۰ تومان):",
            reply_markup=get_cancel_keyboard("btn_smart_advisor")
        )
        return

    await state.clear()
    await message.answer("🔍 در حال تحلیل بهترین دارایی‌ها...")
    response_text = await generate_advisor_response(budget)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu"),
        ]
    ])
    await message.answer(response_text, reply_markup=kb, parse_mode="Markdown")
