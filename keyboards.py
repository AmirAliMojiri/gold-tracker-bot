from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """منوی اصلی شیشه‌ای ربات"""
    keyboard = [
        [
            InlineKeyboardButton(text="📊 ارزش سبد و سود/زیان من", callback_data="btn_portfolio_summary"),
        ],
        [
            InlineKeyboardButton(text="➕ ثبت و ویرایش دارایی‌ها", callback_data="btn_manage_holdings"),
            InlineKeyboardButton(text="📈 نرخ‌های لحظه‌ای بازار", callback_data="btn_live_prices"),
        ],
        [
            InlineKeyboardButton(text="🗑 پاک‌سازی دارایی‌ها", callback_data="btn_clear_confirm"),
            InlineKeyboardButton(text="ℹ️ راهنما", callback_data="btn_help"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_categories_keyboard() -> InlineKeyboardMarkup:
    """منوی انتخاب دسته‌بندی دارایی جهت ثبت یا ویرایش"""
    keyboard = [
        [
            InlineKeyboardButton(text="✨ طلا و آبشده", callback_data="cat_gold"),
            InlineKeyboardButton(text="⚪️ نقره (۹۹۹ و ۹۲۵)", callback_data="cat_silver"),
        ],
        [
            InlineKeyboardButton(text="🪙 سکه‌های طرح جدید (بانکی)", callback_data="cat_coins_new"),
        ],
        [
            InlineKeyboardButton(text="🏛 سکه‌های طرح قدیم (قبل ۸۶)", callback_data="cat_coins_old"),
        ],
        [
            InlineKeyboardButton(text="🎖 سکه‌های پارسیان", callback_data="cat_parsian"),
        ],
        [
            InlineKeyboardButton(text="💵 ارزها و تتر (دلار، یورو و...)", callback_data="cat_currency"),
        ],
        [
            InlineKeyboardButton(text="🔙 بازگشت به منوی اصلی", callback_data="btn_main_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_gold_items_keyboard() -> InlineKeyboardMarkup:
    """زیرمنوی انواع طلا"""
    keyboard = [
        [InlineKeyboardButton(text="طلای ۱۸ عیار (گرم)", callback_data="item_gold_18k")],
        [InlineKeyboardButton(text="طلای ۲۴ عیار (گرم)", callback_data="item_gold_24k")],
        [InlineKeyboardButton(text="طلای دست دوم / کم‌اجرت (گرم)", callback_data="item_gold_used")],
        [InlineKeyboardButton(text="طلای آب‌شده (گرم)", callback_data="item_gold_melted")],
        [InlineKeyboardButton(text="🔙 بازگشت به دسته‌ها", callback_data="btn_manage_holdings")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_silver_items_keyboard() -> InlineKeyboardMarkup:
    """زیرمنوی انواع نقره"""
    keyboard = [
        [InlineKeyboardButton(text="گرم نقره ۹۹۹ (خالص/شمش/ساچمه)", callback_data="item_silver_999")],
        [InlineKeyboardButton(text="گرم نقره ۹۲۵ (عیار استرلینگ)", callback_data="item_silver_925")],
        [InlineKeyboardButton(text="🔙 بازگشت به دسته‌ها", callback_data="btn_manage_holdings")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_new_coins_keyboard() -> InlineKeyboardMarkup:
    """زیرمنوی سکه‌های طرح جدید"""
    keyboard = [
        [InlineKeyboardButton(text="سکه تمام امامی (طرح جدید)", callback_data="item_coin_emami")],
        [InlineKeyboardButton(text="سکه تمام بهار آزادی", callback_data="item_coin_bahar")],
        [InlineKeyboardButton(text="نیم سکه (طرح جدید / بعد ۸۶)", callback_data="item_coin_half_new")],
        [InlineKeyboardButton(text="ربع سکه (طرح جدید / بعد ۸۶)", callback_data="item_coin_rob_new")],
        [InlineKeyboardButton(text="سکه گرمی (بانکی)", callback_data="item_coin_grami")],
        [InlineKeyboardButton(text="🔙 بازگشت به دسته‌ها", callback_data="btn_manage_holdings")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_old_coins_keyboard() -> InlineKeyboardMarkup:
    """زیرمنوی سکه‌های طرح قدیم (قبل از سال ۸۶)"""
    keyboard = [
        [InlineKeyboardButton(text="نیم سکه طرح قدیم (قبل ۸۶)", callback_data="item_coin_half_old")],
        [InlineKeyboardButton(text="ربع سکه طرح قدیم (قبل ۸۶)", callback_data="item_coin_rob_old")],
        [InlineKeyboardButton(text="🔙 بازگشت به دسته‌ها", callback_data="btn_manage_holdings")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_currency_items_keyboard() -> InlineKeyboardMarkup:
    """زیرمنوی ارزها"""
    keyboard = [
        [
            InlineKeyboardButton(text="💵 دلار آمریکا", callback_data="item_currency_usd"),
            InlineKeyboardButton(text="🌐 تتر (USDT)", callback_data="item_currency_usdt"),
        ],
        [
            InlineKeyboardButton(text="💶 یورو", callback_data="item_currency_eur"),
            InlineKeyboardButton(text="🇦🇪 درهم امارات", callback_data="item_currency_aed"),
        ],
        [
            InlineKeyboardButton(text="💷 پوند انگلیس", callback_data="item_currency_gbp"),
            InlineKeyboardButton(text="🇹🇷 لیر ترکیه", callback_data="item_currency_try"),
        ],
        [
            InlineKeyboardButton(text="🇨🇦 دلار کانادا", callback_data="item_currency_cad"),
            InlineKeyboardButton(text="🇦🇺 دلار استرالیا", callback_data="item_currency_aud"),
        ],
        [
            InlineKeyboardButton(text="🇮🇶 ۱۰۰ دینار عراق", callback_data="item_currency_iqd"),
        ],
        [InlineKeyboardButton(text="🔙 بازگشت به دسته‌ها", callback_data="btn_manage_holdings")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_parsian_keyboard() -> InlineKeyboardMarkup:
    """زیرمنوی سکه‌های پارسیان"""
    keyboard = [
        [
            InlineKeyboardButton(text="پارسیان ۱۰۰ سوت (۰.۱ گرم)", callback_data="parsian_0.100"),
            InlineKeyboardButton(text="پارسیان ۲۰۰ سوت (۰.۲ گرم)", callback_data="parsian_0.200"),
        ],
        [
            InlineKeyboardButton(text="پارسیان ۳۰۰ سوت (۰.۳ گرم)", callback_data="parsian_0.300"),
            InlineKeyboardButton(text="پارسیان ۴۰۰ سوت (۰.۴ گرم)", callback_data="parsian_0.400"),
        ],
        [
            InlineKeyboardButton(text="پارسیان ۵۰۰ سوت (نیم گرم)", callback_data="parsian_0.500"),
            InlineKeyboardButton(text="پارسیان ۶۰۰ سوت (۰.۶ گرم)", callback_data="parsian_0.600"),
        ],
        [
            InlineKeyboardButton(text="پارسیان ۷۰۰ سوت (۰.۷ گرم)", callback_data="parsian_0.700"),
            InlineKeyboardButton(text="پارسیان ۸۰۰ سوت (۰.۸ گرم)", callback_data="parsian_0.800"),
        ],
        [
            InlineKeyboardButton(text="پارسیان ۹۰۰ سوت (۰.۹ گرم)", callback_data="parsian_0.900"),
            InlineKeyboardButton(text="پارسیان ۱ گرمی", callback_data="parsian_1.000"),
        ],
        [
            InlineKeyboardButton(text="پارسیان ۱.۲ گرمی", callback_data="parsian_1.200"),
            InlineKeyboardButton(text="پارسیان ۱.۵ گرمی", callback_data="parsian_1.500"),
        ],
        [
            InlineKeyboardButton(text="✏️ ثبت پارسیان با وزن دلخواه", callback_data="parsian_custom"),
        ],
        [
            InlineKeyboardButton(text="🔙 بازگشت به دسته‌ها", callback_data="btn_manage_holdings")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_skip_buy_price_keyboard(skip_callback: str = "skip_buy_price") -> InlineKeyboardMarkup:
    """دکمه رد شدن از مرحله ثبت قیمت خرید"""
    keyboard = [
        [InlineKeyboardButton(text="⏩ ثبت بدون قیمت خرید (رد شدن)", callback_data=skip_callback)],
        [InlineKeyboardButton(text="❌ انصراف", callback_data="btn_manage_holdings")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_cancel_keyboard(back_callback: str = "btn_manage_holdings") -> InlineKeyboardMarkup:
    """دکمه انصراف و بازگشت در حین ورود داده"""
    keyboard = [
        [InlineKeyboardButton(text="❌ انصراف", callback_data=back_callback)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_clear_confirmation_keyboard() -> InlineKeyboardMarkup:
    """تأییدیه پاکسازی کل دارایی‌ها"""
    keyboard = [
        [
            InlineKeyboardButton(text="⚠️ بله، همه را پاک کن", callback_data="btn_clear_execute"),
            InlineKeyboardButton(text="❌ انصراف", callback_data="btn_main_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_back_to_main_keyboard() -> InlineKeyboardMarkup:
    """دکمه ساده بازگشت به منوی اصلی"""
    keyboard = [
        [InlineKeyboardButton(text="🔙 بازگشت به منوی اصلی", callback_data="btn_main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
