from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from database import db_service
from keyboards import (
    get_main_reply_keyboard,
    get_clear_confirmation_keyboard,
    get_back_to_main_keyboard
)

router = Router()

START_TEXT = (
    "🌟 **به سامانه هوشمند مدیریت دارایی و سرمایه‌گذاری طلا، سکه و ارز خوش آمدید!**\n\n"
    "این ربات به عنوان **حسابدار شخصی شما** عمل می‌کند؛ دارایی‌های شما برای همیشه در دیتابیس ذخیره می‌ماند و ارزش لحظه‌ای و سود/زیان را بر اساس نرخ‌های زنده `TGJU.org` محاسبه می‌کند.\n\n"
    "👇 **امکانات اصلی در منوی زیر در دسترس شماست:**\n"
    "• 💼 **دارایی‌های من (پرتفوی):** مشاهده موجودی ذخیره‌شده و سود/زیان کل\n"
    "• ➕ **ثبت / ویرایش دارایی:** افزودن طلا، نقره، سکه‌ها (جدید، قدیم، پارسیان) و ارزها\n"
    "• 📈 **نرخ‌های لحظه‌ای بازار:** تابلوی زنده قیمت‌ها از TGJU\n"
    "• 💡 **پیشنهاد خرید با بودجه:** مشاور هوشمند تخصیص سرمایه\n"
    "• 🔔 **هشدارهای قیمت:** تنظیم تارگت قیمتی و رادار حباب سکه\n"
    "• 🗑 **پاک‌سازی سبد:** حذف و ریست دارایی‌ها"
)

HELP_TEXT = (
    "📖 **راهنمای استفاده از ربات:**\n\n"
    "۱. **💼 مشاهده پرتفوی:** با لمس این دکمه، تمام دارایی‌های ذخیره‌شده شما با ارزش روز بازار و محاسبه سود/زیان نمایش داده می‌شود.\n"
    "۲. **➕ ثبت دارایی:** نوع دارایی را انتخاب کرده، ابتدا مقدار و سپس میانگین قیمت خرید را وارد کنید.\n"
    "۳. **💾 ذخیره‌سازی دائمی:** اطلاعات شما به طور دائم در سیستم ذخیره می‌ماند و با خروج از ربات پاک نمی‌شود.\n"
    "۴. **🗑 ویرایش یا حذف:** برای ویرایش، مجدداً مقدار جدید را ثبت کنید. برای حذف یک دارایی، مقدار آن را عدد `0` وارد فرمایید."
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
    await message.answer(START_TEXT, reply_markup=get_main_reply_keyboard(), parse_mode="Markdown")

@router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(HELP_TEXT, reply_markup=get_main_reply_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "btn_main_menu")
async def cb_main_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await call.message.delete()
    except Exception:
        pass
    await call.message.answer(START_TEXT, reply_markup=get_main_reply_keyboard(), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "btn_help")
async def cb_help(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer(HELP_TEXT, reply_markup=get_main_reply_keyboard(), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "btn_clear_confirm")
async def cb_clear_confirm(call: CallbackQuery):
    text = "⚠️ **آیا مطمئن هستید که می‌خواهید تمام دارایی‌های ثبت‌شده خود را پاک کنید؟**"
    await call.message.answer(text, reply_markup=get_clear_confirmation_keyboard(), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "btn_clear_execute")
async def cb_clear_execute(call: CallbackQuery):
    await db_service.clear_all_holdings(call.from_user.id)
    text = "✅ **تمام دارایی‌های شما با موفقیت از سیستم حذف و بازنشانی شدند.**"
    await call.message.answer(text, reply_markup=get_main_reply_keyboard(), parse_mode="Markdown")
    await call.answer("دارایی‌ها پاک شدند.")
