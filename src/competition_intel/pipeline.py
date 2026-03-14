from __future__ import annotations

from pathlib import Path

from competition_intel.crawler.fetcher import discover_articles_for_source, fetch_html
from competition_intel.crawler.sources import load_sources
from competition_intel.database.db import get_session, init_db
from competition_intel.database.repository import (
    announcement_exists,
    create_announcement,
    upsert_source_health,
    upsert_source,
)
from competition_intel.extractor.content_extractor import ContentExtractor
from competition_intel.llm.information_extractor import extract_information
from competition_intel.logging_utils import configure_logging

LOGGER = configure_logging("competition_intel.pipeline")


def bootstrap_sources(config_path: Path) -> None:
    init_db()
    sources = load_sources(config_path)
    session = get_session()
    try:
        for source in sources:
            upsert_source(
                session=session,
                competition_name=source.competition_name,
                homepage=source.homepage,
                announcement_page=source.announcement_page,
                crawl_frequency=source.crawl_frequency,
            )
        session.commit()
    finally:
        session.close()


def run_once(config_path: Path) -> dict[str, int]:
    init_db()
    sources = load_sources(config_path)
    stats = {"sources": 0, "discovered": 0, "inserted": 0, "skipped": 0, "failed": 0}

    session = get_session()
    try:
        for source in sources:
            stats["sources"] += 1
            source_success = True
            source_error = None
            try:
                seeds = discover_articles_for_source(
                    homepage=source.homepage,
                    announcement_page=source.announcement_page,
                    list_page_hints=source.list_page_hints,
                    article_keywords=source.article_keywords,
                )
                stats["discovered"] += len(seeds)
                LOGGER.info("source discovered competition=%s count=%s", source.competition_name, len(seeds))
            except Exception:
                stats["failed"] += 1
                source_success = False
                source_error = "discover_articles_for_source failed"
                upsert_source_health(
                    session=session,
                    competition_name=source.competition_name,
                    success=False,
                    error_message=source_error,
                )
                session.commit()
                continue

            for seed in seeds:
                if announcement_exists(session, seed.url):
                    stats["skipped"] += 1
                    continue
                try:
                    html = fetch_html(seed.url)
                    text = ContentExtractor.extract_text(html)
                    payload = extract_information(
                        text=text,
                        announcement_title=seed.title,
                        source_url=seed.url,
                        competition_name=source.competition_name,
                    )
                    create_announcement(
                        session=session,
                        competition_name=payload["competition_name"],
                        announcement_title=payload["announcement_title"],
                        registration_deadline=payload["registration_deadline"],
                        competition_date=payload["competition_date"],
                        organizer=payload["organizer"],
                        prize=payload["prize"],
                        source_url=payload["source_url"],
                    )
                    session.commit()
                    stats["inserted"] += 1
                except Exception:
                    session.rollback()
                    stats["failed"] += 1
                    source_success = False
                    source_error = "article processing failed"

            upsert_source_health(
                session=session,
                competition_name=source.competition_name,
                success=source_success,
                error_message=source_error,
            )
            session.commit()
    finally:
        session.close()

    LOGGER.info("run complete stats=%s", stats)
    return stats
