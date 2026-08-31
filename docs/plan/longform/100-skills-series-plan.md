# 每天一个 Agent Skill · 100 天挑战 · 总规划

> ⏸ **本期 P1 候选**（见 [`00-longform-shortform-focus.md`](../00-longform-shortform-focus.md)）  
> 等 P0 长文稳定约 4 周后，与 Vibecoding / 新站案例日拆 **三选一**再开；勿与 Reddit 日更叠满。
>
> 姊妹系列：`ai-series-plan.md` · `vibecoding-series-plan.md` · `tech-depth-series-plan.md` · `tech-crossover-series-plan.md` · `solopreneur-series-plan.md` · `new-site-case-studies-series-plan.md`
>
> 本系列定位：**围绕 skills.sh 生态**，每天挑一个真实 skill 实测、拆解、给出可复用 Prompt  
> 核心承诺：100 天读完，你的 Claude Code / Cursor 会像换了个人  
> 风格锚点：一个钩子 + 一次真实实测 + Prompt 模板 + 优缺点 + 该不该装，1500-2500 字/篇  
> 发布平台：X 中文圈（主，短平快）· 个人博客 · 小红书 · 公众号  
> 规模：14 周 × 7 天 = 98 天 + 收尾 2 天 = **100 篇**

---

## skills.sh 是什么

- **一句话**：AI Agent 的可安装能力包目录（`npx skills add owner/repo`）
- **支持的 Agent**：Claude Code / Cursor / Codex / GitHub Copilot / Windsurf / Gemini / Cline / AMP / Antigravity / OpenClaw
- **生态主要玩家**：
  - `mattpocock/skills`：TypeScript 教父的通用工作流（grill / tdd / handoff / triage）
  - `anthropics/skills`：官方（frontend-design / skill-creator / pptx / pdf）
  - `vercel-labs/agent-skills`：Vercel 出品（find-skills / react-best-practices）
  - `leonxlnx/taste-skill`：design taste 派
  - `heygen-com/hyperframes`：视频生成
  - `microsoft/azure-skills`：企业云
  - `obra/superpowers`：Agent 工作流哲学
  - `prisma/skills`、`supabase/agent-skills`、`firebase/agent-skills`：数据库
  - `juliusbrussee/caveman`：风格化输出

---

## 读者画像

| 项 | 内容 |
|---|---|
| 是谁 | Claude Code / Cursor / Codex 用户；技术型内容创作者 |
| 已经会 | 命令行、装过 CLI 工具、用过 AI 编辑器 |
| 想要 | 快速筛出真正有用的 skill，不用自己 100 天挨个试 |
| 不想看 | 「10 个必装 skill」这种拼盘、只有 README 复读 |

---

## 每篇结构模板

```
【钩子】(200 字)
一个反常识数字 / 一个使用前后对比 / 一个具体场景

【它做了什么】(300 字)
不是 README 翻译，是我用完之后的 mental model

【怎么装 · 怎么触发】(200 字)
npx skills add owner/repo
展示触发词 / 触发场景

【我实测】(500-800 字)
真实项目截图 + 完整对话记录 + 输出对比

【优缺点 · 替代品】(300 字)
什么场景真的省事，什么场景不如自己写
同类替代 skill

【结论：装不装】(200 字)
黄/红/绿 三档评价 + 推荐人群
```

---

## 14 周排期

```
Week 1   入门 & 生态             Day 1-7
Week 2   Mattpocock 通用工作流    Day 8-14
Week 3   Mattpocock 编码质量      Day 15-21
Week 4   前端 & 设计             Day 22-28
Week 5   高端视觉 / 品味          Day 29-35
Week 6   内容 / 营销 / 风格       Day 36-42
Week 7   Anthropic 官方          Day 43-49
Week 8   数据库 / 后端            Day 50-56
Week 9   Superpowers Agent 工作流 Day 57-63
Week 10  Vercel & 通用工具        Day 64-70
Week 11  视频 / 动效              Day 71-77
Week 12  音乐 / 图像              Day 78-84
Week 13  Enterprise / Cloud       Day 85-91
Week 14  Meta：自己写 skill       Day 92-98
Day 99   实测榜 · 我的 Top 30
Day 100  100 天复盘 + 生态未来
```

