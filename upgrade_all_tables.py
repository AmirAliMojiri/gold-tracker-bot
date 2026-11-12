import re
import shutil

# ==========================================
# 1. Update index.html
# ==========================================
with open('d:/gemini/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1.1 Update Table 1 (Market Data Table) thead
old_thead_1 = """              <thead>
                <tr>
                  <th>نام و نماد دارایی</th>
                  <th>دسته‌بندی</th>
                  <th>نرخ لحظه‌ای (تومان)</th>
                  <th>تغییر روزانه</th>
                  <th>دامنه نوسان (کف — سقف)</th>
                  <th>حباب / اسپرد برآوردی</th>
                  <th>موقعیت تکنیکال در دامنه</th>
                </tr>
              </thead>"""

new_thead_1 = """              <thead>
                <tr>
                  <th>نام و نماد دارایی</th>
                  <th>دسته‌بندی</th>
                  <th>نرخ لحظه‌ای معامله</th>
                  <th>تغییر روزانه</th>
                  <th>دامنه نوسان (کف — سقف)</th>
                  <th>حباب / اسپرد برآوردی</th>
                  <th>موقعیت در دامنه روزانه</th>
                </tr>
              </thead>"""

# In case old_thead_1 was different
html = re.sub(r'<table class="data-table" id="marketDataTable">\s*<thead>[\s\S]*?</thead>', 
              f'<table class="data-table" id="marketDataTable">\n{new_thead_1}', html)

# 1.2 Update Table 3 (Alerts Table) thead to include "فاصله تا هدف"
old_thead_3 = """<table class="data-table" id="alertsTable">
              <thead>
                <tr>
                  <th>دارایی</th>
                  <th>قیمت هدف (تارگت)</th>
                  <th>شرط هشدار</th>
                  <th>قیمت فعلی بازار</th>
                  <th>وضعیت</th>
                  <th>عملیات</th>
                </tr>
              </thead>"""

new_thead_3 = """<table class="data-table" id="alertsTable">
              <thead>
                <tr>
                  <th>دارایی</th>
                  <th>قیمت هدف (تارگت)</th>
                  <th>شرط فعال‌سازی</th>
                  <th>نرخ لحظه‌ای بازار</th>
                  <th>فاصله تا هدف</th>
                  <th>وضعیت</th>
                  <th>عملیات</th>
                </tr>
              </thead>"""

html = html.replace(old_thead_3, new_thead_3)

with open('d:/gemini/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

shutil.copy('d:/gemini/index.html', 'd:/gemini/static/index.html')
print("index.html updated successfully!")


# ==========================================
# 2. Update app.js
# ==========================================
with open('d:/gemini/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 2.1 Add getDetailedUnitForAsset to Utils
old_utils_end = """  getUnitForAsset(key, category) {
    if (category === 'gold' || category === 'silver') return 'گرم';
    if (category === 'currencies') return key.includes('usdt') ? 'USDT' : 'واحد';
    return 'عدد';
  }
};"""

new_utils_end = """  getUnitForAsset(key, category) {
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
};"""

js = js.replace(old_utils_end, new_utils_end)

# 2.2 Update renderMarketBoard in app.js
pattern_board = r'renderMarketBoard\(\)\s*\{[\s\S]*?\n  \},'
new_render_board = """renderMarketBoard() {
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
      // 1. Column 3: Professional Price Cell with Detailed Unit & Clean Formatting
      const detailedUnit = Utils.getDetailedUnit(item);
      const priceHtml = `
        <div style="line-height:1.35;">
          <strong style="font-size:1.08rem; color:var(--gold-dark, #b45309); font-weight:800;">${Utils.formatNumber(item.toman)} <small style="font-size:0.75rem; font-weight:normal; color:var(--text-muted);">تومان</small></strong>
          <div style="font-size:0.73rem; color:var(--text-muted); font-weight:500; margin-top:2px;">${detailedUnit}</div>
        </div>`;

      // 2. Column 4: Clean Daily Change
      let changeHtml = '<span style="color:var(--text-muted); font-size:0.83rem;">بدون نوسان (۰٪)</span>';
      if (item.change && item.change !== '-' && item.change !== '(0%) 0') {
        const isNeg = item.change.includes('-');
        changeHtml = `<span class="change compact ${isNeg ? 'negative' : 'positive'}">${item.change}</span>`;
      }

      // 3. Column 5: Daily Range (Low - High)
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

      // 4. Column 6: Estimated Bubble / Spread Column
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

      // 5. Column 7: Technical Position in Daily Range
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
  },"""

js = re.sub(pattern_board, new_render_board, js, count=1)

# 2.3 Update renderPortfolio: enhance PnL column readability
pattern_portfolio_return = r'return `\s*<tr>[\s\S]*?<td>\s*<span class="change compact \$\{isPositive \? \'positive\' : \'negative\'\}">[\s\S]*?<\/tr>\s*`;'
match_port = re.search(pattern_portfolio_return, js)
if match_port:
    new_portfolio_row = """return `
        <tr>
          <td>
            <div class="table-item-name">
              <span>${liveItem ? liveItem.icon : '💼'}</span>
              <div>
                <b>${hold.title}</b>
                <small style="display:block; color:var(--text-muted); font-size:0.74rem;">تاریخ ثبت: ${hold.date}</small>
              </div>
            </div>
          </td>
          <td><b>${hold.qty.toLocaleString('fa-IR')} ${hold.unit}</b></td>
          <td>${Utils.formatNumber(hold.buyPrice)} تومان</td>
          <td><strong style="color:var(--gold-dark);">${Utils.formatNumber(currentUnitRate)}</strong> تومان</td>
          <td><strong style="font-size:0.98rem;">${Utils.formatNumber(currentVal)}</strong> <small>تومان</small></td>
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
      `;"""
    js = js.replace(match_port.group(0), new_portfolio_row)
    print("renderPortfolio row updated successfully!")

# 2.4 Update renderAlerts: include distance-to-target column
pattern_alerts = r'renderAlerts\(\)\s*\{[\s\S]*?\n  \},'
new_render_alerts = """renderAlerts() {
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

      // Distance to target %
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
  },"""

js = re.sub(pattern_alerts, new_render_alerts, js, count=1)

with open('d:/gemini/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

shutil.copy('d:/gemini/app.js', 'd:/gemini/static/app.js')
print("app.js and static/app.js updated successfully!")
