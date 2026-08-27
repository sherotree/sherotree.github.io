---
title: Agent 工程笔记⑤：工具描述怎么写，模型才调得对
date: 2026-09-05
description: 专栏「Agent 工程笔记」第五篇：工具 schema 与描述怎么写，才能让模型稳定选对工具、填对参数。
tags: [AI, Agent, 系列]
series: agent-notes
draft: true
---

工具 schema（Tool Schema）是 Agent 的「菜单」：**告诉模型有哪些能力、每个能力干什么、参数长什么样**。菜单写糊了，Plan 再清晰也会点错菜。

同一套后端 API，描述从「search」改成带边界的中文说明，调用准确率往往会差一截。问题常不在模型，而在 schema 没写清「何时用、何时不用」。

下面是我整理的工具描述写法：命名、description、参数约束与正反例。

顺带一提：工具改名是大事。线上已有会话缓存了旧 tool 名时，Observe 里最好同时识别 alias，否则一次 schema 迁移就能让整站 Agent 集体「找不到工具」。

![工具 schema 好坏对比](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/schema-comparison_POHNLlgotT.png)

## 一、先说一个具体麻烦

你给 Agent 挂了三个工具：`search_docs`、`run_sql`、`send_email`。用户问：「帮我把 Q2 销售数据发给财务。」

模型调了 `send_email`，正文里写「Q2 销售同比增长 12%」——**既没查库，也没检索文档**。因为三个工具的 description 都只有一句话「搜索 / 查询 / 发送」，模型选了看起来最像「完成用户任务」的那个。

这类误调在评测里很常见：用户句子里的动词是「发给」，模型就优先匹配「发送类」工具，而忽略「发之前必须先有数据」这一隐含前提。

## 二、好 schema 的四条原则

（1）**一名一责**：一个工具只做一件事；「又查又写又发」应拆成多个工具或编排层。  
（2）**description 写边界**：说明适用场景 + 明确禁止（例如「不发送邮件，只生成草稿」）。  
（3）**参数名可读**：`query` 不如 `keyword_or_question` 直观；枚举值用文档里会出现的原词。  
（4）**required 真实必填**：可选参数过多，模型会乱填；能默认的放在宿主侧。

此外，`examples` 字段（若平台支持）放一组「典型 question → 该不该用本工具」的短例，往往比再加两百字形容词更有效。

![清晰与模糊的 schema 对照](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/schema-good-bad_l-1mVzckJ.png)

## 三、一个可改写的 JSON Schema 例子

下面是对 `search_docs` 的较完整写法（OpenAI function calling 风格）。

```json
{
  "name": "search_internal_docs",
  "description": "在已索引的内部 Markdown/PDF 中检索段落。用于政策、流程、产品规格等事实性问题。不能执行 SQL、不能发邮件、不能修改文档。检索为空时应停止并告知用户，不要用常识补全。",
  "parameters": {
    "type": "object",
    "properties": {
      "question": {
        "type": "string",
        "description": "用户的自然语言问题，保留关键实体如版本号、部门名"
      },
      "top_k": {
        "type": "integer",
        "description": "返回片段数量，默认 5，最大 10"
      }
    },
    "required": ["question"]
  }
}
```

上面代码中，`description` 前半句讲**何时用**，后半句讲**禁止做什么**；`required` 只留真正缺了就无法执行的字段。`top_k` 可设 default，不必强制模型每次填。

若平台支持 `enum`，把「报告格式 pdf/docx」这类封闭集合写进 schema，比自由字符串更少幻觉参数。

## 四、容易踩坑的参数设计

（1）**布尔开关过多**  
`dry_run`、`force`、`async` 并列时，模型经常组合错。合并为枚举：`mode: preview | execute`。  
（2）**路径参数无约束**  
写清允许的前缀，例如「仅 `/data/reports/` 下只读 `.csv`」。  
（3）**与别工具重名**  
`query` 在五个工具里出现五次，Plan 阶段易混淆；改成 `sql_query` / `doc_query`。  
（4）**description 堆同义词**  
「搜索、查找、检索、query」写一整段，不如一句场景 + 一句反例。

维护 schema 时建议版本化：字段改名尽量保留旧名别名一轮，Observe 里提示 deprecated，避免线上 Agent 突然集体填错参数。

## 五、和 Plan-Act-Observe 的配合

系列第四篇里，Plan 依赖工具列表做决策。工具越多，**互斥说明**越重要：在 description 里写「若需结构化数字，用 `run_sql_readonly`，不要用本工具」。

宿主还可以在 Observe 里校验参数（路径越界、邮箱格式），把错误写回，让下一轮 Plan 改 schema 允许的取值——比单纯重试同一 call 有效。

上线前建议维护「工具选择混淆矩阵」：列出易混淆工具对，用固定用户句跑一遍，看 description 改动是否减少误选。

## 六、常见误区

（1）**只抄 OpenAPI 自动生成的 description**  
面向人的 REST 文档 ≠ 面向模型的工具说明。  
（2）**一个巨型 `execute` 工具**  
参数是任意 JSON，模型几乎必然填错。  
（3）**不写失败语义**  
工具返回 404 与 500 在 Observe 里应区分，否则模型当「没数据」继续编。  
（4）**中英文混用且无一致术语**  
同一概念在 schema 与用户界面用词不一致，检索与调用都会对不齐。  
（5）**上线后不测 bad case**  
应准备「该用 A 却倾向 B」的用例集，改 description 后回归。

另有一条实践：工具列表超过十个时，按场景分组并在 system 里写「本回合可用子集」，比一次性注册全部工具更利于 Plan 聚焦。

最后提醒：schema 是活文档。后端 API 加了必填字段，若不同步改 description 与 examples，模型会继续按旧习惯漏填——这类回归只能靠用例集兜住。

## 七、小结与系列导航

工具 schema 的本质：**把后端能力翻译成模型能稳定消费的契约**。写清边界比堆参数更重要；拆工具比写一个万能接口更稳。改 description 后务必跑回归用例，别把「感觉更清楚」当成「调用更准」。

工具文档最好和 API 文档同源维护：一处改字段，两处一起发版，运维才不会在半夜手工对 schema。

把「工具选择错误」单独记 metrics，比只看最终回答满意度更早暴露 description 问题。

上一篇预告：Agent 最小闭环——Plan → Act → Observe。  
下一篇预告：多步任务——什么时候拆子 Agent。

（完）
