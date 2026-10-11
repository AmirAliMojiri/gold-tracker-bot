/**
 * Tala-Nama Dashboard Core Application Script
 * Real-time prices, High/Low daily range, Portfolio P&L, Macro Advisor, Chart & Alerts
 */

// Application State
const DEFAULT_PRICES = {
  gold: {
    gold_18k: { title: 'طلای ۱۸ عیار', toman: 7485000, rial: 74850000, low_toman: 7410000, high_toman: 7520000, change: '+۱.۲٪', time: '۱۶:۴۰' },
    gold_24k: { title: 'طلای ۲۴ عیار', toman: 9980000, rial: 99800000, low_toman: 9890000, high_toman: 10020000, change: '+۱.۲٪', time: '۱۶:۴۰' },
    gold_used: { title: 'طلای دست دوم', toman: 7380000, rial: 73800000, low_toman: 7310000, high_toman: 7420000, change: '+۱.۱٪', time: '۱۶:۴۰' },
    mesghal: { title: 'مثقال طلا', toman: 32420000, rial: 324200000, low_toman: 32100000, high_toman: 32580000, change: '+۱.۲٪', time: '۱۶:۴۰' },
    gold_melted: { title: 'آبشده نقدی', toman: 32420000, rial: 324200000, low_toman: 32100000, high_toman: 32580000, change: '+۱.۲٪', time: '۱۶:۴۰' },
  },
  silver: {
    silver_999: { title: 'گرم نقره ۹۹۹ (خالص/شمش)', toman: 114000, rial: 1140000, low_toman: 111500, high_toman: 115000, change: '+۲.۱٪', time: '۱۶:۴۰' },
    silver_925: { title: 'گرم نقره ۹۲۵ (استرلینگ)', toman: 105500, rial: 1055000, low_toman: 103200, high_toman: 106500, change: '+۲.۱٪', time: '۱۶:۴۰' },
  },
  coins: {
    coin_emami: { title: 'سکه امامی', toman: 75200000, rial: 752000000, low_toman: 74400000, high_toman: 75600000, change: '+۰.۹٪', time: '۱۶:۴۰' },
    coin_bahar: { title: 'سکه بهار آزادی', toman: 69800000, rial: 698000000, low_toman: 69100000, high_toman: 70200000, change: '+۰.۸٪', time: '۱۶:۴۰' },
    coin_half_new: { title: 'نیم سکه', toman: 42400000, rial: 424000000, low_toman: 41800000, high_toman: 42700000, change: '+۱.۰٪', time: '۱۶:۴۰' },
    coin_rob_new: { title: 'ربع سکه', toman: 25200000, rial: 252000000, low_toman: 24800000, high_toman: 25400000, change: '+۱.۱٪', time: '۱۶:۴۰' },
    coin_grami: { title: 'سکه گرمی', toman: 13900000, rial: 139000000, low_toman: 13700000, high_toman: 14000000, change: '+۰.۵٪', time: '۱۶:۴۰' },
    coin_emami_old: { title: 'تمام سکه طرح قدیم (قبل ۸۶)', toman: 68200000, rial: 682000000, low_toman: 67500000, high_toman: 68600000, change: '+۰.۷٪', time: '۱۶:۴۰' },
    coin_half_old: { title: 'نیم سکه طرح قدیم (قبل ۸۶)', toman: 40800000, rial: 408000000, low_toman: 40200000, high_toman: 41100000, change: '+۰.۸٪', time: '۱۶:۴۰' },
    coin_rob_old: { title: 'ربع سکه طرح قدیم (قبل ۸۶)', toman: 24100000, rial: 241000000, low_toman: 23800000, high_toman: 24300000, change: '+۰.۹٪', time: '۱۶:۴۰' },
  },
  bubbles: {
    bubble_emami: { title: 'حباب سکه امامی', toman: 14450000, rial: 144500000, percentage: 19.2, time: '۱۶:۴۰' },
    bubble_bahar: { title: 'حباب بهار آزادی', toman: 9050000, rial: 90500000, percentage: 13.0, time: '۱۶:۴۰' },
    bubble_nim: { title: 'حباب نیم سکه', toman: 12020000, rial: 120200000, percentage: 28.3, time: '۱۶:۴۰' },
    bubble_rob: { title: 'حباب ربع سکه', toman: 10010000, rial: 100100000, percentage: 39.7, time: '۱۶:۴۰' },
    bubble_grami: { title: 'حباب سکه گرمی', toman: 6310000, rial: 63100000, percentage: 45.4, time: '۱۶:۴۰' },
  },
  currencies: {
    currency_usd: { title: 'دلار آمریکا', toman: 93800, rial: 938000, low_toman: 93200, high_toman: 94100, change: '+۰.۶٪', time: '۱۶:۴۰' },
    currency_usdt: { title: 'تتر (USDT)', toman: 94100, rial: 941000, low_toman: 93600, high_toman: 94300, change: '+۰.۵٪', time: '۱۶:۴۰' },
    currency_eur: { title: 'یورو', toman: 101800, rial: 1018000, low_toman: 101200, high_toman: 102200, change: '+۰.۴٪', time: '۱۶:۴۰' },
    currency_aed: { title: 'درهم امارات', toman: 25550, rial: 255500, low_toman: 25400, high_toman: 25650, change: '+۰.۶٪', time: '۱۶:۴۰' },
    currency_gbp: { title: 'پوند انگلیس', toman: 121500, rial: 1215000, low_toman: 120800, high_toman: 122000, change: '+۰.۳٪', time: '۱۶:۴۰' },
    currency_try: { title: 'لیر ترکیه', toman: 2710, rial: 27100, low_toman: 2690, high_toman: 2730, change: '-۰.۱٪', time: '۱۶:۴۰' },
    currency_cad: { title: 'دلار کانادا', toman: 66800, rial: 668000, low_toman: 66400, high_toman: 67100, change: '+۰.۵٪', time: '۱۶:۴۰' },
    currency_aud: { title: 'دلار استرالیا', toman: 61200, rial: 612000, low_toman: 60800, high_toman: 61500, change: '+۰.۴٪', time: '۱۶:۴۰' },
    currency_iqd: { title: '۱۰۰ دینار عراق', toman: 7150, rial: 71500, low_toman: 7100, high_toman: 7200, change: '۰.۰٪', time: '۱۶:۴۰' },
  },
  parsian: {
    '0.100': { title: 'سکه پارسیان ۰.۱۰۰ گرم', weight: 0.1, toman: 1148000, rial: 11480000, low_toman: 1140000, high_toman: 1155000, change: '+۱.۲٪', time: '۱۶:۴۰' },
    '0.200': { title: 'سکه پارسیان ۰.۲۰۰ گرم', weight: 0.2, toman: 1897000, rial: 18970000, low_toman: 1880000, high_toman: 1910000, change: '+۱.۲٪', time: '۱۶:۴۰' },
    '0.300': { title: 'سکه پارسیان ۰.۳۰۰ گرم', weight: 0.3, toman: 2645000, rial: 26450000, low_toman: 2620000, high_toman: 2660000, change: '+۱.۲٪', time: '۱۶:۴۰' },
    '0.500': { title: 'سکه پارسیان ۰.۵۰۰ گرم', weight: 0.5, toman: 4142000, rial: 41420000, low_toman: 4100000, high_toman: 4170000, change: '+۱.۲٪', time: '۱۶:۴۰' },
    '1.000': { title: 'سکه پارسیان ۱.۰۰۰ گرم', weight: 1.0, toman: 7885000, rial: 78850000, low_toman: 7800000, high_toman: 7920000, change: '+۱.۲٪', time: '۱۶:۴۰' },
    '1.500': { title: 'سکه پارسیان ۱.۵۰۰ گرم', weight: 1.5, toman: 11627000, rial: 116270000, low_toman: 11500000, high_toman: 11700000, change: '+۱.۲٪', time: '۱۶:۴۰' },
  },
  macro: {
    ons_gold: 2915.2,
    ons_silver: 33.1,
    gold_silver_ratio: 88.07,
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
    this.syncPortfolioToServer();
  },

  async syncPortfolioToServer() {
    if (AuthService && AuthService.token) {
      try {
        await fetch('/api/portfolio', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${AuthService.token}`
          },
          body: JSON.stringify({ portfolio: AppState.portfolio })
        });
      } catch (e) {
        console.warn('Sync to server failed', e);
      }
    }
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

// Auth Service
const AuthService = {
  token: localStorage.getItem('tala_auth_token') || null,
  user: null,

  async checkAuth() {
    if (!this.token) {
      UI.updateAuthUI(null);
      return null;
    }
    try {
      const res = await fetch('/api/auth/me', {
        headers: { 'Authorization': `Bearer ${this.token}` }
      });
      if (res.ok) {
        const data = await res.json();
        if (data.authenticated && data.user) {
          this.user = data.user;
          UI.updateAuthUI(this.user);
          if (data.portfolio && Array.isArray(data.portfolio) && data.portfolio.length > 0) {
            AppState.portfolio = data.portfolio;
            localStorage.setItem('tala_portfolio', JSON.stringify(AppState.portfolio));
            UI.updatePortfolioCountBadge();
            UI.renderPortfolio();
          }
          return this.user;
        }
      }
    } catch (e) {
      console.warn('Auth check failed', e);
    }
    this.token = null;
    localStorage.removeItem('tala_auth_token');
    UI.updateAuthUI(null);
    return null;
  },

  async login(username, password) {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      this.token = data.token;
      this.user = data.user;
      localStorage.setItem('tala_auth_token', this.token);
      UI.updateAuthUI(this.user);

      if (data.portfolio && Array.isArray(data.portfolio) && data.portfolio.length > 0) {
        AppState.portfolio = data.portfolio;
        localStorage.setItem('tala_portfolio', JSON.stringify(AppState.portfolio));
      } else if (AppState.portfolio.length > 0) {
        await StorageService.syncPortfolioToServer();
      }
      UI.updatePortfolioCountBadge();
      UI.renderPortfolio();
      return { success: true };
    }
    return { success: false, error: data.error || 'نام کاربری یا رمز عبور اشتباه است.' };
  },

  async register(username, password, display_name) {
    const res = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, display_name })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      this.token = data.token;
      this.user = data.user;
      localStorage.setItem('tala_auth_token', this.token);
      UI.updateAuthUI(this.user);
      if (AppState.portfolio.length > 0) {
        await StorageService.syncPortfolioToServer();
      }
      return { success: true };
    }
    return { success: false, error: data.error || 'خطا در ثبت‌نام.' };
  },

  async logout() {
    if (this.token) {
      try {
        await fetch('/api/auth/logout', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${this.token}` }
        });
      } catch (e) {}
    }
    this.token = null;
    this.user = null;
    localStorage.removeItem('tala_auth_token');
    UI.updateAuthUI(null);
    UI.showToast('از حساب کاربری خارج شدید.');
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

  async fetchChartData(market, period) {
    try {
      const res = await fetch(`/api/chart-history?market=${encodeURIComponent(market)}&period=${encodeURIComponent(period)}`);
      if (res.ok) {
        return await res.json();
      }
    } catch (e) {
      console.warn('Error fetching chart data', e);
    }
    return null;
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
      console.warn('Error fetching advisor', e);
    }
    return null;
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

  updateAuthUI(user) {
    const openBtn = document.getElementById('openAuthModalBtn');
    const badge = document.getElementById('userProfileBadge');
    const nameEl = document.getElementById('userDisplayName');
    const avatarEl = document.getElementById('userAvatarLetter');

    if (user) {
      if (openBtn) openBtn.style.display = 'none';
      if (badge) badge.style.display = 'flex';
      if (nameEl) nameEl.textContent = user.display_name || user.username;
      if (avatarEl) {
        const letter = (user.display_name || user.username || 'ک')[0];
        avatarEl.textContent = letter;
      }
    } else {
      if (openBtn) openBtn.style.display = 'inline-flex';
      if (badge) badge.style.display = 'none';
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
      document.getElementById('cardBubblePct').textContent = `حباب: ${bubbleEmami.percentage || ۰}٪`;
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
    document.getElementById('analysisScoreVal').textContent = chartData.score;
    document.getElementById('analysisSentimentText').textContent = chartData.sentiment;
    document.getElementById('metricSma20Dist').textContent = chartData.sma20Distance;
    document.getElementById('metricSma50Dist').textContent = chartData.sma50Distance;
    document.getElementById('metricRangePos').textContent = `${chartData.rangePosition}٪`;
    document.getElementById('metricRefLow').textContent = Utils.formatNumber(chartData.refLow20);
    document.getElementById('metricRefHigh').textContent = Utils.formatNumber(chartData.refHigh20);

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
    document.getElementById('advisorBubbleVal').textContent = `${macro_metrics.bubble_emami_pct || ۰}٪`;
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
    const goldOunceBase = (AppState.prices.macro && AppState.prices.macro.ons_gold) || 4029.42;
    const usdBase = (AppState.prices.currencies.currency_usd && AppState.prices.currencies.currency_usd.toman) || 188200;
    const gold18Base = (AppState.prices.gold.gold_18k && AppState.prices.gold.gold_18k.toman) || 18360300;

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

  // Mobile menu toggle
  const mobileBtn = document.getElementById('mobileMenuBtn');
  const sidebar = document.getElementById('sidebar');
  const closeBtn = document.getElementById('sidebarCloseBtn');
  if (mobileBtn && sidebar) {
    mobileBtn.addEventListener('click', () => sidebar.classList.add('open'));
  }
  if (closeBtn && sidebar) {
    closeBtn.addEventListener('click', () => sidebar.classList.remove('open'));
  }

  // Theme toggle
  document.getElementById('themeToggleBtn').addEventListener('click', UI.toggleTheme);

  // Initial Data Fetch & Cloud Auth Check
  await ApiService.fetchPrices(true);
  await AuthService.checkAuth();
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

  // Auth Modal Controls
  const authModal = document.getElementById('authModal');
  const openAuthBtn = document.getElementById('openAuthModalBtn');
  const closeAuthBtn = document.getElementById('closeAuthModalBtn');
  const logoutBtn = document.getElementById('logoutBtn');
  const tabBtnLogin = document.getElementById('tabBtnLogin');
  const tabBtnRegister = document.getElementById('tabBtnRegister');
  const loginForm = document.getElementById('loginForm');
  const registerForm = document.getElementById('registerForm');
  const loginMsg = document.getElementById('loginMsg');
  const registerMsg = document.getElementById('registerMsg');

  if (openAuthBtn && authModal) {
    openAuthBtn.addEventListener('click', () => {
      authModal.classList.add('active');
      if (loginMsg) { loginMsg.className = 'auth-msg'; loginMsg.textContent = ''; }
      if (registerMsg) { registerMsg.className = 'auth-msg'; registerMsg.textContent = ''; }
    });
  }

  if (closeAuthBtn && authModal) {
    closeAuthBtn.addEventListener('click', () => authModal.classList.remove('active'));
  }

  if (logoutBtn) {
    logoutBtn.addEventListener('click', async () => {
      if (confirm('آیا مایلید از حساب کاربری خود خارج شوید؟')) {
        await AuthService.logout();
      }
    });
  }

  if (tabBtnLogin && tabBtnRegister) {
    tabBtnLogin.addEventListener('click', () => {
      tabBtnLogin.classList.add('active');
      tabBtnRegister.classList.remove('active');
      loginForm.classList.add('active');
      registerForm.classList.remove('active');
    });

    tabBtnRegister.addEventListener('click', () => {
      tabBtnRegister.classList.add('active');
      tabBtnLogin.classList.remove('active');
      registerForm.classList.add('active');
      loginForm.classList.remove('active');
    });
  }

  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const u = document.getElementById('loginUsername').value.trim();
      const p = document.getElementById('loginPassword').value.trim();
      loginMsg.className = 'auth-msg';
      loginMsg.textContent = 'در حال بررسی اطلاعات...';
      loginMsg.style.display = 'block';

      const res = await AuthService.login(u, p);
      if (res.success) {
        loginMsg.className = 'auth-msg success';
        loginMsg.textContent = 'خوش آمدید! سبد دارایی شما همگام‌سازی شد.';
        setTimeout(() => {
          authModal.classList.remove('active');
          UI.showToast(`خوش آمدید، ${AuthService.user.display_name || u} 👋`);
        }, 800);
      } else {
        loginMsg.className = 'auth-msg error';
        loginMsg.textContent = res.error;
      }
    });
  }

  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const name = document.getElementById('regDisplayName').value.trim();
      const u = document.getElementById('regUsername').value.trim();
      const p = document.getElementById('regPassword').value.trim();
      registerMsg.className = 'auth-msg';
      registerMsg.textContent = 'در حال ایجاد حساب کاربری...';
      registerMsg.style.display = 'block';

      const res = await AuthService.register(u, p, name);
      if (res.success) {
        registerMsg.className = 'auth-msg success';
        registerMsg.textContent = 'حساب با موفقیت ایجاد شد و سبد شما ثبت گردید!';
        setTimeout(() => {
          authModal.classList.remove('active');
          UI.showToast(`حساب کاربری ${name} فعال شد 🎉`);
        }, 800);
      } else {
        registerMsg.className = 'auth-msg error';
        registerMsg.textContent = res.error;
      }
    });
  }

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
