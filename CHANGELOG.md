# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-03-14

### Added

- Initial Dragonfly Pulse release for campus tech competition intelligence.
- Source-driven crawler with candidate list page discovery and keyword filtering.
- Content extraction pipeline with trafilatura, readability, and text fallback.
- Structured information extraction with LLM-first and rule-based fallback.
- SQLite-backed storage for sources, announcements, and source health scoring.
- REST API endpoints for health, sources, announcements, and source reliability.
- MCP tool server skeleton for agent integration workflows.
- CI workflow, contribution templates, security policy, and release checklist.

### Notes

- Core features run on Python 3.9+.
- MCP runtime requires Python 3.10+ to use official SDK.
