#!/usr/bin/env node
/**
 * 导出 CSDN 分发稿：去掉 frontmatter，把 ./images/ 换成 jsDelivr 绝对链接，
 * 写入 dist-publish/csdn/；单篇时默认复制到剪贴板。
 *
 * 用法:
 *   npm run export:csdn -- src/content/blog/2026-08/understanding-moe
 *   npm run export:csdn -- understanding-moe
 *   npm run export:csdn -- src/content/blog/2026-08          # 整月
 *   npm run export:csdn -- 2026-08                           # 整月简写
 *   npm run export:csdn -- src/content/blog                  # 全部
 */

import { spawnSync } from 'node:child_process';
import {
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  statSync,
  writeFileSync,
} from 'node:fs';
import { basename, dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const BLOG_ROOT = join(ROOT, 'src/content/blog');
const OUT_DIR = join(ROOT, 'dist-publish/csdn');
const OWNER_REPO = 'sherotree/sherotree.github.io';
const DEFAULT_REF = 'main';

const IMAGE_MD_RE =
  /!\[([^\]]*)\]\((\.\/)?images\/([^)\s]+)(\s+"[^"]*")?\)/g;

function usage(exitCode = 1) {
  console.error(`用法:
  npm run export:csdn -- <文章|月份目录|blog 根> [--ref <git-ref>] [--no-clipboard] [--out <path>]

示例:
  npm run export:csdn -- understanding-moe
  npm run export:csdn -- src/content/blog/2026-08/understanding-moe
  npm run export:csdn -- 2026-08
  npm run export:csdn -- src/content/blog/2026-08
  npm run export:csdn -- src/content/blog
`);
  process.exit(exitCode);
}

function parseArgs(argv) {
  const args = { target: null, ref: DEFAULT_REF, clipboard: true, out: null };
  const positional = [];

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--help' || a === '-h') usage(0);
    if (a === '--no-clipboard') {
      args.clipboard = false;
      continue;
    }
    if (a === '--ref') {
      args.ref = argv[++i];
      continue;
    }
    if (a === '--out') {
      args.out = argv[++i];
      continue;
    }
    if (a.startsWith('-')) {
      console.error(`未知参数: ${a}`);
      usage(1);
    }
    positional.push(a);
  }

  if (positional.length !== 1) usage(1);
  args.target = positional[0];
  return args;
}

