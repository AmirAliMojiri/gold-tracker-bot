from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from database import db_service
from keyboards import (
    get_main_reply_keyboard,
    get_clear_confirmation_keyboard
)

router = Router()

START_TEXT = (
    "🌟 **به سامانه هوشمند مدیریت دارایی طلا، سکه، نقره و ارز خوش آمدید!**\n\n"
    "این ربات دارایی‌های شما را به صورت دائمی ذخیره کرده و ارزش روز و سود/زیان را بر مبنای نرخ‌های زنده `TGJU.org` محاسبه می‌کند.\n\n"
    "👇 **برای استفاده، از منوی ۴ دکمه‌ای [::] در کنار کادر پیام استفاده کنید:**\n\n"
    "• 💼 **دارایی‌های من (پرتفوی):** مشاهده موجودی ذخیره‌شده و سود/زیان\n"
    "• ➕ **ثبت / ویرایش دارایی:** افزودن طلا، نقره، انواع سکه و ارزها\n"
    "• 📈 **نرخ‌های لحظه‌ای بازار:** تابلوی قیمت زنده TGJU\n"
    "• 💡 **پیشنهاد خرید با بودجه:** مشاور هوشمند تخصیص سرمایه\n"
    "• 🔔 **هشدارهای قیمت:** تعیین تارگت قیمتی و رادار حباب سکه\n"
    "• 🗑 **پاک‌سازی سبد:** حذف و ریست دارایی‌ها"
)

HELP_TEXT = (
    "📖 **راهنمای ربات:**\n\n"
    "• برای باز کردن منو، آیکون مربع‌های منو **[::]** در کنار کادر پیام را بزنید.\n"
    "• با زدن ضربدر روی کیبورد، منو بسته می‌شود و به حالت آیکون [::] درمی‌آید.\n"
    "• تمام اطلاعات واردشده به صورت خودکار و دائمی ذخیره می‌شوند."
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
    # ارسال پیام تمیز فقط همراه با کیبورد بازشونده [::]
    await message.answer(
        START_TEXT,
        reply_markup=get_main_reply_keyboard(),
        parse_mode="Markdown"
    )

@router.message(Command("home"))
@router.message(Command("menu"))
async def cmd_home(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        START_TEXT,
        reply_markup=get_main_reply_keyboard(),
        parse_mode="Markdown"
    )

@router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(HELP_TEXT, reply_markup=get_main_reply_keyboard(), parse_mode="Markdown")

# بستن پیام منوهای اینلاین
@router.callback_query(F.data == "btn_close_menu")
async def cb_close_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await call.message.delete()
    except Exception:
        pass
    await call.answer("بسته شد.")

@router.message(F.text == "🗑 پاک‌سازی سبد")
@router.callback_query(F.data == "btn_clear_confirm")
async def cb_clear_confirm(event: Message | CallbackQuery):
    text = "⚠️ **آیا مطمئن هستید که می‌خواهید تمام دارایی‌های ثبت‌شده خود را پاک کنید؟**\nاین عمل غیرقابل بازگشت است."
    if isinstance(event, CallbackQuery):
        try:
            await event.message.edit_text(text, reply_markup=get_clear_confirmation_keyboard(), parse_mode="Markdown")
        except Exception:
            await event.message.answer(text, reply_markup=get_clear_confirmation_keyboard(), parse_mode="Markdown")
        await event.answer()
    else:
        await event.answer(text, reply_markup=get_clear_confirmation_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "btn_clear_execute")
async def cb_clear_execute(call: CallbackQuery):
    await db_service.clear_all_holdings(call.from_user.id)
    text = "✅ **تمام دارایی‌های شما با موفقیت از سیستم حذف و بازنشانی شدند.**"
    try:
        await call.message.edit_text(text, parse_mode="Markdown")
    except Exception:
        await call.message.answer(text, parse_mode="Markdown")
    await call.answer("دارایی‌ها پاک شدند.")
