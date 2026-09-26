import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

/** 第三方分发渠道目录名；一文只归属一个渠道，由路径决定，不在站点对读者展示 */
export const PLATFORMS = ['csdn', 'cnblogs'] as const;
export type Platform = (typeof PLATFORMS)[number];

const blog = defineCollection({
  loader: glob({
    base: './src/content/blog',
    // 仅收录标准母稿；渠道目录下的计划稿等扁文件不进站点
    pattern: '**/index.md',
    // 路径：`{platform}/{YYYY-MM}/{slug}/index.md`
    // id 始终取末段 slug，路由 /blog/{slug}/；slug 须跨渠道唯一
    generateId: ({ entry }) => {
      const withoutExt = entry.replace(/\/index\.md$/, '');
      const segments = withoutExt.split('/');
      return segments[segments.length - 1] ?? withoutExt;
    },
  }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    updated: z.coerce.date().optional(),
    description: z.string(),
    tags: z.array(z.string()).default([]),
    series: z
      .enum([
        'browser-graphics',
        'agent-notes',
        'understanding-ai',
        'ai-coding-workflow',
      ])
      .optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
