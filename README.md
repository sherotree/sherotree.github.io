# sherotree.github.io

个人技术博客，目标是「把复杂技术讲清楚」。基于 [Astro](https://astro.build/) 构建，部署在 GitHub Pages：<https://sherotree.github.io>

## 本地开发

```bash
npm install
npm run dev       # 本地预览 http://localhost:4321
npm run build     # 构建静态站点到 dist/
npm run preview   # 预览构建产物
```

## 如何新增一篇文章

1. 在 `src/content/blog/` 下新建 `文章-slug.md`，或带图时新建目录 `文章-slug/index.md`（配图放同目录 `images/` 中，正文用相对路径引用）。
2. 填写 frontmatter：

```yaml
---
title: 理解上下文窗口：token 到底在限制什么
date: 2026-08-12
updated:            # 可选，修订日期
description: 一句话摘要，用于列表与 SEO
tags: [AI, 基础概念]
series:             # 可选：browser-graphics | agent-notes
draft: false        # true 时不会构建
---
```

3. 正文从 `##` 二级标题开始写（一级标题由页面模板根据 `title` 渲染）。
4. push 到 `main`，GitHub Actions 自动构建并发布。

## 目录结构

```
src/
  content/blog/       # 文章母稿（权威归档）
  content.config.ts   # 内容集合与 frontmatter 校验
  layouts/            # 页面布局（含 BlogPosting JSON-LD）
  pages/              # 路由：/、/blog/、/series/、/about/
  styles/global.css
  consts.ts
docs/plans/           # 选题、建站档案、周刊副线
.agents/skills/       # 写作 skill（ruanyifeng-tech-writing）
public/robots.txt
.github/workflows/deploy.yml
AGENTS.md
```

选题与分发纪律见 [docs/README.md](./docs/README.md)。新增文章只往 `src/content/blog/` 写，不要写回其他仓库。

## 部署

仓库 Settings → Pages → Source 选择 **GitHub Actions**，之后每次 push `main` 自动上线。
