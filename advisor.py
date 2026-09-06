import asyncio
from typing import Dict, Any, List

class InvestmentAdvisor:
    """
    سامانه تخصصی و کوانتومتریک تحلیل اقتصاد کلان و استراتژی معاملاتی طلا، سکه، نقره و ارز
    طراحی‌شده برای تریدرها، تحلیل‌گران بازار مالی و مدیران سرمایه‌گذاری
    """

    @staticmethod
    def analyze_macro_portfolio(budget_toman: float, prices: Dict[str, Any]) -> Dict[str, Any]:
        """
        تولید گزارش جامع مدیریت پورتفولیو، وزن‌دهی بهینه سبد، نسبت‌های کلان (GSR)،
        حباب‌های ذاتی و استراتژی ورود پله‌ای (DCA Tranches) بر مبنای بودجه
        """
        gold_data = prices.get('gold', {})
        silver_data = prices.get('silver', {})
        coin_data = prices.get('coins', {})
        curr_data = prices.get('currencies', {})
        bubbles_data = prices.get('bubbles', {})
        macro_data = prices.get('macro', {})

        gold_18k = gold_data.get('gold_18k', {}).get('toman', 0)
        silver_999 = silver_data.get('silver_999', {}).get('toman', 0)
        usd_price = curr_data.get('currency_usd', {}).get('toman', 0)
        usdt_price = curr_data.get('currency_usdt', {}).get('toman', 0) or usd_price
        coin_emami = coin_data.get('coin_emami', {}).get('toman', 0)
        coin_bahar = coin_data.get('coin_bahar', {}).get('toman', 0)
        coin_half = coin_data.get('coin_half_new', {}).get('toman', 0)
        coin_rob = coin_data.get('coin_rob_new', {}).get('toman', 0)

        # محاسبه حباب و ارزش ذاتی سکه امامی (وزن ۸.۱۳۳ گرم عیار ۹۰۰)
        intrinsic_emami = 0
        if gold_18k > 0:
            # قیمت هر گرم طلا ۹۰۰ = طلا ۱۸ (۷۵۰) * (۹۰۰/۷۵۰)
            intrinsic_emami = int(gold_18k * (900 / 750) * 8.133)
        bubble_emami_val = bubbles_data.get('bubble_emami', {}).get('toman', 0) or (coin_emami - intrinsic_emami if coin_emami and intrinsic_emami else 0)
        bubble_emami_pct = bubbles_data.get('bubble_emami', {}).get('percentage', 0.0) or (round((bubble_emami_val / coin_emami) * 100, 1) if coin_emami else 0.0)

        # شاخص‌های کلان
        ons_gold = macro_data.get('ons_gold', 0.0)
        ons_silver = macro_data.get('ons_silver', 0.0)
        gsr = macro_data.get('gold_silver_ratio', 0.0)
        if not gsr and gold_18k > 0 and silver_999 > 0:
            gsr = round(gold_18k / silver_999, 2)

        # ماتریس تخصیص بهینه سرمایه (Asset Allocation Weights)
        allocations = []
        if budget_toman < 10_000_000:
            # میکروکپ: بودجه خرد -> تمرکز روی نقره ۹۹۹ ساچمه‌ای، طلای خرد/صندوق، تتر
            w_silver = 0.60
            w_gold = 0.30
            w_usdt = 0.10

            silver_val = budget_toman * w_silver
            gold_val = budget_toman * w_gold
            usdt_val = budget_toman * w_usdt

            allocations.append({
                'name': 'نقره ۹۹۹ ساچمه‌ای / شمش خالص',
                'category': 'فلزات صنعتی/سرمایه‌ای',
                'weight_pct': 60,
                'budget_share': silver_val,
                'target_units': f"{silver_val / silver_999:.1f} گرم" if silver_999 else "-",
                'role': 'موتور تولید آلفا (Alpha Generator) با قابلیت تفکیک خرد',
                'risk': 'متوسط تا پرنوسان (بتا بالاتر از طلا)'
            })
            allocations.append({
                'name': 'طلای خرد (پارسیان کم‌اجرت / صندوق‌های طلای بورس)',
                'category': 'پناهگاه امن (Safe Haven)',
                'weight_pct': 30,
                'budget_share': gold_val,
                'target_units': f"{gold_val / gold_18k:.2f} گرم" if gold_18k else "-",
                'role': 'حفظ ارزش دارایی و پوشش ریسک سیستماتیک',
                'risk': 'کم‌ریسک (بدون حباب)'
            })
            allocations.append({
                'name': 'تتر (USDT) / نقدینگی فعال',
                'category': 'شناوری و مدیریت نقدینگی (Dry Powder)',
                'weight_pct': 10,
                'budget_share': usdt_val,
                'target_units': f"{usdt_val / usdt_price:.1f} USDT" if usdt_price else "-",
                'role': 'ذخیره نقدینگی برای میانگین کم کردن در اصلاح‌ها',
                'risk': 'تک‌عاملی ارزی'
            })
        elif budget_toman <= 80_000_000:
            # میدکپ: بودجه متوسط -> آبشده، نقره شمش، سکه کم‌حباب یا تتر
            w_gold = 0.55
            w_silver = 0.30
            w_usdt = 0.15

            gold_val = budget_toman * w_gold
            silver_val = budget_toman * w_silver
            usdt_val = budget_toman * w_usdt

            allocations.append({
                'name': 'طلای آبشده نقدی / صندوق‌های طلای بورسی',
                'category': 'هسته مرکزی سبد (Core Holding)',
                'weight_pct': 55,
                'budget_share': gold_val,
                'target_units': f"{gold_val / gold_18k:.2f} گرم" if gold_18k else "-",
                'role': 'کارمزد و اجرت صفر، عدم وجود حباب، معاف از مالیات',
                'risk': 'پایین و پایدار'
            })
            allocations.append({
                'name': 'نقره ۹۹۹ فیزیکی (ساچمه استاندارد)',
                'category': 'رشد اهرمی (Leveraged Growth)',
                'weight_pct': 30,
                'budget_share': silver_val,
                'target_units': f"{silver_val / silver_999:.1f} گرم" if silver_999 else "-",
                'role': 'بهره‌مندی از کاهش نسبت طلا به نقره (GSR Compression)',
                'risk': 'متوسط'
            })
            allocations.append({
                'name': 'تتر (USDT) / شناوری نقدی',
                'category': 'مدیریت ریسک و نقدشوندگی',
                'weight_pct': 15,
                'budget_share': usdt_val,
                'target_units': f"{usdt_val / usdt_price:.1f} USDT" if usdt_price else "-",
                'role': 'آمادگی ورود در پله‌های حمایتی مارکت',
                'risk': 'کم'
            })
        else:
            # ماکروکپ: بودجه‌های بزرگ بالای ۸۰ میلیون -> شمش طلا، تمام بهار طرح قدیم، نقره، نقدینگی ارزی
            w_gold = 0.50
            w_coin = 0.25
            w_silver = 0.15
            w_usdt = 0.10

            gold_val = budget_toman * w_gold
            coin_val = budget_toman * w_coin
            silver_val = budget_toman * w_silver
            usdt_val = budget_toman * w_usdt

            coin_choice = "سکه تمام بهار آزادی (حباب کمتر نسبت به امامی)" if coin_bahar else "نیم سکه"
            coin_target = coin_bahar if coin_bahar else (coin_half if coin_half else coin_emami)

            allocations.append({
                'name': 'طلای آبشده شمش / قراردادهای گواهی سپرده طلا',
                'category': 'هسته دفاعی سبد (Core Asset)',
                'weight_pct': 50,
                'budget_share': gold_val,
                'target_units': f"{gold_val / gold_18k:.2f} گرم" if gold_18k else "-",
                'role': 'بزرگترین سنگر حفظ ارزش ریال بدون پرداخت پریمیوم حباب',
                'risk': 'پایین'
            })
            allocations.append({
                'name': coin_choice,
                'category': 'مسکوکات با حباب کنترل‌شده',
                'weight_pct': 25,
                'budget_share': coin_val,
                'target_units': f"{int(coin_val // coin_target)} عدد" if coin_target else "-",
                'role': 'نقدشوندگی سریع بازار آزاد و همراهی با مومنتوم صعودی',
                'risk': 'متوسط'
            })
            allocations.append({
                'name': 'نقره ۹۹۹ فیزیکی شمش و ساچمه',
                'category': 'تولید بازدهی مضاعف',
                'weight_pct': 15,
                'budget_share': silver_val,
                'target_units': f"{silver_val / silver_999:.1f} گرم" if silver_999 else "-",
                'role': 'پوشش اهرمی تقاضای صنعتی و جهانی',
                'risk': 'متوسط'
            })
            allocations.append({
                'name': 'تتر (USDT) / نقدینگی فعال',
                'category': 'مدیریت شناوری و تثبیت سود',
                'weight_pct': 10,
                'budget_share': usdt_val,
                'target_units': f"{usdt_val / usdt_price:.1f} USDT" if usdt_price else "-",
                'role': 'نقدینگی در دسترس جهت مداخله سریع در اصلاح‌ها',
                'risk': 'کم'
            })

        # پله‌های ورود سرمایه (DCA Execution Plan)
        dca_tranches = [
            {
                'tranche': 'پله اول (Initial Entry - مارکت زنده)',
                'pct': '۴۰٪ بودجه',
                'amount': budget_toman * 0.40,
                'action': 'ورود در نرخ جاری بازار جهت تثبیت پوزیشن پایه و جلوگیری از جاماندن (FOMO Hedge)'
            },
            {
                'tranche': 'پله دوم (Support Limit - کف روز / پولبک اول)',
                'pct': '۳۵٪ بودجه',
                'amount': budget_toman * 0.35,
                'action': 'اردر خرید در اصلاح ۲ تا ۳ درصدی به سمت حمایت کف روزانه و میانگین متحرک کوتاه مدت'
            },
            {
                'tranche': 'پله سوم (Correction Reserve - اصلاح عمیق)',
                'pct': '۲۵٪ بودجه',
                'amount': budget_toman * 0.25,
                'action': 'نگهداری به صورت تتر/نقد تا زمان اصلاح ماژور یا شکست پرقدرت مقاومت‌های سقف تاریخی'
            }
        ]

        return {
            'budget_toman': budget_toman,
            'allocations': allocations,
            'dca_tranches': dca_tranches,
            'macro_metrics': {
                'gold_18k': gold_18k,
                'silver_999': silver_999,
                'usd_price': usd_price,
                'usdt_price': usdt_price,
                'ons_gold': ons_gold,
                'ons_silver': ons_silver,
                'gsr': gsr,
                'intrinsic_emami': intrinsic_emami,
                'bubble_emami_val': bubble_emami_val,
                'bubble_emami_pct': bubble_emami_pct,
            }
        }

advisor_service = InvestmentAdvisor()

