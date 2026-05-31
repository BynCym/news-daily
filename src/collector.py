"""
RSS 采集引擎：获取 → 解析 → 排序 → 去重 → 按领域聚合。
"""

import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, List
from collections import defaultdict

import feedparser
import httpx

from config import SOURCES, CATEGORIES, MAX_CHARS_PER_CATEGORY, MAX_ARTICLES_PER_FEED, REQUEST_TIMEOUT, HOUR_BOUNDARY

logger = logging.getLogger(__name__)

CST = timezone(timedelta(hours=8))


def _now_cst() -> datetime:
    return datetime.now(CST)


def _text_len(text: str) -> int:
    if not text:
        return 0
    cn = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    en = len(text.replace(' ', '')) - cn
    return cn + en // 5


def _truncate_text(text: str, max_chars: int) -> str:
    if not text:
        return ""
    if _text_len(text) <= max_chars:
        return text

    result = []
    length = 0
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff':
            length += 1
        else:
            length += 1 / 5
        if length > max_chars:
            break
        result.append(ch)

    trimmed = ''.join(result)
    for punct in ['。', '！', '？', '；', '.', '!', '?']:
        idx = trimmed.rfind(punct)
        if idx > len(trimmed) // 2:
            return trimmed[:idx + 1]
    return trimmed + '……'


def fetch_feed(source) -> List[Dict]:
    articles = []
    try:
        resp = httpx.get(source.rss_url, timeout=REQUEST_TIMEOUT, follow_redirects=True)
        resp.raise_for_status()
        feed = feedparser.parse(resp.content)

        for entry in feed.entries[:MAX_ARTICLES_PER_FEED]:
            title = entry.get('title', '').strip()
            link = entry.get('link', '').strip()
            summary_raw = entry.get('summary', entry.get('description', '')).strip()

            pub_time = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                pub_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                pub_time = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)

            if not title or not link:
                continue

            articles.append({
                "title": title,
                "summary": summary_raw,
                "link": link,
                "source": source.name,
                "category": source.category,
                "lang": source.lang,
                "published": pub_time,
            })

    except Exception as e:
        logger.warning(f"[{source.name}] 抓取失败: {e}")

    return articles


def collect_all() -> Dict[str, list]:
    raw_articles = []
    for src in SOURCES:
        raw_articles.extend(fetch_feed(src))

    grouped: Dict[str, list] = defaultdict(list)
    for art in raw_articles:
        grouped[art["category"]].append(art)

    result = {}
    for cat_id in CATEGORIES:
        arts = grouped.get(cat_id, [])
        seen_links = set()
        deduped = []
        for art in arts:
            if art["link"] not in seen_links:
                seen_links.add(art["link"])
                deduped.append(art)

        def _sort_key(a):
            return a["published"] if a["published"] else datetime.min.replace(tzinfo=timezone.utc)
        deduped.sort(key=_sort_key, reverse=True)

        total_len = 0
        final = []
        for art in deduped:
            art_len = _text_len(art["title"]) + _text_len(art["summary"])
            if total_len + art_len > MAX_CHARS_PER_CATEGORY:
                title_len = _text_len(art["title"])
                if total_len + title_len <= MAX_CHARS_PER_CATEGORY:
                    art["summary"] = ""
                    art["title"] = _truncate_text(art["title"], MAX_CHARS_PER_CATEGORY - total_len)
                    final.append(art)
                break
            total_len += art_len
            art["summary"] = _truncate_text(art["summary"], MAX_CHARS_PER_CATEGORY)
            final.append(art)

        result[cat_id] = final

    return result


def compute_date_label() -> str:
    now = _now_cst()
    if now.hour >= HOUR_BOUNDARY:
        label_date = now + timedelta(days=1)
    else:
        label_date = now
    return label_date.strftime("%Y年%m月%d日")
