import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const blog = defineCollection({
  loader: glob({
    base: './src/content/blog',
    pattern: '**/*.md',
    // `foo.md` 与 `foo/index.md` 均生成 id `foo`，对应路由 /blog/foo/
    generateId: ({ entry }) => entry.replace(/(\/index)?\.md$/, ''),
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
