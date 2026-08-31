# AGENTS Instructions

本仓库为个人技术博客（GitHub Pages）。Agent 改稿、选题、排版时优先遵循下列约定。

## Rules Index

- 中文技术文风：`.agents/skills/ruanyifeng-tech-writing/SKILL.md`
- 选题与分发：`docs/plans/content-plan-3months.md`
- 建站档案：`docs/plans/chinese-blog-github-pages.md`
- 周刊副线：`docs/plans/ai-dev-digest-weekly.md`
- AI 三系列日更：`docs/plans/ai-series-daily-plan.md`

## 内容约定

1. **母稿按平台归档**：`src/content/blog/{platform}/{YYYY-MM}/{slug}/index.md`（配图放同目录 `images/`；`YYYY-MM` 取 `date` 的年月）。
   - 当前平台：`csdn`、`cnblogs`（后续可加，如 `zhihu`）。
   - **一文只归属一个第三方平台**；目录即归属，不要同一篇复制到多个平台目录。
   - `slug` 须跨平台唯一；站点路由仍为 `/blog/{slug}/`，与平台 / 月份目录无关。
2. 新增文章填 frontmatter（`title` / `date` / `description` / `tags` / 可选 `series` / `draft`）；正文从 `##` 起写，不要再写与 `title` 重复的一级标题。
3. **发布闸门**：未到发布周的稿保持 `draft: true`（不进站点列表与详情）；当周要发的改 `draft: false` 再 push `main`，并同步到该篇所属第三方平台。勿一次性把囤稿全部公开。
4. 专栏取值：`browser-graphics`（浏览器里的图形）、`agent-notes`（Agent 工程笔记）、`understanding-ai`（理解 AI）、`ai-coding-workflow`（AI 编程效率）。
5. 站点文案为中文；导流纪律以 `docs/plans/content-plan-3months.md` 为准（分阶段）。
6. **配图风格**：流程 / 架构 / 对比类示意图统一 **牛皮纸手账风**（米色底、虚线圆角卡片、铅笔线+淡彩、手写中文、少量星星/爱心 doodle）；主锚点为 `agent-tool-failure-three-layers` 配图。规范见 `.agents/skills/ruanyifeng-tech-writing/SKILL.md` 6.5。禁止 Mermaid 默认主题直接入稿。发布稿配图上传 ImageKit（`.agents/skills/imagekit-upload/SKILL.md`），正文用 CDN URL。
7. **CSDN 分发**：母稿在 `src/content/blog/csdn/`。向 CSDN 发布时一律**保留原文图片链接**（发布命令带 `--no-rehost-images`），不要重传图片到 CSDN CDN；发布方式默认私密草稿，除非用户明确要求公开发布。规则细则见 `.agents/skills/csdn/SKILL.md`。
8. **博客园分发**：母稿在 `src/content/blog/cnblogs/`（规划见 `docs/plan/cnblogs-agent-interview-calendar.md`）。
9. 本地验证：`npm run build`。
