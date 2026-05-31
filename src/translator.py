"""
翻译模块 —— 将外文新闻标题/摘要翻译为中文。
当前所有信息源均为中文媒体，本模块为预留接口。

接入方式（二选一）：
A. 百度翻译 API（免费额度，需 APP_ID + SECRET_KEY）
B. 调用 LLM API 翻译（如 DeepSeek/OpenAI）
"""

import logging
import hashlib
import time
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

BAIDU_APP_ID = ""
BAIDU_SECRET_KEY = ""


def baidu_translate(text: str, from_lang: str = "en", to_lang: str = "zh") -> Optional[str]:
    if not BAIDU_APP_ID or not BAIDU_SECRET_KEY:
        logger.warning("百度翻译未配置，跳过翻译")
        return None

    salt = str(int(time.time()))
    sign_raw = BAIDU_APP_ID + text + salt + BAIDU_SECRET_KEY
    sign = hashlib.md5(sign_raw.encode()).hexdigest()

    try:
        resp = httpx.post(
            "https://fanyi-api.baidu.com/api/trans/vip/translate",
            data={
                "q": text,
                "from": from_lang,
                "to": to_lang,
                "appid": BAIDU_APP_ID,
                "salt": salt,
                "sign": sign,
            },
            timeout=10,
        )
        result = resp.json()
        if "trans_result" in result:
            return result["trans_result"][0]["dst"]
        else:
            logger.warning(f"翻译失败: {result}")
            return None
    except Exception as e:
        logger.warning(f"翻译请求异常: {e}")
        return None


def translate_article(article: dict) -> dict:
    if article.get("lang", "zh") == "zh":
        return article
    translated_title = baidu_translate(article["title"])
    translated_summary = baidu_translate(article["summary"]) if article.get("summary") else None
    if translated_title:
        article["title_original"] = article["title"]
        article["title"] = translated_title
    if translated_summary:
        article["summary_original"] = article["summary"]
        article["summary"] = translated_summary
    article["lang"] = "zh"
    return article


def translate_all(articles_grouped: dict) -> dict:
    for cat_id, arts in articles_grouped.items():
        articles_grouped[cat_id] = [translate_article(a) for a in arts]
    return articles_grouped
