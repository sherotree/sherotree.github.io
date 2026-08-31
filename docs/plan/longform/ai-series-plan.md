# AI 系列文章 · 总规划

> ✅ **本期 P0 长文主线 B**（见 [`00-longform-shortform-focus.md`](../00-longform-shortform-focus.md)）  
> **本期只做**：Phase 1 + Phase 2（25 篇）。Phase 3–6 → P2 暂缓。  
> **短内容配对**：术语钩子（S4，原料 `ai-terms-explained.md`）+ 长文拆条（S3）。  
> 面试向压缩见：[`agent-interview-series-plan.md`](./agent-interview-series-plan.md)。
>
> 起点：`ai-terms-explained.md`（30 术语地图，已完成）  
> 定位：混合受众（技术+非技术），代码可折叠/可跳过  
> 风格锚点：生活类比开头 → 原理配图（手绘图 / 示意图）→ 可跑代码或选型建议，2000-3500 字/篇  
> 发布平台：个人博客（主） · dev.to（英文） · 公众号 · 知乎
> 规模：6 阶段 × 约 80 篇（本期认 25 篇）

---

## 总体架构

```
Phase 0  地图        1 篇  ← 已完成（30 术语）
Phase 1  基础层     15 篇  概念 10 + 实战 5
Phase 2  交互层     10 篇  概念 6 + 实战 4
Phase 3  能力扩展   18 篇  概念 10 + 实战 8
Phase 4  系统层     15 篇  概念 8 + 实战 7
Phase 5  生产化     10 篇  概念 5 + 实战 5
Phase 6  综合项目   11 篇  纯实战，端到端
                    ────
                    80 篇
```

每阶段独立成册，读者可从任意阶段切入，也可从头顺读。

---

## Phase 1 · 基础层（15 篇）

把黑盒拆开，让读者看到齿轮。

| 序   | 类型 | 主题                                                        |
| ---- | ---- | ----------------------------------------------------------- |
| 1.1  | 概念 | Transformer 全景：一张图看懂 attention/FFN/残差             |
| 1.2  | 概念 | Self-Attention 手算演示（Q/K/V 到底在算什么）               |
| 1.3  | 概念 | Positional Encoding：模型怎么知道谁在前谁在后               |
| 1.4  | 概念 | Tokenizer 的世界：BPE / WordPiece / SentencePiece           |
| 1.5  | 实战 | 用 tiktoken 分析你的 Prompt 有多贵                          |
| 1.6  | 概念 | Embedding 空间可视化：cosine 相似度是什么                   |
| 1.7  | 实战 | 100 行 Python：把「我的博客」变成向量库                     |
| 1.8  | 概念 | Sampling 全解：Temperature / Top-p / Top-k / Beam Search    |
| 1.9  | 概念 | KV Cache：LLM 为什么越聊越贵                                |
| 1.10 | 概念 | Quantization：INT8 / INT4 / GGUF 的取舍                     |
| 1.11 | 实战 | Ollama + llama.cpp：MacBook 上跑 Llama 3                    |
| 1.12 | 概念 | Distillation & Speculative Decoding：小模型如何抄大模型作业 |
| 1.13 | 概念 | MoE 架构：DeepSeek / Mixtral 凭什么便宜                     |
| 1.14 | 实战 | 从零训练一个字符级 LLM（nanoGPT 复刻）                      |
| 1.15 | 概念 | 训练 vs 推理：GPU 到底在忙什么                              |

## Phase 2 · 交互层（10 篇）

学会跟模型对话。

| 序   | 类型 | 主题                                                |
| ---- | ---- | --------------------------------------------------- |
| 2.1  | 概念 | Prompt 的六个成分：角色/任务/示例/约束/格式/自检    |
| 2.2  | 概念 | Few-shot 的正确姿势（顺序、多样性、错误示范）       |
| 2.3  | 概念 | CoT / ToT / Self-Consistency：让模型「想清楚」      |
| 2.4  | 概念 | System Prompt 设计：Anthropic / OpenAI 官方套路拆解 |
| 2.5  | 实战 | 结构化输出：JSON Schema / Structured Output 用法    |
| 2.6  | 实战 | 写一个 Prompt Playground（对比 4 家模型）           |
| 2.7  | 概念 | Prompt Chaining：任务拆分的艺术                     |
| 2.8  | 概念 | ReAct 模式：Thought → Action → Observation 循环     |
| 2.9  | 实战 | 100 行代码复刻 ReAct Agent                          |
| 2.10 | 概念 | Prompt 的可测量性：怎么给一段 Prompt 打分           |

