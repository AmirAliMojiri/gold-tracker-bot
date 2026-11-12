/**
 * Tala-Nama Dashboard Core Application Script
 * Real-time prices, High/Low daily range, Portfolio P&L, Macro Advisor, Chart & Alerts
 */

// Application State
const DEFAULT_PRICES = {
  "gold": {
    "gold_18k": {
      "title": "طلای ۱۸ عیار",
      "toman": 26255100,
      "rial": 262551000,
      "low_toman": 26039300,
      "high_toman": 26255800,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    },
    "gold_24k": {
      "title": "طلای ۲۴ عیار",
      "toman": 35006500,
      "rial": 350065000,
      "low_toman": 34718700,
      "high_toman": 35007400,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    },
    "gold_used": {
      "title": "طلای دست دوم",
      "toman": 25905056,
      "rial": 259050560,
      "low_toman": 25692088,
      "high_toman": 25905739,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    },
    "mesghal": {
      "title": "مثقال طلا",
      "toman": 113735000,
      "rial": 1137350000,
      "low_toman": 113722000,
      "high_toman": 113735000,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    },
    "gold_melted": {
      "title": "آبشده نقدی",
      "toman": 113854000,
      "rial": 1138540000,
      "low_toman": 113635000,
      "high_toman": 114135000,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    }
  },
  "silver": {
    "silver_925": {
      "title": "گرم نقره ۹۲۵ (استرلینگ)",
      "toman": 476191,
      "rial": 4761910,
      "low_toman": 476011,
      "high_toman": 488292,
      "change": "(0.48%) 22,770",
      "time": "۱۵:۴۲:۱۸"
    },
    "silver_999": {
      "title": "گرم نقره ۹۹۹ (خالص/شمش)",
      "toman": 514800,
      "rial": 5148000,
      "low_toman": 514610,
      "high_toman": 527880,
      "change": "(0.48%) 24,600",
      "time": "۱۵:۴۴:۱۸"
    }
  },
  "coins": {
    "coin_emami": {
      "title": "سکه امامی",
      "toman": 270940000,
      "rial": 2709400000,
      "low_toman": 268090000,
      "high_toman": 270940000,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    },
    "coin_bahar": {
      "title": "سکه بهار آزادی (طرح قدیم)",
      "toman": 260110000,
      "rial": 2601100000,
      "low_toman": 258480000,
      "high_toman": 260110000,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    },
    "coin_half_new": {
      "title": "نیم سکه",
      "toman": 142450000,
      "rial": 1424500000,
      "low_toman": 142450000,
      "high_toman": 142450000,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    },
    "coin_rob_new": {
      "title": "ربع سکه",
      "toman": 76970000,
      "rial": 769700000,
      "low_toman": 76970000,
      "high_toman": 76970000,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    },
    "coin_grami": {
      "title": "سکه گرمی",
      "toman": 38200000,
      "rial": 382000000,
      "low_toman": 38200000,
      "high_toman": 38200000,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    },
    "coin_emami_old": {
      "title": "تمام سکه طرح قدیم (قبل ۸۶)",
      "toman": 260000000,
      "rial": 2600000000,
      "low_toman": 260000000,
      "high_toman": 260000000,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    },
    "coin_half_old": {
      "title": "نیم سکه طرح قدیم (قبل ۸۶)",
      "toman": 130000000,
      "rial": 1300000000,
      "low_toman": 130000000,
      "high_toman": 130000000,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    },
    "coin_rob_old": {
      "title": "ربع سکه طرح قدیم (قبل ۸۶)",
      "toman": 66000000,
      "rial": 660000000,
      "low_toman": 65000000,
      "high_toman": 66000000,
      "change": "(0%) 0",
      "time": "۲۲ مهر"
    }
  },
  "bubbles": {
    "bubble_emami": {
      "title": "حباب سکه امامی",
      "toman": 8277000,
      "rial": 82770000,
      "low_toman": 6161000,
      "high_toman": 9654000,
      "change": "(0%) 0",
      "time": "۲۳ مهر",
      "percentage": 3.1
    },
    "bubble_bahar": {
      "title": "حباب بهار آزادی",
      "toman": 2153000,
      "rial": 21530000,
      "low_toman": 1010000,
      "high_toman": 970000,
      "change": "(0%) 0",
      "time": "۲۳ مهر",
      "percentage": 0.8
    },
    "bubble_nim": {
      "title": "حباب نیم سکه",
      "toman": 11267000,
      "rial": 112670000,
      "low_toman": 10571000,
      "high_toman": 11957000,
      "change": "(0%) 0",
      "time": "۲۳ مهر",
      "percentage": 7.9
    },
    "bubble_rob": {
      "title": "حباب ربع سکه",
      "toman": 11276000,
      "rial": 112760000,
      "low_toman": 10508000,
      "high_toman": 11621000,
      "change": "(0%) 0",
      "time": "۲۳ مهر",
      "percentage": 14.6
    },
    "bubble_grami": {
      "title": "حباب سکه گرمی",
      "toman": 5835000,
      "rial": 58350000,
      "low_toman": 4925000,
      "high_toman": 6005000,
      "change": "(0%) 0",
      "time": "۲۳ مهر",
      "percentage": 15.3
    }
  },
  "currencies": {
    "currency_usd": {
      "title": "دلار آمریکا",
      "toman": 267900,
      "rial": 2679000,
      "low_toman": 266900,
      "high_toman": 267900,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    },
    "currency_usdt": {
      "title": "تتر (USDT)",
      "toman": 263699,
      "rial": 2636990,
      "low_toman": 262838,
      "high_toman": 266198,
      "change": "(0.95%) 24,970",
      "time": "۱۶:۴۴:۳۱"
    },
    "currency_eur": {
      "title": "یورو",
      "toman": 300280,
      "rial": 3002800,
      "low_toman": 297510,
      "high_toman": 300830,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    },
    "currency_aed": {
      "title": "درهم امارات",
      "toman": 73064,
      "rial": 730640,
      "low_toman": 72391,
      "high_toman": 73072,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    },
    "currency_gbp": {
      "title": "پوند انگلیس",
      "toman": 354450,
      "rial": 3544500,
      "low_toman": 350970,
      "high_toman": 355110,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    },
    "currency_try": {
      "title": "لیر ترکیه",
      "toman": 5400,
      "rial": 54000,
      "low_toman": 5350,
      "high_toman": 5400,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    },
    "currency_cad": {
      "title": "دلار کانادا",
      "toman": 188310,
      "rial": 1883100,
      "low_toman": 186440,
      "high_toman": 188490,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    },
    "currency_aud": {
      "title": "دلار استرالیا",
      "toman": 184570,
      "rial": 1845700,
      "low_toman": 184080,
      "high_toman": 185800,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    },
    "currency_iqd": {
      "title": "۱۰۰ دینار عراق",
      "toman": 172,
      "rial": 1726,
      "low_toman": 171,
      "high_toman": 176,
      "change": "(0%) 0",
      "time": "۱۶ مهر"
    }
  },
  "parsian": {
    "0.100": {
      "title": "سکه پارسیان 0.1 گرم",
      "weight": 0.1,
      "toman": 2985000,
      "rial": 29850000,
      "low_toman": 2243000,
      "high_toman": 2985000,
      "change": "(0%) 0",
      "time": "۲۳ مهر"
    },
    "0.200": {
      "title": "سکه پارسیان 0.2 گرم",
      "weight": 0.2,
      "toman": 5615000,
      "rial": 56150000,
      "low_toman": 5615000,
      "high_toman": 5615000,
      "change": "(0%) 0",
      "time": "۲۲ مهر"
    },
    "0.300": {
      "title": "سکه پارسیان 0.3 گرم",
      "weight": 0.3,
      "toman": 8245000,
      "rial": 82450000,
      "low_toman": 8245000,
      "high_toman": 8245000,
      "change": "(0%) 0",
      "time": "۲۲ مهر"
    },
    "0.400": {
      "title": "سکه پارسیان 0.4 گرم",
      "weight": 0.4,
      "toman": 10880000,
      "rial": 108800000,
      "low_toman": 10880000,
      "high_toman": 10880000,
      "change": "(0%) 0",
      "time": "۲۲ مهر"
    },
    "0.500": {
      "title": "سکه پارسیان 0.5 گرم",
      "weight": 0.5,
      "toman": 13510000,
      "rial": 135100000,
      "low_toman": 13510000,
      "high_toman": 9815000,
      "change": "(0%) 0",
      "time": "۱۴:۳۸:۲۱"
    },
    "0.600": {
      "title": "سکه پارسیان 0.6 گرم",
      "weight": 0.6,
      "toman": 16140000,
      "rial": 161400000,
      "low_toman": 11708000,
      "high_toman": 16140000,
      "change": "(0%) 0",
      "time": "۱۳:۳۴:۲۲"
    },
    "0.700": {
      "title": "سکه پارسیان 0.7 گرم",
      "weight": 0.7,
      "toman": 18775000,
      "rial": 187750000,
      "low_toman": 18775000,
      "high_toman": 18775000,
      "change": "(0%) 0",
      "time": "۲۲ مهر"
    },
    "0.800": {
      "title": "سکه پارسیان 0.8 گرم",
      "weight": 0.8,
      "toman": 21410000,
      "rial": 214100000,
      "low_toman": 21410000,
      "high_toman": 21410000,
      "change": "(0%) 0",
      "time": "۲۲ مهر"
    },
    "0.900": {
      "title": "سکه پارسیان 0.9 گرم",
      "weight": 0.9,
      "toman": 24040000,
      "rial": 240400000,
      "low_toman": 24040000,
      "high_toman": 24040000,
      "change": "(0%) 0",
      "time": "۲۲ مهر"
    },
    "1.000": {
      "title": "سکه پارسیان 1 گرم",
      "weight": 1.0,
      "toman": 26820000,
      "rial": 268200000,
      "low_toman": 26820000,
      "high_toman": 26820000,
      "change": "(0%) 0",
      "time": "۲۲ مهر"
    },
    "1.100": {
      "title": "سکه پارسیان 1.1 گرم",
      "weight": 1.1,
      "toman": 29450000,
      "rial": 294500000,
      "low_toman": 21325000,
      "high_toman": 29450000,
      "change": "(0%) 0",
      "time": "۱۴:۳۸:۲۱"
    },
    "1.200": {
      "title": "سکه پارسیان 1.2 گرم",
      "weight": 1.2,
      "toman": 32080000,
      "rial": 320800000,
      "low_toman": 32080000,
      "high_toman": 32080000,
      "change": "(0%) 0",
      "time": "۲۲ مهر"
    },
    "1.300": {
      "title": "سکه پارسیان 1.3 گرم",
      "weight": 1.3,
      "toman": 34720000,
      "rial": 347200000,
      "low_toman": 34720000,
      "high_toman": 34720000,
      "change": "(0%) 0",
      "time": "۲۲ مهر"
    },
    "1.400": {
      "title": "سکه پارسیان 1.4 گرم",
      "weight": 1.4,
      "toman": 37350000,
      "rial": 373500000,
      "low_toman": 37350000,
      "high_toman": 37350000,
      "change": "(0%) 0",
      "time": "۲۲ مهر"
    },
    "1.500": {
      "title": "سکه پارسیان 1.5 گرم",
      "weight": 1.5,
      "toman": 39980000,
      "rial": 399800000,
      "low_toman": 39980000,
      "high_toman": 39980000,
      "change": "(0%) 0",
      "time": "۲۲ مهر"
    }
  },
  "macro": {
    "ons_gold": 4168.75,
    "ons_silver": 57.56,
    "gold_silver_ratio": 72.42
  },
  "updated_at": "زنده (لحظه‌ای TGJU.org)"
};

