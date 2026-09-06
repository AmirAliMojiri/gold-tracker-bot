from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from database import db_service
from keyboards import (
    get_main_menu_keyboard,
    get_clear_confirmation_keyboard,
    get_back_to_main_keyboard
)

router = Router()

START_TEXT = (
    "🌟 **به ربات هوشمند مدیریت سرمایه‌گذاری طلا، سکه، نقره و ارز خوش آمدید!**\n\n"
    "این ربات به شما امکان می‌دهد دارایی‌های خود را با **قیمت خرید** ثبت کرده و در هر لحظه:\n"
    "• 📊 **ارزش روز کل سبد دارایی** بر اساس نرخ‌های لحظه‌ای `TGJU.org`\n"
    "• 📈 **میزان سود یا زیان به تومان و درصد بازدهی**\n"
    "را به تفکیک مشاهده نمایید.\n\n"
    "🔹 **بازارهای تحت پوشش:**\n"
    "• ✨ **طلا و آبشده:** ۱۸ عیار، ۲۴ عیار، دست دوم، آبشده\n"
    "• ⚪️ **نقره:** نقره ۹۹۹ (خالص/شمش) و نقره ۹۲۵ (استرلینگ)\n"
    "• 🪙 **سکه‌های بانکی:** امامی، بهار آزادی، نیم، ربع، گرمی\n"
    "• 🏛 **سکه‌های طرح قدیم:** نیم و ربع قبل از ۸۶\n"
    "• 🎖 **سکه‌های پارسیان:** تمام وزن‌ها از ۱۰۰ سوت تا سفارشی\n"
    "• 💵 **ارزها و تتر:** دلار، تتر، یورو، درهم، پوند، لیر، دلار کانادا، استرالیا و دینار\n\n"
    "برای شروع، یکی از گزینه‌های زیر را انتخاب کنید:"
)

HELP_TEXT = (
    "📖 **راهنمای استفاده از ربات:**\n\n"
    "۱. **ثبت دارایی و قیمت خرید:**\n"
    "با زدن دکمه «➕ ثبت و ویرایش دارایی‌ها»، دسته‌بندی و آیتم مورد نظر را انتخاب کنید. ابتدا مقدار/تعداد و در مرحله بعد میانگین قیمت خرید (جهت محاسبه سود/زیان) را وارد کنید.\n\n"
    "۲. **محاسبه سود و زیان:**\n"
    "ربات با مقایسه قیمت خرید شما و آخرین نرخ زنده TGJU، سود (`🟢 +تومان (+%)`) یا زیان (`🔴 -تومان (-%)`) هر دارایی و کل پرتفوی را محاسبه می‌کند.\n\n"
    "۳. **حذف دارایی:**\n"
    "جهت حذف هر دارایی از سبد، کافی است مقدار آن را عدد `0` وارد کنید."
)

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    user = message.from_user
    await db_service.register_user(
        user_id=user.id,
        first_name=user.first_name,
        username=user.username
    )
    await message.answer(START_TEXT, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")

@router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(HELP_TEXT, reply_markup=get_back_to_main_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "btn_main_menu")
async def cb_main_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await call.message.edit_text(START_TEXT, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")
    except Exception:
        await call.message.answer(START_TEXT, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "btn_help")
async def cb_help(call: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await call.message.edit_text(HELP_TEXT, reply_markup=get_back_to_main_keyboard(), parse_mode="Markdown")
    except Exception:
        await call.message.answer(HELP_TEXT, reply_markup=get_back_to_main_keyboard(), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "btn_clear_confirm")
async def cb_clear_confirm(call: CallbackQuery):
    text = "⚠️ **آیا مطمئن هستید که می‌خواهید تمام دارایی‌های ثبت‌شده خود را پاک کنید؟**\nاین عمل غیرقابل بازگشت است."
    try:
        await call.message.edit_text(text, reply_markup=get_clear_confirmation_keyboard(), parse_mode="Markdown")
    except Exception:
        await call.message.answer(text, reply_markup=get_clear_confirmation_keyboard(), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "btn_clear_execute")
async def cb_clear_execute(call: CallbackQuery):
    await db_service.clear_all_holdings(call.from_user.id)
    text = "✅ **تمام دارایی‌های شما با موفقیت از سیستم حذف و بازنشانی شدند.**"
    try:
        await call.message.edit_text(text, reply_markup=get_back_to_main_keyboard(), parse_mode="Markdown")
    except Exception:
        await call.message.answer(text, reply_markup=get_back_to_main_keyboard(), parse_mode="Markdown")
    await call.answer("دارایی‌ها پاک شدند.")
