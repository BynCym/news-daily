"""
新闻采集配置 —— 22 个信息源，分六大领域。
"""

from dataclasses import dataclass
from typing import List


@dataclass
class NewsSource:
    name: str
    rss_url: str
    category: str
    lang: str = "zh"


@dataclass
class Category:
    id: str
    label: str
    icon: str
    color: str


CATEGORIES = {
    "politics":       Category("politics",     "时政",   "🏛", "#E74C3C"),
    "society":        Category("society",      "社会",   "👥", "#E67E22"),
    "economy":        Category("economy",      "经济",   "📈", "#2ECC71"),
    "scitech_edu":    Category("scitech_edu",  "科教文卫", "🔬", "#3498DB"),
    "entertainment":  Category("entertainment","娱乐",   "🎬", "#9B59B6"),
    "world":          Category("world",        "国际",   "🌍", "#1ABC9C"),
}


SOURCES: List[NewsSource] = [
    # ── 时政 ──
    NewsSource("人民网-时政",  "http://www.people.com.cn/rss/politics.xml", "politics"),
    NewsSource("新华网-时政",  "http://www.xinhuanet.com/politics/news_politics.xml", "politics"),
    NewsSource("央视网-国内",  "http://www.cctv.com/program/rss/02/01/index.xml", "politics"),

    # ── 社会 ──
    NewsSource("中国新闻网-社会", "https://www.chinanews.com.cn/rss/society.xml", "society"),
    NewsSource("新华网-地方",    "http://www.xinhuanet.com/local/news_province.xml", "society"),

    # ── 经济 ──
    NewsSource("中国经济网",     "http://www.ce.cn/xwzx/gnsz/index_6273.xml", "economy"),
    NewsSource("新华网-财经",    "http://www.xinhuanet.com/fortune/news_fortune.xml", "economy"),
    NewsSource("央视网-财经",    "http://www.cctv.com/program/rss/02/04/index.xml", "economy"),

    # ── 科教文卫 ──
    NewsSource("新华网-科技",    "http://www.xinhuanet.com/tech/news_tech.xml", "scitech_edu"),
    NewsSource("新华网-教育",    "http://www.xinhuanet.com/edu/news_edu.xml", "scitech_edu"),
    NewsSource("新华网-健康",    "http://www.xinhuanet.com/health/news_health.xml", "scitech_edu"),

    # ── 娱乐 ──
    NewsSource("新华网-娱乐",    "http://www.xinhuanet.com/ent/news_ent.xml", "entertainment"),
    NewsSource("央视网-文娱",    "http://www.cctv.com/program/rss/02/07/index.xml", "entertainment"),
    NewsSource("中国新闻网-文娱", "https://www.chinanews.com.cn/rss/culture.xml", "entertainment"),

    # ── 国际 ──
    NewsSource("中国新闻网-国际", "https://www.chinanews.com.cn/rss/world.xml", "world"),
    NewsSource("BBC中文-国际",   "http://www.bbc.co.uk/zhongwen/simp/world/index.xml", "world"),
    NewsSource("新华网-国际",    "http://www.xinhuanet.com/world/news_world.xml", "world"),
]


MAX_CHARS_PER_CATEGORY = 800
MAX_ARTICLES_PER_FEED   = 20
REQUEST_TIMEOUT         = 15
HOUR_BOUNDARY           = 22
