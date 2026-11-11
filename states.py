from aiogram.fsm.state import State, StatesGroup

class HoldingStates(StatesGroup):
    # دریافت مقدار و قیمت خرید دارایی‌های اصلی
    waiting_for_main_value = State()
    waiting_for_main_buy_price = State()
    
    # مراحل سکه پارسیان
    waiting_for_parsian_weight = State()
    waiting_for_parsian_quantity = State()
    waiting_for_parsian_buy_price = State()

    # مشاور هوشمند بودجه
    waiting_for_advisor_budget = State()

    # سیستم هشدارهای قیمت
    waiting_for_alert_item = State()
    waiting_for_alert_price = State()

    # ابزار تبدیل دارایی (Asset Swapper)
    waiting_for_swapper_amount = State()

    # ابزار خرید پله‌ای و میانگین‌گیری (DCA)
    waiting_for_dca_old_amount = State()
    waiting_for_dca_old_price = State()
    waiting_for_dca_new_amount = State()
    waiting_for_dca_new_price = State()
