import time
import re
import urllib.parse
import aiohttp
import asyncio
from lxml import html
from typing import Dict, Any, Optional

class TGJUService:
    """
    سرویس دریافت و کش قیمت‌های زنده طلا، سکه، نقره و ارزها از سایت TGJU.org
    """
    CACHE_DURATION = 120  # مدت زمان کش: ۲ دقیقه (بر حسب ثانیه)

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    URLS = {
        'gold': 'https://www.tgju.org/gold-chart',
        'coin': 'https://www.tgju.org/coin',
        'parsian': 'https://www.tgju.org/' + urllib.parse.quote('قیمت-سکه-پارسیان'),
        'currency': 'https://www.tgju.org/currency',
        'home': 'https://www.tgju.org/',
    }

    # نگاشت کدهای طلا و آبشده
    GOLD_KEYS = {
        'geram18': ('طلای ۱۸ عیار', 'gold_18k'),
        'geram24': ('طلای ۲۴ عیار', 'gold_24k'),
        'gold_mini_size': ('طلای دست دوم', 'gold_used'),
        'mesghal': ('مثقال طلا', 'mesghal'),
        'gold_futures': ('آبشده نقدی', 'gold_melted'),
        'gold_melted_transfer': ('آبشده معاملاتی', 'gold_melted_alt'),
    }

    # نگاشت کدهای نقره
    SILVER_KEYS = {
        'silver_999': ('گرم نقره ۹۹۹ (خالص/شمش)', 'silver_999'),
        'silver_925': ('گرم نقره ۹۲۵ (استرلینگ)', 'silver_925'),
    }

    # نگاشت کدهای سکه‌ها
    COIN_KEYS = {
        'retail_sekee': ('سکه امامی (طرح جدید)', 'coin_emami'),
        'sekee': ('سکه امامی', 'coin_emami_alt'),
        'retail_sekeb': ('سکه بهار آزادی (طرح قدیم)', 'coin_bahar'),
        'sekeb': ('سکه بهار آزادی', 'coin_bahar_alt'),
        'retail_nim': ('نیم سکه (طرح جدید)', 'coin_half_new'),
        'nim': ('نیم سکه', 'coin_half_new_alt'),
        'nim_down': ('نیم سکه (طرح قدیم / قبل ۸۶)', 'coin_half_old'),
        'retail_rob': ('ربع سکه (طرح جدید)', 'coin_rob_new'),
        'rob': ('ربع سکه', 'coin_rob_new_alt'),
        'rob_down': ('ربع سکه (طرح قدیم / قبل ۸۶)', 'coin_rob_old'),
        'retail_gerami': ('سکه گرمی', 'coin_grami'),
        'gerami': ('سکه گرمی', 'coin_grami_alt'),
    }

    # نگاشت کدهای ارزها
    CURRENCY_KEYS = {
        'price_dollar_rl': ('دلار آمریکا', 'currency_usd'),
        'crypto-tether-irr': ('تتر (USDT)', 'currency_usdt'),
        'crypto-tether': ('تتر (USDT)', 'currency_usdt_alt'),
        'price_eur': ('یورو', 'currency_eur'),
        'price_aed': ('درهم امارات', 'currency_aed'),
        'price_gbp': ('پوند انگلیس', 'currency_gbp'),
        'price_try': ('لیر ترکیه', 'currency_try'),
        'price_cad': ('دلار کانادا', 'currency_cad'),
        'price_aud': ('دلار استرالیا', 'currency_aud'),
        'price_iqd': ('۱۰۰ دینار عراق', 'currency_iqd'),
    }

    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._last_fetch_time: float = 0
        self._lock = asyncio.Lock()

    @staticmethod
    def _clean_number(text: str) -> Optional[int]:
        """تبدیل رشته‌های شامل کاما و ارقام فارسی/انگلیسی به عدد صحیح ریال"""
        if not text:
            return None
        persian_digits = '۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩'
        english_digits = '01234567890123456789'
        translation_table = str.maketrans(persian_digits, english_digits)
        text = text.translate(translation_table)
        
        cleaned = re.sub(r'[^\d]', '', text)
        if cleaned:
            try:
                return int(cleaned)
            except ValueError:
                return None
        return None

    async def _fetch_page(self, session: aiohttp.ClientSession, url: str) -> str:
        try:
            async with session.get(url, headers=self.HEADERS, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status == 200:
                    return await resp.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return ""

    async def get_all_prices(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        دریافت تمام قیمت‌های روز از TGJU با سیستم کش
        خروجی شامل مبالغ به تومان است.
        """
        async with self._lock:
            current_time = time.time()
            if not force_refresh and self._cache and (current_time - self._last_fetch_time < self.CACHE_DURATION):
                return self._cache

            async with aiohttp.ClientSession() as session:
                tasks = [
                    self._fetch_page(session, self.URLS['gold']),
                    self._fetch_page(session, self.URLS['coin']),
                    self._fetch_page(session, self.URLS['parsian']),
                    self._fetch_page(session, self.URLS['currency']),
                    self._fetch_page(session, self.URLS['home']),
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)

            gold_html, coin_html, parsian_html, currency_html, home_html = (
                res if isinstance(res, str) else "" for res in results
            )

            prices_data = {
                'gold': {},
                'silver': {},
                'coins': {},
                'currencies': {},
                'parsian': {},
                'updated_at': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            }

            # ۱. تجزیه قیمت‌های طلا و نقره
            if gold_html:
                try:
                    tree = html.fromstring(gold_html)
                    for row in tree.xpath('//tr[@data-market-row]'):
                        row_id = row.get('data-market-row', '').strip()
                        price_nodes = row.xpath('.//td[@class="current"]//text() | .//td[contains(@class,"nf")][1]//text() | .//td[1]//text()')
                        price_raw = ' '.join(''.join(price_nodes).split())
                        rial_val = self._clean_number(price_raw)
                        
                        if rial_val:
                            toman_val = rial_val // 10
                            if row_id in self.GOLD_KEYS:
                                title, internal_key = self.GOLD_KEYS[row_id]
                                prices_data['gold'][internal_key] = {
                                    'title': title,
                                    'toman': toman_val,
                                    'rial': rial_val,
                                }
                            elif row_id in self.SILVER_KEYS:
                                title, internal_key = self.SILVER_KEYS[row_id]
                                prices_data['silver'][internal_key] = {
                                    'title': title,
                                    'toman': toman_val,
                                    'rial': rial_val,
                                }
                except Exception as e:
                    print(f"Error parsing gold HTML: {e}")

            # ۲. تجزیه قیمت‌های سکه
            if coin_html:
                try:
                    tree = html.fromstring(coin_html)
                    for row in tree.xpath('//tr[@data-market-row]'):
                        row_id = row.get('data-market-row', '').strip()
                        if row_id in self.COIN_KEYS:
                            title, internal_key = self.COIN_KEYS[row_id]
                            price_nodes = row.xpath('.//td[@class="current"]//text() | .//td[contains(@class,"nf")][1]//text() | .//td[1]//text()')
                            price_raw = ' '.join(''.join(price_nodes).split())
                            rial_val = self._clean_number(price_raw)
                            if rial_val:
                                toman_val = rial_val // 10
                                target_key = internal_key.replace('_alt', '')
                                if target_key not in prices_data['coins'] or not internal_key.endswith('_alt'):
                                    prices_data['coins'][target_key] = {
                                        'title': title.replace(' (طرح جدید)', '').replace(' (طرح قدیم)', ''),
                                        'toman': toman_val,
                                        'rial': rial_val,
                                    }
                except Exception as e:
                    print(f"Error parsing coin HTML: {e}")

            # ۳. تجزیه قیمت‌های ارز (ترکیب صفحه ارز و صفحه اصلی برای تتر)
            for raw_html in [currency_html, home_html]:
                if not raw_html:
                    continue
                try:
                    tree = html.fromstring(raw_html)
                    for row in tree.xpath('//tr[@data-market-row]'):
                        row_id = row.get('data-market-row', '').strip()
                        if row_id in self.CURRENCY_KEYS:
                            title, internal_key = self.CURRENCY_KEYS[row_id]
                            price_nodes = row.xpath('.//td[@class="current"]//text() | .//td[contains(@class,"nf")][1]//text() | .//td[1]//text()')
                            price_raw = ' '.join(''.join(price_nodes).split())
                            rial_val = self._clean_number(price_raw)
                            if rial_val:
                                toman_val = rial_val // 10
                                target_key = internal_key.replace('_alt', '')
                                if target_key not in prices_data['currencies'] or not internal_key.endswith('_alt'):
                                    prices_data['currencies'][target_key] = {
                                        'title': title,
                                        'toman': toman_val,
                                        'rial': rial_val,
                                    }
                except Exception as e:
                    print(f"Error parsing currency HTML: {e}")

            # ۴. تجزیه قیمت‌های پارسیان
            if parsian_html:
                try:
                    tree = html.fromstring(parsian_html)
                    for row in tree.xpath('//tr[@data-market-row]'):
                        th_el = row.xpath('.//th')
                        if not th_el:
                            continue
                        row_text = th_el[0].text_content().strip()
                        price_nodes = row.xpath('.//td[@class="current"]//text() | .//td[contains(@class,"nf")][1]//text() | .//td[1]//text()')
                        price_raw = ' '.join(''.join(price_nodes).split())
                        rial_val = self._clean_number(price_raw)
                        
                        weight_match = re.search(r'([۰-۹\d]+)[/\.٫]([۰-۹\d]+)', row_text)
                        if weight_match and rial_val:
                            whole = weight_match.group(1).translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))
                            fraction = weight_match.group(2).translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))
                            weight_float = float(f"{whole}.{fraction}")
                            toman_val = rial_val // 10
                            prices_data['parsian'][f"{weight_float:.3f}"] = {
                                'title': f"سکه پارسیان {weight_float:g} گرم",
                                'weight': weight_float,
                                'toman': toman_val,
                                'rial': rial_val,
                            }
                except Exception as e:
                    print(f"Error parsing parsian HTML: {e}")

            # بررسی و تنظیم کش در صورت موفقیت
            if prices_data['gold'] or prices_data['coins'] or prices_data['currencies']:
                self._cache = prices_data
                self._last_fetch_time = current_time

            return self._cache or prices_data

    def estimate_parsian_price(self, weight_grams: float, prices: Dict[str, Any]) -> int:
        """تخمین قیمت سکه پارسیان در صورت عدم وجود وزن در جدول TGJU"""
        weight_key = f"{weight_grams:.3f}"
        parsian_table = prices.get('parsian', {})
        if weight_key in parsian_table:
            return parsian_table[weight_key]['toman']

        gold_18k_toman = prices.get('gold', {}).get('gold_18k', {}).get('toman', 0)
        if gold_18k_toman > 0:
            base = int(gold_18k_toman * weight_grams)
            fee = int(400_000 * min(1.0, weight_grams + 0.5))
            return base + fee
        return 0

tgju_service = TGJUService()
