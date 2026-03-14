from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import yaml


@dataclass
class SourceConfig:
    competition_name: str
    homepage: str
    announcement_page: str
    crawl_frequency: str = "daily"
    list_page_hints: List[str] = None
    article_keywords: List[str] = None


def load_sources(config_path: Path) -> list[SourceConfig]:
    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    out: list[SourceConfig] = []
    for raw in data.get("sources", []):
        out.append(
            SourceConfig(
                competition_name=raw["competition_name"],
                homepage=raw["homepage"],
                announcement_page=raw.get("announcement_page", raw["homepage"]),
                crawl_frequency=raw.get("crawl_frequency", "daily"),
                list_page_hints=raw.get("list_page_hints", []),
                article_keywords=raw.get("article_keywords", []),
            )
        )
    return out
