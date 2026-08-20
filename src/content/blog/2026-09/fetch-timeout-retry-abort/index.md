---
title: fetch：超时、重试与 AbortController
date: 2026-09-11
description: 说明用 fetch 时如何做超时取消、可重试错误判断与退避重试，核心是 AbortController 与清晰的失败分类。
tags: [前端, fetch, AbortController, 网络]
draft: true
---

`fetch` 是浏览器里发 HTTP 请求的标准方法。默认它**不会**因「等太久」自动失败，也**不会**帮你重试。

线上接口偶发超时、网关 503、限流 429，若页面一直转圈或疯狂连打，体验与服务都会受伤。下面把三件事拆开：超时怎么取消、什么错误值得重试、怎么和 AbortController 配合。

![用 AbortController 做超时取消](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/fetch-abort-timeout_7_E4d-PSz.png)

## 一、先说一个具体麻烦

你写了：

```js
const res = await fetch('/api/report')
const data = await res.json()
```

上面代码中，没有超时。服务端卡住时，Promise 可能一直 pending，按钮转个不停。用户重复点击，又发出第二、第三次请求。

需要两样能力：

（1）到点取消  
（2）区分「可重试」与「不该重试」，避免把 400 校验错误也重打三遍

## 二、AbortController：取消的总闸

`AbortController` 提供一个 `signal`。把它传给 `fetch`，调用 `abort()` 即可取消。

```js
const ac = new AbortController()
fetch('/api/report', { signal: ac.signal })
// 某处：
ac.abort()
```

上面代码中，取消后 `fetch` 会以 AbortError 一类错误拒绝（具体名称因环境略有差异）。同一 `signal` 也可传给多个关联请求，一并取消。

超时只是「到时间自动 abort」的一种用法。

## 三、最小超时封装

思路：（A）创建 controller（B）`setTimeout` 到点 abort（C）`finally` 里清定时器。

```js
export async function fetchWithTimeout(url, options = {}, ms = 8000) {
  const ac = new AbortController()
  const timer = setTimeout(() => ac.abort(), ms)
  try {
    return await fetch(url, { ...options, signal: ac.signal })
  } finally {
    clearTimeout(timer)
  }
}
```

上面代码中，若调用方自己也传了 `signal`，生产代码还应把外部 abort 与超时 abort 合并（例如 `AbortSignal.any`，或手动监听转发）。入门先掌握「超时 = 定时 abort」。

用户离开页面或关闭弹窗时，同样应 abort，避免无用请求占着连接与回调。

## 四、什么错误才重试

不是所有失败都该重试。

通常更值得重试：

（1）网络断开、DNS 临时失败  
（2）`408` / `429` / `502` / `503` / `504`  
（3）你明确标成幂等的 GET / 某些可安全重放的写操作（需业务保证）

通常不要盲着重试：

（1）`400` / `401` / `403` / `404` / `422`（改请求或鉴权，不是再打一次）  
（2）非幂等 POST 已可能成功但响应丢失——重试可能造成重复下单（需幂等键）

![可重试错误才退避重试](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/fetch-retry-backoff_rPgTz7Rx4.png)

## 五、退避重试的最小形状

「立刻再打」容易把服务打崩。常见做法是指数退避：1s、2s、4s……并加一点抖动。

```js
async function fetchWithRetry(url, options, { retries = 2, baseMs = 400 } = {}) {
  let lastErr
  for (let i = 0; i <= retries; i++) {
    try {
      const res = await fetchWithTimeout(url, options, 8000)
      if (res.ok) return res
      if (![429, 502, 503, 504].includes(res.status) || i === retries) return res
    } catch (err) {
      lastErr = err
      if (i === retries) throw err
    }
    const wait = baseMs * 2 ** i + Math.random() * 100
    await new Promise((r) => setTimeout(r, wait))
  }
  throw lastErr
}
```

上面代码中，逻辑是示意：成功或不可重试状态码就返回；可重试则等待后再来。真实项目还应：

（1）尊重 `Retry-After`  
（2）把超时 abort 与「主动取消」区分开——用户取消不应再重试  
（3）对写操作加幂等键或禁止自动重试

## 六、和 UI 状态机对齐

请求层做好了，还要和界面约定：

（1）进行中：禁用提交或显示 loading  
（2）取消：abort，并忽略随后的过期响应  
（3）失败：按状态码给文案（401 去登录，429 提示稍后再试）

竞态常见坑：先发的慢请求后返回，覆盖了新数据。用递增的 request id，或每次新请求 abort 旧请求，可以避免。

## 七、常见误区

（1）**只 `await fetch`，不看 `res.ok`**  
HTTP 404 不会进 catch，需要自己判断。

（2）**所有方法统一重试三次**  
非幂等写操作很危险。

（3）**超时时间设得极短又极多重试**  
等于自己制造雪崩。

（4）**catch 到 AbortError 还弹「网络错误」**  
用户主动取消应静默处理。

（5）**忘记清 timer**  
组件卸载后仍 abort，或 timer 泄漏。

## 八、小结

`fetch` 本身不管超时与重试。用 AbortController 做取消，用定时 abort 做超时，用状态码与幂等性决定是否退避重试。

三件事分开设计，再组合；混在一个「万能 request」里最容易变成黑盒。

（完）
