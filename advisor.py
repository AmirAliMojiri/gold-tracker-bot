import asyncio
import aiohttp
from typing import Dict, Any, List

class InvestmentAdvisor:
    """
    تحلیل‌گر و مشاور هوشمند خرید بر اساس بودجه و روندهای بازار
    """

    @staticmethod
    def analyze_best_options(budget_toman: float, prices: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        بررسی و اولویت‌بندی دارایی‌های قابل خرید با بودجه کاربر
        با لحاظ کردن حباب، کارمزد، و پتانسیل بازدهی ۳ ماهه
        """
        gold_data = prices.get('gold', {})
        silver_data = prices.get('silver', {})
        coin_data = prices.get('coins', {})
        curr_data = prices.get('currencies', {})
        parsian_data = prices.get('parsian', {})

        recommendations = []

        # ۱. نقره ۹۹۹ (پتانسیل اهرمی بالا + مناسب برای مبالغ خرد)
        silver_price = silver_data.get('silver_999', {}).get('toman', 0)
        if silver_price > 0 and budget_toman >= silver_price:
            grams = budget_toman / silver_price
            recommendations.append({
                'category': 'نقره',
                'title': 'گرم نقره ۹۹۹ (ساچمه یا شمش خالص)',
                'unit_price': silver_price,
                'affordable_qty': f"{grams:.1f} گرم",
                'risk': 'متوسط تا بالا (پتانسیل سود عالی)',
                'score': 95,
                'reason': (
                    '• پتانسیل رشد دوطرفه (انس نقره جهانی + دلار)\n'
                    '• بازدهی ۳ ماهه اخیر نقره از طلا و ارز بیشتر بوده است.\n'
                    '• بدون حباب و مناسب برای خریدهای خرد و مبالغ زیر ۵۰ میلیون تومان.'
                )
            })

        # ۲. طلای ۱۸ عیار / آب‌شده یا صندوق‌های طلا
        gold_18k = gold_data.get('gold_18k', {}).get('toman', 0)
        if gold_18k > 0 and budget_toman >= (gold_18k * 0.1):
            grams = budget_toman / gold_18k
            recommendations.append({
                'category': 'طلا',
                'title': 'طلای آب‌شده / دست‌دوم (یا صندوق‌های طلا در بورس)',
                'unit_price': gold_18k,
                'affordable_qty': f"{grams:.2f} گرم",
                'risk': 'پایین و کم‌ریسک‌ترین دارایی امن',
                'score': 90,
                'reason': (
                    '• کمترین کارمزد و اجرت (تقریباً صفر در آبشده و صندوق‌ها)\n'
                    '• عدم وجود حباب قیمت برخلاف سکه‌های بانکی\n'
                    '• حفظ صددرصدی ارزش در برابر تورم در بازه ۳ تا ۶ ماهه.'
                )
            })

        # ۳. سکه‌های پارسیان (برای بودجه‌های خرد فیزیکی)
        # یافتن بهترین ترکیب پارسیان با این بودجه
        parsian_items = sorted(
            [v for k, v in parsian_data.items() if v['toman'] <= budget_toman],
            key=lambda x: x['weight'],
            reverse=True
        )
        if parsian_items:
            best_p = parsian_items[0]
            count = int(budget_toman // best_p['toman'])
            rem = budget_toman - (count * best_p['toman'])
            recommendations.append({
                'category': 'سکه',
                'title': f"{best_p['title']}",
                'unit_price': best_p['toman'],
                'affordable_qty': f"{count} عدد" + (f" + {rem:,.0f} ت باقیمانده" if rem > 500000 else ""),
                'risk': 'پایین (فیزیکی و کادویی)',
                'score': 85,
                'reason': (
                    '• گزینه عالی برای خرید فیزیکی با بودجه کم (زیر ۱۵ میلیون تومان)\n'
                    '• حباب بسیار کمتر در مقایسه با ربع سکه و نیم سکه بانکی\n'
                    '• نقدشوندگی بسیار سریع در تمام طلافروشی‌ها.'
                )
            })

        # ۴. تتر / دلار (حفظ ارزش ریالی بر پایه ارز)
        usdt_price = curr_data.get('currency_usdt', {}).get('toman', 0) or curr_data.get('currency_usd', {}).get('toman', 0)
        if usdt_price > 0 and budget_toman >= usdt_price:
            usdt_units = budget_toman / usdt_price
            recommendations.append({
                'category': 'ارز دیجیتال / دلار',
                'title': 'تتر (USDT) یا دلار نقدی',
                'unit_price': usdt_price,
                'affordable_qty': f"{usdt_units:.1f} واحد",
                'risk': 'متوسط (وابسته فقط به نرخ ارز داخلی)',
                'score': 75,
                'reason': (
                    '• مناسب برای تبدیل سریع و نقدشوندگی آنی ۲۴ ساعته\n'
                    '• توجه: در بازه ۳ تا ۱۲ ماهه، طلا و نقره به دلیل رشد انس جهانی معمولاً بازدهی بالاتری از ارز ساده داشته‌اند.'
                )
            })

        # ۵. بررسی سکه‌های بانکی (اگر بودجه رسید)
        for coin_key, c_title in [('coin_rob_new', 'ربع سکه'), ('coin_half_new', 'نیم سکه'), ('coin_emami', 'سکه امامی')]:
            c_price = coin_data.get(coin_key, {}).get('toman', 0)
            if c_price > 0 and budget_toman >= c_price:
                qty = int(budget_toman // c_price)
                recommendations.append({
                    'category': 'سکه بانکی',
                    'title': c_title,
                    'unit_price': c_price,
                    'affordable_qty': f"{qty} عدد",
                    'risk': 'نوسانی (دارای حباب قیمتی)',
                    'score': 70,
                    'reason': (
                        '• دارای حباب قیمتی بالا نسبت به ارزش ذاتی طلا\n'
                        '• تنها در موج‌های هیجانی صعودی بازدهی بیشتری نسبت به طلا می‌دهد.'
                    )
                })

        # مرتب‌سازی بر اساس امتیاز تحلیل
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations

advisor_service = InvestmentAdvisor()
