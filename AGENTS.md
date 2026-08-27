# AGENTS Instructions

本仓库为个人技术博客（GitHub Pages）。Agent 改稿、选题、排版时优先遵循下列约定。

## Rules Index

- 中文技术文风：`.agents/skills/ruanyifeng-tech-writing/SKILL.md`
- 选题与分发：`docs/plans/content-plan-3months.md`
- 建站档案：`docs/plans/chinese-blog-github-pages.md`
- 周刊副线：`docs/plans/ai-dev-digest-weekly.md`
- AI 三系列日更：`docs/plans/ai-series-daily-plan.md`

## 内容约定

1. **母稿唯一位置**：`src/content/blog/{YYYY-MM}/{slug}/index.md`（配图放同目录 `images/`；`YYYY-MM` 取 `date` 的年月）。路由仍为 `/blog/{slug}/`，与月份目录无关。
2. 新增文章填 frontmatter（`title` / `date` / `description` / `tags` / 可选 `series` / `draft`）；正文从 `##` 起写，不要再写与 `title` 重复的一级标题。
3. **发布闸门**：未到发布周的稿保持 `draft: true`（不进站点列表与详情）；当周要发的改 `draft: false` 再 push `main`，并同步六站。勿一次性把囤稿全部公开。
4. 专栏取值：`browser-graphics`（浏览器里的图形）、`agent-notes`（Agent 工程笔记）、`understanding-ai`（理解 AI）、`ai-coding-workflow`（AI 编程效率）。
5. 站点文案为中文；导流纪律以 `docs/plans/content-plan-3months.md` 为准（分阶段）。
6. 本地验证：`npm run build`。
