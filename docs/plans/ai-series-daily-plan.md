# AI 三系列日更选题计划

> 状态：已存档 · 2026-08-27  
> 关联：[content-plan-3months.md](./content-plan-3months.md)、[ai-dev-digest-weekly.md](./ai-dev-digest-weekly.md)  
> 节奏：**日更**（7 天/周）；三条 AI 系列各 **20 篇**（可调 10–30），合计约 **62 篇**（含已有母稿）  
> 文风：`ruanyifeng-tech-writing`  
> 配图：流程 / 架构 / 对比类统一 **牛皮纸手账风**（虚线卡片 + 淡彩）+ ImageKit CDN；见 skill 6.5，禁止 Mermaid 默认主题入稿  
> **硬约束**：与主计划一致——零软广；囤稿 `draft: true`；按周公开，勿一次性暴露全部存稿

---

## 一、总览：三条线怎么分工

| 系列 | `series` 值 | 读者记住你什么 | 与现有内容关系 |
|------|-------------|----------------|----------------|
| **① Agent 工程笔记** | `agent-notes`（沿用） | 能搭、能排、能上线 Agent | 已有 ①②③，直接续写 |
| **② 理解 AI** | `understanding-ai`（新增） | 大模型名词讲得清楚 | 已有 7+ 篇可 retro-tag |
| **③ AI 编程效率** | `ai-coding-workflow`（新增） | 日常用 AI 写代码不翻车 | 已有 Cursor 入门 1 篇 |

**刻意错开：**

- ② 讲「是什么、为什么」（搜索长尾）
- ③ 讲「我今天怎么用」（完读、关注）
- ① 讲「怎么做成系统」（垂直、回访）

**热点快评**（`ai-hot-take-weekly` 等）**不算系列正文**，每周最多 1 篇机动，不占下面 60 篇名额。

**与图片转化系列的关系：** `src/content/blog/csdn/2026-09/` 下图片转化稿走搜索工具意图；本计划三线走原理与工程，标题不混「在线转换」。

---

## 二、系列一：Agent 工程笔记（20 篇）

**定位：** 从 demo 到可维护的 Agent 系统——工具、上下文、评测、上线。

**`series: agent-notes`**

### 已有（可 retro-tag）

| # | slug（参考） | 标题 |
|---|--------------|------|
| 1 | `agent-tool-failure-three-layers` | Agent 工程笔记①：工具调用失败时，先查哪三层 |
| 2 | `context-too-long-cut-keep` | Agent 工程笔记②：上下文太长——砍什么、留什么 |
| 3 | `why-eval-sets` | Agent 工程笔记③：为什么要有评测集（比单次演示重要） |

### 待写（17 篇）

| # | 标题方向 | 类型 | slug 建议 |
|---|----------|------|-----------|
| 4 | Agent 最小闭环：Plan → Act → Observe | 架构 | `agent-plan-act-observe` |
| 5 | 工具描述怎么写，模型才调得对 | 实践 | `tool-schema-for-agents` |
| 6 | 多步任务：什么时候拆子 Agent | 架构 | `when-to-split-sub-agents` |
| 7 | 记忆分层：会话内 vs 长期存储 | 概念+实践 | `agent-memory-layers` |
| 8 | RAG 入门：检索什么、怎么切块 | 实践 | `rag-chunking-basics` |
| 9 | Grounding：怎么让回答贴文档 | 实践 | `agent-grounding-docs` |
| 10 | 权限与沙箱：工具能碰什么边界 | 安全 | `agent-tool-permissions` |
| 11 | 人机协同：哪些步骤必须人工确认 | 流程 | `human-in-the-loop-agent` |
| 12 | 流式 UI：用户怎么感知 Agent 在工作 | 前端 | `agent-streaming-ui` |
| 13 | 重试与幂等：工具失败怎么恢复 | 工程 | `agent-retry-idempotency` |
| 14 | 成本治理：token、调用次数、模型路由 | 工程 | `agent-cost-governance` |
| 15 | 可观测性：出问题时看哪几层日志 | 工程 | `agent-observability-layers` |
| 16 | 评测集怎么写：从 happy path 到 edge case | 实践 | `eval-set-writing-guide` |
| 17 | 模型升级后的回归测试 | 实践 | `agent-regression-after-upgrade` |
| 18 | MCP Server 最小实现思路 | 教程 | `mcp-server-minimal` |
| 19 | 多 Agent：分工，不是聊天室 | 架构 | `multi-agent-division-not-chat` |
| 20 | 上线清单：从 demo 到可维护服务 | 清单 | `agent-production-checklist` |

**篇末互链：** 每篇文末链回系列索引 + 上下篇，强化回访。

---

## 三、系列二：理解 AI（22 篇）

**定位：** 「理解 X」AI 专版——CSDN / 博客园搜索底盘，零软广，只讲公开原理与协议。

**`series: understanding-ai`**

### 已有（建议 retro-tag）

