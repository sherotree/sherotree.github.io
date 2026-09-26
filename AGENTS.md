# AGENTS Instructions

本仓库为个人技术博客（GitHub Pages）。Agent 改稿、选题、排版时优先遵循下列约定。

## Rules Index

- 中文技术文风：`.agents/skills/ruanyifeng-tech-writing/SKILL.md`
- 选题与分发：`docs/plans/content-plan-3months.md`
- 建站档案：`docs/plans/chinese-blog-github-pages.md`
- 周刊副线：`docs/plans/ai-dev-digest-weekly.md`
- AI 三系列日更：`docs/plans/ai-series-daily-plan.md`

## 内容约定

1. **母稿按分发渠道归档**：`src/content/blog/{platform}/{YYYY-MM}/{slug}/index.md`（配图放同目录 `images/`；`YYYY-MM` 取 `date` 的年月）。
   - 当前渠道：`csdn`、`cnblogs`（后续可加，如 `zhihu`）。
   - **一文只归属一个第三方渠道**；目录即归属，不要同一篇复制到多个渠道目录。
   - 本站统一展示：路由 `/blog/{slug}/`（与渠道 / 月份目录无关）。渠道只用于仓库归档，不要在站点页面、列表或文章 meta 里对读者展示。
   - `slug` 须跨渠道唯一。
2. 新增文章填 frontmatter（`title` / `date` / `description` / `tags` / 可选 `series` / `draft`）；正文从 `##` 起写，不要再写与 `title` 重复的一级标题。
3. **正文只写给读者**。每一句都要帮读者理解、判断或动手。删掉对读者没有意义的话，也不要写出 AI 味。
   - 不写作者自评、写作动机、立场旁白（如「这个判断带偏见」「我这样写是因为」「对写简历的人可能不友好」）。判断要落成读者能用的结论。
   - 不写编辑过程、给模型的备注、发布说明、渠道归属。这些放 `docs/plans/` 或对话里，不进正文。
   - 不用套话和空泛拔高：如「值得注意的是」「不难发现」「在当今」「综上所述」「让我们」「赋能」「闭环式」「深度解析」。不用对称排比凑节奏，不用没有信息的形容词堆砌和营销腔。
4. **发布闸门**：未完成或暂不上线的稿用 `draft: true`（不进站点列表与详情）。本站公开的稿设 `draft: false`，并同步到该篇所属第三方渠道。计划稿、运营笔记不要放进 `{slug}/index.md`，放到 `docs/plans/`。
5. 专栏取值：`browser-graphics`（浏览器里的图形）、`agent-notes`（Agent 工程笔记）、`understanding-ai`（理解 AI）、`ai-coding-workflow`（AI 编程效率）。
6. 站点文案为中文；导流纪律以 `docs/plans/content-plan-3months.md` 为准（分阶段）。
7. **配图风格**：流程 / 架构 / 对比类示意图统一 **牛皮纸手账风**（米色底、虚线圆角卡片、铅笔线+淡彩、手写中文、少量星星/爱心 doodle）；主锚点为 `agent-tool-failure-three-layers` 配图。规范见 `.agents/skills/ruanyifeng-tech-writing/SKILL.md` 6.5。禁止 Mermaid 默认主题直接入稿。发布稿配图上传 ImageKit（`.agents/skills/imagekit-upload/SKILL.md`），正文用 CDN URL。
8. **CSDN 分发**：母稿在 `src/content/blog/csdn/`。向 CSDN 发布时一律**保留原文图片链接**（发布命令带 `--no-rehost-images`），不要重传图片到 CSDN CDN；发布方式默认私密草稿，除非用户明确要求公开发布。规则细则见 `.agents/skills/csdn/SKILL.md`。
9. **博客园分发**：母稿在 `src/content/blog/cnblogs/`（规划见 `docs/plan/cnblogs-agent-interview-calendar.md`）。
10. 本地验证：`npm run build`。
