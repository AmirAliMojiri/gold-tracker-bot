from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

def get_home_reply_keyboard() -> ReplyKeyboardMarkup:
    """دکمه مینیمال و شیک خانه در پایین صفحه (مطابق تصویر)"""
    keyboard = [
        [KeyboardButton(text="🏠")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="منو را باز کنید..."
    )

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """منوی اصلی شیشه‌ای ربات"""
    keyboard = [
        [
            InlineKeyboardButton(text="💼 دارایی‌های من (پرتفوی)", callback_data="btn_portfolio_summary"),
        ],
        [
            InlineKeyboardButton(text="➕ ثبت و ویرایش دارایی", callback_data="btn_manage_holdings"),
            InlineKeyboardButton(text="📈 نرخ‌های لحظه‌ای بازار", callback_data="btn_live_prices"),
        ],
        [
            InlineKeyboardButton(text="💡 پیشنهاد خرید با بودجه", callback_data="btn_smart_advisor"),
            InlineKeyboardButton(text="🔔 هشدارهای قیمت", callback_data="btn_alerts_menu"),
        ],
        [
            InlineKeyboardButton(text="🗑 پاک‌سازی سبد", callback_data="btn_clear_confirm"),
            InlineKeyboardButton(text="❌ بستن منو", callback_data="btn_close_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# --- دسته‌بندی‌های دارایی جهت ثبت ---
def get_categories_keyboard() -> InlineKeyboardMarkup:
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
            InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_gold_items_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="✨ طلای ۱۸ عیار (گرم)", callback_data="item_gold_18k")],
        [InlineKeyboardButton(text="✨ طلای ۲۴ عیار (گرم)", callback_data="item_gold_24k")],
        [InlineKeyboardButton(text="✨ طلای دست دوم / کم‌اجرت (گرم)", callback_data="item_gold_used")],
        [InlineKeyboardButton(text="✨ طلای آب‌شده (گرم)", callback_data="item_gold_melted")],
        [
            InlineKeyboardButton(text="🔙 بازگشت", callback_data="btn_manage_holdings"),
            InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_silver_items_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="⚪️ گرم نقره ۹۹۹ (خالص/شمش/ساچمه)", callback_data="item_silver_999")],
        [InlineKeyboardButton(text="⚪️ گرم نقره ۹۲۵ (عیار استرلینگ)", callback_data="item_silver_925")],
        [
            InlineKeyboardButton(text="🔙 بازگشت", callback_data="btn_manage_holdings"),
            InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_new_coins_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="🪙 سکه تمام امامی (طرح جدید)", callback_data="item_coin_emami")],
        [InlineKeyboardButton(text="🪙 سکه تمام بهار آزادی", callback_data="item_coin_bahar")],
        [InlineKeyboardButton(text="🪙 نیم سکه (طرح جدید / بعد ۸۶)", callback_data="item_coin_half_new")],
        [InlineKeyboardButton(text="🪙 ربع سکه (طرح جدید / بعد ۸۶)", callback_data="item_coin_rob_new")],
        [InlineKeyboardButton(text="🪙 سکه گرمی (بانکی)", callback_data="item_coin_grami")],
        [
            InlineKeyboardButton(text="🔙 بازگشت", callback_data="btn_manage_holdings"),
            InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_old_coins_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="🏛 تمام سکه طرح قدیم (قبل ۸۶)", callback_data="item_coin_emami_old")],
        [InlineKeyboardButton(text="🏛 نیم سکه طرح قدیم (قبل ۸۶)", callback_data="item_coin_half_old")],
        [InlineKeyboardButton(text="🏛 ربع سکه طرح قدیم (قبل ۸۶)", callback_data="item_coin_rob_old")],
        [
            InlineKeyboardButton(text="🔙 بازگشت", callback_data="btn_manage_holdings"),
            InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_currency_items_keyboard() -> InlineKeyboardMarkup:
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
        [
            InlineKeyboardButton(text="🔙 بازگشت", callback_data="btn_manage_holdings"),
            InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_parsian_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="🎖 پارسیان ۱۰۰ سوت (۰.۱ گرم)", callback_data="parsian_0.100"),
            InlineKeyboardButton(text="🎖 پارسیان ۲۰۰ سوت (۰.۲ گرم)", callback_data="parsian_0.200"),
        ],
        [
            InlineKeyboardButton(text="🎖 پارسیان ۳۰۰ سوت (۰.۳ گرم)", callback_data="parsian_0.300"),
            InlineKeyboardButton(text="🎖 پارسیان ۴۰۰ سوت (۰.۴ گرم)", callback_data="parsian_0.400"),
        ],
        [
            InlineKeyboardButton(text="🎖 پارسیان ۵۰۰ سوت (نیم گرم)", callback_data="parsian_0.500"),
            InlineKeyboardButton(text="🎖 پارسیان ۶۰۰ سوت (۰.۶ گرم)", callback_data="parsian_0.600"),
        ],
        [
            InlineKeyboardButton(text="🎖 پارسیان ۷۰۰ سوت (۰.۷ گرم)", callback_data="parsian_0.700"),
            InlineKeyboardButton(text="🎖 پارسیان ۸۰۰ سوت (۰.۸ گرم)", callback_data="parsian_0.800"),
        ],
        [
            InlineKeyboardButton(text="🎖 پارسیان ۹۰۰ سوت (۰.۹ گرم)", callback_data="parsian_0.900"),
            InlineKeyboardButton(text="🎖 پارسیان ۱ گرمی", callback_data="parsian_1.000"),
        ],
        [
            InlineKeyboardButton(text="🎖 پارسیان ۱.۲ گرمی", callback_data="parsian_1.200"),
            InlineKeyboardButton(text="🎖 پارسیان ۱.۵ گرمی", callback_data="parsian_1.500"),
        ],
        [
            InlineKeyboardButton(text="✏️ ثبت پارسیان با وزن دلخواه", callback_data="parsian_custom"),
        ],
        [
            InlineKeyboardButton(text="🔙 بازگشت", callback_data="btn_manage_holdings"),
            InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# --- منوی هشدارهای هوشمند ---
def get_alerts_menu_keyboard(daily_en: bool = True) -> InlineKeyboardMarkup:
    digest_text = "🕒 گزارش شبانه (ساعت ۲۱): فعال ✅" if daily_en else "🕒 گزارش شبانه (ساعت ۲۱): غیرفعال ❌"
    keyboard = [
        [
            InlineKeyboardButton(text="🎯 ثبت هشدار قیمت جدید", callback_data="alert_new_select"),
            InlineKeyboardButton(text="📋 هشدارهای فعال من", callback_data="alert_my_list"),
        ],
        [
            InlineKeyboardButton(text="🎈 رادار و تحلیل حباب سکه", callback_data="alert_bubble_radar"),
        ],
        [
            InlineKeyboardButton(text=digest_text, callback_data="toggle_daily_digest"),
        ],
        [
            InlineKeyboardButton(text="🔙 بازگشت به منوی اصلی", callback_data="btn_main_menu"),
            InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_alert_items_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="✨ طلای ۱۸ عیار", callback_data="setalert_gold_18k"),
            InlineKeyboardButton(text="✨ طلای آب‌شده", callback_data="setalert_gold_melted"),
        ],
        [
            InlineKeyboardButton(text="🪙 سکه امامی", callback_data="setalert_coin_emami"),
            InlineKeyboardButton(text="🪙 تمام بهار آزادی", callback_data="setalert_coin_bahar"),
        ],
        [
            InlineKeyboardButton(text="🪙 نیم سکه", callback_data="setalert_coin_half_new"),
            InlineKeyboardButton(text="🪙 ربع سکه", callback_data="setalert_coin_rob_new"),
        ],
        [
            InlineKeyboardButton(text="💵 دلار آمریکا", callback_data="setalert_currency_usd"),
            InlineKeyboardButton(text="🌐 تتر (USDT)", callback_data="setalert_currency_usdt"),
        ],
        [
            InlineKeyboardButton(text="⚪️ گرم نقره ۹۹۹", callback_data="setalert_silver_999"),
        ],
        [
            InlineKeyboardButton(text="🔙 بازگشت", callback_data="btn_alerts_menu"),
            InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_quick_budget_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="۵ میلیون تومان", callback_data="budget_5000000"),
            InlineKeyboardButton(text="۱۰ میلیون تومان", callback_data="budget_10000000"),
        ],
        [
            InlineKeyboardButton(text="۲۰ میلیون تومان", callback_data="budget_20000000"),
            InlineKeyboardButton(text="۵۰ میلیون تومان", callback_data="budget_50000000"),
        ],
        [
            InlineKeyboardButton(text="۱۰۰ میلیون تومان", callback_data="budget_100000000"),
            InlineKeyboardButton(text="✏️ مبلغ دلخواه دیگر", callback_data="budget_custom"),
        ],
        [
            InlineKeyboardButton(text="🔙 بازگشت به منوی اصلی", callback_data="btn_main_menu"),
            InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_skip_buy_price_keyboard(skip_callback: str = "skip_buy_price") -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="⏩ ثبت بدون قیمت خرید (رد شدن)", callback_data=skip_callback)],
        [
            InlineKeyboardButton(text="🔙 بازگشت", callback_data="btn_manage_holdings"),
            InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_cancel_keyboard(back_callback: str = "btn_manage_holdings") -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="🔙 بازگشت", callback_data=back_callback),
            InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_clear_confirmation_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="⚠️ بله، همه را پاک کن", callback_data="btn_clear_execute"),
            InlineKeyboardButton(text="❌ انصراف و بازگشت", callback_data="btn_main_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_back_to_main_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="🔙 بازگشت به منوی اصلی", callback_data="btn_main_menu"),
            InlineKeyboardButton(text="❌ بستن", callback_data="btn_close_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
