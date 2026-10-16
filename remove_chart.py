import re
import shutil

def update_index_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Remove lightweight-charts.js and chart.js script tags from head
    script_pattern = r'<!-- TradingView Lightweight Charts & Chart\.js -->\s*<script src="lightweight-charts\.js"></script>\s*<script src="https://cdn\.jsdelivr\.net/npm/chart\.js@4\.4\.1/dist/chart\.umd\.min\.js"></script>\s*'
    html = re.sub(script_pattern, '', html)

    # 2. Remove sidebar nav-item for chart
    nav_pattern = r'<a class="nav-item" href="#chart">[\s\S]*?</a>\s*'
    html = re.sub(nav_pattern, '', html)

    # 3. Remove section id="chart"
    section_pattern = r'<!-- 2\. INTERACTIVE CHART \(TradingView Pro Terminal\) -->\s*<section id="chart"[\s\S]*?</section>\s*'
    html = re.sub(section_pattern, '', html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated index.html: removed chart scripts, nav item, and chart section.")

def update_app_js():
    with open('app.js', 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Clean AppState
    old_appstate = """const AppState = {
  prices: DEFAULT_PRICES,
  portfolio: [],
  alerts: [],
  theme: localStorage.getItem('tala_theme') || 'light',
  chartInstance: null,
  tvChart: null,
  activeChartMarket: 'iran',
  activeChartType: 'candlestick',
  activeChartPeriod: '6M',
  activeBoardCategory: 'all',
  activeAnalysisTab: 'trend',
  currentBudget: 50000000,
};"""

    new_appstate = """const AppState = {
  prices: DEFAULT_PRICES,
  portfolio: [],
  alerts: [],
  theme: localStorage.getItem('tala_theme') || 'light',
  activeBoardCategory: 'all',
  activeAnalysisTab: 'trend',
  currentBudget: 50000000,
  lastChartData: null,
};"""

    if old_appstate in code:
        code = code.replace(old_appstate, new_appstate)
        print("Replaced AppState")
    else:
        print("Warning: old_appstate pattern not found")

    # 2. Remove chart update from toggleTheme
    old_toggle_theme = """  toggleTheme() {
    AppState.theme = AppState.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('tala_theme', AppState.theme);
    UI.initTheme();
    if (AppState.chartInstance || AppState.tvChart) {
      UI.renderChart();
    }
  },"""

    new_toggle_theme = """  toggleTheme() {
    AppState.theme = AppState.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('tala_theme', AppState.theme);
    UI.initTheme();
  },"""

    if old_toggle_theme in code:
        code = code.replace(old_toggle_theme, new_toggle_theme)
        print("Updated toggleTheme")
    else:
        print("Warning: old_toggle_theme pattern not found")

    # 3. Replace renderChart and ensure renderAnalysisPanel is self-sufficient
    old_render_chart = """  async renderChart() {"""
    # Find the end of renderChart method (right before renderAnalysisPanel)
    end_render_chart = """  renderAnalysisPanel() {"""

    chart_chunk_pattern = r'  async renderChart\(\) \{[\s\S]*?\}\s*,\s*\n\s*renderAnalysisPanel\(\) \{'
    new_analysis_panel = """  async renderAnalysisPanel() {
    if (!AppState.lastChartData) {
      AppState.lastChartData = await ApiService.fetchChartData('iran', '6M');
    }
    const chartData = AppState.lastChartData;
    if (!chartData) return;"""

    if re.search(chart_chunk_pattern, code):
        code = re.sub(chart_chunk_pattern, new_analysis_panel, code, count=1)
        print("Removed renderChart and updated renderAnalysisPanel")
    else:
        print("Warning: chart_chunk_pattern not matched")

    # 4. Remove UI.renderChart() in DOMContentLoaded and refresh
    code = code.replace("  UI.renderChart();\n", "")
    code = code.replace("    UI.renderChart();\n", "    UI.renderAnalysisPanel();\n")

    # 5. Remove chart event listeners (chartAssetSelect, chartTypeGroup, chartPeriodGroup, tv-tool-btn)
    chart_listeners_pattern = r'  // Chart Controls\s*document\.getElementById\(\'chartAssetSelect\'\)[\s\S]*?btn\.classList\.add\(\'active\'\);\s*\}\);\s*\}\);'
    if re.search(chart_listeners_pattern, code):
        code = re.sub(chart_listeners_pattern, '', code, count=1)
        print("Removed chart event listeners")
    else:
        print("Warning: chart_listeners_pattern not matched")

    # Ensure UI.renderAnalysisPanel() is called in DOMContentLoaded initial fetch
    old_init = """  UI.renderPortfolio();
  UI.renderScenario();"""
    new_init = """  UI.renderPortfolio();
  UI.renderAnalysisPanel();
  UI.renderScenario();"""
    if old_init in code:
        code = code.replace(old_init, new_init)
        print("Added UI.renderAnalysisPanel() to initial load")

    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Updated app.js successfully.")

def sync_static():
    for f in ['index.html', 'app.js', 'styles.css', 'live_tgju.json']:
        shutil.copy(f, f'static/{f}')
    print("Synced all updated files to static/")

if __name__ == '__main__':
    update_index_html()
    update_app_js()
    sync_static()
