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

把 AI 放在 merge 按钮前面是危险的；放在**人眼之前、机器门禁之后**往往划算。lint 与单测是硬规则，AI 是软启发——它可能发现「这里 forgot await」，但不应决定「这个设计可接受」。团队需要写清这一层，避免有人用 AI LGTM 推责。

下面展开分工与流程。Review 是系列里少数「人必须兜底」的环节：Grounding 可以约束生成，但不能替代你对用户与生产的责任——AI 初审只是放大你的注意力，不是转移责任。

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

人不必重复扫 typo——那是 AI 省下来的时间，应花在「错了会不会出事」上。对安全敏感 PR，我会要求 `@` threat model 或内部 checklist，再让人对照 AI 输出——**人机各扫一层，交集才是高置信问题**。

## 三、流程嵌入 CI

（1）PR 打开 → Bot 跑 lint/test（硬门禁）  
（2）可选：AI review 评论（软信号）  
（3）**至少一位人 approve** 才可 merge  
（4）AI 指出的 high，作者必须回复「已修 / 误报原因」

AI review 不应有 merge 权限；它只能评论，不能替代 green CI。若团队用 Bot 账号发 review，要在 CONTRIBUTING 写明：Bot 意见不阻塞 merge，但 author 须回复 high 项——把 Bot 放进流程图，而不是放进权限模型。

## 四、避免 AI review 误伤

（1）给 AI **`AGENTS.md` + 本次 PR 说明**，别只给 diff。  
（2）大 PR 先拆，否则 AI 也只扫表面。  
（3）把 AI 当**清单生成器**，不当法官——误报正常，人过滤。  
（4）对 generated 文件单独说明规则，避免 AI 纠结 lockfile 格式。Bot 评论里若出现「建议大改架构」，默认降级为 low——架构属于人终审，不是 AI 初审该越界的地方；越界意见会稀释 high 信号的 Grounding 价值。

## 五、作者侧用法

提交前自检 prompt：

```text
你是 reviewer。对比 @AGENTS.md 与本次改动。
列出我会在 PR 上被问的 3 个问题。
```

先自己答这三问，PR 质量会明显上去。若 AI 初审与自检重叠，说明规则文件写得够清楚（系列③）；若 AI 仍漏掉 obvious bug，多半是 diff 太大或缺 `AGENTS.md`——回到系列第五篇拆 PR，而不是加长 review prompt。

## 六、常见误区

（1）AI 说 LGTM 就 merge——高置信幻觉仍存在。  
（2）只让人 review AI 已扫过的 typo——浪费人眼。  
（3）把安全审计完全交给 AI——必须配 SAST / 依赖扫描。  
（4）AI review 评论不回复——作者学不到，规则也不更新。

Reviewer 培训里可以加一条：**先扫 AI 标 high 的项，再按自己清单扫**。这样既利用 AI，又不被 low 噪声淹没。最终 merge 责任始终在 approve 的人身上，而不是 bot——Bot 没有 Grounding 责任链，只有评论权限。

## 七、团队尺度

小团队可以 AI 初审 + 一人终审；核心路径（支付、鉴权）建议**两人终审**，AI 仅作清单。公开开源项目要在 CONTRIBUTING 里写清：AI 评论仅供参考，merge 权在人。

定期抽样：AI 指出的 high 有多少是真问题？误报高就收紧 prompt 或补规则文件，而不是关掉 AI review——通常是 Grounding 不够，不是工具不行。把误报样例收进 `AGENTS.md` 的「不要报告」清单，下一轮初审会安静很多。

## 八、小结

AI review = **可核对的第一遍扫雷**；人 review = **承担责任的终审**。分工清楚，才既不偷懒，也不迷信机器意见。每条 AI 意见都要能点到行号——否则就和未 Grounded 的生成一样不可验收；merge 按钮永远绑在人手上。团队规模变大时，把 AI 初审当**培训材料**：新人先读 Bot 评论，再读 diff，比直接看三千行更容易入门。资深同学则把精力放在 Bot 标「需人工确认」的项上——那往往是业务 Grounding 才能判定的灰区。灰区项应进 PR 讨论串，而不是静默 merge——讨论串同样是可审计证据。

（完）
