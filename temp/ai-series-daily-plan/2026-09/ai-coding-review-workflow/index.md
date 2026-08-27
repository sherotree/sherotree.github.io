---
title: AI 编程效率⑨：Code Review——AI 初审 vs 人终审
date: 2026-09-25
description: 专栏「AI 编程效率」第九篇：AI 初审与人终审的分工边界。
tags: [AI, 编辑器, 效率, 系列]
series: ai-coding-workflow
draft: true
---

Code Review 用 AI，合适的位置是**初审**：扫格式、找明显 bug、对规范。终审仍要人——架构、安全、业务边界，模型没有你的 Grounding 责任链，也无法替你对用户承诺负责。

Agent 工程笔记⑨强调「引用可核对」；Review 也一样：**AI 列问题要带位置，人要能点开 diff 验**。下面是我的两阶段分工与 CI 嵌入方式。

![AI 初审与人终审流水线](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/review-ai-human_rTqONu2kD.png)

## 一、AI 初审做什么

（1）命名与风格是否符合 `AGENTS.md`  
（2）明显空指针、未 await、错误吞掉  
（3）测试有没有、断言是否空洞  
（4）diff 是否混入无关格式化  
（5）secrets、调试语句、`console.log`  
（6）新增依赖是否合理、有无已知 CVE（需结合工具，AI 仅提示）

我会贴 PR diff 或 `@` 改动文件，并约束输出：

```text
Review 此 diff。只报告 high/medium 问题。
每条格式：-[级别] 文件:行号 — 问题 — 建议
没有把握的问题标「需人工确认」，不要编造。
```

上面代码中，**文件:行号** 是可核对引用；「不要编造」对应 Grounding 拒猜。

## 二、人终审做什么

![AI 与人 Review 分工清单](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/review-checklist_G1ha_FqL9.png)

（1）**设计**：抽象层次对不对、是否该拆 PR（系列⑤）  
（2）**安全**：权限、注入、敏感数据路径  
（3）**业务**：边界条件是否符合产品定义  
（4）**运维**：迁移、回滚、监控要不要补  
（5）**AI 漏网**：并发、分布式、隐性兼容  
（6）**Grounding 类文档**：README / 注释是否与行为一致

人不必重复扫 typo——那是 AI 省下来的时间，应花在「错了会不会出事」上。

## 三、流程嵌入 CI

（1）PR 打开 → Bot 跑 lint/test（硬门禁）  
（2）可选：AI review 评论（软信号）  
（3）**至少一位人 approve** 才可 merge  
（4）AI 指出的 high，作者必须回复「已修 / 误报原因」

AI review 不应有 merge 权限；它只能评论，不能替代 green CI。

## 四、避免 AI review 误伤

（1）给 AI **`AGENTS.md` + 本次 PR 说明**，别只给 diff。  
（2）大 PR 先拆，否则 AI 也只扫表面。  
（3）把 AI 当**清单生成器**，不当法官——误报正常，人过滤。  
（4）对 generated 文件单独说明规则，避免 AI 纠结 lockfile 格式。

## 五、作者侧用法

提交前自检 prompt：

```text
你是 reviewer。对比 @AGENTS.md 与本次改动。
列出我会在 PR 上被问的 3 个问题。
```

先自己答这三问，PR 质量会明显上去。若 AI 初审与自检重叠，说明规则文件写得够清楚（系列③）。

## 六、常见误区

（1）AI 说 LGTM 就 merge——高置信幻觉仍存在。  
（2）只让人 review AI 已扫过的 typo——浪费人眼。  
（3）把安全审计完全交给 AI——必须配 SAST / 依赖扫描。  
（4）AI review 评论不回复——作者学不到，规则也不更新。

## 七、团队尺度

小团队可以 AI 初审 + 一人终审；核心路径（支付、鉴权）建议**两人终审**，AI 仅作清单。公开开源项目要在 CONTRIBUTING 里写清：AI 评论仅供参考，merge 权在人。

定期抽样：AI 指出的 high 有多少是真问题？误报高就收紧 prompt 或补规则文件，而不是关掉 AI review——通常是 Grounding 不够，不是工具不行。

## 八、小结

AI review = **可核对的第一遍扫雷**；人 review = **承担责任的终审**。分工清楚，才既不偷懒，也不迷信机器意见。每条 AI 意见都要能点到行号——否则就和未 Grounded 的生成一样不可验收。

（完）
