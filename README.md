# 每日新闻速递 📰

每晚 22:00 自动采集六大领域热点新闻，生成可公网访问的日报页面。

## 六大领域

| 领域 | 图标 | 信息源 |
|------|------|--------|
| 时政 | 🏛 | 人民网、新华网、央视网 |
| 社会 | 👥 | 中国新闻网、新华网 |
| 经济 | 📈 | 中国经济网、新华网财经、央视财经 |
| 科教文卫 | 🔬 | 新华网科技/教育/健康 |
| 娱乐 | 🎬 | 新华网娱乐、央视文娱、中国新闻网文娱 |
| 国际 | 🌍 | 中国新闻网、BBC中文、新华网 |

## 技术架构

- **采集**: Python + feedparser + httpx
- **部署**: GitHub Actions（定时）+ GitHub Pages（托管）
- **全免费**，无需服务器

## 使用方式

1. 把这个仓库 fork 到你的 GitHub 账号
2. 进入仓库 Settings → Pages → Source 选 "GitHub Actions"
3. 之后每晚 22:00 自动执行，页面地址为：
   https://BynCym.github.io/news-daily/

也可在 Actions 页面手动触发「每日新闻速递」工作流。

## 本地运行

```bash
pip install -r requirements.txt
python -m src
```

会在当前目录生成 `index.html` 和 `archive/YYYY-MM-DD.html`。
