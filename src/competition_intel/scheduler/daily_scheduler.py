from __future__ import annotations

from apscheduler.schedulers.blocking import BlockingScheduler

from competition_intel.pipeline import run_once
from competition_intel.settings import CONFIG_PATH


def main() -> None:
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")
    scheduler.add_job(lambda: run_once(CONFIG_PATH), trigger="cron", hour=3, minute=0)
    scheduler.start()


if __name__ == "__main__":
    main()