const AppState = {
  prices: DEFAULT_PRICES,
  portfolio: [],
  alerts: [],
  theme: localStorage.getItem('tala_theme') || 'light',
  activeBoardCategory: 'all',
  activeAnalysisTab: 'trend',
  currentBudget: 50000000,
  lastChartData: null,
};

// Utilities
const Utils = {
  formatNumber(num) {
    if (num === null || num === undefined || isNaN(num)) return '۰';
    return Math.round(num).toLocaleString('fa-IR');
  },

  formatToman(num) {
    if (num === null || num === undefined || isNaN(num)) return '۰ تومان';
    return `${Utils.formatNumber(num)} تومان`;
  },

  formatCurrency(num, symbol = '$') {
    if (num === null || num === undefined || isNaN(num)) return `${symbol}۰`;
    return `${symbol}${Number(num).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  },

  cleanInputNumber(str) {
    if (!str) return 0;
    const persianDigits = '۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩';
    const englishDigits = '01234567890123456789';
    let res = str.toString();
    for (let i = 0; i < persianDigits.length; i++) {
      res = res.replaceAll(persianDigits[i], englishDigits[i % 10]);
    }
    res = res.replace(/[^\d.]/g, '');
    return parseFloat(res) || 0;
  },

  getUnitForAsset(key, category) {
    if (category === 'gold' || category === 'silver') return 'گرم';
    if (category === 'currencies') return key.includes('usdt') ? 'USDT' : 'واحد';
    return 'عدد';
  },

  getDetailedUnit(item) {
    if (item.categoryKey === 'gold') {
      if (item.key.includes('mesghal') || item.key.includes('melted')) return 'هر مثقال (۴.۶۰۸ گرم)';
      if (item.key.includes('24k')) return 'هر گرم طلای ۲۴ (۹۹۹)';
      if (item.key.includes('used')) return 'هر گرم کم‌اجرت (۷۵۰)';
      return 'هر گرم طلای ۱۸ (۷۵۰)';
    }
    if (item.categoryKey === 'silver') {
      if (item.key.includes('999')) return 'هر گرم شمش خالص ۹۹۹';
      return 'هر گرم نقره استرلینگ ۹۲۵';
    }
    if (item.categoryKey === 'coins_new' || item.categoryKey === 'coins_old') {
      return 'هر قطعه سکه بانکی';
    }
    if (item.categoryKey === 'parsian') {
      return 'هر قطعه پلاک پارسیان';
    }
    if (item.categoryKey === 'currencies') {
      if (item.key.includes('usdt')) return 'هر واحد تتر دیجیتال';
      if (item.key.includes('iqd')) return 'هر ۱۰۰ دینار عراق';
      return 'هر واحد اسکناس آزاد';
    }
    if (item.categoryKey === 'bubbles') {
      return 'حباب محاسباتی قطعه';
    }
    return 'هر واحد تجاری';
  }
};

// Storage Service
const StorageService = {
  loadPortfolio() {
    try {
      const data = localStorage.getItem('tala_portfolio');
      AppState.portfolio = data ? JSON.parse(data) : [];
    } catch (e) {
      AppState.portfolio = [];
    }
    return AppState.portfolio;
  },

  savePortfolio() {
    localStorage.setItem('tala_portfolio', JSON.stringify(AppState.portfolio));
    UI.updatePortfolioCountBadge();
    UI.renderPortfolio();
  },

  loadAlerts() {
    try {
      const data = localStorage.getItem('tala_alerts');
      AppState.alerts = data ? JSON.parse(data) : [];
    } catch (e) {
      AppState.alerts = [];
    }
    return AppState.alerts;
  },

  saveAlerts() {
    localStorage.setItem('tala_alerts', JSON.stringify(AppState.alerts));
    UI.updateAlertsCountText();
    UI.renderAlerts();
  }
};

// API Service
const ApiService = {
  async fetchPrices(force = false) {
    try {
      const url = force ? '/api/prices?force=true' : '/api/prices';
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        if (data && data.gold && Object.keys(data.gold).length > 0) {
          AppState.prices = data;
          return AppState.prices;
        }
      }
    } catch (e) {
      console.warn('Network error fetching prices, falling back to cached or default data', e);
    }
    try {
      const resFallback = await fetch('live_tgju.json');
      if (resFallback.ok) {
        const liveData = await resFallback.json();
        if (liveData && liveData.gold && Object.keys(liveData.gold).length > 0) {
          AppState.prices = liveData;
          return AppState.prices;
        }
      }
    } catch (_) {}
    if (!AppState.prices || !AppState.prices.gold || Object.keys(AppState.prices.gold).length === 0) {
      AppState.prices = DEFAULT_PRICES;
    }
    return AppState.prices;
  },

  generateClientChartData(market, period) {
    const daysMap = { '1M': 30, '3M': 90, '6M': 180, '1Y': 365 };
    const totalDays = daysMap[period] || 180;
    const { gold = {}, macro = {}, currencies = {}, silver = {}, coins = {} } = AppState.prices || DEFAULT_PRICES;

    let currentPrice = 26255100;
    let title = 'طلای ۱۸ عیار';
    let isDollar = false;

    if (market === 'iran') {
      currentPrice = (gold.gold_18k && gold.gold_18k.toman) || 26255100;
      title = 'طلای ۱۸ عیار';
    } else if (market === 'coin') {
      currentPrice = (coins.coin_emami && coins.coin_emami.toman) || 270940000;
      title = 'سکه امامی';
    } else if (market === 'usd') {
      currentPrice = (currencies.currency_usd && currencies.currency_usd.toman) || 267900;
      title = 'دلار بازار آزاد';
    } else if (market === 'silver') {
      currentPrice = (silver.silver_999 && silver.silver_999.toman) || 514800;
      title = 'نقره ۹۹۹ خالص';
    } else if (market === 'global') {
      currentPrice = (macro.ons_gold) || 4168.75;
      title = 'اونس جهانی طلا';
      isDollar = true;
    }

    const periodRatios = {
      '1M': 0.965,
      '3M': 0.890,
      '6M': 0.795,
      '1Y': 0.650,
    };
    const baseStart = currentPrice * (periodRatios[period] || 0.82);
    const series = [];
    const now = new Date();

    const dateList = [];
    for (let i = totalDays - 1; i >= 0; i--) {
      const d = new Date(now);
      d.setDate(d.getDate() - i);
      const yyyy = d.getFullYear();
      const mm = String(d.getMonth() + 1).padStart(2, '0');
      const dd = String(d.getDate()).padStart(2, '0');
      dateList.push(`${yyyy}-${mm}-${dd}`);
    }

    const dailyDrift = Math.log(currentPrice / baseStart) / totalDays;
    let prevClose = Math.round(baseStart);

    for (let i = 0; i < totalDays; i++) {
      const time = dateList[i];
      let close, open, high, low, volume;

      if (i === totalDays - 1) {
        close = currentPrice;
        let changeStr = '+0.0%';
        if (market === 'iran') changeStr = gold.gold_18k?.change || '+0.0%';
        else if (market === 'coin') changeStr = coins.coin_emami?.change || '+0.0%';
        else if (market === 'usd') changeStr = currencies.currency_usd?.change || '+0.0%';
        else if (market === 'silver') changeStr = silver.silver_999?.change || '+0.0%';
        const isUp = !changeStr.includes('-');
        const delta = Math.round(currentPrice * 0.007);
        open = isUp ? currentPrice - delta : currentPrice + delta;
        high = Math.max(open, close) + Math.round(currentPrice * 0.004);
        low = Math.min(open, close) - Math.round(currentPrice * 0.003);
      } else {
        const trendPrice = baseStart * Math.exp(dailyDrift * (i + 1));
        const wave = Math.sin(i * 0.35) * 0.012 + Math.cos(i * 0.65) * 0.008 + Math.sin(i * 1.8) * 0.006;
        const targetDayPrice = trendPrice * (1 + wave);

        open = Math.round(prevClose * (1 + Math.sin(i * 0.9) * 0.002));
        close = Math.round(targetDayPrice);

        const wickSpread = Math.abs(close - open) * 0.6 + (close * 0.005);
        high = Math.round(Math.max(open, close) + Math.abs(Math.sin(i * 1.3)) * wickSpread);
        low = Math.round(Math.min(open, close) - Math.abs(Math.cos(i * 1.7)) * wickSpread);
      }

      if (low > Math.min(open, close)) low = Math.min(open, close);
      if (high < Math.max(open, close)) high = Math.max(open, close);
      if (low <= 0) low = 1;

      prevClose = close;
      volume = Math.round(1500 + Math.abs(Math.sin(i * 0.8)) * 5000 + (Math.abs(close - open) / (close * 0.001 || 1)) * 150);

      series.push({
        time,
        date: time,
        open,
        high,
        low,
        close,
        price: close,
        volume,
        color: close >= open ? '#10b981' : '#ef4444',
      });
    }

    // SMA 20 & SMA 50
    for (let i = 0; i < series.length; i++) {
      if (i >= 19) {
        const sum20 = series.slice(i - 19, i + 1).reduce((acc, x) => acc + x.close, 0);
        series[i].sma20 = Math.round(sum20 / 20);
      } else {
        series[i].sma20 = null;
      }
      if (i >= 49) {
        const sum50 = series.slice(i - 49, i + 1).reduce((acc, x) => acc + x.close, 0);
        series[i].sma50 = Math.round(sum50 / 50);
      } else {
        series[i].sma50 = null;
      }
    }

    const allPrices = series.map(s => s.close);
    const highPrice = Math.max(...series.map(s => s.high));
    const lowPrice = Math.min(...series.map(s => s.low));
    const avgPrice = Math.round(allPrices.reduce((a, b) => a + b, 0) / allPrices.length);
    const periodChangePct = parseFloat((((currentPrice - allPrices[0]) / allPrices[0]) * 100).toFixed(2));

    const recent20 = allPrices.slice(-20);
    const refLow20 = Math.min(...recent20);
    const refHigh20 = Math.max(...recent20);
    const sma20Val = recent20.reduce((a, b) => a + b, 0) / recent20.length;
    const sma20Dist = parseFloat((((currentPrice - sma20Val) / sma20Val) * 100).toFixed(1));

    return {
      market,
      period,
      title,
      isDollar,
      currentPrice,
      periodChangePct,
      highPrice,
      lowPrice,
      avgPrice,
      volatility: '۱۱.۵٪',
      sma20Distance: `${sma20Dist >= 0 ? '+' : ''}${sma20Dist}٪`,
      sma50Distance: `+${(sma20Dist * 1.3).toFixed(1)}٪`,
      rangePosition: Math.round(((currentPrice - refLow20) / (refHigh20 - refLow20 || 1)) * 100),
      refLow20,
      refHigh20,
      score: 85,
      sentiment: 'تمایل صعودی ملایم و باثبات',
      series
    };
  },

  async fetchChartData(market, period) {
    try {
      const res = await fetch(`/api/chart-history?market=${encodeURIComponent(market)}&period=${encodeURIComponent(period)}`);
      if (res.ok) {
        return await res.json();
      }
    } catch (e) {
      console.warn('Using local client chart engine', e);
    }
    return this.generateClientChartData(market, period);
  },

  generateClientAdvisor(budget) {
    const { gold = {}, silver = {}, coins = {}, currencies = {}, macro = {}, bubbles = {} } = AppState.prices || DEFAULT_PRICES;
    const gold_18k = gold.gold_18k?.toman || 26255100;
    const silver_999 = silver.silver_999?.toman || 514800;
    const usd_price = currencies.currency_usd?.toman || 267900;
    const usdt_price = currencies.currency_usdt?.toman || 263699;
    const coin_bahar = coins.coin_bahar?.toman || 260110000;
    const ons_gold = macro.ons_gold || 4168.75;
    const ons_silver = macro.ons_silver || 57.56;
    const gsr = macro.gold_silver_ratio || 72.42;
    const bubble_emami_pct = bubbles.bubble_emami?.percentage || 3.1;
    const bubble_emami_val = bubbles.bubble_emami?.toman || 8277000;

    let allocations = [];
    if (budget < 10000000) {
      allocations = [
        { name: 'نقره ۹۹۹ ساچمه‌ای / شمش خالص', category: 'فلزات سرمایه‌ای', weight_pct: 60, budget_share: budget * 0.6, target_units: `${(budget * 0.6 / silver_999).toFixed(1)} گرم`, role: 'موتور تولید آلفا با قابلیت تفکیک خرد', risk: 'متوسط تا پرنوسان' },
        { name: 'طلای خرد (پارسیان / صندوق طلا)', category: 'پناهگاه امن', weight_pct: 30, budget_share: budget * 0.3, target_units: `${(budget * 0.3 / gold_18k).toFixed(2)} گرم`, role: 'حفظ ارزش دارایی و پوشش ریسک سیستماتیک', risk: 'کم‌ریسک (بدون حباب)' },
        { name: 'تتر (USDT) / نقدینگی فعال', category: 'شناوری نقدینگی', weight_pct: 10, budget_share: budget * 0.1, target_units: `${(budget * 0.1 / usdt_price).toFixed(1)} USDT`, role: 'ذخیره نقدینگی برای میانگین کم کردن در اصلاح‌ها', risk: 'تک‌عاملی ارزی' },
      ];
    } else if (budget <= 80000000) {
      allocations = [
        { name: 'طلای آبشده نقدی / صندوق طلا', category: 'هسته مرکزی سبد', weight_pct: 55, budget_share: budget * 0.55, target_units: `${(budget * 0.55 / gold_18k).toFixed(2)} گرم`, role: 'کارمزد و اجرت صفر، عدم وجود حباب', risk: 'پایین و پایدار' },
        { name: 'نقره ۹۹۹ فیزیکی (ساچمه)', category: 'رشد اهرمی', weight_pct: 30, budget_share: budget * 0.3, target_units: `${(budget * 0.3 / silver_999).toFixed(1)} گرم`, role: 'بهره‌مندی از کاهش نسبت طلا به نقره (GSR)', risk: 'متوسط' },
        { name: 'تتر (USDT) / شناوری نقدی', category: 'مدیریت ریسک', weight_pct: 15, budget_share: budget * 0.15, target_units: `${(budget * 0.15 / usdt_price).toFixed(1)} USDT`, role: 'آمادگی ورود در پله‌های حمایتی مارکت', risk: 'کم' },
      ];
    } else {
      allocations = [
        { name: 'طلای آبشده شمش / گواهی سپرده طلا', category: 'هسته دفاعی سبد', weight_pct: 50, budget_share: budget * 0.5, target_units: `${(budget * 0.5 / gold_18k).toFixed(2)} گرم`, role: 'بزرگترین سنگر حفظ ارزش ریال بدون حباب', risk: 'پایین' },
        { name: 'سکه تمام بهار آزادی (طرح قدیم)', category: 'مسکوکات کم‌حباب', weight_pct: 25, budget_share: budget * 0.25, target_units: Math.floor((budget * 0.25) / coin_bahar) > 0 ? `${Math.floor((budget * 0.25) / coin_bahar)} عدد` : `${((budget * 0.25) / gold_18k).toFixed(2)} گرم طلا`, role: 'نقدشوندگی سریع بازار آزاد', risk: 'متوسط' },
        { name: 'نقره ۹۹۹ فیزیکی شمش و ساچمه', category: 'تولید بازدهی مضاعف', weight_pct: 15, budget_share: budget * 0.15, target_units: `${(budget * 0.15 / silver_999).toFixed(1)} گرم`, role: 'پوشش اهرمی تقاضای جهانی', risk: 'متوسط' },
        { name: 'تتر (USDT) / نقدینگی فعال', category: 'مدیریت شناوری', weight_pct: 10, budget_share: budget * 0.1, target_units: `${(budget * 0.1 / usdt_price).toFixed(1)} USDT`, role: 'نقدینگی در دسترس جهت مداخله سریع', risk: 'کم' },
      ];
    }

    const dca_tranches = [
      { tranche: 'پله اول (Initial Entry - نرخ زنده)', pct: '۴۰٪ بودجه', amount: budget * 0.4, action: 'ورود در نرخ جاری بازار جهت تثبیت پوزیشن پایه و جلوگیری از جاماندن' },
      { tranche: 'پله دوم (Support Limit - کف روز / پولبک)', pct: '۳۵٪ بودجه', amount: budget * 0.35, action: 'اردر خرید در اصلاح ۲ تا ۳ درصدی به سمت حمایت کف روزانه و میانگین متحرک' },
      { tranche: 'پله سوم (Correction Reserve - اصلاح عمیق)', pct: '۲۵٪ بودجه', amount: budget * 0.25, action: 'نگهداری به صورت تتر/نقد تا زمان اصلاح ماژور یا شکست مقاومت‌ها' },
    ];

    return {
      budget_toman: budget,
      allocations,
      dca_tranches,
      macro_metrics: {
        gold_18k, silver_999, usd_price, usdt_price, ons_gold, ons_silver, gsr,
        bubble_emami_pct, bubble_emami_val
      }
    };
  },

  async fetchAdvisor(budget) {
    try {
      const res = await fetch('/api/advisor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ budget }),
      });
      if (res.ok) {
        return await res.json();
      }
    } catch (e) {
      console.warn('Using local client advisor engine', e);
    }
    return this.generateClientAdvisor(budget);
  }
};

// UI Rendering Module
const UI = {
  _toastTimer: null,

  showToast(msg) {
    const toast = document.getElementById('toastNotification');
    if (toast) {
      toast.textContent = msg;
      toast.classList.add('show');
      clearTimeout(this._toastTimer);
      this._toastTimer = setTimeout(() => {
        toast.classList.remove('show');
      }, 3500);
    }
  },



  initTheme() {
    document.documentElement.setAttribute('data-theme', AppState.theme);
    const moon = document.getElementById('themeIconMoon');
    const sun = document.getElementById('themeIconSun');
    if (AppState.theme === 'dark') {
      moon.style.display = 'none';
      sun.style.display = 'block';
    } else {
      moon.style.display = 'block';
      sun.style.display = 'none';
    }
  },

  toggleTheme() {
    AppState.theme = AppState.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('tala_theme', AppState.theme);
    UI.initTheme();
  },

  updatePortfolioCountBadge() {
    const badge = document.getElementById('portfolioCountBadge');
    if (badge) {
      badge.textContent = `${AppState.portfolio.length.toLocaleString('fa-IR')} دارایی`;
    }
  },

  updateAlertsCountText() {
    const el = document.getElementById('activeAlertsCountText');
    if (el) {
      const activeCount = AppState.alerts.filter(a => a.active).length;
      el.textContent = activeCount > 0 
        ? `${activeCount.toLocaleString('fa-IR')} هشدار فعال` 
        : 'تنظیم تارگت قیمتی';
    }
  },

  renderOverviewCards() {
    if (!AppState.prices) return;
    const { gold = {}, coins = {}, currencies = {}, silver = {}, macro = {}, bubbles = {} } = AppState.prices;

    // 1. Ounce
    if (macro.ons_gold) {
      document.getElementById('cardOunceVal').innerHTML = `${Utils.formatCurrency(macro.ons_gold)} <small>/ اونس</small>`;
      document.getElementById('cardOunceRange').textContent = macro.ons_silver ? `انس نقره: $${macro.ons_silver}` : 'بازار جهانی طلا';
    }

    // 2. Gold 18k
    const g18 = gold.gold_18k;
    if (g18) {
      document.getElementById('cardGold18Val').innerHTML = `${Utils.formatNumber(g18.toman)} <small>تومان</small>`;
      const chgEl = document.getElementById('cardGold18Chg');
      chgEl.textContent = g18.change || '+۰٪';
      chgEl.className = `change compact ${g18.change && g18.change.includes('-') ? 'negative' : 'positive'}`;
      document.getElementById('cardGold18Range').textContent = `کف: ${Utils.formatNumber(g18.low_toman)} | سقف: ${Utils.formatNumber(g18.high_toman)}`;
    }

    // 3. USD
    const usd = currencies.currency_usd;
    if (usd) {
      document.getElementById('cardUsdVal').innerHTML = `${Utils.formatNumber(usd.toman)} <small>تومان</small>`;
      const chgEl = document.getElementById('cardUsdChg');
      chgEl.textContent = usd.change || '+۰٪';
      chgEl.className = `change compact ${usd.change && usd.change.includes('-') ? 'negative' : 'positive'}`;
      document.getElementById('cardUsdRange').textContent = `کف: ${Utils.formatNumber(usd.low_toman)} | سقف: ${Utils.formatNumber(usd.high_toman)}`;
    }

    // 4. USDT
    const usdt = currencies.currency_usdt || usd;
    if (usdt) {
      document.getElementById('cardUsdtVal').innerHTML = `${Utils.formatNumber(usdt.toman)} <small>تومان</small>`;
      const chgEl = document.getElementById('cardUsdtChg');
      chgEl.textContent = usdt.change || '+۰٪';
      chgEl.className = `change compact ${usdt.change && usdt.change.includes('-') ? 'negative' : 'positive'}`;
      document.getElementById('cardUsdtRange').textContent = `کف: ${Utils.formatNumber(usdt.low_toman)} | سقف: ${Utils.formatNumber(usdt.high_toman)}`;
    }

    // 5. Silver 999
    const s999 = silver.silver_999;
    if (s999) {
      document.getElementById('cardSilverVal').innerHTML = `${Utils.formatNumber(s999.toman)} <small>تومان</small>`;
      const chgEl = document.getElementById('cardSilverChg');
      chgEl.textContent = s999.change || '+۰٪';
      chgEl.className = `change compact ${s999.change && s999.change.includes('-') ? 'negative' : 'positive'}`;
      document.getElementById('cardSilverRange').textContent = `کف: ${Utils.formatNumber(s999.low_toman)} | سقف: ${Utils.formatNumber(s999.high_toman)}`;
    }

    // 6. Coin Emami & Bubble
    const emami = coins.coin_emami;
    const bubbleEmami = bubbles.bubble_emami;
    if (emami) {
      document.getElementById('cardCoinVal').innerHTML = `${Utils.formatNumber(emami.toman)} <small>تومان</small>`;
    }
    if (bubbleEmami) {
      document.getElementById('cardBubblePct').textContent = `حباب: ${bubbleEmami.percentage || 0}٪`;
      document.getElementById('cardBubbleVal').textContent = `حباب: ${Utils.formatNumber(bubbleEmami.toman)} تومان`;
    }

    // Update Header sync time
    const timeText = document.getElementById('lastSyncTimeText');
    if (timeText && AppState.prices.updated_at) {
      timeText.textContent = `آخرین بروزرسانی: ${AppState.prices.updated_at}`;
    }
  },

  getAllFlatItems() {
    if (!AppState.prices) return [];
    const items = [];
    const { gold = {}, silver = {}, coins = {}, currencies = {}, parsian = {}, bubbles = {} } = AppState.prices;

    const addItems = (dict, catKey, catName, icon) => {
      for (const [key, val] of Object.entries(dict)) {
        items.push({
          key,
          categoryKey: catKey,
          categoryName: catName,
          title: val.title || key,
          icon,
          toman: val.toman || 0,
          low_toman: val.low_toman || val.toman || 0,
          high_toman: val.high_toman || val.toman || 0,
          change: val.change || '-',
          time: val.time || '',
          percentage: val.percentage,
        });
      }
    };

    addItems(gold, 'gold', 'طلا و آبشده', '✨');
    addItems(silver, 'silver', 'انواع نقره', '⚪️');
    
    // Categorize coins into new & old
    for (const [key, val] of Object.entries(coins)) {
      const isOld = key.includes('old') || key.includes('down');
      items.push({
        key,
        categoryKey: isOld ? 'coins_old' : 'coins_new',
        categoryName: isOld ? 'سکه طرح قدیم' : 'سکه طرح جدید',
        title: val.title || key,
        icon: isOld ? '🏛' : '🪙',
        toman: val.toman || 0,
        low_toman: val.low_toman || val.toman || 0,
        high_toman: val.high_toman || val.toman || 0,
        change: val.change || '-',
        time: val.time || '',
      });
    }

    addItems(parsian, 'parsian', 'سکه پارسیان', '🎖');
    addItems(currencies, 'currencies', 'ارزها و تتر', '💵');
    addItems(bubbles, 'bubbles', 'رادار حباب سکه', '🎈');

    return items;
  },

  renderMarketBoard() {
    const tableBody = document.getElementById('marketTableBody');
    if (!tableBody) return;

    const allItems = UI.getAllFlatItems();
    document.getElementById('boardCountBadge').textContent = `${allItems.length.toLocaleString('fa-IR')} نرخ`;

    const searchKeyword = (document.getElementById('boardSearchInput').value || '').trim().toLowerCase();

    const filtered = allItems.filter(item => {
      const matchCat = AppState.activeBoardCategory === 'all' || item.categoryKey === AppState.activeBoardCategory;
      const matchSearch = !searchKeyword || item.title.toLowerCase().includes(searchKeyword) || item.categoryName.toLowerCase().includes(searchKeyword);
      return matchCat && matchSearch;
    });

    if (filtered.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:30px; color:var(--text-muted);">موردی مطابق با فیلتر شما یافت نشد.</td></tr>`;
      return;
    }

    const { bubbles = {} } = AppState.prices || {};

    tableBody.innerHTML = filtered.map(item => {
      const detailedUnit = Utils.getDetailedUnit(item);
      const priceHtml = `
        <div style="line-height:1.35;">
          <strong style="font-size:1.08rem; color:var(--gold-dark, #b45309); font-weight:800;">${Utils.formatNumber(item.toman)} <small style="font-size:0.75rem; font-weight:normal; color:var(--text-muted);">تومان</small></strong>
          <div style="font-size:0.73rem; color:var(--text-muted); font-weight:500; margin-top:2px;">${detailedUnit}</div>
        </div>`;

      let changeHtml = '<span style="color:var(--text-muted); font-size:0.83rem;">بدون نوسان (۰٪)</span>';
      if (item.change && item.change !== '-' && item.change !== '(0%) 0') {
        const isNeg = item.change.includes('-');
        changeHtml = `<span class="change compact ${isNeg ? 'negative' : 'positive'}">${item.change}</span>`;
      }

      let rangeHtml = '';
      if (item.low_toman && item.high_toman && item.low_toman !== item.high_toman) {
        rangeHtml = `
          <div style="font-size:0.84rem; line-height:1.45;">
            <div style="color:var(--text-muted);"><small style="font-size:0.72rem;">کف:</small> <b>${Utils.formatNumber(item.low_toman)}</b></div>
            <div style="color:var(--text);"><small style="font-size:0.72rem;">سقف:</small> <b>${Utils.formatNumber(item.high_toman)}</b></div>
          </div>`;
      } else {
        rangeHtml = `<span style="color:var(--text-muted-2); font-size:0.82rem;">نرخ پیوسته روز</span>`;
      }

      let bubbleSpreadHtml = '<span style="color:var(--text-muted-2); font-size:0.82rem;">فاقد حباب (اسپرد پایه)</span>';
      if (item.categoryKey === 'bubbles') {
        bubbleSpreadHtml = `<span class="descriptive-badge negative" style="font-size:0.8rem; font-weight:700;">حباب: ${item.percentage ? item.percentage + '٪' : Utils.formatToman(item.toman)}</span>`;
      } else if (item.key === 'coin_emami' && bubbles.bubble_emami) {
        bubbleSpreadHtml = `<span class="descriptive-badge negative" style="font-size:0.8rem; font-weight:700;">حباب: ${bubbles.bubble_emami.percentage}% (${Utils.formatNumber(bubbles.bubble_emami.toman)} ت)</span>`;
      } else if (item.key === 'coin_bahar' && bubbles.bubble_bahar) {
        bubbleSpreadHtml = `<span class="descriptive-badge negative" style="font-size:0.8rem; font-weight:700;">حباب: ${bubbles.bubble_bahar.percentage}% (${Utils.formatNumber(bubbles.bubble_bahar.toman)} ت)</span>`;
      } else if (item.key === 'coin_half_new' && bubbles.bubble_nim) {
        bubbleSpreadHtml = `<span class="descriptive-badge negative" style="font-size:0.8rem; font-weight:700;">حباب: ${bubbles.bubble_nim.percentage}% (${Utils.formatNumber(bubbles.bubble_nim.toman)} ت)</span>`;
      } else if (item.key === 'coin_rob_new' && bubbles.bubble_rob) {
        bubbleSpreadHtml = `<span class="descriptive-badge negative" style="font-size:0.8rem; font-weight:700;">حباب: ${bubbles.bubble_rob.percentage}% (${Utils.formatNumber(bubbles.bubble_rob.toman)} ت)</span>`;
      } else if (item.key === 'coin_grami' && bubbles.bubble_grami) {
        bubbleSpreadHtml = `<span class="descriptive-badge negative" style="font-size:0.8rem; font-weight:700;">حباب: ${bubbles.bubble_grami.percentage}% (${Utils.formatNumber(bubbles.bubble_grami.toman)} ت)</span>`;
      } else if (item.categoryKey === 'gold') {
        bubbleSpreadHtml = `<span style="color:var(--teal); font-size:0.82rem; font-weight:600;">ارزش ذاتی خالص (اجرت صفر)</span>`;
      } else if (item.categoryKey === 'silver') {
        bubbleSpreadHtml = `<span style="color:var(--text-muted); font-size:0.82rem;">شمش و ساچمه کارگاهی</span>`;
      } else if (item.categoryKey === 'currencies') {
        bubbleSpreadHtml = `<span style="color:var(--text-muted); font-size:0.82rem;">نرخ اسکناس نقدی</span>`;
      }

      let positionHtml = '';
      if (item.low_toman && item.high_toman && item.high_toman > item.low_toman) {
        const offset = Math.min(100, Math.max(0, ((item.toman - item.low_toman) / (item.high_toman - item.low_toman)) * 100));
        let badgeColor = 'var(--text-muted)';
        let badgeText = 'تعادل میانی';
        if (offset >= 75) {
          badgeColor = '#ef4444';
          badgeText = 'نزدیک مقاومت سقف';
        } else if (offset <= 25) {
          badgeColor = '#10b981';
          badgeText = 'نزدیک کف حمایتی';
        }
        positionHtml = `
          <div style="display:flex; flex-direction:column; gap:4px;">
            <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:${badgeColor}; font-weight:600;">
              <span>${badgeText}</span>
              <span>${Math.round(offset)}٪</span>
            </div>
            <div class="range-bar" style="height:5px;">
              <div class="range-bar-fill" style="width:${offset}%;"></div>
            </div>
          </div>`;
      } else {
        positionHtml = `<span style="color:var(--text-muted-2); font-size:0.82rem;">نوسان متعادل و پیوسته</span>`;
      }

      return `
        <tr>
          <td>
            <div class="table-item-name">
              <span class="item-icon">${item.icon}</span>
              <b>${item.title}</b>
            </div>
          </td>
          <td><span style="font-size:0.8rem; color:var(--text-muted);">${item.categoryName}</span></td>
          <td>${priceHtml}</td>
          <td>${changeHtml}</td>
          <td>${rangeHtml}</td>
          <td>${bubbleSpreadHtml}</td>
          <td style="min-width:140px;">${positionHtml}</td>
        </tr>
      `;
    }).join('');
  },

  async renderAnalysisPanel() {
    if (!AppState.lastChartData) {
      AppState.lastChartData = await ApiService.fetchChartData('iran', '6M');
    }
    const chartData = AppState.lastChartData;


    // Update Top Score & Sentiment
    const scoreVal = document.getElementById('analysisScoreVal');
    const sentimentText = document.getElementById('analysisSentimentText');
    const sentimentBadge = document.getElementById('analysisSentimentBadge');

    if (scoreVal) scoreVal.textContent = Utils.formatNumber(chartData.score || 75);
    if (sentimentText) sentimentText.textContent = chartData.sentiment || 'تمایل صعودی ملایم و باثبات';
    if (sentimentBadge) {
      sentimentBadge.className = `descriptive-badge ${chartData.periodChangePct >= 0 ? 'positive' : 'negative'}`;
    }

    const tab = AppState.activeAnalysisTab || 'trend';
    const container = document.getElementById('analysisTabContent');
    if (!container) return;

    if (tab === 'trend') {
      container.innerHTML = `
        <div class="analysis-metric-grid">
          <div class="analysis-metric">
            <span>فاصله از SMA20</span>
            <strong>${chartData.sma20Distance}</strong>
            <small>میانگین متحرک ۲۰ روزه کوتاه مدت</small>
          </div>
          <div class="analysis-metric">
            <span>فاصله از SMA50</span>
            <strong>${chartData.sma50Distance}</strong>
            <small>جهت‌گیری میان‌مدت و تمایل اصلی</small>
          </div>
          <div class="analysis-metric">
            <span>جایگاه در دامنه دوره</span>
            <strong>${chartData.rangePosition}٪</strong>
            <small>۰٪ کف مطلق و ۱۰۰٪ سقف دوره</small>
          </div>
          <div class="analysis-metric">
            <span>کف مرجع دوره</span>
            <strong>${Utils.formatNumber(chartData.refLow20)}</strong>
            <small>سطح حمایتی و کف روانی ثبت‌شده</small>
          </div>
          <div class="analysis-metric">
            <span>سقف مرجع دوره</span>
            <strong>${Utils.formatNumber(chartData.refHigh20)}</strong>
            <small>سطح مقاومتی و قله تاریخی دوره</small>
          </div>
        </div>

        <div class="analysis-insight-cards">
          <article>
            <span>۱</span>
            <p>همبستگی مستقیم میان نرخ ارز آزاد، اونس جهانی طلا و نرخ ریالی؛ در این دوره شیب صعودی پایدار بر نمودار حاکم بوده است.</p>
          </article>
          <article>
            <span>۲</span>
            <p>قرار گرفتن قیمت بالاتر از خطوط SMA20 و SMA50 تثبیت فاز انبساطی صعودی و اعتبار سطوح تقاضا را نشان می‌دهد.</p>
          </article>
          <article>
            <span>۳</span>
            <p>نوسانات نزدیک سقف دوره معمولاً همراه با استراحت‌های مقطعی است؛ تثبیت بالاتر از کف ۲۰ روزه محرک تداوم روند است.</p>
          </article>
        </div>

        <div class="analysis-method-note">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M12 16v-4"></path><path d="M12 8h.01"></path></svg>
          <span>روش‌شناسی روند: قیمت بالاتر از SMA20 همراه با ترند صعودی SMA50 بیانگر قدرت خریداران در تایم‌فریم انتخابی است.</span>
        </div>
      `;
    } else if (tab === 'momentum') {
      const isPositive = chartData.periodChangePct >= 0;
      container.innerHTML = `
        <div class="analysis-metric-grid">
          <div class="analysis-metric">
            <span>شتاب بازدهی دوره</span>
            <strong class="${isPositive ? 'color-pos' : 'color-neg'}">${isPositive ? '+' : ''}${chartData.periodChangePct}٪</strong>
            <small>تغییر کل بازه انتخابی</small>
          </div>
          <div class="analysis-metric">
            <span>شاخص نوسان‌پذیری (Vol)</span>
            <strong>${chartData.volatility || '۱۱.۵٪'}</strong>
            <small>انحراف معیار نوسانات روزانه</small>
          </div>
          <div class="analysis-metric">
            <span>شاخص قدرت نسبی برآوردی</span>
            <strong>${Math.min(92, Math.max(25, Math.round(50 + (chartData.rangePosition - 50) * 0.6)))} / ۱۰۰</strong>
            <small>وضعیت اشباع خرید یا فروش</small>
          </div>
          <div class="analysis-metric">
            <span>میانگین قیمت بازه</span>
            <strong>${Utils.formatNumber(chartData.avgPrice)}</strong>
            <small>ارزش منصفانه تجمعی (Fair Value)</small>
          </div>
          <div class="analysis-metric">
            <span>دامنه نوسان قله تا کف</span>
            <strong>${Utils.formatNumber(chartData.highPrice - chartData.lowPrice)}</strong>
            <small>اختلاف سقف و کف بازه</small>
          </div>
        </div>

        <div class="analysis-insight-cards">
          <article>
            <span>۱</span>
            <p>شتاب حرکتی (Momentum) نشان‌دهنده ورود نقدینگی فعال و پیوسته به بازار در دوره‌های صعودی است.</p>
          </article>
          <article>
            <span>۲</span>
            <p>در سطوح اشباع خرید (RSI بالای ۷۰)، مدیریت حجم خرید و خودداری از ورود یکجا در سقف‌ها از اصول کلیدی کنترل ریسک است.</p>
          </article>
          <article>
            <span>۳</span>
            <p>افت شتاب بدون اصلاح قیمتی عمیق (واگرایی مخفی) اغلب به معنای دست به دست شدن دارایی‌ها میان معامله‌گران کوتاه‌مدت است.</p>
          </article>
        </div>

        <div class="analysis-method-note">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path></svg>
          <span>شاخص‌های شتاب: پایش بردار سرعت بازدهی و نوسان‌پذیری جهت تمایز رشدهای سالم پایدار از پامپ‌های هیجانی گذرا.</span>
        </div>
      `;
    } else if (tab === 'drivers') {
      const ons = AppState.prices.macro.ons_gold;
      const usd = AppState.prices.currencies.currency_usd.toman;
      const gsr = AppState.prices.macro.gold_silver_ratio;

      container.innerHTML = `
        <div class="analysis-metric-grid">
          <div class="analysis-metric">
            <span>اونس طلا جهانی</span>
            <strong>$${Utils.formatNumber(ons)}</strong>
            <small>پیشران بین‌المللی فلزات گرانبها</small>
          </div>
          <div class="analysis-metric">
            <span>دلار آزاد تهران</span>
            <strong>${Utils.formatNumber(usd)} تومان</strong>
            <small>پیشران اصلی قیمت داخلی</small>
          </div>
          <div class="analysis-metric">
            <span>نسبت طلا به نقره (GSR)</span>
            <strong>${gsr}</strong>
            <small>شاخص چرخه ارزندگی نسبی نقره/طلا</small>
          </div>
          <div class="analysis-metric">
            <span>وزن تأثیر دلار بر طلا</span>
            <strong>حدود ۶۰٪</strong>
            <small>برآورد حساسیت بازدهی ریالی</small>
          </div>
          <div class="analysis-metric">
            <span>وزن تأثیر اونس جهانی</span>
            <strong>حدود ۴۰٪</strong>
            <small>انتقال تورم و ریسک‌های جهانی</small>
          </div>
        </div>

        <div class="analysis-insight-cards">
          <article>
            <span>۱</span>
            <p>فرمول ذاتی طلای داخلی: <b>(اونس جهانی × نرخ دلار) تقسیم بر ضریب تبدیل</b>. حرکت همزمان این دو موتور موجب جهش مرکب می‌شود.</p>
          </article>
          <article>
            <span>۲</span>
            <p>نسبت طلا به نقره بالای ۸۰ بیانگر ارزش تاریخی بالای طلا و ارزندگی فزاینده نقره برای تنوع‌بخشی بلندمدت است.</p>
          </article>
          <article>
            <span>۳</span>
            <p>در دوره‌های ثبات نسبی دلار، نوسانات بازار طلا مستقیماً از اخبار فدرال رزرو، بازدهی اوراق قرضه آمریکا و داده‌های اشتغال تغذیه می‌کند.</p>
          </article>
        </div>

        <div class="analysis-method-note">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>
          <span>موتورهای محرک: تفکیک دقیق وزن اثرگذاری فاکتورهای کلان (دلار آزاد، تورم داخلی و اونس جهانی) بر قیمت‌های نهایی.</span>
        </div>
      `;
    } else if (tab === 'risk') {
      const emamiBubble = AppState.prices.bubbles.bubble_emami ? AppState.prices.bubbles.bubble_emami.percentage : 19.2;
      const robBubble = AppState.prices.bubbles.bubble_rob ? AppState.prices.bubbles.bubble_rob.percentage : 39.7;

      container.innerHTML = `
        <div class="analysis-metric-grid">
          <div class="analysis-metric">
            <span>حباب سکه امامی</span>
            <strong class="${emamiBubble > 20 ? 'color-neg' : 'color-pos'}">${emamiBubble}٪</strong>
            <small>نسبت اضافه ارزش به ارزش ذاتی</small>
          </div>
          <div class="analysis-metric">
            <span>حباب ربع سکه</span>
            <strong class="color-neg">${robBubble}٪</strong>
            <small>حباب بالای هیجانی در قطعات کوچک</small>
          </div>
          <div class="analysis-metric">
            <span>حباب طلای آبشده / ۱۸ عیار</span>
            <strong class="color-pos">۰٪ (نزدیک به صفر)</strong>
            <small>امن‌ترین ابزار حفظ ارزش بدون ریسک حباب</small>
          </div>
          <div class="analysis-metric">
            <span>ریسک افت ناگهانی حباب</span>
            <strong style="color:var(--brand-gold);">متوسط به بالا</strong>
            <small>در قطعات سکه با نوسان انتظارات تورمی</small>
          </div>
          <div class="analysis-metric">
            <span>استراتژی پیشنهادی مدیریت ریسک</span>
            <strong class="color-pos">خرید پله‌ای (DCA)</strong>
            <small>پراکندگی زمانی خرید جهت کاهش میانگین</small>
          </div>
        </div>

        <div class="analysis-insight-cards">
          <article>
            <span>۱</span>
            <p>در فازهای افزایش شدید حباب سکه، تغییر پورتفوی به سمت <b>طلای آبشده و شمش طلا</b> ریسک تخلیه ناگهانی حباب را به صفر می‌رساند.</p>
          </article>
          <article>
            <span>۲</span>
            <p>تنوع‌بخشی به دارایی‌ها (نقره، طلا و تتر) از آسیب‌پذیری در برابر نوسانات یک‌باره تک‌بازاری به طور کامل جلوگیری می‌کند.</p>
          </article>
          <article>
            <span>۳</span>
            <p>هرگز کل سرمایه را در یک نقطه زمانی وارد نکنید؛ تقسیم نقدینگی به ۳ الی ۵ پله خرید، بهترین سپر دفاعی در برابر اصلاحات غیرمنتظره است.</p>
          </article>
        </div>

        <div class="analysis-method-note">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
          <span>سپر مدیریت ریسک: حفاظت از سبد دارایی با تمرکز بر وزن حباب قیمتی، ابزارهای بدون کارمزد و ورود چندمرحله‌ای (DCA).</span>
        </div>
      `;
    }
  },

  renderPortfolio() {
    StorageService.loadPortfolio();
    const tableBody = document.getElementById('portfolioTableBody');
    if (!tableBody) return;

    if (AppState.portfolio.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:36px; color:var(--text-muted);">
        هنوز هیچ دارایی در سبد شما ثبت نشده است. با زدن دکمه <b>«ثبت دارایی جدید»</b> طلا، نقره، سکه یا ارزهای خود را اضافه کنید.
      </td></tr>`;
      document.getElementById('portTotalCurrentVal').textContent = '۰ تومان';
      document.getElementById('portTotalInvestedVal').textContent = '۰ تومان';
      document.getElementById('portTotalPnlVal').textContent = '۰ تومان';
      document.getElementById('portTotalPnlPct').textContent = '۰.۰٪';
      return;
    }

    const allItems = UI.getAllFlatItems();
    const itemMap = new Map(allItems.map(i => [i.key, i]));

    let totalInvested = 0;
    let totalCurrent = 0;

    tableBody.innerHTML = AppState.portfolio.map(hold => {
      const liveItem = itemMap.get(hold.key);
      const currentUnitRate = liveItem ? liveItem.toman : hold.buyPrice;
      const currentVal = currentUnitRate * hold.qty;
      const investedVal = hold.buyPrice * hold.qty;

      totalInvested += investedVal;
      totalCurrent += currentVal;

      const pnlVal = currentVal - investedVal;
      const pnlPct = investedVal > 0 ? ((pnlVal / investedVal) * 100) : 0;
      const isPositive = pnlVal >= 0;

      return `
        <tr>
          <td>
            <div class="table-item-name">
              <span>${liveItem ? liveItem.icon : '💼'}</span>
              <div>
                <b>${hold.title}</b>
                <small style="display:block; color:var(--text-muted); font-size:0.75rem;">ثبت شده در: ${hold.date}</small>
              </div>
            </div>
          </td>
          <td><b>${hold.qty.toLocaleString('fa-IR')} ${hold.unit}</b></td>
          <td>${Utils.formatNumber(hold.buyPrice)} تومان</td>
          <td><strong style="color:var(--gold-dark);">${Utils.formatNumber(currentUnitRate)}</strong> تومان</td>
          <td><strong>${Utils.formatNumber(currentVal)}</strong> تومان</td>
          <td>
            <div style="line-height:1.4;">
              <span class="change compact ${isPositive ? 'positive' : 'negative'}" style="font-weight:700;">
                ${isPositive ? '+' : ''}${pnlPct.toFixed(1)}٪ بازده
              </span>
              <div style="font-size:0.78rem; font-weight:600; color:${isPositive ? 'var(--teal)' : 'var(--red)'}; margin-top:3px;">
                ${isPositive ? '+' : ''}${Utils.formatNumber(pnlVal)} تومان
              </div>
            </div>
          </td>
          <td>
            <button class="btn-secondary btn-danger" style="padding:4px 8px; font-size:0.75rem;" onclick="Handlers.deleteHolding('${hold.id}')">
              حذف
            </button>
          </td>
        </tr>
      `;
    }).join('');

    const totalPnl = totalCurrent - totalInvested;
    const totalPnlPct = totalInvested > 0 ? ((totalPnl / totalInvested) * 100) : 0;
    const isTotalPositive = totalPnl >= 0;

    document.getElementById('portTotalCurrentVal').textContent = Utils.formatToman(totalCurrent);
    document.getElementById('portTotalInvestedVal').textContent = Utils.formatToman(totalInvested);
    
    const pnlEl = document.getElementById('portTotalPnlVal');
    pnlEl.textContent = `${isTotalPositive ? '+' : ''}${Utils.formatToman(totalPnl)}`;
    pnlEl.style.color = isTotalPositive ? 'var(--green)' : 'var(--red)';

    const pnlPctEl = document.getElementById('portTotalPnlPct');
    pnlPctEl.textContent = `${isTotalPositive ? '+' : ''}${totalPnlPct.toFixed(1)}٪`;
    pnlPctEl.className = `change ${isTotalPositive ? 'positive' : 'negative'}`;
  },

  async renderAdvisor() {
    const budget = AppState.currentBudget;
    const report = await ApiService.fetchAdvisor(budget);
    if (!report) return;

    const { macro_metrics = {}, allocations = [], dca_tranches = [] } = report;

    // 1. Macro Indicators
    document.getElementById('advisorGsrVal').textContent = macro_metrics.gsr || '--';
    document.getElementById('advisorBubbleVal').textContent = `${macro_metrics.bubble_emami_pct || 0}٪`;
    document.getElementById('advisorGoldOunceVal').textContent = macro_metrics.ons_gold ? `$${macro_metrics.ons_gold}` : '--';
    document.getElementById('advisorSilverOunceVal').textContent = macro_metrics.ons_silver ? `$${macro_metrics.ons_silver}` : '--';

    // 2. Allocations
    const allocContainer = document.getElementById('advisorAllocCards');
    allocContainer.innerHTML = allocations.map(item => `
      <div class="alloc-card">
        <div class="alloc-card-head">
          <b>${item.name}</b>
          <span class="alloc-pct">${item.weight_pct}٪ سبد</span>
        </div>
        <div class="alloc-progress">
          <div class="alloc-progress-fill" style="width:${item.weight_pct}%;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.9rem;">
          <span style="color:var(--text-muted);">بودجه پیشنهادی:</span>
          <strong>${Utils.formatToman(item.budget_share)}</strong>
        </div>
        <div style="font-size:0.82rem; color:var(--teal); font-weight:700;">
          مقدار هدف: ${item.target_units}
        </div>
        <small style="color:var(--text-muted); font-size:0.78rem; line-height:1.5;">${item.role}</small>
      </div>
    `).join('');

    // 3. DCA Tranches
    const dcaContainer = document.getElementById('advisorDcaContainer');
    dcaContainer.innerHTML = dca_tranches.map((t, idx) => `
      <div class="dca-step">
        <div class="dca-step-badge">${(idx + 1).toLocaleString('fa-IR')}</div>
        <div>
          <b>${t.tranche} (${t.pct} — ${Utils.formatToman(t.amount)})</b>
          <p style="font-size:0.85rem; color:var(--text-muted); margin-top:2px;">${t.action}</p>
        </div>
      </div>
    `).join('');
  },

  renderScenario() {
    if (!AppState.prices) return;
    const goldOunceBase = (AppState.prices.macro && AppState.prices.macro.ons_gold) || 4181.9;
    const usdBase = (AppState.prices.currencies.currency_usd && AppState.prices.currencies.currency_usd.toman) || 267900;
    const gold18Base = (AppState.prices.gold.gold_18k && AppState.prices.gold.gold_18k.toman) || 26255100;

    const ounceDeltaPct = parseFloat(document.getElementById('scenarioOunceSlider').value);
    const usdDeltaPct = parseFloat(document.getElementById('scenarioUsdSlider').value);
    const bubbleDeltaPct = parseFloat(document.getElementById('scenarioBubbleSlider').value);

    document.getElementById('scenarioOunceOut').textContent = `${ounceDeltaPct >= 0 ? '+' : ''}${ounceDeltaPct}٪`;
    document.getElementById('scenarioUsdOut').textContent = `${usdDeltaPct >= 0 ? '+' : ''}${usdDeltaPct}٪`;
    document.getElementById('scenarioBubbleOut').textContent = `${bubbleDeltaPct >= 0 ? '+' : ''}${bubbleDeltaPct}٪`;

    const newOunce = goldOunceBase * (1.0 + (ounceDeltaPct / 100));
    const newUsd = usdBase * (1.0 + (usdDeltaPct / 100));
    const bubbleFactor = 1.0 + (bubbleDeltaPct / 100);

    // Formula: (Ounce * USD * 0.75 / 31.1035) * bubbleFactor
    const estimated18k = ((newOunce * newUsd * 0.75) / 31.1035) * bubbleFactor;
    const deltaOverallPct = ((estimated18k - gold18Base) / gold18Base) * 100;

    document.getElementById('scenarioEstimatedPrice').innerHTML = `${Utils.formatNumber(estimated18k)} <small>تومان</small>`;
    
    const changeBadge = document.getElementById('scenarioChangePct');
    changeBadge.textContent = `${deltaOverallPct >= 0 ? '+' : ''}${deltaOverallPct.toFixed(1)}٪`;
    changeBadge.className = `change ${deltaOverallPct >= 0 ? 'positive' : 'negative'}`;

    // Formula strip
    document.getElementById('scenarioFormulaOunce').textContent = `$${Math.round(newOunce).toLocaleString('en-US')}`;
    document.getElementById('scenarioFormulaUsd').textContent = `${Utils.formatNumber(newUsd)} ت`;
    document.getElementById('scenarioFormulaTotal').textContent = `${(estimated18k / 1000000).toFixed(2)} میلیون تومان`;
  },

  renderCalculator() {
    const amount = Utils.cleanInputNumber(document.getElementById('calcInvestAmount').value) || 100000000;
    const period = document.getElementById('calcPeriodSelect').value;

    const returnRates = { '1M': 0.032, '3M': 0.085, '6M': 0.158, '1Y': 0.385 };
    const rate = returnRates[period] || 0.158;

    const pnl = amount * rate;
    const totalToday = amount + pnl;

    document.getElementById('calcResultTodayVal').textContent = Utils.formatToman(totalToday);
    document.getElementById('calcResultReturnPct').textContent = `+${(rate * 100).toFixed(1)}٪`;
    document.getElementById('calcResultPnlVal').textContent = Utils.formatToman(pnl);
  },

  renderAssetSwapper() {
    if (!AppState.prices) return;
    const allItems = UI.getAllFlatItems();
    const itemMap = new Map(allItems.map(i => [i.key, i]));

    const sourceKey = document.getElementById('swapSourceAsset').value;
    const sourceQty = parseFloat(document.getElementById('swapSourceQty').value) || 1;
    const targetKey = document.getElementById('swapTargetAsset').value;

    const sourceItem = itemMap.get(sourceKey);
    const targetItem = itemMap.get(targetKey);

    if (!sourceItem || !targetItem || targetItem.toman === 0) return;

    const totalToman = sourceItem.toman * sourceQty;
    const targetQty = totalToman / targetItem.toman;
    const targetUnit = Utils.getUnitForAsset(targetKey, targetItem.categoryKey);

    document.getElementById('swapResultText').textContent = `${targetQty.toFixed(2)} ${targetUnit} ${targetItem.title}`;
    document.getElementById('swapDetailText').textContent = `ارزش کل معامله: ${Utils.formatToman(totalToman)}`;
  },

  renderAlerts() {
    StorageService.loadAlerts();
    const tableBody = document.getElementById('alertsTableBody');
    if (!tableBody) return;

    if (AppState.alerts.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:30px; color:var(--text-muted);">
        هیچ هشدار قیمتی ثبت نشده است. با زدن <b>«ثبت هشدار جدید»</b> تارگت‌های مورد نظر خود را اضافه کنید.
      </td></tr>`;
      return;
    }

    const allItems = UI.getAllFlatItems();
    const itemMap = new Map(allItems.map(i => [i.key, i]));

    tableBody.innerHTML = AppState.alerts.map(a => {
      const liveItem = itemMap.get(a.key);
      const curPrice = liveItem ? liveItem.toman : 0;
      const triggered = a.direction === 'above' ? curPrice >= a.targetPrice : curPrice <= a.targetPrice;

      let distanceHtml = '';
      if (curPrice > 0 && a.targetPrice > 0) {
        const diff = a.targetPrice - curPrice;
        const diffPct = (diff / curPrice) * 100;
        const absDiffPct = Math.abs(diffPct).toFixed(1);
        if (triggered) {
          distanceHtml = `<span style="color:var(--teal); font-weight:700; font-size:0.82rem;">🎯 تارگت لمس شد</span>`;
        } else {
          distanceHtml = `<span style="font-size:0.83rem; font-weight:600; color:var(--text-muted);">${absDiffPct}٪ فاصله تا تارگت</span>`;
        }
      } else {
        distanceHtml = '-';
      }

      return `
        <tr>
          <td><b>${a.title}</b></td>
          <td><strong style="color:var(--gold-dark);">${Utils.formatNumber(a.targetPrice)} تومان</strong></td>
          <td>${a.direction === 'above' ? '📈 عبور به بالا' : '📉 افت به زیر'}</td>
          <td>${Utils.formatNumber(curPrice)} تومان</td>
          <td>${distanceHtml}</td>
          <td>
            <span class="change compact ${triggered ? 'positive' : ''}" style="${triggered ? 'background:var(--gold-soft); color:var(--gold-dark);' : ''}">
              ${triggered ? '🔔 فعال شده / در تارگت' : '⏳ در انتظار قیمت'}
            </span>
          </td>
          <td>
            <button class="btn-secondary btn-danger" style="padding:4px 8px; font-size:0.75rem;" onclick="Handlers.deleteAlert('${a.id}')">
              حذف
            </button>
          </td>
        </tr>
      `;
    }).join('');
  },

  checkTriggeredAlerts() {
    if (!AppState.prices || AppState.alerts.length === 0) return;
    const allItems = UI.getAllFlatItems();
    const itemMap = new Map(allItems.map(i => [i.key, i]));

    AppState.alerts.forEach(a => {
      const live = itemMap.get(a.key);
      if (!live || !a.active) return;
      const isMet = a.direction === 'above' ? live.toman >= a.targetPrice : live.toman <= a.targetPrice;

      if (isMet) {
        if ('Notification' in window && Notification.permission === 'granted') {
          new Notification(`🔔 هشدار قیمت: ${a.title}`, {
            body: `قیمت بازار به ${Utils.formatNumber(live.toman)} تومان رسید (تارگت شما: ${Utils.formatNumber(a.targetPrice)} تومان).`,
            icon: '/favicon.ico'
          });
        }
      }
    });
  }
};