function parseFrontmatter(raw) {
  if (!raw.startsWith('---\n') && !raw.startsWith('---\r\n')) {
    return { data: {}, body: raw };
  }
  const end = raw.indexOf('\n---', 3);
  if (end === -1) return { data: {}, body: raw };

  const fm = raw.slice(4, end).trim();
  const body = raw.slice(end + 4).replace(/^\r?\n/, '');
  const data = {};

  for (const line of fm.split(/\r?\n/)) {
    const m = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!m) continue;
    const key = m[1];
    let value = m[2].trim();
    if (value.startsWith('[') && value.endsWith(']')) {
      value = value
        .slice(1, -1)
        .split(',')
        .map((s) => s.trim().replace(/^["']|["']$/g, ''))
        .filter(Boolean);
    } else {
      value = value.replace(/^["']|["']$/g, '');
    }
    data[key] = value;
  }

  return { data, body };
}

function isPostDir(dir) {
  return existsSync(join(dir, 'index.md'));
}

function listPostDirsIn(dir) {
  if (!existsSync(dir) || !statSync(dir).isDirectory()) return [];
  return readdirSync(dir)
    .map((name) => join(dir, name))
    .filter((p) => statSync(p).isDirectory() && isPostDir(p))
    .sort();
}

/** 收集目标下全部文章目录（单篇则为长度 1） */
function resolvePostDirs(target) {
  const abs = resolve(process.cwd(), target);

  if (existsSync(abs)) {
    if (statSync(abs).isFile() && basename(abs) === 'index.md') {
      return [dirname(abs)];
    }
    if (statSync(abs).isDirectory()) {
      if (isPostDir(abs)) return [abs];

      // 月份目录：直接子目录是文章
      const direct = listPostDirsIn(abs);
      if (direct.length) return direct;

      // blog 根：YYYY-MM/*/index.md
      const nested = [];
      for (const name of readdirSync(abs).sort()) {
        const child = join(abs, name);
        if (!statSync(child).isDirectory()) continue;
        nested.push(...listPostDirsIn(child));
      }
      if (nested.length) return nested;
    }
  }

  // YYYY-MM 简写
  if (/^\d{4}-\d{2}$/.test(target)) {
    const monthDir = join(BLOG_ROOT, target);
    const posts = listPostDirsIn(monthDir);
    if (posts.length) return posts;
    console.error(`月份目录为空或不存在: ${relative(ROOT, monthDir)}`);
    process.exit(1);
  }

  // slug-only：在 blog 下按目录名查找
  const slug = target.replace(/\/+$/, '').split('/').pop();
  const hits = [];
  for (const month of readdirSync(BLOG_ROOT)) {
    const monthDir = join(BLOG_ROOT, month);
    if (!statSync(monthDir).isDirectory()) continue;
    const candidate = join(monthDir, slug);
    if (isPostDir(candidate)) hits.push(candidate);
  }

  if (hits.length === 1) return hits;
  if (hits.length > 1) {
    console.error(`找到多个同名文章，请写完整路径:\n${hits.join('\n')}`);
    process.exit(1);
  }

  console.error(`找不到文章或目录: ${target}`);
  process.exit(1);
}

function toJsdelivrUrl(repoRelPath, ref) {
  const encoded = repoRelPath
    .split('/')
    .map((seg) => encodeURIComponent(seg))
    .join('/');
  return `https://cdn.jsdelivr.net/gh/${OWNER_REPO}@${ref}/${encoded}`;
}

function rewriteImages(body, postDir, ref) {
  const missing = [];
  const rewritten = body.replace(
    IMAGE_MD_RE,
    (_full, alt, _dot, file, title = '') => {
      const local = join(postDir, 'images', file);
      if (!existsSync(local)) missing.push(file);
      const repoRel = relative(ROOT, local).split('\\').join('/');
      const url = toJsdelivrUrl(repoRel, ref);
      return `![${alt}](${url}${title || ''})`;
    },
  );
  return { rewritten, missing };
}

function copyToClipboard(text) {
  if (process.platform === 'darwin') {
    const r = spawnSync('pbcopy', [], { input: text, encoding: 'utf8' });
    return r.status === 0;
  }
  if (process.platform === 'win32') {
    const r = spawnSync('clip', [], { input: text, encoding: 'utf8' });
    return r.status === 0;
  }
  for (const cmd of [
    ['wl-copy'],
    ['xclip', '-selection', 'clipboard'],
  ]) {
    const r = spawnSync(cmd[0], cmd.slice(1), {
      input: text,
      encoding: 'utf8',
    });
    if (r.status === 0) return true;
  }
  return false;
}

function exportOne(postDir, { ref, outPath }) {
  const mdPath = join(postDir, 'index.md');
  const slug = basename(postDir);
  const raw = readFileSync(mdPath, 'utf8');
  const { data, body } = parseFrontmatter(raw);
  const { rewritten, missing } = rewriteImages(body, postDir, ref);

  const title = typeof data.title === 'string' ? data.title.trim() : '';
  const output = title ? `# ${title}\n\n${rewritten}` : rewritten;

  mkdirSync(dirname(outPath), { recursive: true });
  writeFileSync(outPath, output, 'utf8');

  const imgCount = [...rewritten.matchAll(/!\[/g)].length;
  return { slug, title, data, output, missing, imgCount, outPath };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const postDirs = resolvePostDirs(args.target);
  const batch = postDirs.length > 1;

  // 批量时剪贴板只能放一篇，默认跳过；单篇仍可复制
  const useClipboard = args.clipboard && !batch;

  if (batch && args.out && !args.out.endsWith('.md')) {
    // --out 当作输出目录
  } else if (batch && args.out?.endsWith('.md')) {
    console.error('批量导出时 --out 请指定目录，而不是单个 .md 文件');
    process.exit(1);
  }

  const results = [];
  for (const postDir of postDirs) {
    const slug = basename(postDir);
    let outPath;
    if (args.out) {
      const absOut = resolve(process.cwd(), args.out);
      outPath = batch || !args.out.endsWith('.md')
        ? join(absOut, `${slug}.md`)
        : absOut;
    } else {
      outPath = join(OUT_DIR, `${slug}.md`);
    }

    const result = exportOne(postDir, { ref: args.ref, outPath });
    results.push(result);

    console.log(`已导出: ${relative(ROOT, result.outPath)}`);
    if (result.title) console.log(`  标题: ${result.title}`);
    else console.warn('  警告: frontmatter 缺少 title');
    if (result.data.tags) {
      const tags = Array.isArray(result.data.tags)
        ? result.data.tags.join(', ')
        : result.data.tags;
      console.log(`  标签: ${tags}`);
    }
    console.log(`  图片: ${result.imgCount} 张 → jsDelivr @${args.ref}`);
    if (result.missing.length) {
      console.warn(`  警告: 本地缺失图片: ${result.missing.join(', ')}`);
    }
  }

  console.log(
    `\n合计 ${results.length} 篇。提示: 图片需已 push 到远程对应 ref，jsDelivr 才能访问。`,
  );

  if (batch && args.clipboard) {
    console.log('批量导出已跳过剪贴板（请打开 dist-publish/csdn/ 分别复制）。');
  }

  if (useClipboard) {
    const { output } = results[0];
    if (copyToClipboard(output)) {
      console.log('已复制到剪贴板，可直接粘贴到 CSDN Markdown 编辑器。');
    } else {
      console.warn('未能写入剪贴板，请手动打开导出文件复制。');
    }
  }
}

main();
