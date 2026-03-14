from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///competition_intel.db")
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "15"))
    user_agent: str = os.getenv("USER_AGENT", "CompetitionIntelBot/0.1")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    http_retries: int = int(os.getenv("HTTP_RETRIES", "2"))
    http_backoff_seconds: float = float(os.getenv("HTTP_BACKOFF_SECONDS", "1.0"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "")
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))


BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = BASE_DIR / "config" / "sources.yaml"
APP_SETTINGS = Settings()
