---
title: AI 编程效率⑥：让 AI 写测试——验收比生成重要
date: 2026-09-15
description: 专栏「AI 编程效率」第六篇：AI 生成测试的验收标准与常见漏网之鱼。
tags: [AI, 编辑器, 效率, 系列]
series: ai-coding-workflow
draft: true
---

让 AI 写测试很快，但**快不等于有效**。常见结果是：测试全绿，却从没断言业务行为；或 mock 了被测函数本身，测了个寂寞；或断言写死实现细节，重构就碎。

这和 Grounding 的验收思路一样——生成只是第一步，**你要能核对「测的真是那件事」**（见 Agent 工程笔记⑨）。下面是我用的「生成 → 运行 → 验收 → 补洞」循环。

测试是活的规格说明。AI 生成的测试若只断言 `toBeDefined()`，绿灯没有任何信息量；若 mock 掉整个 service，则永远测不到集成问题。我的默认假设是：**AI 测试草稿覆盖率约六成**，剩下四成边界与恶意路径要人补或二轮 prompt。

下面展开具体做法。

![AI 写测试的生成与验收循环](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/test-generate-verify_DC4_ITzgB.png)

## 一、先定验收标准，再让 AI 写

我会先写三条**必须覆盖的行为**，再 `@` 实现文件：

```text
@src/services/order.ts
为 createOrder 写测试，必须覆盖：
1. 库存不足时返回 ERR_OUT_OF_STOCK，且不调用支付
2. 正常下单写入订单表并返回 orderId
3. 支付回调失败时订单状态为 pending_payment
使用现有 test/fixtures/order.json，不要 mock createOrder 本身。
```

上面代码中，第 3 条是**失败分支**；最后一句防止「测 mock 不测逻辑」。

行为清单来自产品或 issue，而不是让 AI 自己「觉得测什么」——否则容易测 trivial 路径。

## 二、生成后必跑

```bash
npm test -- order.test.ts --coverage --collectCoverageFrom=src/services/order.ts
```

看两件事：**是否绿**、**行覆盖率是否含分支**。AI 爱写 happy path，分支常漏。

集成测若慢，至少跑相关 suite；CI 全量留给 push 前。

## 三、人工验收清单

![测试验收清单](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/test-acceptance-checklist_DiJxcuUXc.png)

我逐条勾：

（1）**断言测行为，不是测实现细节**——少绑内部私有函数。  
（2）**失败用例真的会变红**——临时改错断言或注释一行业务逻辑，确认测试能抓 bug。  
（3）**没有过度 mock**——外部 IO 可 mock，核心业务不可。  
（4）**测试名读得懂**——`should reject when stock is zero`。  
（5）**CI 可跑**——不依赖本机路径、不 `@ts-ignore` 糊过去。  
（6）**fixture 最小**——只造必要字段，避免掩盖 schema 变更。

## 四、坏例子 vs 好例子

坏：

```typescript
it('works', () => {
  const fn = jest.fn().mockReturnValue(true);
  expect(fn()).toBe(true);
});
```

好：

```typescript
it('returns ERR_OUT_OF_STOCK when quantity exceeds inventory', async () => {
  await seedInventory({ sku: 'A', qty: 0 });
  await expect(createOrder({ sku: 'A', qty: 1 })).rejects.toMatchObject({
    code: 'ERR_OUT_OF_STOCK',
  });
  expect(chargePayment).not.toHaveBeenCalled();
});
```

上面好例子里，**库存、错误码、副作用** 都可核对，符合 Grounding 式可验证输出。

## 五、补洞：mutation 与边界

AI 常漏：空输入、权限不足、超时、重复提交。我会单独 prompt：

```text
在不改生产代码前提下，列出 createOrder 还缺哪 3 条边界测试；
每条说明预期结果。
```

人挑选后让 AI 补写，再跑一遍验收清单。

## 六、何时让人补测

（1）并发、竞态、时钟——AI 常简化。  
（2）安全与权限边界。  
（3）回归来自线上 bug——应用**最小复现**写一条再扩。  
（4）性能与负载——需要基准环境，不宜全自动信任。

## 七、与 CI 的契约

生成的测试必须**本地与 CI 同命令**通过。若 AI 用了 only-local 的 path 或环境变量，验收阶段就要改。我会在 `AGENTS.md` 里写死测试命令（系列③），并在 prompt 里重复，减少「我这边能跑」式幻觉。

 flaky 测试一律打回，不让 AI 用 `sleep` 或加大 timeout 糊弄——那是掩盖 race，不是修复。

## 八、小结

AI 写测试是**起草**；验收才是工程。先写行为清单，再生成，再跑 coverage，再故意弄红一条。测得不可信，比没测更危险——它会给 false confidence。Grounding 思维在这里的体现是：**每条断言都要对得上真实行为**，而不是对得上 AI 的猜测。

（完）
