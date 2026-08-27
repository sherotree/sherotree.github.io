---
title: AI 编程效率⑩：文档与注释——什么时候让 AI 写
date: 2026-09-29
description: 专栏「AI 编程效率」第十篇：哪些文档适合 AI 起草、哪些必须人写。
tags: [AI, 编辑器, 效率, 系列]
series: ai-coding-workflow
draft: true
---

文档和注释最容易「让 AI 一把写完」——也最容易**写完就过期**。代码还在动，AI 已把假细节写进 README，读者按文档操作失败，信任比没文档更差。

Grounding 要求回答贴证据；文档也要**贴稳定后的代码**。时机不对，AI 只是在放大幻觉。下面是我判断「何时让 AI 写文档」的规则与维护纪律。

![代码稳定 vs 仍在改动](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/doc-stable-moving_PLGrwXvPD.png)

## 一、先问：接口稳定了吗

（1）**函数签名、HTTP 路径、配置项**还会变？→ 别写长文，最多 TODO。  
（2）**PR 已 merge + 测试绿**？→ 可以起草。  
（3）**发布标签已打**？→ 必须更新 changelog。

移动靶上写文档，等于未 Grounded 的生成。若 sprint 内还要改 API，我只在 PR 描述里写临时说明，不进 README。

## 二、四类文档，四种时机

![何时写哪类文档](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/doc-when-write_GhRqlbxz7.png)

| 类型 | AI 适合 | 人必须把关 |
| --- | --- | --- |
| README 用法 | 命令、目录说明 | 对外承诺、许可 |
| 行内注释 | 非显然算法、坑 | 业务「为什么」 |
| ADR | 整理已有决策 | 决策本身 |
| API 文档 | 从类型/ OpenAPI 生成 | 语义与错误码 |

## 三、适合 AI 起草的注释

```typescript
/** 将用户时区转为 UTC 存储；无效时区抛 TZ_INVALID（见 validateTimezone） */
export function normalizeTimezone(tz: string): string
```

让 AI 写注释时，我会 `@` 函数 + 测试 + 相关 issue：

```text
只为 normalizeTimezone 写 JSDoc。
要求：说明抛错条件；不要重复类型里已 obvious 的信息；中文一句即可。
```

上面代码中，「不要 obvious」避免注释噪声；「见 validateTimezone」给出可跳转证据。

## 四、必须人写的部分

（1）**为什么不用另一种方案**——ADR 的 trade-off。  
（2）**合规、隐私、SLA**——法律与商业含义。  
（3）**on-call runbook**——以你真实踩坑为准。  
（4）**对外 API 保证**——版本与废弃策略。  
（5）**安全模型**——威胁与信任边界，AI 容易写 generic 套话。

AI 可整理格式、润色英文，人不能外包责任。

## 五、维护纪律

（1）改行为**同事改测试与文档**——PR checklist 一项。  
（2）定期让 AI **对比代码与 README**，输出 diff 建议，人逐条采纳。  
（3）长文档拆到 `docs/`，需要时再 `@`，别全塞进规则文件（系列③）。  
（4）删除比新增更重要——过期段落删掉，避免和 Grounding 证据冲突。

## 六、和 Review、Onboarding 的衔接

Review（系列⑨）时可查：行为变而文档未变 → 打回。Onboarding 笔记（系列⑦）应是**活文档**，代码改路径后同步更新，否则新人 `@` 旧笔记会被误导。

## 七、常见误区

（1）项目第一天就让 AI 写完整 README。  
（2）注释复述代码 `// increment i`。  
（3）ADR 写「我们考虑了多种方案」但没有记录为何否决。  
（4）把 AI 生成的 API 文档当对外 contract，未人工审 error code。

## 八、起草工作流

我常用的三步：

（1）`@` 稳定后的源码 + 测试，让 AI 出**草稿**；  
（2）人删幻觉、补 trade-off、改错误码表；  
（3）PR 里 **docs + code 同 merge**，避免文档 PR 永远 pending。

对外公告或版本说明，人写第一句「用户可见的变化」，AI 再扩写 bullet——方向不能反。

## 九、小结

AI 写文档的最佳时刻：**代码稳定、证据齐全**。注释解释「为什么这样」；README 解释「怎么用」；ADR 解释「为什么没选别的」。移动靶上别写——等 Grounding 的对象定了再动笔。文档也是证据层，过期文档和检索 miss 一样，都会把读者带沟里去。

（完）
