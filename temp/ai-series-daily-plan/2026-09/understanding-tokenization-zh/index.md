---
title: 理解 Token：为什么中文更费 token
date: 2026-09-07
description: 用白话说明 token 化：英文、中文与代码在 token 计数上的差异，以及这对成本与窗口的影响。
tags: [AI, 基础概念, 系列]
series: understanding-ai
draft: true
---

Token 是大模型读写的最小单位。API 按 token 计费，上下文窗口也按 token 计量——**同样一段话，中文往往比英文消耗更多 token**。

这不是模型「歧视中文」，而是分词器（tokenizer）的设计与训练语料偏向共同造成的。搞清这一点，才能合理估成本、控上下文。

下面是我整理的 token 化要点：英文、中文、代码各怎么切，以及对你写 Prompt 的实际影响。

![英文与中文同样语义的 token 数量对比](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/tokenization-zh-en-count_156ew3eX9.png)

## 一、Token 到底是什么

模型内部不直接处理「字」或「单词」，而是整数 ID 序列。Tokenizer 负责把文本切成子词（subword）片段，每个片段对应一个 ID。

英文常见 BPE（Byte Pair Encoding）：高频词整词保留，低频词拆成更小的块。「internationalization」可能被切成 `inter` + `national` + `ization` 等。

中文没有天然空格分词，多数方案按字或字节级 BPE 切。**单个汉字常常单独占 1～2 个 token**，而英文一个常见词往往只占 1 个 token。

## 二、同样意思，token 差多少

举两个近似对译的短句：

```text
英文：The weather is nice today.        → 约 6 tokens
中文：今天天气很好。                      → 约 8～12 tokens（视模型而定）
```

上面只是量级示意，具体数字因模型与 tokenizer 版本而异。但趋势稳定：**中文信息密度在 token 层面偏低**——表达同一语义，中文通常要更多 token。

代码介于两者之间：关键字往往整词保留，变量名可能被拆开，缩进和符号也会占 token。

## 三、对成本与窗口的实际影响

![中文更占满上下文窗口示意](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/tokenization-cost-window_L5p3Vxz9iG.png)

（1）**API 费用**：输入 + 输出都按 token 计。中文长文档对话，账单会比同等英文内容高出一截。  
（2）**上下文窗口**：128K 窗口装的是 token 数，不是字数。中文塞同样信息，更快触顶。  
（3）**输出长度限制**：`max_tokens` 也是 token 上限。中文回复 500 token，字数可能只有英文 500 token 的一半左右。

可以用 OpenAI 的 tiktoken 或各厂商提供的 tokenizer 工具实测：

```bash
# 示意：用 Python tiktoken 数 token
python3 -c "import tiktoken; enc=tiktoken.get_encoding('cl100k_base'); print(len(enc.encode('今天天气很好')))"
```

上面代码中，不同模型要用对应的 encoding 名称；实测比估算靠谱。

### 3.1 输出 token 也要算钱

很多人只数输入有多长，忽略**模型回复同样按 token 计费**。中文回复 1000 token，可能比英文 1000 token 承载更少汉字，但账单一样。设 `max_tokens` 时留余量，也要意识到中文同样吃输出配额。

## 四、为什么中文更「碎」

主流 tokenizer 多在英文语料上训练。英文有空格天然分词，BPE 合并的是高频字母组合；中文输入往往按 UTF-8 字节或单字切，**常用字和冷僻字都可能各占一个 token**。

标点、 emoji、全角符号也占 token。一条中文推文看起来不长，送进 API 可能比你以为的多出一截。混合文本（中英夹杂、代码注释）更复杂：英文变量名可能整词保留，旁边的中文注释逐字计费。

## 五、写 Prompt 时可以怎么做

（1）**长文档先摘要再喂**，别整篇原文塞进上下文。  
（2）**结构化输出用 JSON 等紧凑格式**，减少废话 token。  
（3）**代码引用用 `@file` 或行号范围**，而不是粘贴整文件（见 Agent 工程笔记相关篇）。  
（4）**估成本时按中文 1.5～2 倍英文 token 留余量**，比拍脑袋准。

## 六、和 Agent / RAG 的联动

Agent 每轮 tool call 的入参、返回 JSON 都按 token 计费。中文错误日志整段粘贴，几次就把窗口吃满。RAG 切块时也要算 chunk 的 token 占用——中文文档同样比英文更「占座」。Embedding 索引阶段虽不按 token 向用户收费，但切块大小仍影响检索质量与后续 Prompt 长度（见本系列 Embedding、RAG 篇）。

## 七、常见误区

（1）**字数 ≠ token 数**——永远以 tokenizer 计数为准。  
（2）**换模型 token 数会变**——GPT、Claude、开源模型的 tokenizer 各不相同。  
（3）**压缩中文没用**——去掉空格、标点几乎不省 token，该拆的字照样拆。  
（4）**以为 GB 级窗口等于 GB 级汉字**——窗口计量单位是 token，中文同样更快触顶。

厂商若在上下文定价上按 token 阶梯收费，中文项目的「等效信息量」成本仍高于英文——这不是偏见，而是 tokenizer 统计事实。换用对中文更友好的 tokenizer（部分开源模型）可略缓解，但 API 侧通常无法自选。

## 八、小结

Token 化是文本进入模型的第一站。中文更费 token，根因是分词器对拉丁语系更友好、汉字常单字成 token。

写中文 Prompt、做 RAG、估 API 成本时，把这个倍率算进去，少踩窗口和账单的坑。

顺带一提：模型「懂中文」与 tokenizer「省 token 地编码中文」是两回事。中文能力强，不代表同样字数更便宜——计费仍以 token 为准，写稿与做预算是两套账本。

做中文长文摘要或全书问答时，**先数 token 再定 chunk 策略**，比写完才发现窗口不够更省事。系列后面的 RAG、Embedding 篇默认你已经接受：中文同样长度，占用的上下文席位更多。

（完）
