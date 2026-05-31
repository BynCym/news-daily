"""
入口脚本 —— 直接运行 `python -m src` 即可执行完整采集流程。
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.collector import collect_all, compute_date_label
from src.generator import generate_html, save_html


def main():
    print("=" * 50)
    print("  每日新闻速递 · 采集引擎")
    print("=" * 50)

    date_label = compute_date_label()
    print(f"  日报日期: {date_label}")
    print()

    print("[1/3] 正在采集 RSS 信息源...")
    articles = collect_all()

    from config import CATEGORIES
    for cat_id, arts in articles.items():
        print(f"  {CATEGORIES[cat_id].label}: {len(arts)} 条")
    print()

    print("[2/3] 正在生成日报页面...")
    html = generate_html(articles, date_label)

    print("[3/3] 正在保存文件...")
    filename_date = date_label.replace("年", "-").replace("月", "-").replace("日", "")
    archive_path = f"archive/{filename_date}.html"
    save_html(html, output_path="index.html", archive_path=archive_path)

    print()
    print("✅ 完成！")


if __name__ == "__main__":
    main()
