# 大学生竞赛情报系统

自动监控中国大学生竞赛官网，抓取公告并结构化入库，作为后续竞赛导航、截止提醒、消息推送的数据源。

一句话简介：一个帮助学生和老师打破竞赛信息差的开源情报系统。

## 产品定位建议（小而精）

不建议一开始覆盖所有全球赛事与所有类型比赛。更推荐：

- 先聚焦高价值赛道：计算机 / AI / 安全 / 数学建模
- 先聚焦高价值级别：国家级 / 国际级
- 同时覆盖高校赛与头部企业赛

推荐定位：

“面向中国大学生的高价值科技竞赛雷达，优先国家级与国际级，逐步扩展全球赛事。”

详细说明见 docs/TARGET_SCOPE.md。

当前产品方向：校园科技赛雷达（Campus Tech Competition Radar）。

品牌名称：Dragonfly Pulse（详见 docs/BRANDING.md）。

## 分阶段路线图

1. 第一阶段（MVP）

- 20-30 个高价值来源
- 保证抓取稳定性、字段准确率、查询可用性

2. 第二阶段

- 扩到 30-50 来源
- 增加更多专业赛道与企业赛事

3. 第三阶段

- 扩到 80+ 来源
- 增加订阅提醒、竞赛日历、个性化推荐

## 适用场景

- 实验室或社团构建竞赛情报看板
- 学校管理部门做竞赛通知聚合
- 个人开发者构建竞赛日历与提醒产品

## 兼容性

- Python 3.9+
- macOS / Linux（Windows 可用，命令需对应调整）
- 默认 SQLite，可切换 MySQL / PostgreSQL

## 功能

- 每日抓取竞赛官网公告列表
- 根据真实站点自动发现候选公告列表页（导航词 + 常见路径 + 配置提示）
- 自动发现新公告 URL
- 正文提取（trafilatura + readability）
- 结构化字段抽取（统一 JSON）
- SQLite/MySQL(PostgreSQL) 可扩展数据库存储
- 支持扩展到 80+ 竞赛站点

## 项目结构

- `src/competition_intel/crawler` 抓取与链接发现
- `src/competition_intel/extractor` 正文提取
- `src/competition_intel/llm` 信息抽取
- `src/competition_intel/database` 数据库模型与仓储
- `src/competition_intel/scheduler` 内置调度
- `config/sources.yaml` 竞赛源配置
- `scripts/init_db.py` 初始化数据库并写入竞赛源
- `scripts/run_daily.py` 单次执行每日抓取流程
- `tests/` 基础单元测试

## 提取字段

输出 JSON 包含字段：

- competition_name
- organizer
- announcement_title
- registration_start
- registration_deadline
- competition_date
- prize
- competition_level
- source_url

缺失字段默认返回 null。

## 快速开始

1. 安装依赖

   pip install -r requirements.txt

2. 配置环境变量

   cp .env.example .env

3. 初始化数据库

   PYTHONPATH=src python scripts/init_db.py

4. 执行一次抓取

   PYTHONPATH=src python scripts/run_daily.py

5. 运行测试

   PYTHONPATH=src python -m pytest -q

也可以使用 Makefile：

- make install
- make init-db
- make run
- make test

## 数据表

### competition_sources

- id
- competition_name
- homepage
- announcement_page
- crawl_frequency

### competition_announcements

- id
- competition_name
- announcement_title
- registration_deadline
- competition_date
- organizer
- prize
- source_url
- created_time

## 定时执行

### Linux cron

参考 `scheduler/cron_example.txt`，每天执行：

- crawler
- extractor
- database

### Python 内置调度

运行：

PYTHONPATH=src python -m competition_intel.scheduler.daily_scheduler

默认每天 03:00（Asia/Shanghai）执行。

## 真实站点策略说明

考虑到各竞赛官网结构差异较大，系统采用组合策略：

