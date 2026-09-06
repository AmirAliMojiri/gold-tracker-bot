from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from database import db_service
from keyboards import (
    get_home_reply_keyboard,
    get_main_menu_keyboard,
    get_clear_confirmation_keyboard
)

router = Router()

START_TEXT = (
    "🌟 **سامانه هوشمند مدیریت دارایی و سرمایه‌گذاری طلا، سکه و ارز**\n\n"
    "این ربات دارایی‌های شما را به صورت امن و دائمی ذخیره کرده و در هر لحظه ارزش روز بازار و سود/زیان را بر مبنای نرخ‌های زنده `TGJU.org` محاسبه می‌کند.\n\n"
    "👇 **لطفاً یکی از بخش‌های زیر را انتخاب فرمایید:**"
)

HELP_TEXT = (
    "📖 **راهنمای سریع ربات:**\n\n"
    "• 💼 **دارایی‌های من:** مشاهده کل دارایی ذخیره‌شده، ارزش روز و سود/زیان\n"
    "• ➕ **ثبت دارایی:** انتخاب نوع طلا، نقره، سکه یا ارز و ورود مقدار و قیمت خرید\n"
    "• 📈 **نرخ‌های بازار:** تابلوی قیمت لحظه‌ای طلا، سکه و ارزها\n"
    "• 💡 **پیشنهاد خرید:** مشاور هوشمند تخصیص بودجه برای خرید بهینه\n"
    "• 🔔 **هشدارهای قیمت:** تعیین تارگت قیمتی و رادار حباب سکه\n"
    "• 🏠 **دکمه خانه:** باز کردن سریع منوی اصلی در هر زمان"
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
    # ارسال کیبورد خانه در پایین صفحه + منوی شیشه‌ای اصلی
    await message.answer(
        START_TEXT,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="Markdown"
    )
    await message.answer(
        "💡 برای دسترسی سریع به منوی اصلی در هر زمان، می‌توانید دکمه 🏠 پایین صفحه را لمس کنید.",
        reply_markup=get_home_reply_keyboard()
    )

# لمس دکمه 🏠 در پایین صفحه یا تایپ /home
@router.message(F.text.in_(["🏠", "خانه", "/home", "/menu"]))
async def msg_home_button(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        START_TEXT,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="Markdown"
    )

@router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(HELP_TEXT, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")

# بازگشت به منوی اصلی
@router.callback_query(F.data == "btn_main_menu")
async def cb_main_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await call.message.edit_text(START_TEXT, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")
    except Exception:
        await call.message.answer(START_TEXT, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")
    await call.answer()

# بستن منو (حذف پیام)
@router.callback_query(F.data == "btn_close_menu")
async def cb_close_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await call.message.delete()
    except Exception:
        pass
    await call.answer("منو بسته شد.")

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
        await call.message.edit_text(text, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")
    except Exception:
        await call.message.answer(text, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")
    await call.answer("دارایی‌ها پاک شدند.")
