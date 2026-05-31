"""
HTML 日报生成器 —— 将采集结果渲染为可直接部署的静态页面。
"""

from datetime import datetime, timezone, timedelta
from typing import Dict

from config import CATEGORIES


CST = timezone(timedelta(hours=8))
NOW = datetime.now(CST)


HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>每日新闻速递 · {date_label}</title>
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
       background: #f5f6fa; color: #2c3e50; line-height: 1.7; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}

.header {{ text-align: center; padding: 40px 0 30px; }}
.header h1 {{ font-size: 1.8em; font-weight: 700; letter-spacing: 2px; }}
.header .date {{ color: #7f8c8d; font-size: 0.95em; margin-top: 6px; }}
.header .subtitle {{ color: #95a5a6; font-size: 0.85em; margin-top: 4px; }}

.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 20px; }}

.card {{ background: #fff; border-radius: 12px; overflow: hidden;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06); transition: box-shadow .2s; }}
.card:hover {{ box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}

.card-header {{ padding: 16px 20px; display: flex; align-items: center; gap: 10px; }}
.card-header .icon {{ font-size: 1.4em; }}
.card-header h2 {{ font-size: 1.15em; font-weight: 600; }}
.card-header .badge {{ margin-left: auto; font-size: 0.75em; padding: 2px 10px;
                       border-radius: 20px; color: #fff; }}

.article-list {{ padding: 0 20px 16px; }}
.article-item {{ padding: 12px 0; border-bottom: 1px solid #f0f0f0; }}
.article-item:last-child {{ border-bottom: none; }}

.article-title {{ font-size: 0.95em; font-weight: 600; line-height: 1.5; }}
.article-title a {{ color: #2c3e50; text-decoration: none; }}
.article-title a:hover {{ color: #3498db; }}

.article-summary {{ font-size: 0.85em; color: #636e72; margin-top: 4px; line-height: 1.6; }}
.article-meta {{ display: flex; align-items: center; gap: 8px; margin-top: 6px;
                 font-size: 0.78em; color: #95a5a6; }}
.article-source {{ display: inline-block; padding: 1px 8px; border-radius: 4px;
                    background: #f0f0f0; font-size: 0.92em; }}
.article-link {{ color: #3498db; text-decoration: none; font-size: 0.92em; }}
.article-link:hover {{ text-decoration: underline; }}

.empty {{ padding: 30px 20px; text-align: center; color: #bdc3c7; font-size: 0.9em; }}

.footer {{ text-align: center; padding: 30px 0; color: #bdc3c7; font-size: 0.8em; }}

@media (max-width: 480px) {{
    .grid {{ grid-template-columns: 1fr; }}
    .container {{ padding: 12px; }}
}}
</style>
</head>
<body>
<div class="container">

<div class="header">
    <h1>📰 每日新闻速递</h1>
    <div class="date">{date_label}</div>
    <div class="subtitle">六大领域 · {total_articles} 条精选 · {generated_at}</div>
</div>

<div class="grid">
{category_sections}
</div>

<div class="footer">
    由 GitHub Actions 自动生成 · {generated_at}<br>
    信息源：人民网、新华网、央视网、中国新闻网、中国经济网、BBC中文等
</div>

</div>
</body>
</html>
"""


def _format_time(dt) -> str:
    if dt is None:
        return ""
    cst_dt = dt.astimezone(CST) if dt.tzinfo else dt.replace(tzinfo=timezone.utc).astimezone(CST)
    return cst_dt.strftime("%H:%M")


def generate_html(articles_grouped: Dict[str, list], date_label: str) -> str:
    total_articles = sum(len(arts) for arts in articles_grouped.values())

    category_sections = []
    for cat_id in ["politics", "society", "economy", "scitech_edu", "entertainment", "world"]:
        cat = CATEGORIES[cat_id]
        arts = articles_grouped.get(cat_id, [])

        if not arts:
            section = f"""\
<div class="card">
    <div class="card-header" style="border-left: 4px solid {cat.color};">
        <span class="icon">{cat.icon}</span>
        <h2>{cat.label}</h2>
        <span class="badge" style="background:{cat.color};">0 条</span>
    </div>
    <div class="empty">暂无新闻</div>
</div>"""
            category_sections.append(section)
            continue

        items_html = []
        for art in arts:
            time_str = _format_time(art.get("published"))
            meta_parts = []
            if art["source"]:
                meta_parts.append(f'<span class="article-source">{art["source"]}</span>')
            if time_str:
                meta_parts.append(f'<span>{time_str}</span>')

            meta = " · ".join(meta_parts) if meta_parts else ""
            summary = art.get("summary", "")
            summary_html = f'<div class="article-summary">{summary}</div>' if summary else ""

            items_html.append(f"""\
<div class="article-item">
    <div class="article-title"><a href="{art["link"]}" target="_blank" rel="noopener">{art["title"]}</a></div>
    {summary_html}
    <div class="article-meta">{meta}</div>
</div>""")

        articles_html = "\n".join(items_html)
        count_badge = f'{len(arts)} 条'

        section = f"""\
<div class="card">
    <div class="card-header" style="border-left: 4px solid {cat.color};">
        <span class="icon">{cat.icon}</span>
        <h2>{cat.label}</h2>
        <span class="badge" style="background:{cat.color};">{count_badge}</span>
    </div>
    <div class="article-list">
    {articles_html}
    </div>
</div>"""
        category_sections.append(section)

    generated_at = NOW.strftime("%Y-%m-%d %H:%M")

    return HTML_TEMPLATE.format(
        date_label=date_label,
        total_articles=total_articles,
        generated_at=generated_at,
        category_sections="\n".join(category_sections),
    )


def save_html(html: str, output_path: str = "index.html", archive_path: str = None) -> None:
    import os
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[✓] 已生成: {output_path}")

    if archive_path:
        os.makedirs(os.path.dirname(archive_path) or ".", exist_ok=True)
        with open(archive_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[✓] 已归档: {archive_path}")
