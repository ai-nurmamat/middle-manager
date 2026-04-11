# Chronos-MCP: 时空记忆引擎 (Temporal Knowledge Graph Engine)

**Chronos-MCP** 是一个颠覆性的，极简、强大的“即插即用”时间序列知识图谱架构。它摒弃了传统 RAG 中低效的文档切片和静态向量检索，将世界还原为其本来的面貌：**由事件驱动的、随时间流动的实体网络**。

通过原生的 Model Context Protocol (MCP)，任何大模型（Claude, Trae, Dify 等）均可无缝接入此引擎，从而拥有穿梭于时间线、分析长期趋势、横向对比以及洞察深层图谱关系的“投研级外脑”。

## 为什么是“颠覆性”的？

1. **时序优先 (Time-Series First)**：抛弃关键字，改用实体+时间线。宁德时代的研报不再是散落的文本块，而是一条 `2021 -> 2022 -> 2023 -> 2024` 的连续毛利率与业务演化时间线。
2. **零幻觉，可溯源 (Zero-Hallucination)**：每一个时序数据点（TimePoint）都带有 `SourceEvidence`，包含置信度、来源 ID 及原始文本切片。大模型在做计算对比时，随时可以回溯到当年的那一句话。
3. **流式接入 (Zero-ETL Streaming)**：基于 LLM 的强类型抽取管道。拿到一段非结构化文本，直接解析出 `(Entity, Time, Property, Value)` 写入内存，毫秒级更新。
4. **统一重写，少文件架构**：不到 500 行代码的核心逻辑，将实体消歧、时间序列存储、动态图谱遍历和高阶数据分析工具（趋势、对比、关联）整合在极少的文件中，易于理解，极易拓展。

## 核心架构设计

- `core_models.py`：基于 Pydantic 的核心数据结构设计。定义了 `Entity`（实体）、`TimeSeries`（时间线）、`TimePoint`（数据点）以及 `TemporalRelation`（随时间演化的关系边）。
- `engine.py`：纯内存实现的 `TemporalGraphEngine`。负责 O(1) 级实体索引、别名消歧、时序数据 Upsert 与 O(log n) 级关系维护。这是整个“记忆大脑”的底座。
- `pipeline.py`：模拟从流式文本到结构化图谱的数据注入层。利用 LLM（此处为 Mock）抽取非结构化新闻/研报中的核心属性并直接写入引擎。
- `query_engine.py`：高阶分析算子。为 LLM 提供 `query_trend`（趋势分析）、`compare_entities`（跨实体多维度对齐对比）和 `discover_relations`（图谱关系发现）。
- `mcp_server.py`：极其轻量的 MCP 协议适配层。通过 stdio (JSON-RPC) 向上层大模型暴露这些投研分析工具。

## 快速体验

本项目不依赖任何复杂的外部图数据库，核心全部采用纯 Python 构建，仅依赖 `pydantic`。

```bash
# 1. 安装依赖
pip install pydantic

# 2. 运行本地测试（直接查看引擎在趋势计算、关系拉取和多维对比上的能力）
python test_local.py

# 3. 运行 MCP Server 模拟测试（通过 stdio 交互）
python test_mcp.py
```

## 面向未来的演进路线 (Future Roadmap)

如果你准备将其部署到千万级数据的真实生产环境，可以保持此架构不变，仅在 `engine.py` 层进行存储替换：

- **All-in-One 经典栈**：迁移至 **PostgreSQL**。
  - 使用 `TimescaleDB` 插件存储 `TimePoint`，获得极速的时序分析能力。
  - 使用 `Apache AGE` 或原生递归 CTE 维护 `TemporalRelation`。
  - 使用 `pgvector` 存储 `SourceEvidence` 的向量以备兜底文本检索。
- **流式抽取集群**：在 `pipeline.py` 前端接入 `Redpanda/Kafka` 和本地部署的 vLLM (如 Qwen2.5-Coder)，将全网爬虫抓取的研报和新闻源源不断地转化为时序事件流。
