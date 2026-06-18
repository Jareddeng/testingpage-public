# 🤖 AI Industry Intelligence Dashboard

基于 GitHub Actions 定时构建的 AI 行业可视化看板。每日自动抓取最新研报数据，生成静态网站并部署到 GitHub Pages。

---

## 📁 项目结构

```
ai-dashboard/
├── .github/
│   └── workflows/
│       └── update-dashboard.yml    # GitHub Actions 定时工作流
├── scripts/
│   └── build_dashboard.py          # 数据抓取 + HTML 构建脚本
├── templates/
│   └── dashboard.html              # Jinja2 HTML 模板
├── output/                         # 构建输出目录（GitHub Pages 托管）
│   └── index.html
├── cache/                          # 每日数据缓存
├── requirements.txt
└── README.md
```

---

## 🚀 快速部署

### 1. 创建 GitHub 仓库

```bash
# 本地初始化
git init
git add .
git commit -m "init: ai dashboard"

# 推送到 GitHub（替换为你的仓库地址）
git remote add origin https://github.com/YOUR_USERNAME/ai-dashboard.git
git push -u origin main
```

### 2. 开启 GitHub Pages

进入仓库 **Settings → Pages**：
- **Source**: GitHub Actions
- 保存即可

### 3. 配置自动更新（已内置）

工作流已配置 **每天 2 次自动构建**：

| 时间 (UTC) | 北京时间 | 说明 |
|-----------|---------|------|
| `0 6 * * *` | 14:00 | 午盘数据更新 |
| `0 22 * * *` | 06:00 | 早盘数据更新 |

也可随时进入 **Actions → Update AI Dashboard → Run workflow** 手动触发。

### 4. 访问看板

构建完成后，访问：
```
https://YOUR_USERNAME.github.io/ai-dashboard/
```

---

## 🔧 接入真实数据源

当前脚本使用**模拟数据**作为占位，你可以轻松替换为真实 API：

### 研报数据（推荐接入）

在 `build_dashboard.py` 的 `_fetch_reports()` 方法中，替换为：

```python
def _fetch_reports(self):
    # 方案 A：券商研报 API（需申请权限）
    # response = requests.get(
    #     "https://api.citics.com/reports/daily",
    #     headers={"Authorization": f"Bearer {os.getenv('CITICS_TOKEN')}"}
    # )

    # 方案 B：使用 OpenAI API 自动摘要
    # import openai
    # raw_reports = requests.get("https://your-report-source.com/api").json()
    # summaries = []
    # for r in raw_reports:
    #     summary = openai.ChatCompletion.create(...)
    #     summaries.append({"title": r["title"], "summary": summary, ...})

    # 方案 C：RSS / 爬虫抓取（BeautifulSoup）
    from bs4 import BeautifulSoup
    url = "https://www.example-research.com/daily"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    # ... 解析逻辑

    return reports
```

### 市场数据（推荐接入）

| 数据源 | 说明 | 接入方式 |
|-------|------|---------|
| **Tushare** | 中国金融数据 | `pip install tushare` + Token |
| **AKShare** | 免费开源金融数据 | `pip install akshare` |
| **Yahoo Finance** | 全球股票/指数 | `yfinance` 库 |
| **World Bank** | 宏观经济数据 | API 直接调用 |
| **IDC / Gartner** | 行业报告 | 需购买或申请试用 |

示例（AKShare 接入 AI 概念板块）：

```python
import akshare as ak

def _fetch_kpis(self):
    # 获取 AI 概念板块行情
    df = ak.stock_board_industry_name_em()
    ai_board = df[df["板块名称"].str.contains("人工智能|AI")]

    return {
        "market_cap": ai_board["总市值"].sum(),
        "change_pct": ai_board["涨跌幅"].mean(),
        # ...
    }
```

---

## 🔐 配置 Secrets（如需 API 密钥）

进入仓库 **Settings → Secrets and variables → Actions → New repository secret**：

| Secret 名称 | 用途 |
|------------|------|
| `TUSHARE_TOKEN` | Tushare 金融数据接口 |
| `OPENAI_API_KEY` | OpenAI 自动摘要生成 |
| `CITICS_TOKEN` | 中信证券研报 API |

在 `build_dashboard.py` 中通过 `os.getenv('SECRET_NAME')` 读取。

---

## 🎨 自定义配置

### 修改更新频率

编辑 `.github/workflows/update-dashboard.yml`：

```yaml
on:
  schedule:
    - cron: '0 6 * * *'    # 每天 1 次
    - cron: '0 */6 * * *'   # 每 6 小时 1 次
    - cron: '0 0 * * 1'     # 每周一 1 次
```

[Cron 表达式在线工具](https://crontab.guru/)

### 修改看板样式

编辑 `templates/dashboard.html`：
- 颜色主题：搜索 `color:` 或 Tailwind 类如 `text-sky-400`
- 布局：调整 `grid-cols-*` 类
- 图表：修改 ECharts 配置项

### 添加新图表

1. 在 `build_dashboard.py` 的 `fetch_all()` 中添加新数据字段
2. 在 `templates/dashboard.html` 中添加 `<div id="chart-new"></div>`
3. 在 `<script>` 中初始化 ECharts 实例

---

## 📊 数据缓存机制

脚本会自动将每日数据缓存到 `cache/data_YYYYMMDD.json`：

- **API 抓取失败时**：自动读取最近一次缓存，保证看板不中断
- **历史数据追溯**：保留每日快照，便于回溯分析
- **增量更新**：可扩展为仅更新变化部分，加速构建

---

## 🛠️ 本地调试

```bash
# 1. 克隆仓库
git clone https://github.com/YOUR_USERNAME/ai-dashboard.git
cd ai-dashboard

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行构建脚本
python scripts/build_dashboard.py

# 4. 查看输出
open output/index.html
```

---

## 📜 开源协议

MIT License — 可自由商用、修改、分发。

---

## 💡 进阶建议

| 功能 | 实现方式 |
|------|---------|
| **邮件/钉钉推送** | GitHub Actions + Webhook |
| **数据版本对比** | 缓存目录 `git diff` |
| **多语言支持** | Jinja2 模板 + `lang` 参数 |
| **用户订阅** | 接入 Firebase / 自建后端 |
| **PDF 导出** | Playwright + `page.pdf()` |

---

> 构建时间：{{ meta.build_time }} | 版本：{{ meta.version }}
