import re
import shutil

# 1. Update index.html
with open('d:/gemini/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update the description under title
old_desc = "قیمت لحظه‌ای، بالاترین و پایین‌ترین نرخ ثبت‌شده امروز، میزان تغییر و زمان نوسان"
new_desc = "رصد لحظه‌ای نرخ‌ها، محاسبه حباب واقعی انواع سکه و تحلیل موقعیت تکنیکال در دامنه روزانه"
html = html.replace(old_desc, new_desc)

# Update thead
old_thead = """              <thead>
                <tr>
                  <th>نام دارایی</th>
                  <th>دسته‌بندی</th>
                  <th>قیمت لحظه‌ای (تومان)</th>
                  <th>کمترین (کف روز)</th>
                  <th>دامنه نوسان روز</th>
                  <th>بیشترین (سقف روز)</th>
                  <th>تغییر امروز</th>
                  <th>ساعت نوسان</th>
                </tr>
              </thead>"""

new_thead = """              <thead>
                <tr>
                  <th>نام و نماد دارایی</th>
                  <th>دسته‌بندی</th>
                  <th>نرخ لحظه‌ای (تومان)</th>
                  <th>تغییر روزانه</th>
                  <th>دامنه نوسان (کف — سقف)</th>
                  <th>حباب / اسپرد برآوردی</th>
                  <th>موقعیت در دامنه روزانه</th>
                </tr>
              </thead>"""

if old_thead in html:
    html = html.replace(old_thead, new_thead)
    print("Updated thead in index.html")
else:
    # Check if already partially updated
    print("Checking current thead in index.html...")

with open('d:/gemini/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

shutil.copy('d:/gemini/index.html', 'd:/gemini/static/index.html')


# 2. Update app.js
new_render_market_board = """  renderMarketBoard() {
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
      // 1. Calculate clean daily change
      let changeHtml = '<span style="color:var(--text-muted); font-size:0.85rem;">بدون نوسان (۰٪)</span>';
      if (item.change && item.change !== '-' && item.change !== '(0%) 0') {
        const isNeg = item.change.includes('-');
        changeHtml = `<span class="change compact ${isNeg ? 'negative' : 'positive'}">${item.change}</span>`;
      }

      // 2. Daily Range (Low - High)
      let rangeHtml = '';
      if (item.low_toman && item.high_toman && item.low_toman !== item.high_toman) {
        rangeHtml = `
          <div style="font-size:0.85rem; line-height:1.4;">
            <span style="color:var(--text-muted);">کف: ${Utils.formatNumber(item.low_toman)}</span><br>
            <span style="color:var(--text); font-weight:600;">سقف: ${Utils.formatNumber(item.high_toman)}</span>
          </div>`;
      } else {
        rangeHtml = `<span style="color:var(--text-muted-2); font-size:0.82rem;">نرخ پیوسته روز</span>`;
      }

      // 3. Estimated Bubble / Spread Column
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

      // 4. Technical Position in Daily Range
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
          <td><strong style="font-size:1.05rem; color:var(--gold-dark, #b45309);">${Utils.formatNumber(item.toman)}</strong></td>
          <td>${changeHtml}</td>
          <td>${rangeHtml}</td>
          <td>${bubbleSpreadHtml}</td>
          <td style="min-width:140px;">${positionHtml}</td>
        </tr>
      `;
    }).join('');
  },"""

with open('d:/gemini/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

pattern = r'  renderMarketBoard\(\)\s*\{[\s\S]*?\n  \},'
js_new = re.sub(pattern, new_render_market_board, js, count=1)

with open('d:/gemini/app.js', 'w', encoding='utf-8') as f:
    f.write(js_new)

shutil.copy('d:/gemini/app.js', 'd:/gemini/static/app.js')
print("Successfully updated app.js and static/app.js!")
