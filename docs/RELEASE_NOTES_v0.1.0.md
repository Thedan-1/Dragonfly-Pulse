# Dragonfly Pulse v0.1.0

## 中文说明

### 亮点

Dragonfly Pulse 首个开源版本发布，定位为校园科技赛雷达。

本版本核心目标是减少竞赛信息差：自动汇总公告、抽取关键字段、提供可搜索 API。

### 包含能力

- 多来源抓取与来源配置化管理
- 公告候选页发现 + 链接去重
- 正文提取与结构化抽取
- 来源健康评分
- REST API:
  - GET /health
  - GET /sources
  - GET /announcements
  - GET /sources/health
- MCP 工具接口骨架

### 兼容性

- 核心能力：Python 3.9+
- MCP 官方 SDK：Python 3.10+

### 快速体验

1. `pip install -r requirements.txt`
2. `PYTHONPATH=src python scripts/init_db.py`
3. `PYTHONPATH=src python scripts/run_daily.py`
4. `PYTHONPATH=src python scripts/run_api.py`

### 已知限制

- 部分网站存在反爬或证书异常，可能导致单站点抓取失败
- Python 3.9 下不支持官方 MCP 运行时

---

## English Notes

### Highlights

Dragonfly Pulse v0.1.0 is the first open-source release of our campus tech competition radar.

This release focuses on reducing information gaps by aggregating official announcements, extracting key fields, and exposing searchable APIs.

### Included

- Multi-source crawler with configuration-driven source management
- Candidate list page discovery and URL-level deduplication
- Content extraction and structured information extraction
- Source health scoring for reliability monitoring
- REST API endpoints:
  - GET /health
  - GET /sources
  - GET /announcements
  - GET /sources/health
- MCP tool-server skeleton for agent integration

### Compatibility

- Core pipeline: Python 3.9+
- Official MCP runtime: Python 3.10+

### Known Limitations

- Some websites may block crawling or use non-standard SSL certificates
- Official MCP SDK is unavailable on Python 3.9 runtime

## Credits

Core contributor: Thedan-1