- 配置层：每个 source 可配置 list_page_hints 和 article_keywords
- 自动发现层：从导航词与常见路径发现候选公告列表页
- 正文抽取层：trafilatura 优先，readability 与纯文本回退兜底
- 信息抽取层：LLM 抽取优先，规则抽取回退

该策略便于扩展到 80+ 站点，并降低单站结构变更对整体可用性的影响。

## 调试启动

已提供 VS Code 调试配置：

- Debug Init DB
- Debug Daily Competition Crawler

直接在 Run and Debug 面板选择即可启动。

## API 配置（可选）

系统默认使用规则抽取；当你配置了 LLM API 后，会优先走 LLM 抽取，失败时自动回退到规则抽取。

在 `.env` 中配置：

- `OPENAI_API_KEY`：必填，模型服务密钥
- `OPENAI_MODEL`：可选，默认 `gpt-4o-mini`
- `OPENAI_BASE_URL`：可选，默认 `https://api.openai.com/v1`

另外建议配置：

- `HTTP_RETRIES`：HTTP 重试次数，默认 2
- `HTTP_BACKOFF_SECONDS`：重试退避秒数基线，默认 1.0
- `LOG_LEVEL`：日志级别，默认 INFO
- `LOG_FILE`：日志文件路径，留空则只输出控制台
- `API_HOST`：REST API 监听地址，默认 0.0.0.0
- `API_PORT`：REST API 端口，默认 8000

请求使用 OpenAI 兼容接口：

- `POST /chat/completions`
- 需要字段：`model`、`messages`
- 返回内容需是可解析 JSON（系统会自动提取首个 JSON 对象）

示例（OpenAI 官方）：

curl https://api.openai.com/v1/chat/completions \
   -H "Authorization: Bearer $OPENAI_API_KEY" \
   -H "Content-Type: application/json" \
   -d '{
      "model": "gpt-4o-mini",
      "messages": [{"role":"user","content":"hello"}],
      "temperature": 0
   }'

## REST API（最小可用）

启动 API：

PYTHONPATH=src python scripts/run_api.py

提供接口：

- `GET /health`：服务健康检查
- `GET /sources?keyword=`：来源列表（支持按比赛名搜索）
- `GET /announcements?limit=20&offset=0&competition_name=&keyword=`：公告列表（支持关键词）
- `GET /sources/health?limit=200`：站点健康评分

## MCP 接口

启动 MCP：

PYTHONPATH=src python scripts/run_mcp.py

已提供 MCP Tools：

- health
- get_sources
- search_announcements
- get_source_health

## 集成文档

- 品牌命名建议：docs/BRANDING.md
- MCP/OpenClaw 集成：docs/INTEGRATIONS.md

健康评分说明：

- 分数范围 0-100，越高越稳定
- 综合成功次数、失败占比、连续失败次数计算
- 可用于优先排查低分站点

## 扩展说明

- 新增竞赛网站：在 `config/sources.yaml` 增加一条 source。
- 为特定站点定制解析：在 `crawler` 中新增站点策略类。
- 可追加日历与提醒模块，直接消费 `competition_announcements` 数据。

## 开源协作

- 许可证：MIT（见 LICENSE）
- 贡献规范：CONTRIBUTING.md
- 行为准则：CODE_OF_CONDUCT.md
- 安全披露：SECURITY.md
- 发布检查清单：docs/RELEASE_CHECKLIST.md

## 核心贡献者

- Thedan-1

发布到 GitHub 前请替换以下占位信息：

- pyproject.toml 中的 Homepage / Repository / Issues URL
- SECURITY.md 与 CODE_OF_CONDUCT.md 中的联系邮箱

## 常见问题

1. 为什么有些站点抓不到数据？

- 可能原因包括动态渲染、反爬限制、证书异常或区域限制。
- 建议先在 config/sources.yaml 中补充 list_page_hints 与 article_keywords。

2. 为什么有些公告被跳过？

- 系统按 source_url 去重，数据库已存在则跳过，这是预期行为。

3. 如何上生产环境？

- 建议增加日志落盘、失败重试、指标监控与告警，并使用 PostgreSQL。
