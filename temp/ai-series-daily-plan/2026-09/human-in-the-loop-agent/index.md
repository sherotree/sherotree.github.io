---
title: Agent 工程笔记⑪：人机协同——哪些步骤必须人工确认
date: 2026-09-26
description: 专栏「Agent 工程笔记」第十一篇：Human-in-the-loop 在 Agent 流程里落在哪些步骤，如何设计确认点。
tags: [AI, Agent, 系列]
series: agent-notes
draft: true
---

Human-in-the-loop（HITL，人机协同）不是「每个按钮都人点」，而是：**在不可逆或高风险动作前，刻意插入可暂停、可驳回的确认点**。Agent 可以自动查、自动写草稿；发邮件、合并代码、扣款应默认等人拍板。

全自动很炫，一旦误操作，成本远高于多一次点击。HITL 的设计问题是：确认什么、展示什么、超时怎么办。

下面是我整理的 HITL 落点：确认类型、界面信息与流程嵌入。

HITL 不是产品经理多加一个弹窗：它是安全架构的一部分。没有确认门的对外动作，等于把 OAuth 令牌交给不可信脚本随便花。

![人工确认门在流程中的位置](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/approval-gate_3RF2aXXA4k.png)

## 一、先说一个具体麻烦

Coding Agent 自动开 PR 并 @ 全组 review。某次它改错了鉴权逻辑，PR 描述却写「修复登录问题，已通过本地测试」——**没有人看过 diff 就进入团队队列**。

事后大家花一小时 revert。根因不是模型能力，而是**写仓库权限与 merge 权限之间缺一道确认门**。

客服场景同理：Agent 草拟回复可以自动，「发送给外部客户」这一 click 必须让人看见收件人与附件清单。

## 二、哪些步骤必须 HITL

（1）**对外通信**：邮件、IM、客户工单回复。  
（2）**金钱与配额**：下单、退款、升配、删付费资源。  
（3）**权限变更**：加用户、改 IAM、发长期 token。  
（4）**不可逆写**：删数据、force push、生产配置发布。  
（5）**低置信高影响**：Grounding 未命中仍建议执行的操作，见系列第九篇。

只读检索、本地草稿、预览模式通常不必每次确认；但用户应能**随时打断**自动循环。

![HITL 多检查点工作流](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/hitl-workflow_26PO2rUS6.png)

## 三、确认界面应展示什么

人无法在空白对话框里做判断。有效确认至少包含：

（1）**将要执行的原子动作**（工具名 + 关键参数）  
（2）**差异或摘要**（邮件正文预览、文件 diff 统计）  
（3）**影响范围**（收件人列表、目标环境 prod/staging）  
（4）**允许的操作**：批准 / 编辑后批准 / 拒绝 / 稍后

编辑后批准尤其重要：用户改一句收件人或金额，Agent 应拿**编辑后的 payload** 执行，而不是仍用原计划 silently 落地。

拒绝时 Observe 应写 `user_rejected`，Plan 下一轮改方案或询问，而不是悄悄重试同一 call。

## 四、状态机嵌入示例

```python
def act_with_hitl(plan, risk_level):
    if risk_level >= "L2":
        ticket = create_approval(plan.summary, plan.diff_preview)
        state = wait_for_user(ticket, timeout=3600)
        if state == "rejected":
            return {"ok": False, "error": "user_rejected"}
        if state == "edited":
            plan = apply_user_edits(plan, ticket.edits)
    return run_tool(plan.tool, plan.args)
```

上面代码中，`risk_level` 与系列第十篇权限分级对齐；`timeout` 到期应 fail closed（不执行），而非默认批准。

超时后的 UX 也要讲清楚：是「已取消」还是「仍可在工单里稍后批」，别让用户以为动作已经悄悄执行了。

## 五、与 Plan-Act-Observe 的配合

HITL 插在 **Act 之前**，不是事后补救。Plan 阶段可标注 `requires_approval: true`，宿主 UI 在流式界面里显示「等待确认」——见系列第十二篇。

批量任务可「一次批准多步计划」，但每步风险累加时要拆批，避免用户对着笼统「执行 12 个工具」点 OK。

对熟手用户可配置「记住本次会话对 L1 写操作不再询问」，但 L2 对外动作仍应每次确认——默认安全，而不是默认方便。

## 六、常见误区

（1）**确认框只写「Agent 想要执行操作」**  
信息不足等于形式主义。  
（2）**拒绝后 Agent 立即重试同一动作**  
应退回到 Plan 或结束。  
（3）**所有步骤都 HITL**  
用户疲劳后会无脑点通过，反而更危险。  
（4）**异步确认无状态**  
刷新页面后 pending 任务丢失。  
（5）**HITL 只在前端拦，后端不验**  
恶意客户端可绕过 UI 直接调 API。

确认记录也应入库：谁批、何时批、批之前 diff 长什么样。争议发生时，这是比聊天截图更干净的证据链。

对团队内部工具，可以把「低风险 L1 写操作默认自动、L2 起强制 HITL」写进角色策略，而不是所有用户同一套门槛。

## 七、小结与系列导航

HITL 的本质：**把不可逆决策交还给人，Agent 负责准备可判断的摘要**。权限划定红线（系列第十篇），HITL 在红线上加门；流式 UI 让用户看见「正在等什么」。宁可多一次确认，也不要在事故邮件里解释「模型误触发了生产」。

培训用户时强调：拒绝不是失败，而是把方向盘夺回来——Agent 应礼貌地进入 replan，而不是反复弹同一确认骚扰人。

移动端 HITL 要防误触：批准按钮与关闭按钮分开、关键动作二次确认，避免口袋模式帮你在生产点通过。

Night shift 场景还要考虑审批人不在线：超时策略与升级值班路由，应写进 runbook 而不是临时拍脑袋。

上一篇预告：权限与沙箱——工具能碰什么边界。  
下一篇预告：流式 UI——用户怎么感知 Agent 在工作。

（完）
