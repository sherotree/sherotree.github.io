---
title: Agent 工程笔记⑧：RAG 入门——检索什么、怎么切块
date: 2026-09-16
description: 专栏「Agent 工程笔记」第八篇：RAG 最小路径——检索对象、切块策略与常见坑。
tags: [AI, Agent, 系列]
series: agent-notes
draft: true
---

RAG（Retrieval-Augmented Generation，检索增强生成）在 Agent 里解决一件事：**回答前先把你自己的资料里相关片段找出来，再交给模型生成**。没有检索，内部文档 Agent 只能靠训练记忆「像真的」；有了检索，至少知道材料从哪来。

RAG 难在细节：切多大块、检索什么粒度、空结果怎么办。切块切错了，后面 Grounding 再严也贴不住文档——见系列第九篇。

下面是我整理的 RAG 最小路径：检索对象、切块策略与流水线。

RAG 不是装向量库就结束：同样的 top-k，元数据过滤（只搜 2026 版手册）常常比盲目加 embedding 维度更管用。

![切块过大与过小的对比](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/chunk-size_DPVcOfnTc.png)

## 一、先说一个具体麻烦

你把整本 200 页手册每页一个 chunk 塞进向量库。用户问「远程办公需要谁审批？」

检索 top-3 返回三页泛泛的「办公政策概述」，没有命中「主管书面审批」那句。模型仍答得很自信——**不是向量库坏了，是 chunk 太大、信号被稀释**。

反过来，按单句切，「试用期六个月」和「不得延长」被拆到两个 chunk，检索只命中半句，语义也不完整。

还有一种折中失败：按固定 token 切，却把表格行拦腰截断，检索到的「数字」与「单位」分列在两个 chunk，模型拼接时容易张冠李戴。

## 二、先定「检索对象」再谈算法

（1）**段落 / 小节**：适合 Markdown、Wiki，结构清晰。  
（2）**滑动窗口**：适合长 PDF、缺标题的纯文本。  
（3）**结构化行**：CSV、日志、工单字段，按行或按记录。  
（4）**混合**：标题块 + 窗口重叠，兼顾语义与定位。

算法上，关键词 + 向量混合检索往往比纯向量稳；但**对象粒度不对，换模型也救不了**。

## 三、切块参数怎么起步

经验起点（需按语料微调）：

（1）**块大小**：512～1024 token 量级常见；技术文档可略大，FAQ 可略小。  
（2）**重叠（overlap）**：10%～20%，避免句意断在边界。  
（3）**元数据**：`doc_id`、`section_title`、`page`、`updated_at` 必带，便于引用与过滤过期文档。  
（4）**预清洗**：去页眉页脚、重复导航，减少噪声 chunk。

有目录的 PDF 可先用大纲切一级节，再对超长节做窗口切；这比从头滑动更保语义。代码仓库类资料则宜按文件 + 函数块切，别把整个 repo 拼成一条字符串。

![RAG 切块与检索流水线](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/chunk-pipeline_0uzkJe8GzC.png)

## 四、最小索引脚本长什么样

下面是一段概念性伪代码，展示从原文到可检索 chunk。

```python
def chunk_document(text, size=800, overlap=120):
    chunks = []
    start = 0
    while start < len(text):
        piece = text[start : start + size]
        chunks.append({
            "text": piece,
            "char_start": start,
            "char_end": start + len(piece),
        })
        start += size - overlap
    return chunks

for doc in load_docs():
    for c in chunk_document(doc.body):
        c["meta"] = {"doc_id": doc.id, "title": doc.title}
        index.add(embed(c["text"]), c)
```

上面代码中，`overlap` 让跨边界的定义不被截断；`meta` 供 Grounding 阶段输出 `[doc_id:offset]` 类引用。生产环境应按标题先切，再对过长节做窗口切。

入库前可为每个 chunk 算一个短标题（首句或模型摘要），检索结果展示时人也能一眼判断该不该点进原文。

## 五、检索结果怎么交给 Agent

RAG 输出应是**带元数据的片段列表**，不是拼成一篇「参考文章」：

（1）top-k 不宜过大，3～8 段常见，避免上下文被噪声占满。  
（2）空检索要有明确分支：拒答或澄清问题，不要默认生成。  
（3）与系列第七篇记忆层配合：用户偏好走 memory，事实问答走 RAG。

评测时可记录「命中 chunk 是否含答案句」而不只看最终回答像不像——切块问题会在这一层暴露得最清楚。

## 六、常见误区

（1）**只 embedding 不维护索引**  
文档更新后旧 chunk 仍在，答案过期。  
（2）**chunk 与引用粒度不一致**  
引用显示整章，实际只依据一句话，用户无法核对。  
（3）**把所有 PDF 转纯文本不保留结构**  
表格、列表打平后语义丢失。  
（4）**检索与生成用同一温度**  
检索是确定性的更好；生成在 Grounding 约束下偏低温度。  
（5）**跳过评测**  
应用固定问题集测 recall，比凭感觉调 k 值靠谱。

混合检索时，给关键词命中与向量命中分别设权重，并在 Observe 里记录用了哪一路，方便复盘「为什么这次 miss」。

切块不是一劳永逸：文档结构变了（新增 FAQ 页、合并章节）应触发增量重切；至少更新受影响 `doc_id` 的 chunk，否则索引与新 Grounding 规则会对不上。

上线 RAG 时，给运营一个「这条答案引用了哪几个 chunk」的后台视图，比用户前台看见引用编号更能快速发现切块事故。

## 七、小结与系列导航

RAG 的本质：**用切块与检索把「你的资料」变成可引用的上下文**。块大小与元数据质量，直接决定后面 Grounding 能不能贴文档。先用二十条真实用户问题做 recall 基线，再调 chunk 与 k，比从论文抄参数靠谱。

上一篇预告：记忆分层——会话内 vs 长期存储。  
下一篇预告：Grounding——怎么让回答贴文档。

（完）
