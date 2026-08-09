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

1. 在 `src/content/blog/{YYYY-MM}/` 下新建 `文章-slug/index.md`（`YYYY-MM` 与 frontmatter `date` 年月一致；配图放同目录 `images/`，正文用相对路径引用）。
2. 填写 frontmatter：

```yaml
---
title: 理解上下文窗口：token 到底在限制什么
date: 2026-08-12
updated:            # 可选，修订日期
description: 一句话摘要，用于列表与 SEO
tags: [AI, 基础概念]
series:             # 可选：browser-graphics | agent-notes
draft: true         # 囤稿默认 true；发布周改为 false
---
```

3. 正文从 `##` 二级标题开始写（一级标题由页面模板根据 `title` 渲染）。
4. 发布：当周稿改 `draft: false` 后 push `main`，GitHub Actions 自动构建；站点 URL 为 `/blog/{slug}/`（不含月份路径）。

## 目录结构

```
src/
  content/blog/       # 文章母稿（按 YYYY-MM/slug/ 归档）
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

## 导出 CSDN 分发稿

把母稿里的 `./images/` 相对路径换成 jsDelivr 绝对链接，去掉 frontmatter，并复制到剪贴板：

```bash
npm run export:csdn -- src/content/blog/2026-08/understanding-moe
# 或按 slug：
npm run export:csdn -- understanding-moe
```

产物在 `dist-publish/csdn/{slug}.md`。可选参数：`--no-clipboard`、`--ref <git-ref>`（默认 `main`）。  
注意：图片需已 push 到对应远程分支，jsDelivr 才能访问。

## 部署

仓库 Settings → Pages → Source 选择 **GitHub Actions**，之后每次 push `main` 自动上线。
