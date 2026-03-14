# 集成说明：MCP 与 OpenClaw

## 1. MCP 接口（已支持）

前提：运行环境 Python 3.10+。

### 启动方式

PYTHONPATH=src python scripts/run_mcp.py

### 已提供 MCP Tools

- health: 健康检查
- get_sources: 获取比赛来源列表
- search_announcements: 按关键词/比赛名查公告
- get_source_health: 获取来源健康评分

### 适用场景

- 在支持 MCP 的 AI Agent 中直接调用竞赛数据
- 做助手类产品时，减少重复写 API 对接代码

## 2. OpenClaw 适配策略

说明：OpenClaw 生态更新较快，建议采用“适配层”而不是强绑定。

推荐方案：

1. 一级适配
- OpenClaw 通过 HTTP 调用本项目 REST API
- 接口：/sources /announcements /sources/health

2. 二级适配
- OpenClaw 通过 MCP 调用本项目 Tools
- 优势：与 AI Agent 协作更自然

## 3. 为什么先做 MCP + REST 双轨

- REST：稳定、通用、前后端都能用
- MCP：面向 Agent 场景，扩展快
- 双轨并行可以降低技术路线风险

## 4. 最佳实践

- 对外统一走 REST
- AI 工作流优先走 MCP
- 保持分类与字段标准稳定，减少上层适配成本
