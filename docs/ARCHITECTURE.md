# 系统架构（通俗版）

## 你这个项目的核心目标

打破信息差：把分散在不同竞赛官网的公告，自动汇总成统一数据。

## 架构分成 5 层

1. 来源层（Source）
- 文件：config/sources.yaml
- 作用：定义要监控哪些比赛网站
- 可扩展点：新增一条 source 就能接入新比赛

2. 抓取层（Crawler）
- 文件：src/competition_intel/crawler/
- 作用：从公告列表页发现文章链接，再抓文章页
- 特点：支持候选列表页自动发现 + 重试 + 失败隔离

3. 内容层（Extractor + LLM）
- 文件：src/competition_intel/extractor/ 和 src/competition_intel/llm/
- 作用：先提取正文，再抽取结构化字段
- 策略：LLM 优先，失败回退规则抽取

4. 存储层（Database）
- 文件：src/competition_intel/database/
- 作用：保存公告、来源、健康评分
- 去重：按 source_url 去重，避免重复写入

5. 服务层（API）
- 文件：src/competition_intel/api/app.py
- 作用：给前端/小程序提供查询接口
- 当前接口：/health /sources /announcements /sources/health

## 以后想接入“其他比赛”怎么做

最简单三步：

1. 在 config/sources.yaml 增加一个 source
2. 填好 announcement_page、list_page_hints、article_keywords
3. 运行一次抓取看结果，再微调关键词

## 为什么这套设计适合打破信息差

- 每个比赛官网结构不同：配置化接入，不用每次改核心代码
- 站点会不稳定：重试 + 健康评分，能知道哪个站点常出问题
- 数据要统一：抽取后统一字段，方便检索、提醒和展示

## 规模扩展建议（从 20 到 80+）

1. 来源治理
- 给每个 source 增加 owner（谁负责维护）和 last_checked

2. 抓取治理
- 按站点分层频率（高频站点每天，多数站点每 2-3 天）

3. 质量治理
- 每周看一次 /sources/health，把低分站点优先修复

4. 服务治理
- 数据库切换到 PostgreSQL
- API 前加缓存层（比如 Redis）
