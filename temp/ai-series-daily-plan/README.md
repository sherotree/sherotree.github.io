# AI 三系列待写骨架（暂存）

本目录存放 [`docs/plans/ai-series-daily-plan.md`](../../docs/plans/ai-series-daily-plan.md) 对应的 **51 篇**母稿，全部为 `draft: true`。

**不要**放在 `src/content/blog/` 下，避免 Astro 构建扫描与误发布。

## 进度

| 月份 | 篇数 | 状态 |
|------|------|------|
| `2026-09/` | 26 | **正文已完成**（阮一峰文风 + 手绘风配图 + ImageKit CDN） |
| `2026-10/` | 24 | 骨架占位「（正文待写）」 |
| `2026-11/` | 1 | 骨架占位「（正文待写）」 |

## 移回正式目录

单篇移回：

```bash
mv temp/ai-series-daily-plan/2026-09/{slug} src/content/blog/2026-09/
```

批量移回某月：

```bash
cp -R temp/ai-series-daily-plan/2026-09/* src/content/blog/2026-09/
```

移回后执行 `npm run build` 验证。

## 目录结构

与 `src/content/blog/{YYYY-MM}/{slug}/index.md` 相同，按排期月份分目录：

- `2026-09/` — 26 篇
- `2026-10/` — 24 篇
- `2026-11/` — 1 篇
