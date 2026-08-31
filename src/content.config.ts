import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

/** 第三方分发平台；一文只归属一个平台，由目录决定 */
export const PLATFORMS = ['csdn', 'cnblogs'] as const;
export type Platform = (typeof PLATFORMS)[number];

const blog = defineCollection({
  loader: glob({
    base: './src/content/blog',
    // 仅收录标准母稿；平台下的扁文件 / 计划稿（如 csdn 引流 md）不进站点
    pattern: '**/index.md',
    // 路径：`{platform}/{YYYY-MM}/{slug}/index.md`
    // id 始终取末段 slug，路由 /blog/{slug}/；slug 须跨平台唯一
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