---

## 详细排期

### Week 1 · 入门 & 生态（Day 1-7）

| Day | 主题 |
|---|---|
| 1 | 什么是 Agent Skill：一个 npm 包能改变 AI 的世界观 |
| 2 | skills.sh 生态全景：谁在建、为什么建、赚不赚钱 |
| 3 | 一键安装：`npx skills add` 底层做了什么 |
| 4 | Skill 的四种形态：procedural / reference / workflow / meta |
| 5 | 我的 Claude Code / Cursor / Codex 配置全公开 |
| 6 | Skill 排行榜解读：Top 20 说明了什么 |
| 7 | 本周小结 + 下周预告 |

### Week 2 · Mattpocock 通用工作流（Day 8-14）

| Day | Skill | 一句话 |
|---|---|---|
| 8 | `grill-me` | 让 AI 反过来拷问你的方案 |
| 9 | `grill-with-docs` | 带文档一起拷问 |
| 10 | `tdd` | 强制先写测试再实现 |
| 11 | `improve-codebase-architecture` | 从整体架构层面重构 |
| 12 | `handoff` | 长会话压缩成交接文档 |
| 13 | `triage` | 面对一堆 issue 怎么排序 |
| 14 | `prototype` | 快速做实验性原型 |

### Week 3 · Mattpocock 编码质量（Day 15-21）

| Day | Skill | 一句话 |
|---|---|---|
| 15 | `codebase-design` | 项目结构规范化 |
| 16 | `diagnosing-bugs` | 系统化诊断 |
| 17 | `domain-modeling` | 领域建模引导 |
| 18 | `implement` | 从 spec 到实现 |
| 19 | `resolving-merge-conflicts` | 冲突解决 |
| 20 | `code-review` | AI 帮你 review 自己 |
| 21 | `teach` | 让 AI 解释代码给你听 |

### Week 4 · 前端 & 设计（Day 22-28）

| Day | Skill | 一句话 |
|---|---|---|
| 22 | `frontend-design` (anthropics) | 官方前端设计流程 |
| 23 | `vercel-react-best-practices` | Vercel 出品的 React 规范 |
| 24 | `shadcn` | shadcn/ui 官方 skill |
| 25 | `web-design-guidelines` | 通用网页设计准则 |
| 26 | `anti-ui-slop` | 反 AI 感、反模板感 |
| 27 | `impeccable` | 高完成度 UI 打磨 |
| 28 | `design-taste-frontend` | 设计品味养成 |

### Week 5 · 高端视觉 / 品味（Day 29-35）

| Day | Skill | 一句话 |
|---|---|---|
| 29 | `high-end-visual-design` | 高端感视觉 |
| 30 | `minimalist-ui` | 极简派 |
| 31 | `industrial-brutalist-ui` | 工业粗野派 |
| 32 | `brandkit` | 品牌资产整合 |
| 33 | `image-to-code` | 图 → 代码 |
| 34 | `extract-design-system` | 从产品截图逆向设计系统 |
| 35 | `ui-radar` | UI 巡检 |

### Week 6 · 内容 / 营销 / 风格（Day 36-42）

| Day | Skill | 一句话 |
|---|---|---|
| 36 | `copywriting` | 文案创作 |
| 37 | `content-strategy` | 内容策略 |
| 38 | `seo-audit` | SEO 巡检 |
| 39 | `marketing-psychology` | 营销心理学 |
| 40 | `caveman` | 洞穴人风格输出（本篇文章用的就是这个）|
| 41 | `caveman-commit` / `caveman-review` | commit / review 风格化 |
| 42 | `writing-skills` (obra) | 一般写作 |

### Week 7 · Anthropic 官方（Day 43-49）

| Day | Skill | 一句话 |
|---|---|---|
| 43 | `skill-creator` | 创建你自己的 skill |
| 44 | `pptx` | 生成 PPT |
| 45 | `pdf` | 生成 PDF |
| 46 | `docx` | 生成 Word |
| 47 | `xlsx` | 生成 Excel |
| 48 | `webapp-testing` | Web 应用测试 |
| 49 | 官方 skills 深度对比：什么时候用官方、什么时候用社区 |

