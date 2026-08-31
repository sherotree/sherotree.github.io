# 技术深度型系列 · 总规划

> ⏸ **本期 P2 暂缓**（见 [`00-longform-shortform-focus.md`](../00-longform-shortform-focus.md)）。个人项目强依赖 MCP / Claude Code / Agent 时再开。  
> 面试话术向内容见姊妹：[`agent-interview-series-plan.md`](./agent-interview-series-plan.md)。
>
> 姊妹系列：`ai-series-plan.md` · `vibecoding-series-plan.md` · `agent-interview-series-plan.md`
>
> 本系列定位：**已经会用 AI 编码的开发者**，深挖三个 2026 年最热的技术主题  
> 核心承诺：每一篇都能直接用到你今天的项目里  
> 风格锚点：真实项目截图 + 架构图 + 可复制配置 + 踩坑复盘，2500-4000 字/篇  
> 发布平台：个人博客（主） · dev.to（英文） · 掘金 · 知乎
> 规模：3 个子系列共 45 篇

---

## 读者画像

| 项     | 内容                                                         |
| ------ | ------------------------------------------------------------ |
| 是谁   | 会写代码、每天用 AI 辅助开发的工程师 / 技术 Leader           |
| 已经会 | Cursor / Claude Code 基础、能读 API 文档、跑得起 Node/Python |
| 想要   | 把 AI 从「加速器」变成「基础设施」，用到生产环境             |
| 不想看 | 快捷键教程 / hello world / 抖音式「10 秒学会」               |

---

## 三条子线

```
子系列 1  MCP 生态深挖             15 篇
子系列 2  Claude Code 深度工作流   15 篇
子系列 3  AI Agent 生产化          15 篇
                                 ────
                                 45 篇
```

三条线独立成册，也可以串起来读（MCP 是 Agent 的工具层，Claude Code 是 Agent 的编辑器形态）。

---

## 子系列 1 · MCP 生态深挖（15 篇）

_从"这是什么"到"我的团队离不开"_

| 序   | 类型 | 主题                                                 |
| ---- | ---- | ---------------------------------------------------- |
| 1.1  | 概念 | MCP 到底解决什么问题：LSP 之于编辑器 = MCP 之于 AI   |
| 1.2  | 概念 | MCP 协议全解：Tools / Resources / Prompts / Sampling |
| 1.3  | 实战 | 第一次接一个 MCP Server（Cursor + filesystem）       |
| 1.4  | 实战 | Chrome DevTools MCP：让 AI 帮你查前端 bug            |
| 1.5  | 实战 | Playwright MCP：让 AI 开浏览器做 E2E                 |
| 1.6  | 实战 | GitHub / GitLab MCP：让 AI 管你的仓库                |
| 1.7  | 实战 | 数据库 MCP（Postgres / SQLite）：让 AI 查 SQL        |
| 1.8  | 实战 | Slack / Notion / Linear MCP：办公流自动化            |
| 1.9  | 实战 | 从 0 写一个 MCP Server（TypeScript SDK）             |
| 1.10 | 概念 | MCP Server 的 Resource / Prompt / Sampling 深挖      |
| 1.11 | 概念 | MCP 鉴权与安全：Token / Scope / 沙箱                 |
| 1.12 | 实战 | 部署 MCP Server：本地 vs 远程（HTTP / SSE）          |
| 1.13 | 概念 | MCP Server 排行榜：10 个我天天用的                   |
| 1.14 | 概念 | MCP 生态地图：客户端 / 服务端 / 注册中心             |
| 1.15 | 概念 | MCP 的未来：会不会成为 AI 的 HTTP                    |

## 子系列 2 · Claude Code 深度工作流（15 篇）

_不是快捷键，是把整个项目变成 AI-native_

| 序   | 类型 | 主题                                                |
| ---- | ---- | --------------------------------------------------- |
| 2.1  | 概念 | Claude Code vs Cursor vs Codex CLI：怎么选          |
| 2.2  | 实战 | Claude Code 第一天：命令 / 快捷键 / 会话结构        |
| 2.3  | 概念 | CLAUDE.md 全解：给 AI 的项目说明书                  |
| 2.4  | 概念 | Subagent 是什么，什么时候用哪种类型                 |
| 2.5  | 实战 | Custom Slash Command：把你的工作流沉淀下来          |
| 2.6  | 实战 | Hooks 全场景：pre-commit / on-error / on-success    |
| 2.7  | 实战 | Skills 系统：可复用的技能包怎么组织                 |
| 2.8  | 概念 | Plan Mode / Build Mode：什么时候切换                |
| 2.9  | 实战 | 用 Claude Code 做完整的 PR review                   |
| 2.10 | 实战 | 用 Claude Code 处理长期项目：session / context 管理 |
| 2.11 | 实战 | 用 Claude Code 从需求到 PR 提交（含 issue triage）  |
| 2.12 | 实战 | 处理遗留代码：让 Claude Code 读得懂 10 年老仓库     |
| 2.13 | 实战 | 调试神技：把报错、日志、栈交给 Claude Code          |
| 2.14 | 实战 | Claude Code + MCP：我最常用的 5 个 Server 组合      |
| 2.15 | 概念 | 我的 CLAUDE.md 模板全公开（含个人风格约束）         |

