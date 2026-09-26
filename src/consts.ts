export const SITE_URL = 'https://sherotree.github.io';
export const SITE_TITLE = 'sherotree 的网络日志';
export const SITE_DESCRIPTION = '把复杂技术讲清楚';
export const AUTHOR = 'sherotree';
export const GITHUB_URL = 'https://github.com/sherotree';
export const REPO_URL = 'https://github.com/sherotree/sherotree.github.io';
/** 与产品站共用的 GA4 Measurement ID */
export const GA_MEASUREMENT_ID = 'G-DTQJMNLS97';

/**
 * 第三方分发渠道（与 `src/content/blog/{platform}/` 目录一一对应）。
 * 母稿一文只归属一个渠道；本站统一以 `/blog/{slug}/` 展示。
 */
export const PLATFORMS = {
  csdn: {
    title: 'CSDN',
    description: '搜索长尾与教程完整度优先的分发渠道母稿。',
  },
  cnblogs: {
    title: '博客园',
    description: '长文与工程向读者优先的分发渠道母稿。',
  },
} as const;

export type Platform = keyof typeof PLATFORMS;
export const PLATFORM_IDS = Object.keys(PLATFORMS) as Platform[];

export const SERIES: Record<string, { title: string; description: string }> = {
  'browser-graphics': {
    title: '浏览器里的图形',
    description: 'Canvas、像素与矢量：讲清浏览器图形的通用原理。',
  },
  'agent-notes': {
    title: 'Agent 工程笔记',
    description: '工具调用、上下文管理与评测：Agent 工程的实践笔记。',
  },
  'understanding-ai': {
    title: '理解 AI',
    description: '把模型与系统里的关键概念讲清楚。',
  },
  'ai-coding-workflow': {
    title: 'AI 编程效率',
    description: '编辑器 Agent、规则与工作流：把 AI 编程用稳。',
  },
};

export function formatDate(date: Date): string {
  return `${date.getUTCFullYear()}年${date.getUTCMonth() + 1}月${date.getUTCDate()}日`;
}

/** 从母稿路径解析分发渠道：`src/content/blog/{platform}/...` */
export function getPostPlatform(post: { filePath?: string }): Platform | undefined {
  if (!post.filePath) return undefined;
  const match = post.filePath.match(/(?:^|\/)content\/blog\/([^/]+)\//);
  const id = match?.[1];
  if (id && id in PLATFORMS) return id as Platform;
  return undefined;
}
