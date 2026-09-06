import time
import re
import urllib.parse
import aiohttp
import asyncio
from lxml import html
from typing import Dict, Any, Optional

class TGJUService:
    """
    سرویس دریافت و کش قیمت‌های زنده طلا، سکه، نقره، ارزها، حباب‌ها،
    سقف و کف روزانه و شاخص‌های کلان اقتصاد (GSR و انس) از سایت TGJU.org
    """
    CACHE_DURATION = 120  # ۲ دقیقه کش

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

    GOLD_KEYS = {
        'geram18': ('طلای ۱۸ عیار', 'gold_18k'),
        'geram24': ('طلای ۲۴ عیار', 'gold_24k'),
        'gold_mini_size': ('طلای دست دوم', 'gold_used'),
        'mesghal': ('مثقال طلا', 'mesghal'),
        'gold_futures': ('آبشده نقدی', 'gold_melted'),
        'gold_melted_transfer': ('آبشده معاملاتی', 'gold_melted_alt'),
    }

    SILVER_KEYS = {
        'silver_999': ('گرم نقره ۹۹۹ (خالص/شمش)', 'silver_999'),
        'silver_925': ('گرم نقره ۹۲۵ (استرلینگ)', 'silver_925'),
    }

    COIN_KEYS = {
        'retail_sekee': ('سکه امامی (طرح جدید)', 'coin_emami'),
        'sekee': ('سکه امامی', 'coin_emami_alt'),
        'retail_sekeb': ('سکه بهار آزادی (طرح قدیم)', 'coin_bahar'),
        'sekeb': ('سکه بهار آزادی', 'coin_bahar_alt'),
        'retail_nim': ('نیم سکه (طرح جدید)', 'coin_half_new'),
        'nim': ('نیم سکه', 'coin_half_new_alt'),
        'retail_rob': ('ربع سکه (طرح جدید)', 'coin_rob_new'),
        'rob': ('ربع سکه', 'coin_rob_new_alt'),
        'retail_gerami': ('سکه گرمی', 'coin_grami'),
        'gerami': ('سکه گرمی', 'coin_grami_alt'),
        # سکه‌های طرح قدیم (قبل ۸۶)
        'sekee_down': ('تمام سکه طرح قدیم (قبل ۸۶)', 'coin_emami_old'),
        'nim_down': ('نیم سکه طرح قدیم (قبل ۸۶)', 'coin_half_old'),
        'rob_down': ('ربع سکه طرح قدیم (قبل ۸۶)', 'coin_rob_old'),
    }

    BUBBLE_KEYS = {
        'coin_blubber': ('حباب سکه امامی', 'bubble_emami'),
        'sekeb_blubber': ('حباب بهار آزادی', 'bubble_bahar'),
        'nim_blubber': ('حباب نیم سکه', 'bubble_nim'),
        'rob_blubber': ('حباب ربع سکه', 'bubble_rob'),
        'gerami_blubber': ('حباب سکه گرمی', 'bubble_grami'),
    }

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
        if not text:
            return None
        persian_digits = '۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧۸۹'
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

    @staticmethod
    def _parse_float(text: str) -> float:
        if not text:
            return 0.0
        persian_digits = '۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩'
        english_digits = '01234567890123456789'
        translation_table = str.maketrans(persian_digits, english_digits)
        text = text.translate(translation_table).replace(',', '').strip()
        match = re.search(r'[\d\.]+', text)
        if match:
            try:
                return float(match.group(0))
            except ValueError:
                return 0.0
        return 0.0

    def _extract_row_metrics(self, row) -> Optional[Dict[str, Any]]:
        tds = row.xpath('.//td')
        if not tds:
            return None
        price_raw = ' '.join(''.join(tds[0].xpath('.//text()')).split())
        rial_val = self._clean_number(price_raw)
        if not rial_val:
            return None
        
        toman_val = rial_val // 10
        
        change_text = tds[1].text_content().strip() if len(tds) > 1 else ""
        low_rial = self._clean_number(tds[2].text_content().strip()) if len(tds) > 2 else None
        high_rial = self._clean_number(tds[3].text_content().strip()) if len(tds) > 3 else None
        time_text = tds[4].text_content().strip() if len(tds) > 4 else ""
        
        low_toman = (low_rial // 10) if (low_rial and low_rial > 0) else toman_val
        high_toman = (high_rial // 10) if (high_rial and high_rial > 0) else toman_val
        
        return {
            'toman': toman_val,
            'rial': rial_val,
            'low_toman': low_toman,
            'high_toman': high_toman,
            'change': change_text,
            'time': time_text,
        }

    async def _fetch_page(self, session: aiohttp.ClientSession, url: str) -> str:
        try:
            async with session.get(url, headers=self.HEADERS, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status == 200:
                    return await resp.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return ""

    async def get_all_prices(self, force_refresh: bool = False) -> Dict[str, Any]:
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
                'bubbles': {},
                'currencies': {},
                'parsian': {},
                'macro': {},
                'updated_at': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            }

            # ۱. طلا و نقره از صفحه gold-chart
            if gold_html:
                try:
                    tree = html.fromstring(gold_html)
                    for row in tree.xpath('//tr[@data-market-row]'):
                        row_id = row.get('data-market-row', '').strip()
                        metrics = self._extract_row_metrics(row)
                        if not metrics:
                            continue
                        
                        if row_id in self.GOLD_KEYS:
                            title, internal_key = self.GOLD_KEYS[row_id]
                            target_key = internal_key.replace('_alt', '')
                            if target_key not in prices_data['gold'] or not internal_key.endswith('_alt'):
                                prices_data['gold'][target_key] = {
                                    'title': title,
                                    **metrics
                                }
                        elif row_id in self.SILVER_KEYS:
                            title, internal_key = self.SILVER_KEYS[row_id]
                            prices_data['silver'][internal_key] = {
                                'title': title,
                                **metrics
                            }
                except Exception as e:
                    print(f"Error parsing gold HTML: {e}")

            # ۲. سکه‌ها و حباب‌ها از صفحه coin
            if coin_html:
                try:
                    tree = html.fromstring(coin_html)
                    for row in tree.xpath('//tr[@data-market-row]'):
                        row_id = row.get('data-market-row', '').strip()
                        metrics = self._extract_row_metrics(row)
                        if not metrics:
                            continue

                        if row_id in self.COIN_KEYS:
                            title, internal_key = self.COIN_KEYS[row_id]
                            target_key = internal_key.replace('_alt', '')
                            if target_key not in prices_data['coins'] or not internal_key.endswith('_alt'):
                                prices_data['coins'][target_key] = {
                                    'title': title.replace(' (طرح جدید)', ''),
                                    **metrics
                                }
                        elif row_id in self.BUBBLE_KEYS:
                            title, internal_key = self.BUBBLE_KEYS[row_id]
                            prices_data['bubbles'][internal_key] = {
                                'title': title,
                                **metrics
                            }
                except Exception as e:
                    print(f"Error parsing coin HTML: {e}")

            # محاسبه درصدی حباب‌ها
            for coin_k, bub_k in [
                ('coin_emami', 'bubble_emami'),
                ('coin_bahar', 'bubble_bahar'),
                ('coin_half_new', 'bubble_nim'),
                ('coin_rob_new', 'bubble_rob'),
                ('coin_grami', 'bubble_grami'),
            ]:
                if coin_k in prices_data['coins'] and bub_k in prices_data['bubbles']:
                    c_price = prices_data['coins'][coin_k]['toman']
                    b_val = prices_data['bubbles'][bub_k]['toman']
                    if c_price > 0:
                        prices_data['bubbles'][bub_k]['percentage'] = round((b_val / c_price) * 100, 1)

            # ۳. ارزها از صفحه currency و home
            for raw_html in [currency_html, home_html]:
                if not raw_html:
                    continue
                try:
                    tree = html.fromstring(raw_html)
                    for row in tree.xpath('//tr[@data-market-row]'):
                        row_id = row.get('data-market-row', '').strip()
                        metrics = self._extract_row_metrics(row)
                        if not metrics:
                            continue

                        if row_id in self.CURRENCY_KEYS:
                            title, internal_key = self.CURRENCY_KEYS[row_id]
                            target_key = internal_key.replace('_alt', '')
                            if target_key not in prices_data['currencies'] or not internal_key.endswith('_alt'):
                                prices_data['currencies'][target_key] = {
                                    'title': title,
                                    **metrics
                                }
                        elif row_id == 'silver_999' and 'silver_999' not in prices_data['silver']:
                            prices_data['silver']['silver_999'] = {
                                'title': 'گرم نقره ۹۹۹ (خالص/شمش)',
                                **metrics
                            }
                except Exception as e:
                    print(f"Error parsing currency HTML: {e}")

            # محاسبه نقره ۹۲۵ در صورت نبود نرخ مجزا
            if 'silver_999' in prices_data['silver'] and 'silver_925' not in prices_data['silver']:
                s999 = prices_data['silver']['silver_999']
                ratio = 925 / 999
                prices_data['silver']['silver_925'] = {
                    'title': 'گرم نقره ۹۲۵ (استرلینگ)',
                    'toman': int(s999['toman'] * ratio),
                    'rial': int(s999['rial'] * ratio),
                    'low_toman': int(s999.get('low_toman', s999['toman']) * ratio),
                    'high_toman': int(s999.get('high_toman', s999['toman']) * ratio),
                    'change': s999.get('change', ''),
                    'time': s999.get('time', ''),
                }

            # ۴. پارسیان
            if parsian_html:
                try:
                    tree = html.fromstring(parsian_html)
                    for row in tree.xpath('//tr[@data-market-row]'):
                        th_el = row.xpath('.//th')
                        if not th_el:
                            continue
                        row_text = th_el[0].text_content().strip()
                        metrics = self._extract_row_metrics(row)
                        if not metrics:
                            continue
                        
                        weight_match = re.search(r'([۰-۹\d]+)[/\.٫]([۰-۹\d]+)', row_text)
                        if weight_match:
                            whole = weight_match.group(1).translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))
                            fraction = weight_match.group(2).translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))
                            weight_float = float(f"{whole}.{fraction}")
                            prices_data['parsian'][f"{weight_float:.3f}"] = {
                                'title': f"سکه پارسیان {weight_float:g} گرم",
                                'weight': weight_float,
                                **metrics
                            }
                except Exception as e:
                    print(f"Error parsing parsian HTML: {e}")

            # ۵. استخراج شاخص‌های کلان اقتصاد (انس طلا و انس نقره و GSR)
            if home_html:
                try:
                    tree = html.fromstring(home_html)
                    ons_gold = 0.0
                    ons_silver = 0.0
                    for row in tree.xpath('//tr[@data-market-row]'):
                        row_id = row.get('data-market-row', '').strip()
                        tds = [td.text_content().strip() for td in row.xpath('.//td')]
                        if row_id == 'ons' and tds and not ons_gold:
                            ons_gold = self._parse_float(tds[0])
                        elif row_id == 'silver' and tds and not ons_silver:
                            ons_silver = self._parse_float(tds[0])

                    if ons_gold > 0:
                        prices_data['macro']['ons_gold'] = ons_gold
                    if ons_silver > 0:
                        prices_data['macro']['ons_silver'] = ons_silver
                    if ons_gold > 0 and ons_silver > 0:
                        prices_data['macro']['gold_silver_ratio'] = round(ons_gold / ons_silver, 2)
                except Exception as e:
                    print(f"Error parsing macro metrics: {e}")

            if prices_data['gold'] or prices_data['coins'] or prices_data['currencies']:
                self._cache = prices_data
                self._last_fetch_time = current_time

            return self._cache or prices_data

    def estimate_parsian_price(self, weight_grams: float, prices: Dict[str, Any]) -> int:
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

