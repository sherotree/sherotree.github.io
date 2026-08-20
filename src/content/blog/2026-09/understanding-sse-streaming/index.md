---
title: 理解流式输出：SSE 在聊天里干什么
date: 2026-09-18
description: 说明聊天产品里的流式输出常见实现 SSE：服务器按事件推送文本碎片，前端边收边渲染，以及它解决什么、不替代什么。
tags: [SSE, 流式输出, 前端, AI 应用]
draft: true
---

流式输出指的是：模型或服务端不是等整段答完再一次性返回，而是边生成边把文本碎片推给客户端。

聊天界面里「一个字一个字往外冒」，多半就是这种体验。实现上常见路径之一是 SSE（Server-Sent Events，服务器推送事件）。资料里还夹着 WebSocket、chunk、token，读完仍常不清楚：**SSE 在链路里到底干哪一段活**。

下面按「为什么要流 → SSE 是什么 → 聊天里怎么用 → 边界」说明。

![一次性返回与 SSE 流式对比](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/sse-vs-oneshot_sCXiD16hG.png)

## 一、先说一个具体麻烦

若接口只在全部生成结束后返回 JSON：

（1）用户要干等十几秒，以为页面卡死  
（2）中途无法取消，白白耗完配额  
（3）网关或浏览器超时，可能直接失败

流式输出解决的是：**先把已有 token 送出门，降低首字时间，并允许边看边停**。它不自动让模型更聪明，只改善交付节奏。

## 二、SSE 是什么

SSE 是浏览器原生支持的一种**服务端到客户端**的文本事件流。

典型响应头包含：

```http
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive
```

正文按事件块推送，常见形态：

```text
data: 你

data: 好

data: [DONE]
```

上面文本中，每条 `data:` 后面是载荷；空行分隔事件。聊天场景里，载荷常常是增量文本，或一层 JSON（含 delta 字段）。具体协议由各家 API 约定，但「长连接 + 多次 data」的骨架类似。

![服务端按 data 行推送，客户端追加到界面](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/sse-event-stream_Fat9OIe00.png)

和 WebSocket 比，SSE 的直觉是：

（1）SSE 主要是**单向**（服务器 → 浏览器），实现简单  
（2）WebSocket 双向更灵活，也更重一些  
（3）聊天「提问一次、回答流式回来」非常契合 SSE；若要高频双向二进制，再评估 WebSocket

## 三、前端怎么接

### 3.1 EventSource

适合简单 GET 流：

```js
const es = new EventSource('/api/chat/stream')
es.onmessage = (ev) => {
  appendText(ev.data)
}
es.onerror = () => es.close()
```

上面代码中，浏览器自动重连是 EventSource 的特性之一；聊天若带复杂鉴权或不想自动重放，要小心处理。

### 3.2 fetch + ReadableStream

很多 AI API 用 POST，且要自定义 Header，这时更常见 `fetch` 读 body 流，再按行解析 `data:`。

```js
const res = await fetch('/api/chat', {
  method: 'POST',
  headers: { Accept: 'text/event-stream' },
  body: JSON.stringify({ messages }),
  signal,
})
const reader = res.body.getReader()
// 再按 TextDecoder + 行缓冲解析 data:
```

上面代码中，`signal` 可接 AbortController，用户点「停止生成」时 abort，避免继续耗流量与配额。解析时务必做行缓冲：TCP 分包不会保证每次 read 都对齐一行。

## 四、聊天产品里 SSE 实际承担的角色

把它放回整条链路：

（A）用户发送消息  
（B）服务端调用模型，拿到 token 流  
（C）服务端把增量写成 SSE 事件转给浏览器  
（D）前端追加到气泡，必要时做打字机或直接拼接  
（E）结束事件或 `[DONE]` 后收尾（解除 loading、存历史）

SSE 干的是 **C→D 的运输与呈现节奏**。模型本身是否流式，取决于上游 API；没有上游流时，服务端也可以伪流式（切句推送），但首字时间改善有限。

## 五、它不替代什么

（1）**不替代鉴权与配额**  
流式照样要登录、计费、限流。

（2）**不替代错误协议**  
中途上游失败，需要明确错误事件或关闭方式，不能只靠连接断开让用户猜。

（3）**不自动解决「完整 JSON 结构」**  
若你要严格 JSON Mode，流式过程中对象可能长期不完整，需在结束后校验，或改用缓冲策略。

（4）**不是唯一流式方案**  
HTTP chunked、WebSocket、gRPC stream 都能流；SSE 只是 Web 里好用的一种。

## 六、常见误区

（1）**把 SSE 当成 WebSocket**  
默认单向；客户端→服务端仍用普通请求。

（2）**代理缓冲整段再转发**  
Nginx 等若缓冲 response，流式体验会消失；需关掉缓冲或设合适头。

（3）**不处理半包粘包**  
按 read 一次当一条事件，解析会乱。

（4）**停止按钮只改 UI，不 abort**  
请求仍在跑，浪费钱。

（5）**把每个 token 都打进 DOM 重排**  
可合并到动画帧再渲染，避免主线程过忙。

## 七、小结

SSE 在聊天里的工作，是把服务端陆续产生的文本，按事件流推到浏览器，让界面边收边画。

它解决等待与可中止的体验问题；不解决模型质量本身。接的时候抓住三点：正确的 `text/event-stream`、可靠的行解析、可 abort 的取消。

（完）
