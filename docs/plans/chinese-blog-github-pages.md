# 中文个人技术博客（GitHub Pages）实施计划

> 状态：**已归档**（2026-08-09）——本文件留在博客仓库作建站记录；日常写稿与选题以 `src/content/blog/` + [content-plan-3months.md](./content-plan-3months.md) 为准  
> 关联：[content-plan-3months.md](./content-plan-3months.md)、[ai-dev-digest-weekly.md](./ai-dev-digest-weekly.md)  
> 对标：[阮一峰的个人网站](https://www.ruanyifeng.com/)  
> 托管：[GitHub Pages](https://pages.github.com/) · 仓库 https://github.com/sherotree/sherotree.github.io

## 一、目标与定位

| 项 | 决定 |
|----|------|
| 定位 | **对外主站**：母稿权威归档；六站分发后逐步导流回来 |
| 语言 / 文风 | 中文；`ruanyifeng-tech-writing` |
| 形态 | 极简个人站：首页目录 + 网络日志，非产品 landing |
| 代码 | 独立公开仓库，开源 |
| 部署 | GitHub Pages → `https://{username}.github.io` |
| 与 `one` monorepo | **已脱钩**：选题、母稿、写作 skill 均在本仓库；产品站仍在 `one` |

**为何不用本 monorepo + Vercel：** 个人技术博客与产品工具站品牌隔离；纯 Markdown 静态页不需要 SSR；`username.github.io` 是开源个人站的经典形态。

---

## 二、前置条件（执行前确认）

1. **GitHub 用户名** `{username}` → 仓库名必须为 `{username}.github.io`（用户站根域名硬约束）。
2. 本地已装 Node / Bun；可使用 `gh` CLI 创建仓库与开 Pages。
3. 自定义域名非首期必做；可后挂 CNAME。

---

## 三、技术选型（已定）

| 项 | 选择 | 原因 |
|----|------|------|
| 框架 | Astro + Content Collections + Markdown | 静态导出一流，写稿接近纯 Markdown |
| 部署 | GitHub Actions → GitHub Pages（官方 `actions/deploy-pages`） | push `main` 即发 |
| 样式 | 极简排版：可读行宽、高对比正文、少装饰 | 贴近阮式「目录站」 |
| 包管理 | bun 或 npm 均可 | 独立仓库，不跟 `one` 强制一致 |

不选 Next.js static export：对纯博客过重，Pages 上也无 ISR/SSR 收益。

---

## 四、信息架构

| 路由 | 用途 |
|------|------|
| `/` | 站名 + 一句话定位 + 入口（网络日志 / 系列 / 关于 / GitHub） |
| `/blog/` | 文章列表，按日期倒序；可选按月归档 |
| `/blog/{slug}/` | 单篇正文 |
| `/series/browser-graphics/` | 专栏「浏览器里的图形」 |
| `/series/agent-notes/` | 专栏「Agent 工程笔记」 |
| `/about/` | 关于与联系 |
| `/sitemap.xml`、`/robots.txt` | SEO |
| 每篇页内 | `BlogPosting` JSON-LD（中文 headline / description） |

### Frontmatter 约定

```yaml
---
title: 理解上下文窗口：token 到底在限制什么
date: 2026-08-12
updated: # 可选
description: 一句话摘要，用于列表与 SEO
tags: [AI, 基础概念]
series: # 可选：browser-graphics | agent-notes
draft: false
---
```

---

## 五、仓库目录骨架

独立 repo：`{username}.github.io`

```
src/
  content/blog/*.md          # 母稿（对接 3 个月约 36 篇）
  pages/ 或 src/pages/       # 路由
  layouts/BlogPost.astro
  styles/global.css
  consts.ts                  # SITE_TITLE、SITE_DESCRIPTION、GitHub URL
public/
  robots.txt                 # 或由集成生成
.github/workflows/deploy.yml
astro.config.mjs             # site: https://{username}.github.io
README.md                    # 开源说明 + 本地开发命令
```

视觉边界：

- 首页：站名（人设）+ 一句「把复杂技术讲清楚」+ 日志入口；无产品 hero / CTA 堆砌
- 正文：清晰标题层级与代码块；无卡片墙、无统计条
- 可选：按年/月归档页

---

## 六、内容工作流（对接选题计划）

```text
Markdown 母稿（本博客仓库）
        ├─► 博客上线（canonical）
        └─► 六站改编分发（掘金 / CSDN / 公众号 / …）
                    └─► 后期文末挂「完整版 / 归档」链回本站
```

1. 在博客仓库写/改 Markdown → 合并 `main` → Pages 上线。  
2. 同一母稿改编发六站（标题/标签按平台改；公众号删减版）。  
3. **导流节奏**（与「永久零软广」的衔接）：  
   - **第 1～6 周**：平台稿可不挂自有站链接，先养平台权重。  
   - **第 7 周起**：文末加一行「完整版 / 归档：https://{username}.github.io/blog/{slug}/」或系列索引。  
4. 执行本计划时，同步改 [content-plan-3months.md](./content-plan-3months.md)：写明主站 URL，并把硬约束从「永久不导流」改为上述分阶段导流。

---

## 七、执行清单（按顺序做）

### 阶段 A：仓库与脚手架

- [x] 确认 `{username}` = `sherotree`（远程仓库待用户创建，`gh` 未登录）
- [x] 脚手架（未走 `npm create astro`，直接手写最小 Astro 7 项目，无需再删 landing 组件）
- [x] 删掉多余 landing 组件，压成「目录站」（手写即为目录站形态）
- [x] 配置 `astro.config.mjs` 的 `site: 'https://sherotree.github.io'`

### 阶段 B：页面与排版

- [x] 实现 `/`、`/blog/`、`/blog/[slug]/`、`/about/`
- [x] 实现 `/series/browser-graphics/`、`/series/agent-notes/`（当前空列表，显示「筹备中」）
- [x] 中文 UI 文案；极简全局样式
- [x] 文章 layout：日期、标签、系列、正文；内嵌 `BlogPosting` JSON-LD
- [x] `sitemap`（`@astrojs/sitemap`）+ `robots.txt`（手写，指向 sitemap-index）

### 阶段 C：样例内容

- [x] 已放入 W1《理解上下文窗口：token 到底在限制什么》（含 3 图，构建时自动压为 WebP）
- [x] 本地 `astro build` 通过（6 页；h1 唯一、JSON-LD / canonical / sitemap 已验证）

### 阶段 D：部署

- [x] 添加 `.github/workflows/deploy.yml`（build + `actions/deploy-pages`）
- [ ] 仓库 Settings → Pages：Source = GitHub Actions（**待用户操作**）
- [ ] push `main`，确认 `https://sherotree.github.io` 可访问（**待用户操作**：创建远程仓库后 `git remote add origin git@github.com:sherotree/sherotree.github.io.git && git push -u origin main`）
- [x] README 写清：本地 `dev` / `build`、如何新增一篇文章

### 阶段 E：回写本仓库计划

- [x] 更新 [content-plan-3months.md](./content-plan-3months.md)：主站 URL + 分阶段导流
- [x] 本文件状态已更新；上线后可再补实际上线日期与仓库链接

---

## 八、首期明确不做

- 评论、站内搜索、账号体系  
- CMS / Sanity（母稿即 Git 内 Markdown）  
- 放进 `one/apps` 或 Vercel（日后若换自定义域名再评估）  
- 自定义域名（可后挂，不阻塞 `*.github.io` 上线）

---

## 九、验收标准

| 项 | 标准 |
|----|------|
| 可访问 | `https://{username}.github.io` 首页与样例文可打开 |
| 开源 | 仓库公开，README 可复现本地开发 |
| 结构 | 路由与系列页齐全，frontmatter 可支撑后续 36 篇 |
| SEO 底线 | sitemap、robots、文章 JSON-LD 存在 |
| 纪律对齐 | 内容计划已写明主站与导流节奏，不再与「永久零软广」冲突 |

---

## 十、执行时建议命令备忘

```bash
# 创建仓库（需已登录 gh）
gh repo create {username}.github.io --public --description "个人技术博客" --clone

cd {username}.github.io
npm create astro@latest . -- --template blog
# 按阶段 B～D 改代码后：
git add -A && git commit -m "feat: 初始化中文个人技术博客"
git push -u origin main
```

新增文章：在 `src/content/blog/` 增加 `.md`，填 frontmatter，push 即可。
