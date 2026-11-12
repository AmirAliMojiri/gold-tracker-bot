import io, sys, shutil

with open('d:/gemini/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update Utils with getDetailedUnit
target_utils = """  getUnitForAsset(key, category) {
    if (category === 'gold' || category === 'silver') return 'گرم';
    if (category === 'currencies') return key.includes('usdt') ? 'USDT' : 'واحد';
    return 'عدد';
  }"""

replacement_utils = """  getUnitForAsset(key, category) {
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
  }"""

if target_utils in code:
    code = code.replace(target_utils, replacement_utils, 1)
    print("1. Added getDetailedUnit to Utils")
else:
    print("Error: target_utils not found")


# 2. Update renderMarketBoard safely by exact replacement
target_board_render = """    tableBody.innerHTML = filtered.map(item => {
      const rangeSpan = Math.max(1, item.high_toman - item.low_toman);
      const currentOffset = Math.min(100, Math.max(0, ((item.toman - item.low_toman) / rangeSpan) * 100));
      const isNegative = item.change && item.change.includes('-');

      return `
        <tr>
          <td>
            <div class=\"table-item-name\">
              <span class=\"item-icon\">${item.icon}</span>
              <b>${item.title}</b>
            </div>
          </td>
          <td><span style=\"font-size:0.8rem; color:var(--text-muted);\">${item.categoryName}</span></td>
          <td><strong style=\"font-size:1.05rem;\">${Utils.formatNumber(item.toman)}</strong></td>
          <td style=\"color:var(--text-muted); font-size:0.9rem;\">${Utils.formatNumber(item.low_toman)}</td>
          <td class=\"range-bar-cell\">
            <div class=\"range-bar-wrap\">
              <span style=\"font-size:0.75rem; color:var(--text-muted);\">${Math.round(currentOffset)}٪</span>
              <div class=\"range-bar\">
                <div class=\"range-bar-fill\" style=\"width:${currentOffset}%;\"></div>
              </div>
            </div>
          </td>
          <td style=\"color:var(--text-muted); font-size:0.9rem;\">${Utils.formatNumber(item.high_toman)}</td>
          <td>
            <span class=\"change compact ${isNegative ? 'negative' : 'positive'}\">
              ${item.change}
            </span>
          </td>
          <td style=\"font-size:0.82rem; color:var(--text-muted-2);\">${item.time || '-'}</td>
        </tr>
      `;
    }).join('');"""

replacement_board_render = """    const { bubbles = {} } = AppState.prices || {};

    tableBody.innerHTML = filtered.map(item => {
      const detailedUnit = Utils.getDetailedUnit(item);
      const priceHtml = `
        <div style=\"line-height:1.35;\">
          <strong style=\"font-size:1.08rem; color:var(--gold-dark, #b45309); font-weight:800;\">${Utils.formatNumber(item.toman)} <small style=\"font-size:0.75rem; font-weight:normal; color:var(--text-muted);\">تومان</small></strong>
          <div style=\"font-size:0.73rem; color:var(--text-muted); font-weight:500; margin-top:2px;\">${detailedUnit}</div>
        </div>`;

      let changeHtml = '<span style=\"color:var(--text-muted); font-size:0.83rem;\">بدون نوسان (۰٪)</span>';
      if (item.change && item.change !== '-' && item.change !== '(0%) 0') {
        const isNeg = item.change.includes('-');
        changeHtml = `<span class=\"change compact ${isNeg ? 'negative' : 'positive'}\">${item.change}</span>`;
      }

      let rangeHtml = '';
      if (item.low_toman && item.high_toman && item.low_toman !== item.high_toman) {
        rangeHtml = `
          <div style=\"font-size:0.84rem; line-height:1.45;\">
            <div style=\"color:var(--text-muted);\"><small style=\"font-size:0.72rem;\">کف:</small> <b>${Utils.formatNumber(item.low_toman)}</b></div>
            <div style=\"color:var(--text);\"><small style=\"font-size:0.72rem;\">سقف:</small> <b>${Utils.formatNumber(item.high_toman)}</b></div>
          </div>`;
      } else {
        rangeHtml = `<span style=\"color:var(--text-muted-2); font-size:0.82rem;\">نرخ پیوسته روز</span>`;
      }

      let bubbleSpreadHtml = '<span style=\"color:var(--text-muted-2); font-size:0.82rem;\">فاقد حباب (اسپرد پایه)</span>';
      if (item.categoryKey === 'bubbles') {
        bubbleSpreadHtml = `<span class=\"descriptive-badge negative\" style=\"font-size:0.8rem; font-weight:700;\">حباب: ${item.percentage ? item.percentage + '٪' : Utils.formatToman(item.toman)}</span>`;
      } else if (item.key === 'coin_emami' && bubbles.bubble_emami) {
        bubbleSpreadHtml = `<span class=\"descriptive-badge negative\" style=\"font-size:0.8rem; font-weight:700;\">حباب: ${bubbles.bubble_emami.percentage}% (${Utils.formatNumber(bubbles.bubble_emami.toman)} ت)</span>`;
      } else if (item.key === 'coin_bahar' && bubbles.bubble_bahar) {
        bubbleSpreadHtml = `<span class=\"descriptive-badge negative\" style=\"font-size:0.8rem; font-weight:700;\">حباب: ${bubbles.bubble_bahar.percentage}% (${Utils.formatNumber(bubbles.bubble_bahar.toman)} ت)</span>`;
      } else if (item.key === 'coin_half_new' && bubbles.bubble_nim) {
        bubbleSpreadHtml = `<span class=\"descriptive-badge negative\" style=\"font-size:0.8rem; font-weight:700;\">حباب: ${bubbles.bubble_nim.percentage}% (${Utils.formatNumber(bubbles.bubble_nim.toman)} ت)</span>`;
      } else if (item.key === 'coin_rob_new' && bubbles.bubble_rob) {
        bubbleSpreadHtml = `<span class=\"descriptive-badge negative\" style=\"font-size:0.8rem; font-weight:700;\">حباب: ${bubbles.bubble_rob.percentage}% (${Utils.formatNumber(bubbles.bubble_rob.toman)} ت)</span>`;
      } else if (item.key === 'coin_grami' && bubbles.bubble_grami) {
        bubbleSpreadHtml = `<span class=\"descriptive-badge negative\" style=\"font-size:0.8rem; font-weight:700;\">حباب: ${bubbles.bubble_grami.percentage}% (${Utils.formatNumber(bubbles.bubble_grami.toman)} ت)</span>`;
      } else if (item.categoryKey === 'gold') {
        bubbleSpreadHtml = `<span style=\"color:var(--teal); font-size:0.82rem; font-weight:600;\">ارزش ذاتی خالص (اجرت صفر)</span>`;
      } else if (item.categoryKey === 'silver') {
        bubbleSpreadHtml = `<span style=\"color:var(--text-muted); font-size:0.82rem;\">شمش و ساچمه کارگاهی</span>`;
      } else if (item.categoryKey === 'currencies') {
        bubbleSpreadHtml = `<span style=\"color:var(--text-muted); font-size:0.82rem;\">نرخ اسکناس نقدی</span>`;
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
          <div style=\"display:flex; flex-direction:column; gap:4px;\">
            <div style=\"display:flex; justify-content:space-between; font-size:0.75rem; color:${badgeColor}; font-weight:600;\">
              <span>${badgeText}</span>
              <span>${Math.round(offset)}٪</span>
            </div>
            <div class=\"range-bar\" style=\"height:5px;\">
              <div class=\"range-bar-fill\" style=\"width:${offset}%;\"></div>
            </div>
          </div>`;
      } else {
        positionHtml = `<span style=\"color:var(--text-muted-2); font-size:0.82rem;\">نوسان متعادل و پیوسته</span>`;
      }

      return `
        <tr>
          <td>
            <div class=\"table-item-name\">
              <span class=\"item-icon\">${item.icon}</span>
              <b>${item.title}</b>
            </div>
          </td>
          <td><span style=\"font-size:0.8rem; color:var(--text-muted);\">${item.categoryName}</span></td>
          <td>${priceHtml}</td>
          <td>${changeHtml}</td>
          <td>${rangeHtml}</td>
          <td>${bubbleSpreadHtml}</td>
          <td style=\"min-width:140px;\">${positionHtml}</td>
        </tr>
      `;
    }).join('');"""

# Also update colspan in empty state of market table if needed
old_empty_market = '`<tr><td colspan="8" style="text-align:center; padding:30px; color:var(--text-muted);">'
new_empty_market = '`<tr><td colspan="7" style="text-align:center; padding:30px; color:var(--text-muted);">'
code = code.replace(old_empty_market, new_empty_market)

if target_board_render in code:
    code = code.replace(target_board_render, replacement_board_render, 1)
    print("2. Updated renderMarketBoard table rows")
else:
    print("Error: target_board_render not found")


# 3. Update renderPortfolio PnL cell safely
target_port_pnl = """          <td>
            <span class=\"change compact ${isPositive ? 'positive' : 'negative'}\">
              ${isPositive ? '+' : ''}${pnlPct.toFixed(1)}٪ (${Utils.formatNumber(pnlVal)})
            </span>
          </td>"""

replacement_port_pnl = """          <td>
            <div style=\"line-height:1.4;\">
              <span class=\"change compact ${isPositive ? 'positive' : 'negative'}\" style=\"font-weight:700;\">
                ${isPositive ? '+' : ''}${pnlPct.toFixed(1)}٪ بازده
              </span>
              <div style=\"font-size:0.78rem; font-weight:600; color:${isPositive ? 'var(--teal)' : 'var(--red)'}; margin-top:3px;\">
                ${isPositive ? '+' : ''}${Utils.formatNumber(pnlVal)} تومان
              </div>
            </div>
          </td>"""

if target_port_pnl in code:
    code = code.replace(target_port_pnl, replacement_port_pnl, 1)
    print("3. Updated renderPortfolio PnL cell")
else:
    print("Error: target_port_pnl not found")


# 4. Update renderAlerts safely
target_alerts_row = """      return `
        <tr>
          <td><b>${a.title}</b></td>
          <td><strong>${Utils.formatNumber(a.targetPrice)} تومان</strong></td>
          <td>${a.direction === 'above' ? '📈 عبور به بالا' : '📉 افت به زیر'}</td>
          <td>${Utils.formatNumber(curPrice)} تومان</td>
          <td>
            <span class=\"change compact ${triggered ? 'positive' : ''}\" style=\"${triggered ? 'background:var(--gold-soft); color:var(--gold-dark);' : ''}\">
              ${triggered ? '🔔 فعال شده / در تارگت' : '⏳ در انتظار قیمت'}
            </span>
          </td>
          <td>
            <button class=\"btn-secondary btn-danger\" style=\"padding:4px 8px; font-size:0.75rem;\" onclick=\"Handlers.deleteAlert('${a.id}')\">
              حذف
            </button>
          </td>
        </tr>
      `;"""

replacement_alerts_row = """      let distanceHtml = '';
      if (curPrice > 0 && a.targetPrice > 0) {
        const diff = a.targetPrice - curPrice;
        const diffPct = (diff / curPrice) * 100;
        const absDiffPct = Math.abs(diffPct).toFixed(1);
        if (triggered) {
          distanceHtml = `<span style=\"color:var(--teal); font-weight:700; font-size:0.82rem;\">🎯 تارگت لمس شد</span>`;
        } else {
          distanceHtml = `<span style=\"font-size:0.83rem; font-weight:600; color:var(--text-muted);\">${absDiffPct}٪ فاصله تا تارگت</span>`;
        }
      } else {
        distanceHtml = '-';
      }

      return `
        <tr>
          <td><b>${a.title}</b></td>
          <td><strong style=\"color:var(--gold-dark);\">${Utils.formatNumber(a.targetPrice)} تومان</strong></td>
          <td>${a.direction === 'above' ? '📈 عبور به بالا' : '📉 افت به زیر'}</td>
          <td>${Utils.formatNumber(curPrice)} تومان</td>
          <td>${distanceHtml}</td>
          <td>
            <span class=\"change compact ${triggered ? 'positive' : ''}\" style=\"${triggered ? 'background:var(--gold-soft); color:var(--gold-dark);' : ''}\">
              ${triggered ? '🔔 فعال شده / در تارگت' : '⏳ در انتظار قیمت'}
            </span>
          </td>
          <td>
            <button class=\"btn-secondary btn-danger\" style=\"padding:4px 8px; font-size:0.75rem;\" onclick=\"Handlers.deleteAlert('${a.id}')\">
              حذف
            </button>
          </td>
        </tr>
      `;"""

old_empty_alerts = '`<tr><td colspan="6" style="text-align:center; padding:30px; color:var(--text-muted);">'
new_empty_alerts = '`<tr><td colspan="7" style="text-align:center; padding:30px; color:var(--text-muted);">'
code = code.replace(old_empty_alerts, new_empty_alerts)

if target_alerts_row in code:
    code = code.replace(target_alerts_row, replacement_alerts_row, 1)
    print("4. Updated renderAlerts row with distance metric")
else:
    print("Error: target_alerts_row not found")

with open('d:/gemini/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

shutil.copy('d:/gemini/app.js', 'd:/gemini/static/app.js')
print("Successfully modified and saved app.js and static/app.js!")
