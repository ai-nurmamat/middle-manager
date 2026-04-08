# Middle-Manager AI 项目实施计划 (Implementation Plan)

## 1. 总结 (Summary)
本计划旨在将 `Middle-Manager AI` 项目从架构设计图（Spec）落地为完整的开源代码实现。该系统是一个颠覆传统企业组织架构的**中央管理枢纽**，旨在彻底替代人类中层管理者。它能够接收 CEO 的顶层战略（如需求、行业情况、公司情况），并自动将其转化为具体任务直接派发给基层员工，同时集成请假、入职初筛、报告、汇报、秘书等办公工作。

为了满足“必须最先进”且“至少动用 100 个核心技能（Skills）”的要求，我们将采用当前业界最前沿的多智能体架构，并原生支持 MCP（Model Context Protocol）以实现技能的无限扩展。

## 2. 现状分析 (Current State Analysis)
- **已有资产**：已在 `.trae/specs/design-middle-management-ai-repo/` 目录下产出了高质量的架构蓝图、优缺点分析和 50+ 核心管理技能定义（需扩充至 100+）。
- **缺失内容**：暂无任何代码实现。需要从零开始搭建前后端项目、数据库、Agent 核心引擎以及复杂的技能调度系统。

## 3. 提出的架构与技术栈 (Proposed Architecture & Tech Stack)
基于确认，我们将采用以下最先进的技术栈：
- **前端 (高管端与基层端驾驶舱)**：`Next.js` (React 18+) + `Tailwind CSS` + `Shadcn UI` + `Tremor` (用于高管 ROI 数据大屏图表)。
- **后端与 Agent 核心引擎**：`Python 3.11+` + `FastAPI` (提供高性能 API) + `LangGraph` (构建复杂的、可控的多智能体 Swarm 协同流程)。
- **数据库与企业全量记忆库 (RAG)**：`PostgreSQL` + `pgvector` 扩展，实现关系型业务数据（任务、人员、绩效）与非结构化向量数据（文档、沟通记录）的一体化存储与检索。
- **动态技能与插件层**：原生集成 **MCP (Model Context Protocol)**，将 100+ 个管理技能（如自动化排期、离职预警、薪酬模拟等）封装为标准的 MCP Tools，支持即插即用和跨语言扩展。

## 4. 实施步骤 (Implementation Steps)

### 第一阶段：项目初始化与基础设施搭建 (Project Initialization)
1. 创建 Monorepo 目录结构，包含 `backend/` (Python) 和 `frontend/` (Next.js)。
2. 配置 Docker Compose，一键拉取并运行带 `pgvector` 的 PostgreSQL 容器。
3. 初始化 FastAPI 后端项目，配置 SQLAlchemy ORM、Alembic 迁移工具以及 Pydantic schemas。
4. 初始化 Next.js 前端项目，配置基础路由（`/ceo-dashboard`, `/employee-dashboard`）。

### 第二阶段：数据库建模与企业记忆库 (Database & RAG Layer)
1. 设计核心表结构：
   - `User` (CEO, 员工角色定义)。
   - `StrategicObjective` (高管下达的战略/OKR)。
   - `Task` (拆解后的具体任务及状态)。
   - `PerformanceLog` (员工行为与绩效日志，用于客观打分)。
2. 实现 RAG 模块：配置 Embedding 模型（如 OpenAI `text-embedding-3-small` 或开源模型），提供向量存储与检索接口，让 Agent 能够“回忆”历史决策和公司上下文。

### 第三阶段：核心多智能体引擎开发 (Core Agent Engine via LangGraph)
1. **意图路由中心 (Router Agent)**：接收老板自然语言输入，识别意图（下发战略、询问进度、处理人事）并路由给对应的专家 Agent。
2. **构建多角色 Agent 矩阵**：
   - `TaskMaster Agent`：负责将战略拆解为 Task，评估工时，并派发给员工。
   - `QA & Tracker Agent`：负责监控员工进度，自动识别延期风险和虚假繁荣。
   - `HR BP Agent`：负责监控员工情绪（Burnout / Flight Risk）、自动打分、生成 PIP 及入职初筛。
   - `Secretary/Coordination Agent`：处理老板日常秘书工作、跨部门协调与会议安排。
