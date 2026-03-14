from __future__ import annotations

import logging
from logging import Logger

from competition_intel.settings import APP_SETTINGS


def configure_logging(name: str = "competition_intel") -> Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    level = getattr(logging, APP_SETTINGS.log_level.upper(), logging.INFO)
    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if APP_SETTINGS.log_file:
        file_handler = logging.FileHandler(APP_SETTINGS.log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