| # | slug（参考） | 标题 |
|---|--------------|------|
| 1 | `understanding-context-window` | 理解上下文窗口：token 到底在限制什么 |
| 2 | `understanding-moe` | 理解 MoE：总参数很大，为何还能跑 |
| 3 | `understanding-thinking-mode` | 理解「思考模式」：什么时候该开 |
| 4 | `understanding-mcp` | 理解 MCP：模型如何接上外部工具 |
| 5 | `understanding-sse-streaming` | 理解流式输出：SSE 在聊天里干什么 |
| 6 | `sparse-attention-dsa-plain` | 稀疏注意力 / DSA：用白话讲清在优化什么 |
| 7 | `structured-output-json-mode` | 结构化输出 / JSON Mode 入门 |

### 待写（15 篇）

| # | 标题方向 | 搜索意图 | slug 建议 |
|---|----------|----------|-----------|
| 8 | 理解 Transformer：Attention 在算什么 | 基础 | `understanding-transformer-attention` |
| 9 | 理解 Token：为什么中文更费 token | 基础 | `understanding-tokenization-zh` |
| 10 | 理解 Embedding：相似搜索在算什么 | RAG 前置 | `understanding-embeddings` |
| 11 | 理解 Temperature / Top-p | 调参 | `understanding-temperature-top-p` |
| 12 | 理解 Fine-tuning vs Prompt | 选型 | `understanding-finetune-vs-prompt` |
| 13 | 理解 RAG：检索增强在补什么 | 架构 | `understanding-rag` |
| 14 | 理解 KV Cache：推理为什么能加速 | 推理 | `understanding-kv-cache` |
| 15 | 理解 Quantization：INT4 损失的是什么 | 部署 | `understanding-quantization` |
| 16 | 理解 Prefill vs Decode | 延迟 | `understanding-prefill-decode` |
| 17 | 理解 Function Calling 与 MCP 的分工 | 工具 | `understanding-function-calling-vs-mcp` |
| 18 | 理解多模态：图像怎么进模型 | 多模态 | `understanding-multimodal-input` |
| 19 | 理解 RLHF / DPO：对齐在改什么 | 训练 | `understanding-rlhf-dpo` |
| 20 | 理解 Context Caching：重复前缀为何便宜 | 成本 | `understanding-context-caching` |
| 21 | 理解 Model Router：大小模型怎么分工 | 架构 | `understanding-model-router` |
| 22 | 理解 Agent vs Chatbot：差在哪一步 | 概念 | `understanding-agent-vs-chatbot` |

### 可选 capstone（数据好再加码）

| slug（参考） | 标题 | 说明 |
|--------------|------|------|
| `context-engineering-deep-dive` | 上下文工程加强版详解 | 已有，可作系列收束 |
| `local-open-source-models-five-questions` | 本地跑开源模型前要问的 5 个问题 | 已有 |
| `prompt-constraints-acceptance` | Prompt 里「约束 + 验收」 | 已有，偏实践，可作附录 |

---

## 四、系列三：AI 编程效率（20 篇）

**定位：** 开发者每天用 AI 写代码——编辑器、规则、隐私、团队协作；**不是**搭 Agent 系统（那是系列一）。

**`series: ai-coding-workflow`**

### 已有

| # | slug（参考） | 标题 |
|---|--------------|------|
| 1 | `cursor-tab-inline-agent` | Cursor 入门：Tab、行内编辑与 Agent 怎么选 |

### 待写（19 篇）

| # | 标题方向 | 场景 | slug 建议 |
|---|----------|------|-----------|
| 2 | 三种节奏：补全、行内编辑、Agent 何时切换 | 日常 | `ai-coding-three-rhythms` |
| 3 | 规则文件写什么：`.cursorrules` / `AGENTS.md` | 配置 | `ai-coding-rules-files` |
| 4 | IDE 里怎么省上下文：@ 引用策略 | 效率 | `ai-coding-context-at-refs` |
| 5 | 大重构：怎么拆 PR 给 Agent | 重构 | `ai-coding-large-refactor-pr` |
| 6 | 让 AI 写测试：验收比生成重要 | 质量 | `ai-coding-test-acceptance` |
| 7 | 读陌生代码库：AI 辅助 onboarding | 阅读 | `ai-coding-codebase-onboarding` |
| 8 | Debug：报错信息怎么贴才有效 | 排障 | `ai-coding-debug-paste-errors` |
| 9 | Code Review：AI 初审 vs 人终审 | 流程 | `ai-coding-review-workflow` |
| 10 | 文档与注释：什么时候让 AI 写 | 文档 | `ai-coding-when-to-doc` |
| 11 | 技术调研：用 AI 但不盲信 | 选型 | `ai-coding-research-without-trust` |
| 12 | 多文件改动：分支 / Worktree 策略 | 工程 | `ai-coding-multi-file-worktree` |
| 13 | 隐私边界：什么代码不能送云端 | 合规 | `ai-coding-privacy-boundary` |
| 14 | 本地模型 + 云端模型日常搭配 | 成本 | `ai-coding-local-cloud-mix` |
| 15 | Skills / MCP：扩展编辑器能力 | 扩展 | `ai-coding-skills-mcp` |
| 16 | 提示词模板：个人 vs 团队怎么沉淀 | 协作 | `ai-coding-prompt-templates` |
| 17 | 从 Chat 到脚本：什么时候自动化 | 进阶 | `ai-coding-chat-to-script` |
| 18 | AI 改坏生产的 5 种常见模式 | 反模式 | `ai-coding-production-failures` |
| 19 | 怎么度量：AI 到底省了多少时间 | 方法论 | `ai-coding-measure-productivity` |
| 20 | 结对编程心态：你是机长不是乘客 | 收束 | `ai-coding-pilot-not-passenger` |

