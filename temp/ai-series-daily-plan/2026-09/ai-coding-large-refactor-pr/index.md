---
title: AI 编程效率⑤：大重构——怎么拆 PR 给 Agent
date: 2026-09-11
description: 专栏「AI 编程效率」第五篇：大重构如何拆 PR，让 Agent 改动可控可 review。
tags: [AI, 编辑器, 效率, 系列]
series: ai-coding-workflow
draft: true
---

大重构最怕一件事：Agent 一次改三十个文件，PR 三千行，人看不完、CI 红一片、回滚 impossible。

这和 Agent 工程里分批 Grounding 一样——**一次只给一块可验证的改动面**，而不是把整本手册塞进一轮生成。你设计阶梯，Agent 填每一级；每一级都有测试绿、diff 可读、可单独 revert。

Agent 很擅长「同时改很多处」，但不擅长「同时保证很多处都对」。人类 reviewer 的认知上限也在那里：一次看五百行可能，一次看三千行就只能扫格式。拆 PR 既是给 Agent 划边界，也是给团队留可审计性。

下面是我拆 PR 给 Agent 的做法。

![一个大 PR vs 拆分小 PR 对比](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/refactor-big-pr_5bnelIwZY.png)

## 一、为什么要拆

（1）**Review 可完成**：人能在 20 分钟内判断对错。  
（2）**CI 可定位**：哪一步红就停在哪一步。  
（3）**Agent 可复述**：每步任务短，模型 less likely 漏 import。  
（4）**可回滚**：生产出问题只 revert 一层。  
（5）**并行友好**：小 PR 更容易被同事接力。

经验值：单 PR **≤ 400 行有效 diff**，或 **≤ 8 个文件**（生成物、lockfile 另计）。

## 二、典型拆法：堆叠 PR

![堆叠小 PR 工作流](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/refactor-stacked-pr_NTpWoKKOl.png)

以「把 class 组件迁到 hooks」为例：

（1）**PR1 脚手架**：新 hook + 并行导出，行为不变，测试全绿。  
（2）**PR2 迁移调用方**：逐个页面替换，每页可单独 review。  
（3）**PR3 删旧 class**：纯删除，diff 清晰。  
（4）**PR4 清理类型**：收尾，不影响运行时。

以「统一错误码」为例：PR1 只加新 enum；PR2 改调用；PR3 删旧字符串——**行为每一步都可运行**。

## 三、给 Agent 的任务卡

我不说「重构整个 auth 模块」，而写：

```text
PR2 范围：仅 src/pages/login.tsx 与 src/pages/register.tsx。
目标：改用 useAuth hook（见 @src/hooks/useAuth.ts）。
禁止：改 API 层、改路由配置。
完成：列出改动文件，确认 npm test -- auth 通过。
```

上面代码中，**范围 + 禁止 + 验收** 构成 Grounding 边界；`@` hook 文件是证据。

每步只开一个 Agent thread，避免它「顺手」做 PR3 的事。

## 四、机械步骤优先自动化

适合 Agent 的往往是：

（1）重命名 + codemod  
（2）统一 import 路径  
（3）提取重复函数  
（4）按模板批量改测试

适合人先定的：

（1）模块边界  
（2）是否兼容旧 API  
（3）哪一步可以 breaking  
（4）feature flag 要不要挂

## 五、分支策略

（1）**stacked branches**：`feat/auth-hook` → `feat/auth-pages` → `feat/auth-delete-class`。  
（2）每 PR merge 后再开下一 PR，或 rebase 保持线性历史。  
（3）Agent 每次只 checkout **当前 PR 分支**，工作区干净再开始。  
（4）PR 描述写「依赖 #123 merge 后再 review」，减少误 merge。

## 六、验收与 Grounding

每步 merge 前，我要求 Agent 输出：

```text
- 改动文件列表
- 执行的测试命令与结果
- 已知未迁移清单（若有）
```

这和 Grounding 的「引用可核对」同构——reviewer 不用猜还有没有隐藏改动。

## 七、常见误区

（1）「反正最后都能跑」合并成一个 PR。  
（2）PR 里混功能与重构——review 无法判断回归来源。  
（3）不跑 CI 就堆下一步——错误指数放大。  
（4）让 Agent 同时改命名和业务逻辑——失败时无法二分。  
（5）跳过「行为不变」的中间 PR——直接大 bang 迁移。

## 八、Review 与沟通

每个小 PR 的 description 我会写三行：**本 PR 做什么、不做什么、如何验证**。Reviewer 不必读整个重构 epic，只看当前阶梯。若 Agent 生成 commit message，人仍要改到与 PR 范围一致，避免 message 写「完成全量迁移」而 diff 只有一页。

Epic 链接或 checklist 放在 Issue 里，PR 只勾一项。合并后更新 Issue，下一 PR 再开——这样 Grounding 边界在组织层面也清晰。

## 九、小结

大重构不是让 Agent 一次写完，而是**你设计阶梯，Agent 填每一级**。PR 越小，Grounding 越准，review 越像人能做的工作。宁可多 merge 几次，也不要一次 diff 看不完——回滚成本会教你这一点。

（完）
