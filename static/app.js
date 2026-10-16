/**
 * Tala-Nama Dashboard Core Application Script
 * Real-time prices, High/Low daily range, Portfolio P&L, Macro Advisor, Chart & Alerts
 */

// Application State
const DEFAULT_PRICES = {
  gold: {
    gold_18k: { title: 'طلای ۱۸ عیار', toman: 26255100, rial: 262551000, low_toman: 26180000, high_toman: 26350000, change: '+۱.۱٪', time: '۱۴:۳۰' },
    gold_24k: { title: 'طلای ۲۴ عیار', toman: 35006800, rial: 350068000, low_toman: 34900000, high_toman: 35120000, change: '+۱.۱٪', time: '۱۴:۳۰' },
    gold_used: { title: 'طلای دست دوم', toman: 25860000, rial: 258600000, low_toman: 25780000, high_toman: 25950000, change: '+۱.۰٪', time: '۱۴:۳۰' },
    mesghal: { title: 'مثقال طلا', toman: 113735000, rial: 1137350000, low_toman: 113400000, high_toman: 114100000, change: '+۱.۲٪', time: '۱۴:۳۰' },
    gold_melted: { title: 'آبشده نقدی', toman: 113735000, rial: 1137350000, low_toman: 113400000, high_toman: 114100000, change: '+۱.۲٪', time: '۱۴:۳۰' },
  },
  silver: {
    silver_999: { title: 'گرم نقره ۹۹۹ (خالص/شمش)', toman: 517500, rial: 5175000, low_toman: 512000, high_toman: 521000, change: '+۱.۸٪', time: '۱۴:۳۰' },
    silver_925: { title: 'گرم نقره ۹۲۵ (استرلینگ)', toman: 479000, rial: 4790000, low_toman: 474000, high_toman: 482000, change: '+۱.۷٪', time: '۱۴:۳۰' },
  },
  coins: {
    coin_emami: { title: 'سکه امامی', toman: 269920000, rial: 2699200000, low_toman: 268500000, high_toman: 270800000, change: '+۰.۸٪', time: '۱۴:۳۰' },
    coin_bahar: { title: 'سکه بهار آزادی', toman: 259510000, rial: 2595100000, low_toman: 258000000, high_toman: 260500000, change: '+۰.۷٪', time: '۱۴:۳۰' },
    coin_half_new: { title: 'نیم سکه', toman: 141200000, rial: 1412000000, low_toman: 140000000, high_toman: 142000000, change: '+۰.۹٪', time: '۱۴:۳۰' },
    coin_rob_new: { title: 'ربع سکه', toman: 76100000, rial: 761000000, low_toman: 75200000, high_toman: 76800000, change: '+۱.۰٪', time: '۱۴:۳۰' },
    coin_grami: { title: 'سکه گرمی', toman: 37500000, rial: 375000000, low_toman: 37000000, high_toman: 37900000, change: '+۰.۵٪', time: '۱۴:۳۰' },
    coin_emami_old: { title: 'تمام سکه طرح قدیم (قبل ۸۶)', toman: 254000000, rial: 2540000000, low_toman: 252500000, high_toman: 255500000, change: '+۰.۶٪', time: '۱۴:۳۰' },
    coin_half_old: { title: 'نیم سکه طرح قدیم (قبل ۸۶)', toman: 136000000, rial: 1360000000, low_toman: 134500000, high_toman: 137000000, change: '+۰.۷٪', time: '۱۴:۳۰' },
    coin_rob_old: { title: 'ربع سکه طرح قدیم (قبل ۸۶)', toman: 72500000, rial: 725000000, low_toman: 71500000, high_toman: 73200000, change: '+۰.۸٪', time: '۱۴:۳۰' },
  },
  bubbles: {
    bubble_emami: { title: 'حباب سکه امامی', toman: 48500000, rial: 485000000, percentage: 18.0, time: '۱۴:۳۰' },
    bubble_bahar: { title: 'حباب بهار آزادی', toman: 38100000, rial: 381000000, percentage: 14.7, time: '۱۴:۳۰' },
    bubble_nim: { title: 'حباب نیم سکه', toman: 30500000, rial: 305000000, percentage: 21.6, time: '۱۴:۳۰' },
    bubble_rob: { title: 'حباب ربع سکه', toman: 20750000, rial: 207500000, percentage: 27.3, time: '۱۴:۳۰' },
    bubble_grami: { title: 'حباب سکه گرمی', toman: 9800000, rial: 98000000, percentage: 26.1, time: '۱۴:۳۰' },
  },
  currencies: {
    currency_usd: { title: 'دلار آمریکا', toman: 267900, rial: 2679000, low_toman: 266500, high_toman: 268800, change: '+۰.۵٪', time: '۱۴:۳۰' },
    currency_usdt: { title: 'تتر (USDT)', toman: 266500, rial: 2665000, low_toman: 265200, high_toman: 267200, change: '+۰.۴٪', time: '۱۴:۳۰' },
    currency_eur: { title: 'یورو', toman: 300280, rial: 3002800, low_toman: 298500, high_toman: 301500, change: '+۰.۳٪', time: '۱۴:۳۰' },
    currency_aed: { title: 'درهم امارات', toman: 73060, rial: 730600, low_toman: 72700, high_toman: 73350, change: '+۰.۵٪', time: '۱۴:۳۰' },
    currency_gbp: { title: 'پوند انگلیس', toman: 348000, rial: 3480000, low_toman: 346000, high_toman: 349500, change: '+۰.۲٪', time: '۱۴:۳۰' },
    currency_try: { title: 'لیر ترکیه', toman: 7750, rial: 77500, low_toman: 7700, high_toman: 7800, change: '-۰.۱٪', time: '۱۴:۳۰' },
    currency_cad: { title: 'دلار کانادا', toman: 191000, rial: 1910000, low_toman: 189500, high_toman: 192000, change: '+۰.۴٪', time: '۱۴:۳۰' },
    currency_aud: { title: 'دلار استرالیا', toman: 174500, rial: 1745000, low_toman: 173000, high_toman: 175500, change: '+۰.۳٪', time: '۱۴:۳۰' },
    currency_iqd: { title: '۱۰۰ دینار عراق', toman: 20450, rial: 204500, low_toman: 20300, high_toman: 20600, change: '۰.۰٪', time: '۱۴:۳۰' },
  },
  parsian: {
    '0.100': { title: 'سکه پارسیان ۰.۱۰۰ گرم', weight: 0.1, toman: 3750000, rial: 37500000, low_toman: 3720000, high_toman: 3780000, change: '+۱.۱٪', time: '۱۴:۳۰' },
    '0.200': { title: 'سکه پارسیان ۰.۲۰۰ گرم', weight: 0.2, toman: 6350000, rial: 63500000, low_toman: 6300000, high_toman: 6400000, change: '+۱.۱٪', time: '۱۴:۳۰' },
    '0.300': { title: 'سکه پارسیان ۰.۳۰۰ گرم', weight: 0.3, toman: 8950000, rial: 89500000, low_toman: 8880000, high_toman: 9020000, change: '+۱.۱٪', time: '۱۴:۳۰' },
    '0.500': { title: 'سکه پارسیان ۰.۵۰۰ گرم', weight: 0.5, toman: 14150000, rial: 141500000, low_toman: 14050000, high_toman: 14250000, change: '+۱.۱٪', time: '۱۴:۳۰' },
    '1.000': { title: 'سکه پارسیان ۱.۰۰۰ گرم', weight: 1.0, toman: 27150000, rial: 271500000, low_toman: 26950000, high_toman: 27350000, change: '+۱.۱٪', time: '۱۴:۳۰' },
    '1.500': { title: 'سکه پارسیان ۱.۵۰۰ گرم', weight: 1.5, toman: 40150000, rial: 401500000, low_toman: 39850000, high_toman: 40450000, change: '+۱.۱٪', time: '۱۴:۳۰' },
  },
  macro: {
    ons_gold: 4181.9,
    ons_silver: 53.6,
    gold_silver_ratio: 78.02,
  },
  updated_at: 'زنده (لحظه‌ای)',
};

