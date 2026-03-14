from __future__ import annotations

import uvicorn

from competition_intel.settings import APP_SETTINGS


def main() -> None:
    uvicorn.run(
        "competition_intel.api.app:app",
        host=APP_SETTINGS.api_host,
        port=APP_SETTINGS.api_port,
        reload=False,
    )


if __name__ == "__main__":
    main()
