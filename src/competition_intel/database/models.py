from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class CompetitionSource(Base):
    __tablename__ = "competition_sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    competition_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    homepage: Mapped[str] = mapped_column(String(1000), nullable=False)
    announcement_page: Mapped[str] = mapped_column(String(1000), nullable=False)
    crawl_frequency: Mapped[str] = mapped_column(String(50), nullable=False, default="daily")


class CompetitionAnnouncement(Base):
    __tablename__ = "competition_announcements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    competition_name: Mapped[str] = mapped_column(String(255), nullable=False)
    announcement_title: Mapped[str] = mapped_column(String(500), nullable=False)
    registration_deadline: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    competition_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    organizer: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    prize: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    source_url: Mapped[str] = mapped_column(String(1000), nullable=False, unique=True)
    created_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class SourceHealth(Base):
    __tablename__ = "source_health"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    competition_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    success_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    fail_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    consecutive_failures: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    health_score: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)
    last_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_run_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