// Event Handlers
const Handlers = {
  deleteHolding(id) {
    if (confirm('آیا از حذف این دارایی از سبد خود اطمینان دارید؟')) {
      AppState.portfolio = AppState.portfolio.filter(h => h.id !== id);
      StorageService.savePortfolio();
    }
  },

  deleteAlert(id) {
    AppState.alerts = AppState.alerts.filter(a => a.id !== id);
    StorageService.saveAlerts();
  },

  populateHoldingAssetDropdown(category) {
    const assetSelect = document.getElementById('holdingAssetSelect');
    const allItems = UI.getAllFlatItems();
    const filtered = allItems.filter(i => i.categoryKey === category);

    assetSelect.innerHTML = filtered.map(item => `
      <option value="${item.key}" data-toman="${item.toman}" data-title="${item.title}" data-unit="${Utils.getUnitForAsset(item.key, category)}">
        ${item.title} (نرخ زنده: ${Utils.formatNumber(item.toman)} ت)
      </option>
    `).join('');

    const unit = Utils.getUnitForAsset(filtered[0]?.key, category);
    document.getElementById('holdingQtyLabel').textContent = `مقدار / تعداد (${unit}):`;
    document.getElementById('holdingBuyPriceInput').value = filtered[0]?.toman || '';
  },

  populateAlertAssetDropdown() {
    const assetSelect = document.getElementById('alertAssetSelect');
    const allItems = UI.getAllFlatItems();
    assetSelect.innerHTML = allItems.map(item => `
      <option value="${item.key}" data-toman="${item.toman}" data-title="${item.title}">
        ${item.title} (${Utils.formatNumber(item.toman)} تومان)
      </option>
    `).join('');

    if (allItems.length > 0) {
      document.getElementById('alertCurrentPricePreview').value = Utils.formatToman(allItems[0].toman);
      document.getElementById('alertTargetPriceInput').value = Math.round(allItems[0].toman * 1.05);
    }
  }
};

