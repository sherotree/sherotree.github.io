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

同样一条 NullPointer，完整 stack 可能指向一行越界访问；只有「null 了」则可能引出五种无关建议。Debug 贴报错的成本很低——复制终端比打字解释还快——但多数人仍习惯用自然语言描述「感觉」，这相当于主动拆掉 Grounding。养成四段式后，AI 首轮命中率会明显上去。

下面展开四段式与闭环。建议把模板存进编辑器 snippet：环境、期望/实际、报错、已尝试——四个占位符，比每次口头组织更 Grounded，也更省 token。

![差的贴法 vs 好的贴法](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/debug-good-bad_DC34QFjRA.png)

## 一、四段式粘贴

![报错粘贴四段结构](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/debug-error-format_1q5k2IXqK.png)

（1）**环境**：OS、Node 版本、分支、相关 commit。  
（2）**期望 vs 实际**：一句话对比。  
（3）**完整报错**：从第一行 Error 到最后一行 stack，不要截断中间。  
（4）**已尝试**：避免 AI 重复你已做过的步骤。

缺任何一段，都可能让 AI 走偏——尤其是「期望 vs 实际」，否则它不知道你要修复的是 crash 还是错误结果。若报错来自浏览器控制台，打开「保留日志」再复现，否则 stack 可能被导航冲掉；这类细节写在「已尝试」里，能省来回追问。前端还要贴**复现 URL 与操作步骤**，否则 AI 只能猜 DOM 状态——页面类 bug 的 Grounding 离不开交互路径。

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

上面代码中，**行号 + 文件** 让 AI 能 `@` 精准位置；「单测过、集成挂」缩小范围到环境或 wiring。若有多条 cascade 报错，只贴**根因那条**的完整 stack，衍生错误写在「实际」段即可——否则模型会在次要错误上浪费推理。

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

把输出格式写死，Debug 结果才能从「听起来对」变成「点开就能验」——和 Agent 笔记里的结构化 JSON 同一思路。

## 六、常见贴法错误

（1）只贴最后一行 `undefined is not an object`。  
（2）用截图代替文本——模型难检索行号。  
（3）混进无关日志上千行——先过滤再贴。  
（4）不说复现步骤——别人无法验证 fix。  
（5）同时问三个无关报错——一次一个 thread。

生产事故贴报错时，记得**脱敏**：用户 id、token、内网域名打码后再给 AI。证据要全，但不要泄漏。脱敏后若 stack 断档，在「已尝试」里说明哪些行被替换——否则模型会基于不完整 stack 给出不可执行的修复。

## 七、修完后的闭环

Debug 结束不要只 merge——让 AI 根据根因**起草一条回归测试**（系列⑥），人验收后再合。并在 PR 里贴**精简版四段式**，方便以后 search。

若根因是文档或配置误导，同步改 README 或 sample env，否则下一个同事还会贴同样的报错。Debug 的 Grounding 不只服务于当前对话，也服务于**下一次同类问题还能不能一键定位**——四段式模板值得存成 snippet。

## 八、小结

贴报错不是倾诉，是**提交证据包**。环境、对比、完整 stack、已尝试——四段齐，Debug 才从猜谜变成核对。这和 Grounding「找不到就停」是同一套纪律：**证据不够就补，不要先让模型猜修复**；修完后用回归测试把证据链闭环。下次同类报错，优先复用四段式模板，而不是从零描述——模板本身就是可复用的 Grounding 脚手架。团队 wiki 里存一份「好 paste 样例」，新人 Debug 时直接复制改字段，比培训会有效。好 paste 样例应来自真实 solved ticket，并定期更新 stack 格式——证据模板也要版本化。Stack 格式随框架升级会变，旧样例误导比没有样例更糟——这和 Grounding 文档版本同理。

（完）