## Phase 3 · 能力扩展（18 篇）

让模型跳出「只能聊天」。

| 序   | 类型 | 主题                                                    |
| ---- | ---- | ------------------------------------------------------- |
| 3.1  | 概念 | RAG 完整流程图（Ingest / Retrieve / Rerank / Generate） |
| 3.2  | 概念 | Chunking 策略大全：固定窗口 / 递归 / 语义 / 命题        |
| 3.3  | 实战 | 用 LanceDB 从零搭 RAG（读你的 Obsidian）                |
| 3.4  | 概念 | 混合检索：BM25 + Dense + Rerank                         |
| 3.5  | 概念 | RAG 评测：Ragas / TruLens / 自建 eval 集                |
| 3.6  | 实战 | 给博客加语义搜索（Vercel + pgvector）                   |
| 3.7  | 概念 | GraphRAG：从检索段落到检索关系                          |
| 3.8  | 概念 | 微调家族：SFT / LoRA / QLoRA / DPO                      |
| 3.9  | 实战 | 用 Unsloth 微调 Llama 3 的客服口吻                      |
| 3.10 | 概念 | Tool Calling 内部机制：schema、路由、错误处理           |
| 3.11 | 实战 | 给 LLM 一个 Playwright，让它自己开浏览器                |
| 3.12 | 概念 | Streaming SSE 详解：TTFT / TPS / 中断处理               |
| 3.13 | 实战 | Next.js + Vercel AI SDK 做一个流式 ChatBot              |
| 3.14 | 概念 | 长上下文的代价：Lost in the Middle / Context Rot        |
| 3.15 | 概念 | Context Engineering：不是 Prompt Engineering            |
| 3.16 | 实战 | 100 万 Token 上下文能干什么（Gemini 实测）              |
| 3.17 | 概念 | Prompt Caching：Anthropic / OpenAI 缓存机制             |
| 3.18 | 实战 | 缓存策略实测：账单能降 80%                              |

## Phase 4 · 系统层（15 篇）

多组件协作。

| 序   | 类型 | 主题                                                  |
| ---- | ---- | ----------------------------------------------------- |
| 4.1  | 概念 | Agent 架构谱系：ReAct / Plan-Execute / Reflexion      |
| 4.2  | 概念 | Multi-Agent：CrewAI / AutoGen / LangGraph 对比        |
| 4.3  | 实战 | 用 LangGraph 搭一个「有记忆的研究员」                 |
| 4.4  | 概念 | Agent Memory：Short / Long / Episodic                 |
| 4.5  | 概念 | Workflow vs Agent：什么时候不用 Agent                 |
| 4.6  | 实战 | Temporal + LLM：可回放的 AI 工作流                    |
| 4.7  | 概念 | MCP 协议深挖：Tools / Resources / Prompts             |
| 4.8  | 实战 | 写一个 MCP Server：暴露你的知识库                     |
| 4.9  | 实战 | Chrome DevTools MCP 实战：让 AI 帮你查 bug            |
| 4.10 | 概念 | 向量数据库选型：Pinecone / Qdrant / Milvus / pgvector |
| 4.11 | 实战 | pgvector 优化：HNSW 参数怎么调                        |
| 4.12 | 概念 | RLHF / DPO / RLAIF：模型「懂事」是怎么练出来的        |
| 4.13 | 概念 | Multimodal 三种流派：Fusion / Late / Native           |
| 4.14 | 实战 | GPT-4V / Claude Vision 做 UI 自动化测试               |
| 4.15 | 概念 | Code Interpreter / Sandbox 是怎么隔离的               |

## Phase 5 · 生产化（10 篇）

从 demo 到线上。

