---
title: Agent 工程笔记④：Agent 最小闭环——Plan → Act → Observe
date: 2026-09-02
description: 专栏「Agent 工程笔记」第四篇：用 Plan-Act-Observe 建立 Agent 最小闭环，说明每步输入输出与常见反模式。
tags: [AI, Agent, 系列]
series: agent-notes
draft: true
---

Plan → Act → Observe（计划 → 行动 → 观察）是 Agent 最小闭环：**先想清楚下一步，再调工具执行，最后读回结果决定要不要继续**。

很多 Agent 看起来像「一直聊天」，工程上却缺少稳定循环：模型要么一口气编完答案，要么工具报错后不知道改计划。把三步拆开，宿主才好记录状态、限步数、做重试。

下面是我整理的 Plan-Act-Observe 最小做法：每步输入输出、一轮循环长什么样、以及常见反模式。

![Plan-Act-Observe 循环示意](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/plan-act-loop_-ltLgWLzg.png)

## 一、先说一个具体麻烦

你让 Agent「查上周错误日志，汇总前三类问题，写进工单」。它直接回复一份看起来很专业的报告，附了三条「常见错误类型」。

你去对日志，发现两类是编的，一类把 INFO 当成了 ERROR。原来它**根本没调查询工具**，或者调了一次失败后继续「发挥」。

没有 Observe 环节，宿主无法判断「这一步算不算完成」；没有 Plan，模型会在一次生成里混掉「该查什么」和「该怎么写」。

更隐蔽的情况是：工具其实调用成功了，但返回空列表。若 Observe 只写「调用完成」而不写「命中 0 条」，Plan 下一轮仍可能当作「已经查过」而进入写报告阶段。

## 二、三步各自做什么

可以把它想成带工具的 REPL：每圈键盘输入是上下文，输出是工具调用或最终答复；**Observe 就是读 stdout**。

（1）**Plan（计划）**：根据用户目标与已有观察，产出「下一步意图」——调哪个工具、参数大概是什么、成功标准是什么。  
（2）**Act（行动）**：宿主执行工具调用（读文件、HTTP、跑命令等），把原始结果交给 Observe。  
（3）**Observe（观察）**：把工具返回整理成模型可读摘要（含成功/失败、关键字段），写回对话或状态机，再进入下一轮 Plan。

![Plan、Act、Observe 三步卡片](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/plan-act-steps_9PvfF2yW9V.png)

Plan 不必长篇大论；工程上更常见的是结构化「下一步」：`tool`、`args`、`done` 布尔值。

若任务本身需要多步，Plan 也可以只输出「当前步」而不是完整路线图——完整计划会在 Observe 后不断修订，比一次生成 ten-step plan 更贴实际情况。

## 三、一轮循环的最小数据结构

宿主侧建议显式保存 `step` 与 `observations`，而不是只靠聊天记录堆叠。

下面是一段伪代码骨架，展示三步如何串起来。

```python
state = {"goal": user_message, "observations": [], "step": 0}

while state["step"] < MAX_STEPS and not state.get("done"):
    plan = model.plan(state)          # Plan：返回 tool / args / rationale
    if plan["done"]:
        break
    raw = run_tool(plan["tool"], plan["args"])  # Act
    obs = normalize(raw)              # Observe：截断、标错误码
    state["observations"].append(obs)
    state["step"] += 1

answer = model.synthesize(state)
```

上面代码中，`normalize` 负责把几百 KB 日志压成可进上下文的摘要；`MAX_STEPS` 防止死循环。Plan 与最终 `synthesize` 可以同一模型，也可以分开以省 token。

## 四、Observe 写得好，Plan 才跟得上

Observe 不是把 JSON 原样贴回模型。至少应包含：

（1）**状态**：`ok` / `error` / `partial`  
（2）**与计划相关的字段**：例如查询命中的条数、文件是否存在  
（3）**失败可行动信息**：错误码、缺哪个参数，而不是一整段 stack trace

还可以加（4）**耗时与体积**：`duration_ms`、`truncated: true`，方便 UI 展示进度，也方便你发现某工具总返回巨型 payload。

工具失败时，Observe 应明确写「本步未达成计划中的成功标准」，让下一轮 Plan 选择改参数、换工具或向用户提问——而不是默认进入总结。

若同一错误重复出现两次，宿主可直接中断循环并向用户展示最后一次 Observe，比让模型第三次「再试一次同样的调用」更省 token，也更好排查。

## 五、什么时候可以省略显式 Plan

简单单工具任务（例如「把这段文字翻译成英文」）有时可以 Act 直连。但一旦涉及**多源信息、分支判断、或失败重试**，就应恢复显式 Plan。

判断 heuristic：若用户目标用一句话说不清「成功标准」，就别省 Plan。宿主日志里应能还原每一步的 rationale，方便对齐系列第三篇「工具失败三层」的排障路径。

## 六、常见反模式

（1）**只有 Act，没有 Plan**  
模型直接 function call，失败就重试同一调用，缺少「为什么要用这个工具」的记录。  
（2）**Observe 过长**  
把完整 API 响应塞进上下文，挤掉用户目标与历史观察。  
（3）**没有 done 条件**  
循环跑到 max steps 强行结束，用户看到半拉子答案。  
（4）**Plan 与最终回答混在一次生成里**  
难以插 Human-in-the-loop；见系列第十一篇。  
（5）**把 Observe 当成最终回复**  
用户需要的是结论与引用，不是原始工具 dump。

## 七、小结与系列导航

Plan-Act-Observe 的本质：**把「想、做、看」拆成可观测的三拍**，宿主才能在中间加权限、限步、重试与流式进度。工具描述写清楚，Plan 才选得对——见系列第五篇「工具描述怎么写」。先把闭环跑通，再叠子 Agent 与 RAG 不迟。

上一篇预告：工具失败三层——协议、参数、权限怎么排。  
下一篇预告：工具描述怎么写——模型才调得对。

（完）