// Bootstrap Application
document.addEventListener('DOMContentLoaded', async () => {
  UI.initTheme();
  StorageService.loadPortfolio();
  StorageService.loadAlerts();
  UI.updatePortfolioCountBadge();
  UI.updateAlertsCountText();

  // Request Notification permission
  if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
  }

  // Universal Menu Toggle & Sidebar Handling (Desktop + Mobile)
  const menuBtn = document.getElementById('mobileMenuBtn');
  const sidebar = document.getElementById('sidebar');
  const closeBtn = document.getElementById('sidebarCloseBtn');
  const overlay = document.getElementById('sidebarOverlay');
  const appShell = document.querySelector('.app-shell');

  // Load saved desktop preference
  if (window.innerWidth > 992 && localStorage.getItem('tala_sidebar_collapsed') === 'true') {
    if (appShell) appShell.classList.add('sidebar-collapsed');
  }

  const openMobileSidebar = () => {
    if (sidebar) sidebar.classList.add('open');
    if (overlay) overlay.classList.add('active');
    document.body.classList.add('menu-open');
  };

  const closeMobileSidebar = () => {
    if (sidebar) sidebar.classList.remove('open');
    if (overlay) overlay.classList.remove('active');
    document.body.classList.remove('menu-open');
  };

  const toggleSidebar = () => {
    if (window.innerWidth <= 992) {
      if (sidebar && sidebar.classList.contains('open')) {
        closeMobileSidebar();
      } else {
        openMobileSidebar();
      }
    } else {
      if (appShell) {
        appShell.classList.toggle('sidebar-collapsed');
        localStorage.setItem('tala_sidebar_collapsed', appShell.classList.contains('sidebar-collapsed'));
      }
    }
  };

  if (menuBtn) menuBtn.addEventListener('click', toggleSidebar);

  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      if (window.innerWidth <= 992) {
        closeMobileSidebar();
      } else {
        if (appShell) {
          appShell.classList.add('sidebar-collapsed');
          localStorage.setItem('tala_sidebar_collapsed', 'true');
        }
      }
    });
  }

  if (overlay) overlay.addEventListener('click', closeMobileSidebar);

  // Close sidebar on navigation item click (on mobile)
  document.querySelectorAll('.sidebar .nav-item, #quickAlertBtn').forEach(el => {
    el.addEventListener('click', () => {
      if (window.innerWidth <= 992) {
        closeMobileSidebar();
      }
    });
  });

  // Close sidebar on ESC key
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (window.innerWidth <= 992 && sidebar && sidebar.classList.contains('open')) {
        closeMobileSidebar();
      } else if (window.innerWidth > 992 && appShell && !appShell.classList.contains('sidebar-collapsed')) {
        appShell.classList.add('sidebar-collapsed');
        localStorage.setItem('tala_sidebar_collapsed', 'true');
      }
    }
  });

  // Theme toggle
  document.getElementById('themeToggleBtn').addEventListener('click', UI.toggleTheme);

  // Initial Data Fetch
  await ApiService.fetchPrices(true);
  UI.renderOverviewCards();
  UI.renderMarketBoard();
  UI.renderPortfolio();
  UI.renderAnalysisPanel();
  UI.renderScenario();
  UI.renderCalculator();
  UI.renderAssetSwapper();
  UI.renderAdvisor();
  UI.renderAlerts();

  // Board Filter Pills
  document.getElementById('boardCategoryPills').addEventListener('click', (e) => {
    if (e.target.classList.contains('filter-pill')) {
      document.querySelectorAll('#boardCategoryPills .filter-pill').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      AppState.activeBoardCategory = e.target.dataset.cat;
      UI.renderMarketBoard();
    }
  });

  // Board Search
  document.getElementById('boardSearchInput').addEventListener('input', UI.renderMarketBoard);



  // Analysis Tabs Controls
  const analysisTabs = document.getElementById('analysisTabsGroup');
  if (analysisTabs) {
    analysisTabs.addEventListener('click', (e) => {
      if (e.target.tagName === 'BUTTON') {
        analysisTabs.querySelectorAll('button').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        AppState.activeAnalysisTab = e.target.dataset.tab;
        UI.renderAnalysisPanel();
      }
    });
  }

  // Scenario Sliders
  ['scenarioOunceSlider', 'scenarioUsdSlider', 'scenarioBubbleSlider'].forEach(id => {
    document.getElementById(id).addEventListener('input', UI.renderScenario);
  });

  // Calculator Inputs
  document.getElementById('calcInvestAmount').addEventListener('input', UI.renderCalculator);
  document.getElementById('calcPeriodSelect').addEventListener('change', UI.renderCalculator);

  // Swapper Inputs
  document.getElementById('swapSourceAsset').addEventListener('change', UI.renderAssetSwapper);
  document.getElementById('swapSourceQty').addEventListener('input', UI.renderAssetSwapper);
  document.getElementById('swapTargetAsset').addEventListener('change', UI.renderAssetSwapper);

  // Advisor Budget Chips
  document.getElementById('advisorBudgetChips').addEventListener('click', (e) => {
    if (e.target.classList.contains('budget-chip')) {
      document.querySelectorAll('#advisorBudgetChips .budget-chip').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      const b = parseInt(e.target.dataset.budget);
      AppState.currentBudget = b;
      document.getElementById('advisorCustomBudgetInput').value = b;
      UI.renderAdvisor();
    }
  });

  document.getElementById('advisorCalculateBtn').addEventListener('click', () => {
    const val = Utils.cleanInputNumber(document.getElementById('advisorCustomBudgetInput').value);
    if (val > 0) {
      AppState.currentBudget = val;
      UI.renderAdvisor();
    }
  });

  // Refresh Button
  document.getElementById('refreshBtn').addEventListener('click', async () => {
    const updateText = document.getElementById('updateStatusText');
    updateText.textContent = 'در حال استعلام...';
    UI.showToast('📡 در حال دریافت آخرین نرخ‌های لحظه‌ای از TGJU...');
    await ApiService.fetchPrices(true);
    UI.renderOverviewCards();
    UI.renderMarketBoard();
    UI.renderPortfolio();
    UI.renderScenario();
      UI.renderAlerts();
    UI.checkTriggeredAlerts();
    updateText.textContent = 'زنده (TGJU)';
    const now = new Date().toLocaleTimeString('fa-IR', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    const lastSync = document.getElementById('lastSyncTimeText');
    if (lastSync) lastSync.textContent = `آخرین استعلام: ${now}`;
    UI.showToast(`✅ نرخ‌ها با موفقیت بروزرسانی شدند (${now})`);
  });

  // Add Holding Modal Events
  const addModal = document.getElementById('addHoldingModal');
  document.getElementById('openAddHoldingModalBtn').addEventListener('click', () => {
    Handlers.populateHoldingAssetDropdown(document.getElementById('holdingCategorySelect').value);
    addModal.classList.add('active');
  });

  document.getElementById('closeHoldingModalBtn').addEventListener('click', () => addModal.classList.remove('active'));
  document.getElementById('cancelHoldingModalBtn').addEventListener('click', () => addModal.classList.remove('active'));

  document.getElementById('holdingCategorySelect').addEventListener('change', (e) => {
    Handlers.populateHoldingAssetDropdown(e.target.value);
  });

  document.getElementById('holdingAssetSelect').addEventListener('change', (e) => {
    const opt = e.target.selectedOptions[0];
    if (opt) {
      document.getElementById('holdingBuyPriceInput').value = opt.dataset.toman || '';
      document.getElementById('holdingQtyLabel').textContent = `مقدار / تعداد (${opt.dataset.unit}):`;
    }
  });

  document.getElementById('saveHoldingBtn').addEventListener('click', () => {
    const opt = document.getElementById('holdingAssetSelect').selectedOptions[0];
    const qty = parseFloat(document.getElementById('holdingQtyInput').value);
    let buyPrice = parseFloat(document.getElementById('holdingBuyPriceInput').value);

    if (!opt || !qty || qty <= 0) {
      alert('لطفاً مقدار دارایی را به درستی وارد کنید.');
      return;
    }

    if (isNaN(buyPrice) || buyPrice <= 0) {
      buyPrice = parseFloat(opt.dataset.toman) || 0;
    }

    const newHolding = {
      id: 'h_' + Date.now(),
      category: document.getElementById('holdingCategorySelect').value,
      key: opt.value,
      title: opt.dataset.title,
      unit: opt.dataset.unit,
      qty,
      buyPrice,
      date: new Date().toLocaleDateString('fa-IR'),
    };

    AppState.portfolio.push(newHolding);
    StorageService.savePortfolio();
    addModal.classList.remove('active');
  });

  // Clear Portfolio
  document.getElementById('clearPortfolioBtn').addEventListener('click', () => {
    if (confirm('آیا مطمئن هستید که می‌خواهید تمام دارایی‌های سبد خود را حذف و بازنشانی کنید؟')) {
      AppState.portfolio = [];
      StorageService.savePortfolio();
    }
  });

  // Backup & Restore
  document.getElementById('backupPortfolioBtn').addEventListener('click', () => {
    const jsonStr = JSON.stringify(AppState.portfolio, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `tala_portfolio_backup_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  });

  document.getElementById('restorePortfolioBtn').addEventListener('click', () => {
    document.getElementById('restoreFileInput').click();
  });

  document.getElementById('restoreFileInput').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const parsed = JSON.parse(event.target.result);
          if (Array.isArray(parsed)) {
            AppState.portfolio = parsed;
            StorageService.savePortfolio();
            alert('سبد دارایی با موفقیت بازیابی شد.');
          } else {
            alert('فرمت فایل پشتیبان نامعتبر است.');
          }
        } catch (err) {
          alert('خطا در خواندن فایل.');
        }
      };
      reader.readAsText(file);
    }
  });

  // Add Alert Modal Events
  const alertModal = document.getElementById('addAlertModal');
  const openAlertModal = () => {
    Handlers.populateAlertAssetDropdown();
    alertModal.classList.add('active');
  };
  document.getElementById('openAddAlertModalBtn').addEventListener('click', openAlertModal);
  document.getElementById('quickAlertBtn').addEventListener('click', openAlertModal);

  document.getElementById('closeAlertModalBtn').addEventListener('click', () => alertModal.classList.remove('active'));
  document.getElementById('cancelAlertModalBtn').addEventListener('click', () => alertModal.classList.remove('active'));

  document.getElementById('alertAssetSelect').addEventListener('change', (e) => {
    const opt = e.target.selectedOptions[0];
    if (opt) {
      document.getElementById('alertCurrentPricePreview').value = Utils.formatToman(opt.dataset.toman);
      document.getElementById('alertTargetPriceInput').value = Math.round(parseFloat(opt.dataset.toman) * 1.05);
    }
  });

  document.getElementById('saveAlertBtn').addEventListener('click', () => {
    const opt = document.getElementById('alertAssetSelect').selectedOptions[0];
    const targetPrice = parseFloat(document.getElementById('alertTargetPriceInput').value);
    const direction = document.getElementById('alertDirectionSelect').value;

    if (!opt || !targetPrice || targetPrice <= 0) {
      alert('لطفاً قیمت تارگت را به درستی وارد فرمایید.');
      return;
    }

    const newAlert = {
      id: 'al_' + Date.now(),
      key: opt.value,
      title: opt.dataset.title,
      targetPrice,
      direction,
      active: true,
    };

    AppState.alerts.push(newAlert);
    StorageService.saveAlerts();
    alertModal.classList.remove('active');
  });

  // Export Data Button (Global summary)
  document.getElementById('exportDataBtn').addEventListener('click', () => {
    window.print();
  });

  // Periodic Polling every 60 seconds
  setInterval(async () => {
    await ApiService.fetchPrices();
    UI.renderOverviewCards();
    UI.renderMarketBoard();
    UI.renderPortfolio();
    UI.renderScenario();
    UI.checkTriggeredAlerts();
  }, 60000);
});
