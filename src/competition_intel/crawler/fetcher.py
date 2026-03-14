from __future__ import annotations

from dataclasses import dataclass
from typing import List, Set
from urllib.parse import urljoin
from time import sleep

import requests
from bs4 import BeautifulSoup

from competition_intel.logging_utils import configure_logging
from competition_intel.settings import APP_SETTINGS

DEFAULT_ARTICLE_KEYWORDS = [
    "通知",
    "公告",
    "新闻",
    "报名",
    "大赛",
    "竞赛",
    "Notice",
    "Announcement",
]
LIST_PAGE_NAV_KEYWORDS = ["通知", "公告", "新闻", "资讯", "动态", "news", "notice", "announcement"]
DEFAULT_LIST_PATH_HINTS = ["/news", "/notice", "/notices", "/announcement", "/media/news", "/tzb/media"]

LOGGER = configure_logging("competition_intel.fetcher")


@dataclass
class ArticleSeed:
    title: str
    url: str


def fetch_html(url: str) -> str:
    headers = {"User-Agent": APP_SETTINGS.user_agent}
    attempts = APP_SETTINGS.http_retries + 1
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=APP_SETTINGS.request_timeout)
            resp.raise_for_status()
            return resp.text
        except Exception as exc:
            last_error = exc
            if attempt < attempts:
                wait = APP_SETTINGS.http_backoff_seconds * attempt
                LOGGER.warning("request failed, retrying url=%s attempt=%s/%s wait=%.1fs", url, attempt, attempts, wait)
                sleep(wait)
            else:
                LOGGER.error("request failed after retries url=%s error=%s", url, exc)
    raise last_error


def discover_article_links(list_url: str, article_keywords: List[str] = None) -> list[ArticleSeed]:
    html = fetch_html(list_url)
    soup = BeautifulSoup(html, "html.parser")
    keywords = article_keywords or DEFAULT_ARTICLE_KEYWORDS

    seeds: list[ArticleSeed] = []
    seen: Set[str] = set()

    for a in soup.find_all("a"):
        href = (a.get("href") or "").strip()
        title = " ".join(a.get_text(" ", strip=True).split())
        if not href or len(title) < 6:
            continue
        if not any(k.lower() in title.lower() for k in keywords):
            continue
        url = urljoin(list_url, href)
        if url in seen:
            continue
        seen.add(url)
        seeds.append(ArticleSeed(title=title, url=url))

    return seeds[:50]


def discover_candidate_list_pages(base_url: str, list_page_hints: List[str] = None) -> List[str]:
    candidates: List[str] = [base_url]
    seen: Set[str] = {base_url}

    hints = list_page_hints or []
    path_hints = hints if hints else DEFAULT_LIST_PATH_HINTS
    for hint in path_hints:
        url = urljoin(base_url, hint)
        if url not in seen:
            seen.add(url)
            candidates.append(url)

    try:
        html = fetch_html(base_url)
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a"):
            href = (a.get("href") or "").strip()
            text = (a.get_text(" ", strip=True) or "").lower()
            if not href:
                continue
            if not any(k.lower() in text for k in LIST_PAGE_NAV_KEYWORDS):
                continue
            url = urljoin(base_url, href)
            if url not in seen:
                seen.add(url)
                candidates.append(url)
    except Exception:
        pass

    return candidates[:10]


def discover_articles_for_source(
    homepage: str,
    announcement_page: str,
    list_page_hints: List[str] = None,
    article_keywords: List[str] = None,
) -> List[ArticleSeed]:
    list_pages = discover_candidate_list_pages(announcement_page or homepage, list_page_hints=list_page_hints)

    merged: List[ArticleSeed] = []
    seen: Set[str] = set()
    for page in list_pages:
        try:
            seeds = discover_article_links(page, article_keywords=article_keywords)
        except Exception:
            continue
        for seed in seeds:
            if seed.url in seen:
                continue
            seen.add(seed.url)
            merged.append(seed)

    return merged[:80]
