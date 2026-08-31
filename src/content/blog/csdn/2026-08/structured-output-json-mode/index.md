---
title: 结构化输出 / JSON Mode 入门
date: 2026-08-20
description: 说明结构化输出与 JSON Mode：让模型按 schema 产出可解析 JSON，适合接程序，而不是只靠「请输出 JSON」形容词。
tags: [AI, JSON Mode, 结构化输出, API]
series: understanding-ai
draft: true
---

结构化输出（structured output）指让模型按约定形态返回数据，常见是 JSON，便于程序直接解析。JSON Mode / schema 约束是各厂商实现这一目标的手段。

聊天可以是散文；自动化要把结果喂给代码。这时「大概是个 JSON」不够，缺字段或尾随逗号都会让流水线断掉。

![自由文本与 JSON Mode 对照](https://ik.imagekit.io/4pjac7gmxh/blog/2026/10/json-mode-vs-free_aWYCGY41Z.png)

## 一、先说一个具体麻烦

你写：

```text
请用 JSON 返回用户姓名和邮箱。
```

模型有时返回 Markdown 代码块，有时多写解释，有时字段名飘成 `e-mail`。人工能看懂，`JSON.parse` 不能。

结构化输出要解决的，是把「像 JSON」变成「可校验的 JSON」。

## 二、核心思路：用 schema 当合同

与其用自然语言求情，不如提供 JSON Schema（或等价定义）：字段、类型、必填、枚举。

宿主侧流程通常是：

（A）声明 schema  
（B）开启 JSON / structured 模式（名称因厂商而异）  
（C）拿到字符串后仍做一次解析与校验  
（D）失败则重试或降级

![Schema 约束有效 JSON 输出](https://ik.imagekit.io/4pjac7gmxh/blog/2026/10/json-schema-flow_clpUCm1MK.png)

下面是一个最小 schema 直觉（示意）。

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["name", "email"],
  "properties": {
    "name": { "type": "string" },
    "email": { "type": "string" }
  }
}
```

上面代码中，`required` 与 `additionalProperties` 减少少字段、乱字段。真实 API 字段名以文档为准。

## 三、它解决什么，不解决什么

解决：

（1）程序化消费  
（2）字段稳定性  
（3）与函数参数、工作流节点对接

不解决：

（1）内容事实正确  
（2）业务规则是否合理（仍要你自己验）  
（3）超长散文叙述（结构化偏短数据）

JSON Mode 不是智商开关，是**输出形状开关**。

## 四、实践建议

（1）字段名用稳定英文；枚举写死  
（2）能在服务端校验，就不要只信模型  
（3）流式场景：对象可能长期不完整，结束后再 parse，或用支持增量的方案  
（4）错误时返回可区分的 parse_error，便于重试策略

## 五、常见误区

（1）**只靠提示「必须 JSON」**  
偶发成功，难上生产。  
（2）**schema 过大过深**  
失败率与 token 上升。  
（3）**校验失败却把脏数据写入库**  
结构化输出仍要守门。  
（4）**把解释性文字和 JSON 混在同一通道**  
能分开就分开。

## 六、小结

结构化输出让模型结果变成程序可吃的数据。用 schema 当合同，再用解析校验当门禁；形容词「请输出 JSON」只是弱提醒。

（完）
