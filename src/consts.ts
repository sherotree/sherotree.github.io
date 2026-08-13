export const SITE_URL = 'https://sherotree.github.io';
export const SITE_TITLE = 'sherotree 的网络日志';
export const SITE_DESCRIPTION = '把复杂技术讲清楚';
export const AUTHOR = 'sherotree';
export const GITHUB_URL = 'https://github.com/sherotree';
export const REPO_URL = 'https://github.com/sherotree/sherotree.github.io';
/** 与产品站共用的 GA4 Measurement ID */
export const GA_MEASUREMENT_ID = 'G-DTQJMNLS97';

export const SERIES: Record<string, { title: string; description: string }> = {
  'browser-graphics': {
    title: '浏览器里的图形',
    description: 'Canvas、像素与矢量：讲清浏览器图形的通用原理。',
  },
  'agent-notes': {
    title: 'Agent 工程笔记',
    description: '工具调用、上下文管理与评测：Agent 工程的实践笔记。',
  },
};

export function formatDate(date: Date): string {
  return `${date.getUTCFullYear()}年${date.getUTCMonth() + 1}月${date.getUTCDate()}日`;
}
