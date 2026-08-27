---
title: 理解 KV Cache：推理为什么能加速
date: 2026-09-24
description: 用白话说明 KV Cache 在推理阶段如何复用中间结果，以及和延迟的关系。
tags: [AI, 基础概念, 系列]
series: understanding-ai
draft: true
---

KV Cache 是推理阶段的常见优化：**把已经算过的 Key 和 Value 存起来，生成新 token 时直接复用**，避免重复计算。

没有它，自回归生成（一个 token 一个 token 往外吐）会慢很多。流式输出、长回复、Agent 多轮对话，背后都有 KV Cache 在撑。

下面是我整理的 KV Cache 要点：它在复用什么，以及和显存、延迟的关系。

![KV Cache 复用过去 token 的 Key 和 Value](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/kv-cache-reuse_8Hi6gwZKr.png)

## 一、先说一个具体麻烦

模型生成「今天天气很好」共 6 个 token，自回归模式下：

- 生成第 2 个 token 时，第 1 个 token 的 K/V 已经算过  
- 生成第 6 个 token 时，前 5 个 token 的 K/V 也都算过

如果每步都从头重算整段序列的 Attention，计算量随长度平方增长——**越写越慢**。

## 二、Attention 里哪些可以缓存

回顾 Self-Attention：每个 token 产生 Q、K、V。生成新 token 时：

- **新 token 的 Q** 必须新算  
- **过去 token 的 K、V** 不变，可以存进 Cache  
- 只需把新 token 的 K、V **追加**到 Cache，再做 Attention

这就是 KV Cache 的名字来源：**缓存 Key 和 Value**。

## 三、有 Cache 和没 Cache 的差别

![无 Cache 全量重算 vs 有 Cache 增量追加](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/kv-cache-speed-compare_vObB_tAxr.png)

| | 无 KV Cache | 有 KV Cache |
| --- | --- | --- |
| 每步计算 | 重算全部历史 token | 只算新 token + 读 Cache |
| 时间复杂度趋势 | O(n²) 量级 | 接近 O(n) 每步 |
| 显存 | 低（不存中间态） | 高（存每层每 token 的 K/V） |

所以：**KV Cache 用显存换速度**。上下文越长、层数越多，Cache 占的显存越大——这也是长上下文贵的原因之一。

## 四、显存大概怎么估

粗算公式（每层）：

```text
KV 显存 ≈ 2 × 层数 × 序列长度 × 隐藏维度 × 字节数
```

上面公式中，「2」是 K 和 V 两份；FP16 每元素 2 字节，INT8 量化 Cache 可减半。32 层、128K 上下文、4096 维 hidden，Cache  alone 就是 GB 级别——工程上需要分页 Cache（PagedAttention 等）、量化 Cache、或限制并发。

## 五、和 Prefill / Decode 的关系

推理常分两阶段：

（1）**Prefill（预填充）**—— 一次性处理用户输入的所有 token，填满初始 Cache  
（2）**Decode（解码）**—— 每步生成 1 个 token，追加 Cache

首 token 延迟（TTFT）主要看 Prefill 有多长；后续每个 token 的间隔（TPOT）主要看 Decode 和 Cache 效率。Prompt 很长时，Prefill 本身也吃算力——这和 KV Cache 是不同瓶颈。

### 5.1 PagedAttention 直觉

vLLM 等框架把 KV Cache 切成页、按需分配，减少显存碎片，提高并发——就像操作系统分页。单机要同时服务多个长对话，PagedAttention 往往是标配；个人本地推理单会话则感知不强。

和 Attention 篇对照：Prefill 阶段要为整段 Prompt 算一遍 K/V 并写入 Cache；Decode 阶段才体现「复用」价值。所以**首包慢、后续流式快**的体感，正是两阶段分工的结果。优化长 Prompt 场景，有时要拆系统提示、做缓存命中，而不只是买更快的 GPU。

## 六、多轮对话与 Cache

同一轮对话里，只要上下文没被截断，Decode 阶段会持续追加 KV Cache，越聊越长、Cache 越大。Session 结束或上下文被裁剪后，对应 Cache 作废，下一轮 Prefill 重新来。

Agent 工具调用返回的大段 JSON 也会占序列长度——**每次 tool result 都在撑 Cache 和窗口**。工程上常做摘要、只保留关键字段， partly 就是为了控 Cache 体积与延迟。

## 七、常见误区

（1）**KV Cache 不减少总计算量**—— 只是避免重复算，首次 Prefill 仍要全算。  
（2）**多轮对话要清 Cache**—— 新 session 或上下文截断时，旧 Cache 无效，不能无限复用。  
（3）**Cache 和训练无关**—— 只发生在推理（inference）阶段。  
（4）**长 Prompt 的瓶颈可能在 Prefill**—— Cache 主要加速 Decode，首 token 慢要另查输入长度与批大小。

## 八、小结

KV Cache 把历史 token 的 Key、Value 存起来，生成新 token 时增量计算而非全量重算。它是流式推理加速的关键，代价是显存随上下文长度线性增长。

长上下文产品宣传「128K」时，除了 Attention 算力，还要问 KV Cache 显存是否扛得住、并发是否会被 Cache 挤爆。用户侧感知到的「越聊越卡」，有时不是模型变慢，而是 Cache 与窗口在悄悄变胖。

Batch 推理时，不同请求的 Cache 长度不同，调度器要处理 padding 与批合并——这是 serving 框架的隐藏复杂度。应用开发者虽不用手写 Cache，但要知道**并发用户 × 平均对话长度**直接乘在显存账单上。

Speculative decoding（投机解码）是另一条加速路线：小模型先猜几个 token，大模型再批量验证——与 KV Cache 正交。读性能优化文章时，先分清「少算 Attention」还是「少跑 forward 步数」，再对号入座。

若你在本地用 llama.cpp 或 Ollama，上下文越长，显存占用越接近「模型权重 + KV Cache」之和。关掉其他占 GPU 的程序仍 OOM，先查是不是 Cache 把长度撑爆了，而不是模型文件下错了。

总结成一句：**KV Cache 记住过去算过的 K/V，让生成阶段只做增量**——Attention 篇讲怎么算，本篇讲怎么少算第二次。长对话产品若支持「清空上下文」，本质上也是在释放 Cache 占用的显存。

部署侧常把 max context length 设得比营销数字保守， partly 就是为了在并发与 Cache 显存之间留安全边际——用户可见的窗口上限，往往是工程权衡后的结果。

（完）