## 子系列 3 · AI Agent 生产化（15 篇）

_为什么大部分 Agent Demo 上不了生产_

| 序   | 类型 | 主题                                                           |
| ---- | ---- | -------------------------------------------------------------- |
| 3.1  | 概念 | Agent Demo 到生产之间的 10 座大山                              |
| 3.2  | 概念 | Agent 架构谱系：ReAct / Plan-Execute / Reflexion / Multi-Agent |
| 3.3  | 概念 | Agent Memory：Short / Long / Episodic / Working                |
| 3.4  | 实战 | 错误处理三件套：重试 / 回退 / 中断                             |
| 3.5  | 实战 | 可观测性：LangSmith / Langfuse / OpenTelemetry                 |
| 3.6  | 概念 | 成本控制：Token 预算 / 模型路由 / 缓存                         |
| 3.7  | 概念 | Agent 评测：怎么知道 Agent 是变好了还是变坏了                  |
| 3.8  | 概念 | Human-in-the-loop 的设计模式                                   |
| 3.9  | 概念 | 安全边界：沙箱 / 权限最小化 / Prompt Injection 防御            |
| 3.10 | 实战 | 部署架构：长任务 / 异步 / 队列 / 断点恢复                      |
| 3.11 | 概念 | Manus / Devin / OpenAI Operator 的架构猜想                     |
| 3.12 | 实战 | Browser Agent 从零到线上（Playwright + Rerank）                |
| 3.13 | 实战 | Coding Agent 从零到线上（AST + Diff + Test）                   |
| 3.14 | 实战 | Deep Research Agent 从零到线上（多轮检索 + 引用）              |
| 3.15 | 概念 | Agent 上线第一周踩过的所有坑（真实复盘）                       |

---

## 与其他系列的关系

| 系列                | 定位         | 引流方向                                |
| ------------------- | ------------ | --------------------------------------- |
| AI 系列（80 篇）    | 底层原理     | 本系列引流到 AI 系列做深度补课          |
| Vibecoding（39 篇） | 非程序员     | 本系列的 Claude Code 篇是他们进阶的入口 |
| **本系列（45 篇）** | 工程师工程化 | 三条子线互相引用                        |

---

## 平台适配策略

| 平台           | 处理方式                                 |
| -------------- | ---------------------------------------- |
| 个人博客       | 主发布地，全文 + 完整配置                |
| dev.to（英文） | MCP / Claude Code 篇优先翻译，海外热度高 |
| 掘金           | 完整版，配封面，参与征文                 |
| 知乎           | 完整版，尾部加互动                       |

---

## 推进节奏

- **前 2 周**：出 1.1（MCP 是什么）+ 2.1（Claude Code vs Cursor）+ 3.1（Agent 上生产的 10 座大山），一次性建立三条子线的门面
- **月度节奏**：每月出 5-6 篇（每子系列 2 篇）
- **每 5 篇**：整合成一份小册子（MCP 手册 / Claude Code 手册 / Agent 生产手册）
- **每篇产出物**：正文 md + 架构示意图 + 可跑代码仓 + 一份可复制的配置文件

---

## 进度追踪

| 子系列                     | 计划   | 已完成 | 进度   |
| -------------------------- | ------ | ------ | ------ |
| 1 · MCP 生态深挖           | 15     | 0      | ⬜     |
| 2 · Claude Code 深度工作流 | 15     | 0      | ⬜     |
| 3 · AI Agent 生产化        | 15     | 0      | ⬜     |
| **合计**                   | **45** | **0**  | **0%** |

---

## 下一步待办

- [ ] 定命名 / 目录约定（如 `202609/tech-depth/mcp-01-what-is/`）
- [ ] 建立三条子线的示例项目仓（demo repo）
- [ ] 1.1 / 2.1 / 3.1 详细大纲
- [ ] 统一的架构示意图风格模板
