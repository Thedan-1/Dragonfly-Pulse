from __future__ import annotations

from typing import Any, Optional

try:
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]
except Exception:  # pragma: no cover
    FastMCP = None

from competition_intel.database.db import get_session, init_db
from competition_intel.database.repository import (
    list_recent_announcements,
    list_source_health,
    list_sources,
)

if FastMCP is not None:
    mcp_server = FastMCP("Dragonfly Pulse")
else:  # pragma: no cover
    mcp_server = None


def health() -> dict[str, str]:
    """Basic health check for MCP clients."""
    return {"status": "ok"}


def get_sources(keyword: Optional[str] = None) -> list[dict[str, Any]]:
    """List configured competition sources, optionally filtered by keyword."""
    init_db()
    session = get_session()
    try:
        rows = list_sources(session=session, keyword=keyword)
        return [
            {
                "competition_name": row.competition_name,
                "homepage": row.homepage,
                "announcement_page": row.announcement_page,
                "crawl_frequency": row.crawl_frequency,
            }
            for row in rows
        ]
    finally:
        session.close()


def search_announcements(
    keyword: Optional[str] = None,
    competition_name: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """Search announcements with keyword and competition filters."""
    init_db()
    session = get_session()
    try:
        rows = list_recent_announcements(
            session=session,
            limit=max(1, min(limit, 200)),
            offset=max(0, offset),
            competition_name=competition_name,
            keyword=keyword,
        )
        return [
            {
                "competition_name": row.competition_name,
                "announcement_title": row.announcement_title,
                "registration_deadline": row.registration_deadline,
                "competition_date": row.competition_date,
                "organizer": row.organizer,
                "source_url": row.source_url,
                "created_time": row.created_time.isoformat() if row.created_time else None,
            }
            for row in rows
        ]
    finally:
        session.close()


def get_source_health(limit: int = 50) -> list[dict[str, Any]]:
    """Return source reliability scoreboard for maintenance and observability."""
    init_db()
    session = get_session()
    try:
        rows = list_source_health(session=session, limit=max(1, min(limit, 500)))
        return [
            {
                "competition_name": row.competition_name,
                "health_score": row.health_score,
                "success_count": row.success_count,
                "fail_count": row.fail_count,
                "consecutive_failures": row.consecutive_failures,
                "last_error": row.last_error,
            }
            for row in rows
        ]
    finally:
        session.close()


def run() -> None:
    if mcp_server is None:
        raise RuntimeError(
            "MCP runtime is unavailable. Install an MCP Python SDK compatible with "
            "mcp.server.fastmcp before running scripts/run_mcp.py"
        )
    mcp_server.run()


if mcp_server is not None:
    mcp_server.tool()(health)
    mcp_server.tool()(get_sources)
    mcp_server.tool()(search_announcements)
    mcp_server.tool()(get_source_health)
