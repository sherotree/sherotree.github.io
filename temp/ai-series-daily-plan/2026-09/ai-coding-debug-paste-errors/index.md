---
title: AI 编程效率⑧：Debug——报错信息怎么贴才有效
date: 2026-09-22
description: 专栏「AI 编程效率」第八篇：向 AI 贴报错与日志的正确姿势。
tags: [AI, 编辑器, 效率, 系列]
series: ai-coding-workflow
draft: true
---

Debug 时把报错丢给 AI，若只写「报错了帮看看」，等于**未 Grounding**——模型只能猜。Agent 工程笔记⑨要求证据片段完整；贴报错也是：**给可核对的栈、环境、复现**，回答才贴问题。

报错粘贴的质量，直接决定 AI 是在帮你定位，还是在编造 plausible 的修复。下面是我用的四段式模板与反例。

同样一条 NullPointer，完整 stack 可能指向一行越界访问；只有「null 了」则可能引出五种无关建议。Debug 贴报错的成本很低——复制终端比打字解释还快——但多数人仍习惯用自然语言描述「感觉」，这相当于主动拆掉 Grounding。

下面展开四段式与闭环。

![差的贴法 vs 好的贴法](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/debug-good-bad_DC34QFjRA.png)

## 一、四段式粘贴

![报错粘贴四段结构](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/debug-error-format_1q5k2IXqK.png)

（1）**环境**：OS、Node 版本、分支、相关 commit。  
（2）**期望 vs 实际**：一句话对比。  
（3）**完整报错**：从第一行 Error 到最后一行 stack，不要截断中间。  
（4）**已尝试**：避免 AI 重复你已做过的步骤。

缺任何一段，都可能让 AI 走偏——尤其是「期望 vs 实际」，否则它不知道你要修复的是 crash 还是错误结果。

## 二、模板示例

```text
## 环境
Node 20.11, macOS, branch feat/checkout, commit abc1234

## 期望 / 实际
期望：createOrder 返回 201
实际：500, 见下方 stack

## 报错
TypeError: Cannot read properties of undefined (reading 'id')
    at createOrder (src/services/order.ts:47:22)
    at async handler (src/routes/order.ts:18:5)
...

## 已尝试
- 确认 inventory 表有数据
- 单测 order.test.ts 通过，仅集成测失败
```

上面代码中，**行号 + 文件** 让 AI 能 `@` 精准位置；「单测过、集成挂」缩小范围到环境或 wiring。

## 三、该 @ 什么

（1）stack 里**最上面属于你代码**的那一帧对应文件。  
（2）若涉及配置， `@` `.env.example` 而非真 `.env`。  
（3）相关测试文件——Often 测试即最小复现。  
（4）最近改动的 diff 或 PR 链接——若 regression 明显。

## 四、日志与间歇性 bug

日志太长时，先本地 `grep Error` 或 `--since 5m`，只贴**第一次出现到 stack 结束**的一段。间歇性 bug 必须写：触发频率、是否并发、是否仅生产。

```text
约每 50 次请求出现 1 次；本地无法复现；生产 Node 18，本地 Node 20。
```

上面信息帮助 AI 区分 race 与版本差异，而不是给 generic retry 建议。

## 五、让 AI 输出也可验证

要求结构化回答，类似 Grounding 的 citations：

```text
请按以下格式回答：
1. 根因（一句话）
2. 证据（引用文件:行号）
3. 修复 diff 建议
4. 如何写回归测试
若信息不足，列出还需要的片段，不要猜。
```

## 六、常见贴法错误

（1）只贴最后一行 `undefined is not an object`。  
（2）用截图代替文本——模型难检索行号。  
（3）混进无关日志上千行——先过滤再贴。  
（4）不说复现步骤——别人无法验证 fix。  
（5）同时问三个无关报错——一次一个 thread。

## 七、修完后的闭环

Debug 结束不要只 merge——让 AI 根据根因**起草一条回归测试**（系列⑥），人验收后再合。并在 PR 里贴**精简版四段式**，方便以后 search。

若根因是文档或配置误导，同步改 README 或 sample env，否则下一个同事还会贴同样的报错。

## 八、小结

贴报错不是倾诉，是**提交证据包**。环境、对比、完整 stack、已尝试——四段齐，Debug 才从猜谜变成核对。这和 Grounding「找不到就停」是同一套纪律：**证据不够就补，不要先让模型猜修复。**

（完）
