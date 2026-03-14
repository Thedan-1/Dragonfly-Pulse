# Dragonfly Pulse v0.1.0

## Highlights

Dragonfly Pulse is now publicly available as an open-source campus tech competition radar.

This release focuses on solving information gaps for students and mentors by aggregating official competition announcements and exposing searchable APIs.

## What's Included

- Multi-source crawler for campus competitions with per-source config.
- Announcement discovery from list pages and navigation hints.
- Content extraction and normalized structured fields.
- URL-level deduplication and persistent storage.
- Source health scoring for observability and maintenance.
- REST API:
  - GET /health
  - GET /sources
  - GET /announcements
  - GET /sources/health
- MCP tools skeleton for AI-agent integration.

## Stability and Compatibility

- Core pipeline: Python 3.9+
- MCP runtime: Python 3.10+

## Getting Started

1. Install dependencies: pip install -r requirements.txt
2. Initialize DB: PYTHONPATH=src python scripts/init_db.py
3. Run crawler once: PYTHONPATH=src python scripts/run_daily.py
4. Run API: PYTHONPATH=src python scripts/run_api.py

## Known Limitations

- Some target sites use strong anti-crawling or non-standard SSL certificates.
- MCP official SDK is not available for Python 3.9 runtime.

## Credits

Core contributor: Thedan-1
