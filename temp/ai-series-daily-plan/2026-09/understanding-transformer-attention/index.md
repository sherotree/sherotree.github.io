---
title: 理解 Transformer：Attention 在算什么
date: 2026-09-03
description: 用白话说明 Transformer 与 Self-Attention：模型如何在序列里分配「注意力」，以及这和上下文窗口的关系。
tags: [AI, 基础概念, 系列]
series: understanding-ai
draft: true
---

Self-Attention（自注意力）是 Transformer 的核心机制：**让序列里每个位置，都能「看见」其他位置，并按相关程度加权取信息**。

大模型能处理长上下文、理解指代关系，Attention 功不可没。但 Q、K、V、Softmax 这些术语堆在一起，初看像黑箱。

下面是我整理的 Attention 最小理解：它到底在算什么，以及和上下文窗口的关系。

![Self-Attention 中 Q/K/V 的加权示意](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/attention-qkv-weighting_kzGXMqD7p.png)

## 一、先说一个具体麻烦

句子是：「小明把书交给了小红，因为她需要复习。」

「她」指谁？人一眼能判断，模型得从上下文里找线索。传统 RNN 按顺序传递，距离一远就容易丢信息。

Attention 的思路是：**写每个词时，直接问一遍「前面哪些词跟当前词有关」**，相关多的多分一点权重，相关少的少分。

## 二、Q、K、V 各是什么

可以把每个 token 想成图书馆里的一本书，Attention 分三步：

（1）**Query（查询）**：当前词在问——「我想找什么信息？」  
（2）**Key（键）**：每个词贴的标签——「我这儿有什么信息？」  
（3）**Value（值）**：每个词实际携带的内容

当前词的 Query 和所有词的 Key 做匹配，得到一组分数；分数越高，说明越相关。再用 Softmax 把分数变成权重（加起来等于 1），最后对 Value 加权求和，得到当前词的新表示。

![Attention 三步：算相似度、Softmax、加权求和](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/attention-softmax-flow_dkYGJSlf8.png)

简单说：**Attention 就是在算「该看哪里、看多少」**。

## 三、一个最小计算例子

假设只有三个词，当前词对它们的原始分数是 `[2.0, 1.0, 0.5]`。Softmax 之后可能变成 `[0.58, 0.32, 0.10]`——第一个词拿到最多注意力。

```python
import math
scores = [2.0, 1.0, 0.5]
weights = [math.exp(s) / sum(math.exp(x) for x in scores) for s in scores]
# 约 [0.58, 0.32, 0.10]
```

上面代码中，`scores` 来自 Query 与 Key 的点积（再除以维度的平方根做缩放）；`weights` 就是注意力权重，用来混合 Value。

### 3.1 掩码：哪些位置能看

Decoder-only 模型（GPT 类）生成时，当前 token **不能偷看未来**。实现上会给 Attention 矩阵加**因果掩码（causal mask）**：未来位置的分数设为负无穷，Softmax 后权重为 0。

Encoder 侧（如 BERT）做理解任务时，往往允许双向 Attention——整句互相可见。读论文或调 API 时，先分清是「生成」还是「理解」架构，Attention 的可见范围不一样。

## 四、Scaled Dot-Product 在算什么

正式写法里，注意力分数不是直接点积，而是：

```text
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) · V
```

上面公式中，`QK^T` 是 Query 与 Key 的相似度矩阵；除以 `sqrt(d_k)` 是为了维度高时点积数值过大、Softmax 梯度消失；最后的 `· V` 就是按权重混合 Value。

你可以把它记成：**先算谁和谁像，再决定从谁那里取多少信息**。

## 五、Multi-Head 与上下文窗口

一层 Attention 只学一种「看哪里」的方式。**Multi-Head Attention** 把 Q/K/V 拆成多组头，每组独立算注意力，最后拼起来——相当于同时从语法、语义、指代等多个角度读上下文。

比如 12 个头，可能有的头关注相邻词搭配，有的头关注远距离指代。多头并行，比单头硬算一张大表更灵活。

上下文窗口（context window）能装多少 token，Attention 就要在多少 token 之间算权重。窗口越大，Prefill 阶段计算量按序列长度平方增长——这也是长上下文贵、且需要 KV Cache 等优化的原因（见本系列 KV Cache 篇）。

另外，**因果掩码（causal mask）** 在解码时很常见：当前 token 只能看前面的 token，不能偷看未来——这样生成才是一个字一个字往外吐，而不是整段一次性泄露。

推理服务里的 **Flash Attention** 等实现，不改变 Attention 的数学含义，只是更高效地算 QK^T 和乘 V——省显存、提速度，对使用者透明。你调 API 时一般不用手改，但知道「慢 often 在 Attention 算子」有助于读 profiling 报告。

## 六、常见误区

（1）**Attention 不等于「理解」**——它只是可学习的加权汇总，理解来自多层堆叠与训练数据。  
（2）**权重高不等于因果正确**——模型可能关注到错误位置，输出仍可能错。  
（3）**不是所有层都在做同一件事**——浅层偏局部，深层偏全局与抽象。  
（4）**可视化权重不等于可解释**——热力图好看，但「模型为什么选这个词」仍难严格归因。

## 七、和系列其他篇的关系

Attention 读上下文；Token 化决定上下文能装多少（本系列 Token 篇）；KV Cache 让 Attention 在推理时不必重复算历史（KV Cache 篇）。三条串起来，是大模型「读→记→写」的基本面。

## 八、小结

Attention 的本质：**对每个位置，算一组权重，从全序列里按需取信息**。Q 提问、K 应答、V 交货，Softmax 定比例。

它是 Transformer 读上下文的方式，也是大模型能处理长文本、解析指代的基础构件。

读论文时看到 «Attention Is All You Need»，现在你可以把标题直译成工程语言：**只要会把序列里该看的位置加权读出来，堆叠多层就能做翻译、摘要、对话**。RNN 的长距离遗忘，在这里被显式注意力矩阵接住了。

（完）
