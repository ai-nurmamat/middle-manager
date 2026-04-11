<div align="center">
  <h1>🌌 Chronos-MCP</h1>
  <p><b>A Disruptive 4D Cognitive Hypergraph Memory Engine for LLMs</b></p>
  <p><b>“不要预设世界，让 AI 去理解和创造世界。”</b></p>
</div>

---

## 💡 What is Chronos-MCP?

Chronos-MCP 彻底抛弃了传统的时序数据库（TSDB）、静态知识图谱（GraphDB）以及基于文档切片的向量检索（Vector RAG）。它是专门为大语言模型（如 Minimax M2.7、Claude、OpenAI）设计的**“即插即用型、自进化数字记忆外脑”**。

在传统的 RAG 架构中，系统被死板的数据库表结构（Schema）所限制，或者被静态的文档文本所困扰。Chronos 引入了极其精简但强大的 **Universal 4D Hypergraph (S-P-O-T)** 架构，将世界上所有发生的事件、产生的数据、演变的关系，统一抽象为四个维度：
**Subject (主体) — Predicate (谓语) — Object (客体) — Time (时间)**。

## 🚀 核心颠覆性创新 (Disruptive Features)

### 1. 万物皆 4D Tuple (S-P-O-T)，打破时序与图谱的边界
不再区分“时间线（毛利率）”和“实体关系（竞争对手）”。
- 财务数据：`("宁德时代", "毛利率", "28.5%", "2023-09-30")`
- 投资动作：`("宁德时代", "投资", "固态电池", "2023-10-15")`
- 宏观事件：`("美联储", "宣布", "降息", "2024-09-01")`
**颠覆点**：一个极简的 O(1) 倒排索引数据结构，就能容纳金融市场的全部动态，一招秒杀图数据库和时序数据库的复杂拼接。

### 2. 100% Schema-less 的通用 LLM 抽取器
通过标准的 OpenAI 兼容协议（支持 Minimax 等自定义模型），系统**不预定义任何字段名或实体类型**。
大模型阅读非结构化文本后，自由“发明”并提取出最能概括商业逻辑的 Predicate（谓语）。
**颠覆点**：如果明天出了一个新概念叫“低空经济市占率”，系统连一行代码都不用改，图谱里就会自动长出这条线。

### 3. “睡眠与做梦”机制 (Cognitive Consolidation)
由于给了 LLM 绝对的自由，图谱里必然会充满同义词噪音（如“CATL”与“宁王”、“毛利”与“毛利率”）。
**颠覆点**：Chronos 引入了类人脑的睡眠整理机制。在系统闲时，后台会唤醒大模型或本地聚类算法，自动将同义词进行本体归一化合并，实现**图谱的自我生长与纠错 (Self-Evolving Ontology)**。

### 4. 零幻觉与可溯源 (Zero-Hallucination)
每一个四维数据点都强制挂载 `SourceEvidence`，包含来源 ID 和原始文本切片。大模型在推理时，随时可以精确回溯到当年的原始研报语句。

---

## 🛠️ Installation & Quick Start

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

直接体验记忆注入、噪音查询失败、系统睡眠自愈、再次精准查询的惊艳过程。

```bash
# In Python
python src/chronos/mcp.py
```

### 3. 使用真实的 LLM (以 Minimax 为例)

编辑并运行 `examples/demo_minimax.py`，向大模型投喂真实的非结构化新闻/研报文本。

```bash
export MINIMAX_API_KEY="your_api_key"
export MINIMAX_BASE_URL="https://api.minimax.chat/v1"
export MINIMAX_MODEL="abab6.5-chat"

python examples/demo_minimax.py
```

---

## 📁 极简代码结构 (Minimalist Architecture)

整个系统不到 300 行核心逻辑，被浓缩为四个文件：

```text
src/chronos/
├── graph.py   # 万能 4D 记忆引擎核心，取代传统图数据库。纯 Python 字典实现的超高并发倒排索引。
├── llm.py     # 基于 OpenAI 兼容协议的通用提取管道。把文本转化为 S-P-O-T。
├── sleep.py   # 睡眠与记忆整理机制（自进化本体）。
├── mcp.py     # 极简 MCP 网关。暴露万能的 `query_graph` 接口。
```

---

## 🔮 Roadmap: 生产环境部署

在 MVP 阶段，Chronos 使用纯 Python 内存数据结构，速度极快。当需要处理千万级数据时，**无需修改任何顶层逻辑**，只需在 `graph.py` 层进行存储替换：

- **All-in-One 经典底座**：迁移至 **PostgreSQL**。
  - 使用 `TimescaleDB` 插件存储时序。
  - 使用 `pgvector` 存储 `SourceEvidence` 的文本嵌入。
- **流式抽取集群**：在 `llm.py` 之前接入 `Redpanda/Kafka`，将全网抓取的研报和新闻源源不断地转化为时序事件流。

## License

MIT License
