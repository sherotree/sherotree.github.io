import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const blog = defineCollection({
  loader: glob({
    base: './src/content/blog',
    pattern: '**/*.md',
    // 目录可为 `slug/` 或 `YYYY-MM/slug/`；id 始终取末段 slug，路由 /blog/{slug}/
    generateId: ({ entry }) => {
      const withoutExt = entry.replace(/(\/index)?\.md$/, '');
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
    series: z.enum(['browser-graphics', 'agent-notes']).optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