### Week 8 · 数据库 / 后端（Day 50-56）

| Day | Skill | 一句话 |
|---|---|---|
| 50 | `supabase-postgres-best-practices` | Supabase 最佳实践 |
| 51 | `supabase` | Supabase 通用 |
| 52 | `prisma-database-setup` | Prisma 建库 |
| 53 | `prisma-client-api` | Prisma 客户端 |
| 54 | `firebase-basics` | Firebase 入门 |
| 55 | `firebase-auth-basics` | Firebase Auth |
| 56 | `firebase-hosting-basics` | Firebase Hosting |

### Week 9 · Superpowers Agent 工作流（Day 57-63）

| Day | Skill | 一句话 |
|---|---|---|
| 57 | `systematic-debugging` | 系统化 debug |
| 58 | `brainstorming` | 头脑风暴 |
| 59 | `writing-plans` | 写计划 |
| 60 | `executing-plans` | 执行计划 |
| 61 | `verification-before-completion` | 收尾前验证 |
| 62 | `test-driven-development` | TDD 派 |
| 63 | `subagent-driven-development` | Subagent 驱动开发 |

### Week 10 · Vercel & 通用工具（Day 64-70）

| Day | Skill | 一句话 |
|---|---|---|
| 64 | `find-skills` (Vercel) | Skill 发现器 |
| 65 | `agent-browser` (Vercel) | Agent 用的浏览器 |
| 66 | `vercel-composition-patterns` | React 组合模式 |
| 67 | `vercel-react-native-skills` | React Native 规范 |
| 68 | `playwright-cli` | Playwright 命令行 |
| 69 | `just-scrape` | 通用爬取 |
| 70 | `orca-cli` | orca 编排 |

### Week 11 · 视频 / 动效（Day 71-77）

| Day | Skill | 一句话 |
|---|---|---|
| 71 | `hyperframes-cli` | HeyGen Hyperframes CLI |
| 72 | `hyperframes-creative` | 创意生成 |
| 73 | `hyperframes-animation` | 动画 |
| 74 | `ai-video-generation` | 通用视频生成 |
| 75 | `ai-avatar-video` | AI 数字人视频 |
| 76 | `image-to-video` | 图 → 视频 |
| 77 | `video-edit` | 视频剪辑 |

### Week 12 · 音乐 / 图像（Day 78-84）

| Day | Skill | 一句话 |
|---|---|---|
| 78 | `ai-music` | AI 音乐 |
| 79 | `ai-image-generation` | AI 出图 |
| 80 | `relight` | 重打光 |
| 81 | `video-outpainting` | 视频外扩 |
| 82 | `talking-head-recut` | 数字人重剪 |
| 83 | `motion-graphics` | 动态图形 |
| 84 | `slideshow` | 幻灯片式视频 |

### Week 13 · Enterprise / Cloud（Day 85-91）

| Day | Skill | 一句话 |
|---|---|---|
| 85 | `microsoft-foundry` | 微软 AI 平台 |
| 86 | `azure-messaging` | Azure 消息 |
| 87 | `azure-rbac` | Azure 权限 |
| 88 | `azure-compute` | Azure 计算 |
| 89 | `azure-cost` | Azure 成本 |
| 90 | `entra-agent-id` | Agent 身份 |
| 91 | `sentry-cli` | 错误监控 |

### Week 14 · Meta：自己写 skill（Day 92-98）

| Day | 主题 |
|---|---|
| 92 | `writing-great-skills`：官方元技能拆解 |
| 93 | `write-a-skill`：另一派元技能对比 |
| 94 | `setup-matt-pocock-skills`：一次性装一整套 |
| 95 | 实战：从 0 写一个我自己的 skill |
| 96 | 实战：发布到 skills.sh 全流程 |
| 97 | 私有 skill vs 公开 skill：什么内容不该开源 |
| 98 | skill 版本管理、更新、废弃 |