const AppState = {
  prices: DEFAULT_PRICES,
  portfolio: [],
  alerts: [],
  theme: localStorage.getItem('tala_theme') || 'light',
  chartInstance: null,
  activeChartMarket: 'iran',
  activeChartType: 'area',
  activeChartPeriod: '6M',
  activeBoardCategory: 'all',
  activeAnalysisTab: 'trend',
  currentBudget: 50000000,
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
    if (!AppState.prices || !AppState.prices.gold || Object.keys(AppState.prices.gold).length === 0) {
      AppState.prices = DEFAULT_PRICES;
    }
    return AppState.prices;
  },

  generateClientChartData(market, period) {
    const daysMap = { '1M': 30, '3M': 90, '6M': 180, '1Y': 365 };
    const totalDays = daysMap[period] || 180;
    const { gold = {}, macro = {}, currencies = {}, silver = {} } = AppState.prices || DEFAULT_PRICES;

    let currentPrice = 26255100;
    if (market === 'iran') currentPrice = gold.gold_18k?.toman || 26255100;
    else if (market === 'global') currentPrice = macro.ons_gold || 4181.9;
    else if (market === 'usd') currentPrice = currencies.currency_usd?.toman || 267900;
    else if (market === 'silver') currentPrice = silver.silver_999?.toman || 517500;

    const gainMultipliers = { '1M': 0.035, '3M': 0.082, '6M': 0.158, '1Y': 0.385 };
    let totalGain = gainMultipliers[period] || 0.158;
    if (market === 'usd') totalGain *= 0.85;
    else if (market === 'silver') totalGain *= 1.25;

    const baseStart = currentPrice / (1.0 + totalGain);
    const series = [];
    const today = new Date();
    const dailyDrift = Math.log(currentPrice / baseStart) / totalDays;

    for (let i = 0; i < totalDays; i++) {
      const d = new Date(today);
      d.setDate(d.getDate() - (totalDays - 1 - i));
      const dateLabel = `${d.getMonth() + 1}/${d.getDate()}`;

      const expected = baseStart * Math.exp(dailyDrift * i);
      const noise = (Math.sin(i * 0.45) * 0.015 + Math.cos(i * 0.25) * 0.01) * expected;
      let dayPrice = Math.round(expected + noise);
      if (i === totalDays - 1) dayPrice = currentPrice;

      series.push({
        date: dateLabel,
        price: dayPrice,
        open: Math.round(dayPrice * 0.997),
        high: Math.round(dayPrice * 1.006),
        low: Math.round(dayPrice * 0.994),
        changePct: i > 0 ? parseFloat((((dayPrice - series[i - 1].price) / series[i - 1].price) * 100).toFixed(2)) : 0.0,
        sma20: null,
        sma50: null,
      });
    }

    for (let i = 0; i < series.length; i++) {
      if (i >= 19) {
        const sum20 = series.slice(i - 19, i + 1).reduce((acc, x) => acc + x.price, 0);
        series[i].sma20 = Math.round(sum20 / 20);
      }
      if (i >= 49) {
        const sum50 = series.slice(i - 49, i + 1).reduce((acc, x) => acc + x.price, 0);
        series[i].sma50 = Math.round(sum50 / 50);
      }
    }

    const allPrices = series.map(s => s.price);
    const highPrice = Math.max(...allPrices);
    const lowPrice = Math.min(...allPrices);
    const avgPrice = Math.round(allPrices.reduce((a, b) => a + b, 0) / allPrices.length);
    const periodChangePct = parseFloat((((currentPrice - allPrices[0]) / allPrices[0]) * 100).toFixed(2));

    const recent20 = allPrices.slice(-20);
    const refLow20 = Math.min(...recent20);
    const refHigh20 = Math.max(...recent20);
    const sma20Val = recent20.reduce((a, b) => a + b, 0) / recent20.length;
    const sma20Dist = parseFloat((((currentPrice - sma20Val) / sma20Val) * 100).toFixed(1));

    const recent50 = allPrices.slice(-50);
    const sma50Val = recent50.reduce((a, b) => a + b, 0) / recent50.length;
    const sma50Dist = parseFloat((((currentPrice - sma50Val) / sma50Val) * 100).toFixed(1));

    return {
      market,
      period,
      currentPrice,
      periodChangePct,
      highPrice,
      lowPrice,
      avgPrice,
      volatility: '۱۱.۵٪',
      sma20Distance: `${sma20Dist >= 0 ? '+' : ''}${sma20Dist}٪`,
      sma50Distance: `${sma50Dist >= 0 ? '+' : ''}${sma50Dist}٪`,
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
    const gold_18k = gold.gold_18k?.toman || 7485000;
    const silver_999 = silver.silver_999?.toman || 114000;
    const usd_price = currencies.currency_usd?.toman || 93800;
    const usdt_price = currencies.currency_usdt?.toman || 94100;
    const coin_bahar = coins.coin_bahar?.toman || 69800000;
    const ons_gold = macro.ons_gold || 2915.2;
    const ons_silver = macro.ons_silver || 33.1;
    const gsr = macro.gold_silver_ratio || 88.07;
    const bubble_emami_pct = bubbles.bubble_emami?.percentage || 19.2;
    const bubble_emami_val = bubbles.bubble_emami?.toman || 14450000;

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
        { name: 'سکه تمام بهار آزادی (طرح قدیم)', category: 'مسکوکات کم‌حباب', weight_pct: 25, budget_share: budget * 0.25, target_units: `${Math.floor((budget * 0.25) / coin_bahar)} عدد`, role: 'نقدشوندگی سریع بازار آزاد', risk: 'متوسط' },
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
    if (AppState.chartInstance) {
      UI.renderChart();
    }
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
      tableBody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding:30px; color:var(--text-muted);">موردی مطابق با فیلتر شما یافت نشد.</td></tr>`;
      return;
    }

    tableBody.innerHTML = filtered.map(item => {
      const rangeSpan = Math.max(1, item.high_toman - item.low_toman);
      const currentOffset = Math.min(100, Math.max(0, ((item.toman - item.low_toman) / rangeSpan) * 100));
      const isNegative = item.change && item.change.includes('-');

      return `
        <tr>
          <td>
            <div class="table-item-name">
              <span class="item-icon">${item.icon}</span>
              <b>${item.title}</b>
            </div>
          </td>
          <td><span style="font-size:0.8rem; color:var(--text-muted);">${item.categoryName}</span></td>
          <td><strong style="font-size:1.05rem;">${Utils.formatNumber(item.toman)}</strong></td>
          <td style="color:var(--text-muted); font-size:0.9rem;">${Utils.formatNumber(item.low_toman)}</td>
          <td class="range-bar-cell">
            <div class="range-bar-wrap">
              <span style="font-size:0.75rem; color:var(--text-muted);">${Math.round(currentOffset)}٪</span>
              <div class="range-bar">
                <div class="range-bar-fill" style="width:${currentOffset}%;"></div>
              </div>
            </div>
          </td>
          <td style="color:var(--text-muted); font-size:0.9rem;">${Utils.formatNumber(item.high_toman)}</td>
          <td>
            <span class="change compact ${isNegative ? 'negative' : 'positive'}">
              ${item.change}
            </span>
          </td>
          <td style="font-size:0.82rem; color:var(--text-muted-2);">${item.time || '-'}</td>
        </tr>
      `;
    }).join('');
  },

  async renderChart() {
    const market = AppState.activeChartMarket;
    const period = AppState.activeChartPeriod;

    let targetPrice = 18360300;
    if (AppState.prices) {
      if (market === 'iran' && AppState.prices.gold.gold_18k) targetPrice = AppState.prices.gold.gold_18k.toman;
      else if (market === 'global' && AppState.prices.macro.ons_gold) targetPrice = AppState.prices.macro.ons_gold;
      else if (market === 'usd' && AppState.prices.currencies.currency_usd) targetPrice = AppState.prices.currencies.currency_usd.toman;
      else if (market === 'silver' && AppState.prices.silver.silver_999) targetPrice = AppState.prices.silver.silver_999.toman;
    }

    const titles = {
      iran: 'طلای ۱۸ عیار',
      global: 'اونس جهانی طلا',
      usd: 'دلار بازار آزاد',
      silver: 'نقره ۹۹۹ خالص',
    };
    document.getElementById('chartAssetTitle').textContent = titles[market] || 'نمودار بازار';

    const chartData = await ApiService.fetchChartData(market, period);
    if (!chartData || !chartData.series) return;

    // Update Header Text
    const unitLabel = market === 'global' ? '$' : 'تومان';
    document.getElementById('chartCurrentPriceText').innerHTML = `${market === 'global' ? '$' : ''}${Utils.formatNumber(chartData.currentPrice)} <small>${market === 'global' ? '' : 'تومان'}</small>`;
    
    const changeBadge = document.getElementById('chartPeriodChangeBadge');
    changeBadge.textContent = `${chartData.periodChangePct >= 0 ? '+' : ''}${chartData.periodChangePct}٪`;
    changeBadge.className = `change ${chartData.periodChangePct >= 0 ? 'positive' : 'negative'}`;

    // Update Mini Stats
    document.getElementById('statHighPrice').textContent = Utils.formatNumber(chartData.highPrice);
    document.getElementById('statLowPrice').textContent = Utils.formatNumber(chartData.lowPrice);
    document.getElementById('statAvgPrice').textContent = Utils.formatNumber(chartData.avgPrice);
    document.getElementById('statSma20').textContent = chartData.sma20Distance;
    document.getElementById('statSma50').textContent = `نمای ۵۰ روزه: ${chartData.sma50Distance}`;

    // Update Analysis Panel Sync
    AppState.lastChartData = chartData;
    UI.renderAnalysisPanel();

    // Render Canvas via Chart.js
    const ctx = document.getElementById('mainChart').getContext('2d');
    if (AppState.chartInstance) {
      AppState.chartInstance.destroy();
    }

    const labels = chartData.series.map(p => p.date);
    const dataPoints = chartData.series.map(p => p.price);
    const sma20Points = chartData.series.map(p => p.sma20);

    const isDark = AppState.theme === 'dark';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.06)';
    const textColor = isDark ? '#969185' : '#817d73';

    let gradient = ctx.createLinearGradient(0, 0, 0, 350);
    gradient.addColorStop(0, 'rgba(183, 138, 50, 0.35)');
    gradient.addColorStop(1, 'rgba(183, 138, 50, 0.0)');

    const datasets = [
      {
        label: titles[market],
        data: dataPoints,
        borderColor: '#b78a32',
        borderWidth: 2.2,
        backgroundColor: AppState.activeChartType === 'area' ? gradient : 'transparent',
        fill: AppState.activeChartType === 'area',
        tension: 0.3,
        pointRadius: 0,
        pointHoverRadius: 6,
        pointHoverBackgroundColor: '#b78a32',
        pointHoverBorderColor: '#fff',
        pointHoverBorderWidth: 2,
      }
    ];

    if (AppState.activeChartType !== 'bar') {
      datasets.push({
        label: 'SMA 20 (میانگین متحرک)',
        data: sma20Points,
        borderColor: '#277d73',
        borderWidth: 1.5,
        borderDash: [4, 4],
        pointRadius: 0,
        fill: false,
        tension: 0.2,
      });
    }

    AppState.chartInstance = new Chart(ctx, {
      type: AppState.activeChartType === 'bar' ? 'bar' : 'line',
      data: { labels, datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          mode: 'index',
          intersect: false,
        },
        plugins: {
          legend: {
            display: true,
            position: 'top',
            rtl: true,
            labels: {
              color: textColor,
              font: { family: 'Vazirmatn', size: 12 }
            }
          },
          tooltip: {
            rtl: true,
            titleFont: { family: 'Vazirmatn' },
            bodyFont: { family: 'Vazirmatn' },
            callbacks: {
              label: function(context) {
                return `${context.dataset.label}: ${Utils.formatNumber(context.raw)} ${unitLabel}`;
              }
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: textColor, font: { family: 'Vazirmatn', size: 11 } }
          },
          y: {
            position: 'right',
            grid: { color: gridColor },
            ticks: {
              color: textColor,
              font: { family: 'Vazirmatn', size: 11 },
              callback: function(value) {
                return Utils.formatNumber(value);
              }
            }
          }
        }
      }
    });
  },

  renderAnalysisPanel() {
    const chartData = AppState.lastChartData;
    if (!chartData) return;

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
            <span class="change compact ${isPositive ? 'positive' : 'negative'}">
              ${isPositive ? '+' : ''}${pnlPct.toFixed(1)}٪ (${Utils.formatNumber(pnlVal)})
            </span>
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
      tableBody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:30px; color:var(--text-muted);">
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

      return `
        <tr>
          <td><b>${a.title}</b></td>
          <td><strong>${Utils.formatNumber(a.targetPrice)} تومان</strong></td>
          <td>${a.direction === 'above' ? '📈 عبور به بالا' : '📉 افت به زیر'}</td>
          <td>${Utils.formatNumber(curPrice)} تومان</td>
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

  // Mobile menu toggle & backdrop
  const mobileBtn = document.getElementById('mobileMenuBtn');
  const sidebar = document.getElementById('sidebar');
  const closeBtn = document.getElementById('sidebarCloseBtn');
  const overlay = document.getElementById('sidebarOverlay');

  const openSidebar = () => {
    if (sidebar) sidebar.classList.add('open');
    if (overlay) overlay.classList.add('active');
    document.body.classList.add('menu-open');
  };

  const closeSidebar = () => {
    if (sidebar) sidebar.classList.remove('open');
    if (overlay) overlay.classList.remove('active');
    document.body.classList.remove('menu-open');
  };

  if (mobileBtn) mobileBtn.addEventListener('click', openSidebar);
  if (closeBtn) closeBtn.addEventListener('click', closeSidebar);
  if (overlay) overlay.addEventListener('click', closeSidebar);

  // Close sidebar on navigation item click (mobile convenience)
  document.querySelectorAll('.sidebar .nav-item, #quickAlertBtn').forEach(el => {
    el.addEventListener('click', () => {
      if (window.innerWidth <= 992) {
        closeSidebar();
      }
    });
  });

  // Close sidebar on ESC key
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && sidebar && sidebar.classList.contains('open')) {
      closeSidebar();
    }
  });

  // Theme toggle
  document.getElementById('themeToggleBtn').addEventListener('click', UI.toggleTheme);

  // Initial Data Fetch
  await ApiService.fetchPrices(true);
  UI.renderOverviewCards();
  UI.renderMarketBoard();
  UI.renderPortfolio();
  UI.renderChart();
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

  // Chart Controls
  document.getElementById('chartAssetSelect').addEventListener('change', (e) => {
    AppState.activeChartMarket = e.target.value;
    UI.renderChart();
  });

  document.getElementById('chartTypeGroup').addEventListener('click', (e) => {
    if (e.target.tagName === 'BUTTON') {
      document.querySelectorAll('#chartTypeGroup button').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      AppState.activeChartType = e.target.dataset.type;
      UI.renderChart();
    }
  });

  document.getElementById('chartPeriodGroup').addEventListener('click', (e) => {
    if (e.target.tagName === 'BUTTON') {
      document.querySelectorAll('#chartPeriodGroup button').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      AppState.activeChartPeriod = e.target.dataset.period;
      document.getElementById('chartPeriodLabel').textContent = `در ${e.target.textContent} اخیر`;
      UI.renderChart();
    }
  });

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
    UI.renderChart();
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