---

## 五、日更排期

三条线共 **62 篇**（含已有）。日更若 **7 天全发 AI**，约 **9 周**跑完一轮；若每周还穿插图片转化 / 前端稿，周期拉到 **12–14 周**更稳。

### 推荐周模板（7 天）

```text
Mon  理解 AI（搜索向，周一利于 CSDN 收录）
Tue  AI 编程效率（实操向）
Wed  Agent 工程笔记（垂直深度）
Thu  理解 AI
Fri  AI 编程效率
Sat  Agent 工程笔记
Sun  机动：热点快评 / 系列复盘 / 休息囤稿
```

### 阶段建议（避免三条线同时浅）

| 阶段 | 周数 | 主攻 | 辅线 |
|------|------|------|------|
| Phase 1 | W1–4 | 理解 AI 补基础（8–10 篇） | 各系列各 1–2 篇开篇 |
| Phase 2 | W5–8 | Agent 工程笔记密集（8–10 篇） | 理解 AI 每周 1 篇 |
| Phase 3 | W9–12 | AI 编程效率密集（8–10 篇） | Agent 收尾 + 理解 AI 长尾 |

---

## 六、与现有计划的衔接

1. **母稿位置**：`src/content/blog/{platform}/{YYYY-MM}/{slug}/index.md`（一文一平台）；未发周保持 `draft: true`。
2. **`series` 枚举**：`agent-notes` · `understanding-ai` · `ai-coding-workflow`（另：`browser-graphics` 等非 AI 系列照旧）。
3. **六站分发**：
   - 理解 AI → CSDN / 博客园标题偏「理解 / 详解」
   - AI 编程效率 → 掘金 / 思否偏「实践 / 踩坑」
   - Agent 工程 → 全站统一系列名「Agent 工程笔记」
4. **导流纪律**：仍按 [content-plan-3months.md](./content-plan-3months.md) 分阶段执行。
5. **副线**：Twitter 中文精选周刊不占本表名额（见 [ai-dev-digest-weekly.md](./ai-dev-digest-weekly.md)）。

---

## 七、产能粗算

| 项 | 估算 |
|----|------|
| 单篇母稿（ruanyifeng 文风） | 1.5–2.5 h |
| 六站改编 + 发布 | 0.5–1 h |
| 日更 1 篇 | 约 2–3.5 h/天 |
| 62 篇 AI 系列 + 囤稿缓冲 | 建议一次写 2 周存量（14 篇 draft） |

若日更压力过大，可把 **周日改为「纯囤稿 / 只发快评」**，实际 AI 原创维持 **6 篇/周**，系列周期略拉长但质量更稳。

---

## 八、成功标准（跑完一轮后复盘）

| 指标 | 参考线 |
|------|--------|
| 稳定性 | ≥10/12 周日更达标（或 6 篇/周 AI + 1 机动） |
| 系列认知 | 读者能叫出至少 1 个系列名 |
| 搜索 | CSDN「理解 X」类出现稳定搜索进入 |
| 回访 | 系列互链带来单篇 → 系列索引跳转 |
| 纪律 | 计划内稿件 **0 篇**软广 |

---

## 九、执行清单

- [x] 已有母稿补 `series` frontmatter（`agent-notes` / `understanding-ai` / `ai-coding-workflow`）— 2026-08-27
- [x] 待写 51 篇骨架已生成（`draft: true`，排期自 2026-09-01 起按周模板轮转）— 2026-08-27；**暂存**于 `temp/ai-series-daily-plan/`，未进 `src/content/blog/{platform}/`
- [x] `2026-09/` 共 26 篇正文已写完（`ruanyifeng-tech-writing` + 手绘风配图 + ImageKit CDN）— 2026-08-28
- [ ] 主站增加系列索引页或系列 tag 聚合（可选，建站层）
- [ ] 每周末记录：哪条线阅读/搜索更好，调 Phase 2/3 比重

---

## 十、一句话结论

日更节奏下，用 **Agent 工程笔记**、**理解 AI**、**AI 编程效率** 三条互不重叠的 AI 系列各约 20 篇，按周一～六轮转、分三阶段推进；热点快评与图片转化线并行但不抢系列名额。
