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
    recommendations = advisor_service.analyze_best_options(budget_toman, prices)

    lines = [
        f"💡 **تحلیل هوشمند بازار و گزینه‌های بهینه خرید**",
        f"💵 بودجه شما: `{format_price(budget_toman)}`\n",
        "🎯 **اولویت‌بندی دارایی‌ها بر اساس بازدهی، حباب قیمتی و کارمزد:**\n"
    ]

    for idx, rec in enumerate(recommendations, 1):
        lines.append(
            f"**{idx}. {rec['title']}** ({rec['category']})\n"
            f"  🔹 مقدار قابل خرید: `{rec['affordable_qty']}`\n"
            f"  🔹 نرخ هر واحد: `{format_price(rec['unit_price'])}`\n"
            f"  🔹 سطح ریسک: `{rec['risk']}`\n"
            f"  📋 **دلیل اولویت:**\n{rec['reason']}\n"
        )

    lines.append(
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🔍 **جمع‌بندی تحلیلی برای بازه ۳ تا ۶ ماهه:**\n"
        "• برای بودجه‌های خرد، **نقره ۹۹۹** و **سکه‌های پارسیان/صندوق‌های طلا** به دلیل حذف حباب سکه، بهترین ارزش خرید را دارند."
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
