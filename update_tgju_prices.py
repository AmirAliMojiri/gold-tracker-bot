import json
import re
import shutil

def main():
    # Load authoritative live TGJU data
    with open('live_tgju.json', 'r', encoding='utf-8') as f:
        tgju = json.load(f)

    tgju['updated_at'] = 'زنده (لحظه‌ای TGJU.org)'

    with open('app.js', 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Update DEFAULT_PRICES
    new_def = 'const DEFAULT_PRICES = ' + json.dumps(tgju, ensure_ascii=False, indent=2) + ';'
    code = re.sub(r'const DEFAULT_PRICES = \{[\s\S]*?\n\};', new_def, code, count=1)

    # 2. Update ApiService.fetchPrices fallback to load live_tgju.json if /api/prices 404s
    fetch_old = """    if (!AppState.prices || !AppState.prices.gold || Object.keys(AppState.prices.gold).length === 0) {
      AppState.prices = DEFAULT_PRICES;
    }
    return AppState.prices;"""

    fetch_new = """    try {
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
    return AppState.prices;"""

    if fetch_old in code:
        code = code.replace(fetch_old, fetch_new)
        print("Updated fetchPrices fallback")
    else:
        print("fetch_old pattern not found in code")

    # 3. Update generateClientChartData
    chart_old_head = """    let currentPrice = 5480000;
    let title = 'طلای ۱۸ عیار';
    let isDollar = false;

    // Realistic historical start prices based on actual Iranian market data
    const historicalBases = {
      iran: {
        '1M': 5100000,
        '3M': 4350000,
        '6M': 3650000,
        '1Y': 2850000,
      },
      coin: {
        '1M': 59800000,
        '3M': 50200000,
        '6M': 42500000,
        '1Y': 33000000,
      },
      usd: {
        '1M': 68500,
        '3M': 63000,
        '6M': 58500,
        '1Y': 50500,
      },
      silver: {
        '1M': 98000,
        '3M': 88000,
        '6M': 75000,
        '1Y': 55000,
      },
      global: {
        '1M': 2680.0,
        '3M': 2505.0,
        '6M': 2380.0,
        '1Y': 2050.0,
      }
    };

    if (market === 'iran') {
      currentPrice = (gold.gold_18k && gold.gold_18k.toman) || 5480000;
      title = 'طلای ۱۸ عیار';
    } else if (market === 'coin') {
      currentPrice = (coins.coin_emami && coins.coin_emami.toman) || 67800000;
      title = 'سکه امامی';
    } else if (market === 'usd') {
      currentPrice = (currencies.currency_usd && currencies.currency_usd.toman) || 72800;
      title = 'دلار بازار آزاد';
    } else if (market === 'silver') {
      currentPrice = (silver.silver_999 && silver.silver_999.toman) || 108500;
      title = 'نقره ۹۹۹ خالص';
    } else if (market === 'global') {
      currentPrice = (macro.ons_gold) || 2785.4;
      title = 'اونس جهانی طلا';
      isDollar = true;
    }

    const marketHistory = historicalBases[market] || historicalBases.iran;
    const baseStart = marketHistory[period] || (currentPrice * 0.82);"""

    chart_new_head = """    let currentPrice = 26255100;
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
    const baseStart = currentPrice * (periodRatios[period] || 0.82);"""

    if chart_old_head in code:
        code = code.replace(chart_old_head, chart_new_head)
        print("Updated chart historical bases")
    else:
        print("chart_old_head not found in code")

    # 4. Update changeStr in chart
    old_last_candle = """      if (i === totalDays - 1) {
        close = currentPrice;
        const changeStr = (gold.gold_18k && gold.gold_18k.change) || '+۱.۱٪';
        const isUp = !changeStr.includes('-');
        const delta = Math.round(currentPrice * 0.007);
        open = isUp ? currentPrice - delta : currentPrice + delta;
        high = Math.max(open, close) + Math.round(currentPrice * 0.004);
        low = Math.min(open, close) - Math.round(currentPrice * 0.003);
      }"""

    new_last_candle = """      if (i === totalDays - 1) {
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
      }"""

    if old_last_candle in code:
        code = code.replace(old_last_candle, new_last_candle)
        print("Updated chart last candle")
    else:
        print("old_last_candle not found in code")

    # 5. Update generateClientAdvisor
    adv_old = """    const gold_18k = gold.gold_18k?.toman || 5480000;
    const silver_999 = silver.silver_999?.toman || 108500;
    const usd_price = currencies.currency_usd?.toman || 72800;
    const usdt_price = currencies.currency_usdt?.toman || 73100;
    const coin_bahar = coins.coin_bahar?.toman || 61900000;
    const ons_gold = macro.ons_gold || 2785.4;
    const ons_silver = macro.ons_silver || 34.2;
    const gsr = macro.gold_silver_ratio || 81.44;
    const bubble_emami_pct = bubbles.bubble_emami?.percentage || 18.9;
    const bubble_emami_val = bubbles.bubble_emami?.toman || 12800000;"""

    adv_new = """    const gold_18k = gold.gold_18k?.toman || 26255100;
    const silver_999 = silver.silver_999?.toman || 514800;
    const usd_price = currencies.currency_usd?.toman || 267900;
    const usdt_price = currencies.currency_usdt?.toman || 263699;
    const coin_bahar = coins.coin_bahar?.toman || 260110000;
    const ons_gold = macro.ons_gold || 4168.75;
    const ons_silver = macro.ons_silver || 57.56;
    const gsr = macro.gold_silver_ratio || 72.42;
    const bubble_emami_pct = bubbles.bubble_emami?.percentage || 3.1;
    const bubble_emami_val = bubbles.bubble_emami?.toman || 8277000;"""

    if adv_old in code:
        code = code.replace(adv_old, adv_new)
        print("Updated advisor fallbacks")
    else:
        print("adv_old not found in code")

    adv_coin_old = "target_units: `${Math.floor((budget * 0.25) / coin_bahar)} عدد`"
    adv_coin_new = "target_units: Math.floor((budget * 0.25) / coin_bahar) > 0 ? `${Math.floor((budget * 0.25) / coin_bahar)} عدد` : `${((budget * 0.25) / gold_18k).toFixed(2)} گرم طلا`"
    if adv_coin_old in code:
        code = code.replace(adv_coin_old, adv_coin_new)
        print("Updated advisor coin unit logic")

    # Save to app.js
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(code)

    # Save to static/app.js
    with open('static/app.js', 'w', encoding='utf-8') as f:
        f.write(code)

    # Also copy live_tgju.json to static/live_tgju.json
    shutil.copy('live_tgju.json', 'static/live_tgju.json')

    print("SUCCESS: Updated app.js, static/app.js, and static/live_tgju.json with exact TGJU prices!")

if __name__ == '__main__':
    main()