3. 使用 LangGraph 将这些 Agent 编排为状态图（State Graph），确保复杂工作流（如“发现延期 -> 重新排期 -> 通知高管”）的确定性执行。

### 第四阶段：100+ 核心技能与 MCP 集成 (100+ Skills & MCP Engine)
1. 实现一个 MCP Client（Python端），使我们的 Agent 引擎能够动态连接外部的 MCP Servers。
2. 开发内置的 Python 技能工具库，覆盖以下核心维度，总计 100 个技能（部分作为函数级 Tool 实现）：
   - *战略与分发类 (20个)*：如 `decompose_okr`, `auto_assign_task`, `estimate_velocity` 等。
   - *进度与风控类 (20个)*：如 `detect_blocker`, `generate_auto_standup`, `alert_scope_creep` 等。
   - *人力与绩效类 (20个)*：如 `calculate_objective_score`, `generate_pip`, `predict_flight_risk`, `onboarding_screening` 等。
   - *办公与秘书类 (20个)*：如 `draft_company_announcement`, `schedule_meeting`, `summarize_industry_report` 等。
   - *外部系统对接与扩展类 (20个)*：模拟或对接 GitHub、Jira、Slack 等 API。
3. 封装“技能自动安装”逻辑：当 Agent 需要的 Tool 不在本地时，模拟从云端插件市场检索并加载的机制。

### 第五阶段：前端高管驾驶舱与基层终端开发 (Frontend Dashboards)
1. **高管端 (Top Management Dashboard)**：
   - 战略下达对话框（支持文字、语音模拟）。
   - 全局 ROI、进度燃尽图、团队健康度（情绪指标）可视化面板。
2. **基层端 (Grassroots/IC Dashboard)**：
   - 今日最高优先级任务流（Task Feed）。
   - 与 AI 中层（Support Bot）的 24/7 交互窗口，处理请假、寻求技术/业务支持、跨部门资源申请。

### 第六阶段：全链路联调与验收 (End-to-End Integration)
1. 跑通主干流程：CEO 登录 -> 输入一句话战略 -> 系统拆解 -> 任务自动分配至员工列表 -> 员工完成任务 -> 系统自动汇总客观进度汇报给 CEO。
2. 跑通 HR 流程：员工发起请假 -> HR BP Agent 自动评估项目进度风险 -> 秒级审批 -> 重新排期并通知团队。

## 5. 假设与决策 (Assumptions & Decisions)
- **大模型 API**：默认项目运行需配置一个强大的 LLM API（如 OpenAI GPT-4o 或 Anthropic Claude 3.5 Sonnet），以支撑复杂的 LangGraph 推理和大量 Tool 的调用。
- **外部系统集成**：由于当前是 MVP 阶段，与真实企业微信、Slack、Jira 等外部系统的对接将使用 Mock 数据或抽象接口层替代，重点展示 AI 的核心决策与调度能力。
- **MCP 架构**：采用 MCP 是为了未来的可扩展性，项目初期，大部分 100 个技能将直接作为 Python Native Tools 提供给大模型，少部分演示通过本地进程 MCP Server 动态加载。

## 6. 验证步骤 (Verification)
1. 后端服务启动正常，数据库（含 pgvector）连接成功。
2. 前端可正常访问两个核心 Dashboard。
3. 在 CEO 界面输入“公司下个月要上线出海电商业务”，能成功看到 Agent 拆解任务、分配角色并在后台调用至少 3-5 个不同技能（如查阅行业报告、建立排期表、分配人力）。
4. 员工界面的任务状态变更，能实时反馈到高管大屏，实现无人工干预的信息透明。