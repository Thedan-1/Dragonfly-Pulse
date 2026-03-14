from __future__ import annotations

from typing import Optional

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from competition_intel.database.models import CompetitionAnnouncement, CompetitionSource, SourceHealth


def source_exists(session: Session, competition_name: str) -> bool:
    stmt = select(CompetitionSource).where(CompetitionSource.competition_name == competition_name)
    return session.execute(stmt).scalar_one_or_none() is not None


def upsert_source(
    session: Session,
    competition_name: str,
    homepage: str,
    announcement_page: str,
    crawl_frequency: str,
) -> None:
    stmt = select(CompetitionSource).where(CompetitionSource.competition_name == competition_name)
    source = session.execute(stmt).scalar_one_or_none()
    if source is None:
        source = CompetitionSource(
            competition_name=competition_name,
            homepage=homepage,
            announcement_page=announcement_page,
            crawl_frequency=crawl_frequency,
        )
        session.add(source)
    else:
        source.homepage = homepage
        source.announcement_page = announcement_page
        source.crawl_frequency = crawl_frequency


def announcement_exists(session: Session, source_url: str) -> bool:
    stmt = select(CompetitionAnnouncement).where(CompetitionAnnouncement.source_url == source_url)
    return session.execute(stmt).scalar_one_or_none() is not None


def create_announcement(
    session: Session,
    competition_name: str,
    announcement_title: str,
    registration_deadline: Optional[str],
    competition_date: Optional[str],
    organizer: Optional[str],
    prize: Optional[str],
    source_url: str,
) -> CompetitionAnnouncement:
    row = CompetitionAnnouncement(
        competition_name=competition_name,
        announcement_title=announcement_title,
        registration_deadline=registration_deadline,
        competition_date=competition_date,
        organizer=organizer,
        prize=prize,
        source_url=source_url,
    )
    session.add(row)
    return row


def _compute_health_score(success_count: int, fail_count: int, consecutive_failures: int) -> float:
    total = success_count + fail_count
    fail_ratio_penalty = (fail_count / total) * 30.0 if total > 0 else 0.0
    consecutive_penalty = min(consecutive_failures * 12.5, 60.0)
    score = 100.0 - fail_ratio_penalty - consecutive_penalty
    return round(max(0.0, min(100.0, score)), 2)


def upsert_source_health(
    session: Session,
    competition_name: str,
    success: bool,
    error_message: Optional[str] = None,
) -> None:
    stmt = select(SourceHealth).where(SourceHealth.competition_name == competition_name)
    row = session.execute(stmt).scalar_one_or_none()
    if row is None:
        row = SourceHealth(competition_name=competition_name)
        session.add(row)

    row.success_count = int(row.success_count or 0)
    row.fail_count = int(row.fail_count or 0)
    row.consecutive_failures = int(row.consecutive_failures or 0)

    if success:
        row.success_count += 1
        row.consecutive_failures = 0
        row.last_error = None
    else:
        row.fail_count += 1
        row.consecutive_failures += 1
        row.last_error = (error_message or "")[:1000] if error_message else None

    row.health_score = _compute_health_score(
        success_count=row.success_count,
        fail_count=row.fail_count,
        consecutive_failures=row.consecutive_failures,
    )


def list_recent_announcements(
    session: Session,
    limit: int = 20,
    offset: int = 0,
    competition_name: Optional[str] = None,
    keyword: Optional[str] = None,
) -> list[CompetitionAnnouncement]:
    stmt = select(CompetitionAnnouncement)
    if competition_name:
        stmt = stmt.where(CompetitionAnnouncement.competition_name == competition_name)
    if keyword:
        like = f"%{keyword}%"
        stmt = stmt.where(
            or_(
                CompetitionAnnouncement.announcement_title.like(like),
                CompetitionAnnouncement.competition_name.like(like),
            )
        )
    stmt = stmt.order_by(CompetitionAnnouncement.created_time.desc()).offset(offset).limit(limit)
    return list(session.execute(stmt).scalars().all())


def list_source_health(session: Session, limit: int = 200) -> list[SourceHealth]:
    stmt = select(SourceHealth).order_by(SourceHealth.health_score.asc()).limit(limit)
    return list(session.execute(stmt).scalars().all())


def list_sources(session: Session, keyword: Optional[str] = None) -> list[CompetitionSource]:
    stmt = select(CompetitionSource).order_by(CompetitionSource.competition_name.asc())
    if keyword:
        like = f"%{keyword}%"
        stmt = stmt.where(CompetitionSource.competition_name.like(like))
    return list(session.execute(stmt).scalars().all())