| 序   | 类型 | 主题                                                 |
| ---- | ---- | ---------------------------------------------------- |
| 5.1  | 概念 | 延迟解剖：TTFT / TPS / 网络 / Cold Start             |
| 5.2  | 实战 | LLM 网关：Portkey / LiteLLM 实战                     |
| 5.3  | 概念 | 成本模型：Token 定价 / 缓存 / 路由 / 降级            |
| 5.4  | 实战 | 用便宜模型兜底 + 贵模型 fallback                     |
| 5.5  | 概念 | 可观测性：LangSmith / Langfuse / OpenLLMetry         |
| 5.6  | 概念 | 幻觉治理三板斧：Grounding / Citations / Verification |
| 5.7  | 概念 | Prompt Injection 攻防实战案例                        |
| 5.8  | 实战 | 用 Guardrails / NeMo Guardrails 加护栏               |
| 5.9  | 概念 | Eval 体系：从 Vibes 到指标                           |
| 5.10 | 实战 | 用 Braintrust 建一套回归测试集                       |

## Phase 6 · 综合项目（11 篇）

每篇一个端到端应用。

| 序   | 主题                                                 |
| ---- | ---------------------------------------------------- |
| 6.1  | 「读我全部笔记的第二大脑」（本地 RAG + MCP）         |
| 6.2  | 「自动整理周报的 Agent」（Slack + Notion）           |
| 6.3  | 「AI 竞品调研员」（浏览器 Agent + 结构化输出）       |
| 6.4  | 「自动写 PR review 的 bot」（GitHub App）            |
| 6.5  | 「像 Perplexity 的搜索问答」（搜索 + Rerank + 引用） |
| 6.6  | 「Cursor 补全的最小复刻」                            |
| 6.7  | 「语音助手」（Whisper + LLM + TTS 全链路）           |
| 6.8  | 「PDF 论文对话」（多模态 + 章节感知）                |
| 6.9  | 「自动生成小红书图文」（Prompt + 图片生成）          |
| 6.10 | 「AI 面试官」（长对话 + 评分 + 反馈）                |
| 6.11 | 「多 Agent 辩论产出报告」                            |

---

## 平台适配策略

| 平台           | 处理方式                                     |
| -------------- | -------------------------------------------- |
| 个人博客       | 主发布地，全文 + 可折叠代码块（`<details>`） |
| dev.to（英文） | 翻译版，代码块保留，标题偏 SEO               |
| 公众号         | 精简版，删代码留结论，加封面                 |
| 知乎           | 完整版，尾部加互动问题                       |

---

## 推进节奏

- **前 2 周**：先补 3 篇基础层（1.1 Transformer / 1.6 Embedding / 1.8 Sampling）+ 1 篇实战（1.7 博客向量化），检验风格和数据反馈
- **月度盘点**：每月末做一篇「阶段回顾 + 下月预告」，帮读者串起来
- **每 10 篇**：整合成一份 PDF / EPUB，作为订阅 / 获客钩子
- **每篇产出物**：正文 md + 手绘图 / 示意图 + 可跑代码仓库（如涉及）

---

## 进度追踪

| Phase        | 计划   | 已完成 | 进度      |
| ------------ | ------ | ------ | --------- |
| 0 · 地图     | 1      | 1      | ✅        |
| 1 · 基础层   | 15     | 0      | ⬜        |
| 2 · 交互层   | 10     | 0      | ⬜        |
| 3 · 能力扩展 | 18     | 0      | ⬜        |
| 4 · 系统层   | 15     | 0      | ⬜        |
| 5 · 生产化   | 10     | 0      | ⬜        |
| 6 · 综合项目 | 11     | 0      | ⬜        |
| **合计**     | **80** | **1**  | **1.25%** |

---

## 下一步待办

- [ ] 确定文章命名 / 目录结构约定（如 `202609/ai-series/phase1-01-transformer/`）
- [ ] Phase 1 前 3 篇详细大纲（三级标题 + 类比选材 + 代码范围）
- [ ] 系列封面图 / 统一视觉规范
- [ ] 建立术语表 / 引用规范（跨篇章互链）
