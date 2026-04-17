<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/TypeScript-5.0%2B-blue?logo=typescript" alt="TypeScript 5.0+">
  <img src="https://img.shields.io/badge/MCP-Ready-green" alt="MCP Ready">
  <img src="https://img.shields.io/badge/License-MIT-purple" alt="License MIT">
  
  <h1>🌌 Chronos-MCP</h1>
  <p><b>A Disruptive 4D Cognitive Hypergraph Memory Engine for LLMs</b></p>
  <p><i>“Don't pre-define the world. Let AI understand and create it.”</i></p>
</div>

---

## 📖 English Introduction

**Chronos-MCP** completely abandons traditional Time-Series Databases (TSDB), static Knowledge Graphs (GraphDB), and document-slicing Vector RAG architectures. It is a **"Plug-and-Play, Self-Evolving Digital Memory Cortex"** specifically designed for Large Language Models (e.g., Minimax, Claude, OpenAI).

In traditional RAG architectures, systems are constrained by rigid database schemas or static text blocks. Chronos introduces an extremely minimalist yet powerful **Universal 4D Hypergraph (S-P-O-T)** architecture, abstracting all events, data, and relationships in the world into four dimensions:
**Subject — Predicate — Object — Time**.

### 🚀 Core Disruptive Features

1. **Everything is a 4D Tuple (S-P-O-T)**: Breaks the boundary between timelines and graphs. 
   - Financial Data: `("CATL", "gross margin", "28.5%", "2023-09-30")`
   - Investment: `("CATL", "invests in", "Solid State Battery", "2023-10-15")`
   A single minimalist O(1) inverted index can hold all dynamics of the financial market.
2. **100% Schema-less LLM Extraction**: No predefined fields. The LLM reads unstructured text and freely "invents" predicates that best capture the business logic.
3. **Cognitive Consolidation ("Sleep" Mechanism)**: Because the LLM has absolute freedom, the graph will inevitably accumulate noisy synonyms (e.g., "CATL" vs. "Ningwang"). Chronos introduces a human-like "sleep" mechanism. During idle time, a background process wakes up the LLM to automatically merge synonyms and normalize relationships, achieving a **Self-Evolving Ontology**.
4. **Zero-Hallucination & Traceability**: Every 4D data point is forcibly linked to `SourceEvidence` (source ID and raw text snippet), allowing the LLM to trace back to the exact sentence in the original report at any time.

---

## 📖 中文介绍 (Chinese Introduction)

**Chronos-MCP** 彻底抛弃了传统的时序数据库（TSDB）、静态知识图谱（GraphDB）以及基于文档切片的向量检索（Vector RAG）。它是专门为大语言模型（如 Minimax M2.7、Claude、OpenAI）设计的**“即插即用型、自进化数字记忆外脑”**。

在传统的 RAG 架构中，系统被死板的数据库表结构（Schema）所限制，或者被静态的文档文本所困扰。Chronos 引入了极其精简但强大的 **Universal 4D Hypergraph (S-P-O-T)** 架构，将世界上所有发生的事件、产生的数据、演变的关系，统一抽象为四个维度：
**Subject (主体) — Predicate (谓语) — Object (客体) — Time (时间)**。

### 🚀 核心颠覆性创新

1. **万物皆 4D Tuple (S-P-O-T)**：打破时序与图谱的边界。
   - 财务数据：`("宁德时代", "毛利率", "28.5%", "2023-09-30")`
   - 投资动作：`("宁德时代", "投资", "固态电池", "2023-10-15")`
   一个极简的 O(1) 倒排索引数据结构，就能容纳金融市场的全部动态，一招秒杀图数据库和时序数据库的复杂拼接。
2. **100% Schema-less 的通用抽取器**：不预定义任何字段名。大模型阅读非结构化文本后，自由“发明”并提取出最能概括商业逻辑的 Predicate（谓语）。如果明天出了一个新概念叫“低空经济市占率”，系统连一行代码都不用改，图谱里就会自动长出这条线。
3. **“睡眠与做梦”机制 (Cognitive Consolidation)**：由于给了 LLM 绝对的自由，图谱里必然会充满同义词噪音。Chronos 引入了类人脑的睡眠整理机制。在系统闲时，后台自动将同义词进行本体归一化合并，实现**图谱的自我生长与纠错 (Self-Evolving Ontology)**。
4. **零幻觉与可溯源 (Zero-Hallucination)**：每一个四维数据点都强制挂载 `SourceEvidence`，大模型在推理时，随时可以精确回溯到当年的原始研报语句。

---

## 🛠️ Installation & Quick Start

Chronos-MCP provides first-class support for both Python and TypeScript/Node.js ecosystems.

### 🐍 Python (Pip)

```bash
# Install directly from source (or PyPI when published)
pip install chronos-mcp
```

### 📦 Node.js / TypeScript (NPM)

```bash
# Install the typescript version
npm install chronos-mcp
```

### 🏃 Running a Mock Demo

Experience memory injection, noisy query failure, system sleep self-healing, and precise querying.

```bash
# In Python
python src/chronos/mcp.py
```

### 🤖 Using a Real LLM (e.g., Minimax)

Feed real unstructured news/reports to the LLM and watch it build the graph.

```bash
export MINIMAX_API_KEY="your_api_key"
export MINIMAX_BASE_URL="https://api.minimax.chat/v1"
export MINIMAX_MODEL="abab6.5-chat"

python examples/demo_minimax.py
```

---

## 🏗️ Architecture & Extensibility

The entire system is condensed into fewer than 300 lines of core logic:

- **`graph`**: Universal 4D Memory Engine core. An ultra-high concurrency inverted index implemented in pure memory.
- **`llm`**: Universal extraction pipeline based on OpenAI-compatible protocols. Converts text into S-P-O-T.
- **`sleep`**: Sleep and memory consolidation mechanism (self-evolving ontology).
- **`mcp` / `server`**: Minimalist MCP gateway and standard Stdio Server implementation. Exposes the universal `query_graph` tool.

### Production Roadmap
In the MVP phase, Chronos uses pure memory structures for extreme speed. For millions of records, **no top-level logic needs to change**. Simply replace the storage layer in `graph` with:
- **PostgreSQL**: Use `TimescaleDB` for time-series and `pgvector` for text embeddings.

## 📄 License

MIT License