### 收尾（Day 99-100）

| Day | 主题 |
|---|---|
| 99 | 100 天实测榜：我最爱用的 Top 30 / 最踩雷的 Top 5 |
| 100 | 100 天复盘：Agent Skills 生态未来 3 年会是什么样 |

---

## 与其他系列的关系

| 系列 | 定位 | 与本系列关系 |
|---|---|---|
| AI 系列 / 技术深度 | 底层原理 | 本系列是把原理转成日常工具的具体动作 |
| 技术破圈（小红书） | 传播 | 每一天的 skill 都能拆成一条小红书 / X thread |
| 一人公司 | 变现 | 100 天日更本身就是一次高强度自我 branding |

---

## 平台适配策略

| 平台 | 处理方式 |
|------|---------|
| X 中文圈（主） | 每天一条 thread（5-9 帖），主打「今天装了 X，感觉像装了 Y」 |
| 个人博客 | 主发布地，长文 + 截图 + 完整对话记录 |
| 小红书 | 每 5 天挑一篇拆成 9 图（爆款潜力最大） |
| 公众号 | 每周 1 篇「本周 skill 精选」 |
| YouTube / B 站 | 每周 1 期「本周 skill 实测」（可选） |

### X thread 模板

```
今天试了 <skill 名>。

一句话：<反常识总结>

装完之后我做了 <具体动作>，结果 <数字 / 对比截图>。

它做对了 3 件事：
1. ...
2. ...
3. ...

它做错了 2 件事：
1. ...
2. ...

推荐指数：X / 5
适合谁：...

全文博客：<链接>
```

---

## 日更 SOP（关键）

日更 100 天非常重、必须有 SOP：

| 时间 | 动作 |
|---|---|
| 前一天晚上 | 安装 skill、跑 1 个真实场景、截图存档 |
| 当天早上 30 分钟 | 按结构模板填内容、生成 X thread |
| 当天中午 | 发 X + 更博客 |
| 每周日 | 补拍视频（可选）、下周排期检查 |

### 断更保险

- **预写缓冲**：始终保持 3-5 天存稿
- **降级方案**：出差 / 生病时发「短版」（只保留「一句话 + 装不装」）
- **替补名单**：留 20 个后备 skill，主排期出问题时替换

---

## 进度追踪

| Week | 计划 | 已完成 | 进度 |
|---|---|---|---|
| 1 · 入门 & 生态 | 7 | 0 | ⬜ |
| 2 · Mattpocock 通用 | 7 | 0 | ⬜ |
| 3 · Mattpocock 质量 | 7 | 0 | ⬜ |
| 4 · 前端 & 设计 | 7 | 0 | ⬜ |
| 5 · 高端视觉 | 7 | 0 | ⬜ |
| 6 · 内容 / 营销 | 7 | 0 | ⬜ |
| 7 · Anthropic 官方 | 7 | 0 | ⬜ |
| 8 · 数据库 / 后端 | 7 | 0 | ⬜ |
| 9 · Superpowers | 7 | 0 | ⬜ |
| 10 · Vercel & 工具 | 7 | 0 | ⬜ |
| 11 · 视频 / 动效 | 7 | 0 | ⬜ |
| 12 · 音乐 / 图像 | 7 | 0 | ⬜ |
| 13 · Enterprise | 7 | 0 | ⬜ |
| 14 · Meta 自建 | 7 | 0 | ⬜ |
| 收尾 | 2 | 0 | ⬜ |
| **合计** | **100** | **0** | **0%** |

---

## 下一步待办

- [ ] 目录约定（如 `202609/100-skills/day-01-what-is/`）
- [ ] 建立「skill 实测账户」：Cursor + Claude Code + Codex 三个空项目做统一测试
- [ ] Day 1-3 详细稿（提前 3 天存稿再上线）
- [ ] X 账号定位 + 前 10 条 thread 提前排版
- [ ] 系列封面 / 每日大图模板（含 Day XX / 100 编号）
- [ ] Landing page：`100skills.你的域名/`，把所有 skill 汇总，做 SEO
