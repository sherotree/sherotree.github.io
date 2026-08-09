# AGENTS Instructions

本仓库为个人技术博客（GitHub Pages）。Agent 改稿、选题、排版时优先遵循下列约定。

## Rules Index

- 中文技术文风：`.agents/skills/ruanyifeng-tech-writing/SKILL.md`
- 选题与分发：`docs/plans/content-plan-3months.md`
- 建站档案：`docs/plans/chinese-blog-github-pages.md`
- 周刊副线：`docs/plans/ai-dev-digest-weekly.md`

## 内容约定

1. **母稿唯一位置**：`src/content/blog/{slug}/index.md`（配图放同目录 `images/`）。
2. 新增文章填 frontmatter（`title` / `date` / `description` / `tags` / 可选 `series` / `draft`）；正文从 `##` 起写，不要再写与 `title` 重复的一级标题。
3. 专栏取值：`browser-graphics`（浏览器里的图形）或 `agent-notes`（Agent 工程笔记）。
4. 站点文案为中文；导流纪律以 `docs/plans/content-plan-3months.md` 为准（分阶段）。
5. 本地验证：`npm run build`。
