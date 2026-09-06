from aiogram.fsm.state import State, StatesGroup

class HoldingStates(StatesGroup):
    # دریافت مقدار عددی دارایی‌های اصلی
    waiting_for_main_value = State()
    # دریافت میانگین قیمت خرید دارایی اصلی
    waiting_for_main_buy_price = State()
    
    # مراحل سکه پارسیان
    waiting_for_parsian_weight = State()
    waiting_for_parsian_quantity = State()
    waiting_for_parsian_buy_price = State()
