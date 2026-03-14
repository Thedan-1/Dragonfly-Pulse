from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, Query

from competition_intel.database.db import get_session, init_db
from competition_intel.database.repository import (
    list_recent_announcements,
    list_source_health,
    list_sources,
)

app = FastAPI(title="Competition Intel API", version="0.1.0")


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/announcements")
def announcements(
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    competition_name: Optional[str] = None,
    keyword: Optional[str] = None,
) -> dict:
    session = get_session()
    try:
        rows = list_recent_announcements(
            session=session,
            limit=limit,
            offset=offset,
            competition_name=competition_name,
            keyword=keyword,
        )
        data = [
            {
                "id": row.id,
                "competition_name": row.competition_name,
                "announcement_title": row.announcement_title,
                "registration_deadline": row.registration_deadline,
                "competition_date": row.competition_date,
                "organizer": row.organizer,
                "prize": row.prize,
                "source_url": row.source_url,
                "created_time": row.created_time.isoformat() if row.created_time else None,
            }
            for row in rows
        ]
        return {"items": data, "count": len(data)}
    finally:
        session.close()


@app.get("/sources")
def sources(keyword: Optional[str] = None) -> dict:
    session = get_session()
    try:
        rows = list_sources(session=session, keyword=keyword)
        data = [
            {
                "id": row.id,
                "competition_name": row.competition_name,
                "homepage": row.homepage,
                "announcement_page": row.announcement_page,
                "crawl_frequency": row.crawl_frequency,
            }
            for row in rows
        ]
        return {"items": data, "count": len(data)}
    finally:
        session.close()


@app.get("/sources/health")
def source_health(limit: int = Query(default=200, ge=1, le=500)) -> dict:
    session = get_session()
    try:
        rows = list_source_health(session=session, limit=limit)
        data = [
            {
                "competition_name": row.competition_name,
                "health_score": row.health_score,
                "success_count": row.success_count,
                "fail_count": row.fail_count,
                "consecutive_failures": row.consecutive_failures,
                "last_error": row.last_error,
                "last_run_time": row.last_run_time.isoformat() if row.last_run_time else None,
            }
            for row in rows
        ]
        return {"items": data, "count": len(data)}
    finally:
        session.close()
