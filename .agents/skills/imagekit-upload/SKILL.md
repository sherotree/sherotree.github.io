---
name: imagekit-upload
description: Upload images (and other media) to ImageKit.io Media Library via server-side Upload File V2 API (POST /api/v2/files/upload), return CDN URLs, and by default compress/resize plus convert PNG/JPG to WebP via ImageKit pre-transformation on upload (opt out with --no-compress / --image-format keep). Use when the user asks to upload to ImageKit, ImageKit CDN, ik.imagekit.io, or host/optimize images with ImageKit.
---

# ImageKit Upload

Upload local files or remote image URLs to [ImageKit](https://imagekit.io/) Media Library via **Upload File V2** (`POST /api/v2/files/upload`) and return the delivered CDN URL.

Server-side auth: HTTP Basic Auth with `IMAGEKIT_PRIVATE_KEY` (no JWT). JWT `token` is only for client-side uploads.

## Prerequisites

1. Create an account at https://imagekit.io/
2. Copy keys from https://imagekit.io/dashboard/developer/api-keys
3. Provide `IMAGEKIT_PRIVATE_KEY` via **one** of (priority high → low):

```bash
# A) process env
export IMAGEKIT_PRIVATE_KEY=private_xxx

# B) app .env / .env.local (preferred for this monorepo)
# e.g. apps/3005-ox/.env or apps/3005-ox/.env.local
IMAGEKIT_PRIVATE_KEY=private_xxx
```

Optional related keys:

```bash
IMAGEKIT_PUBLIC_KEY=public_xxx
IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/your_imagekit_id
IMAGEKIT_FOLDER=/uploads   # optional default Media Library folder
```

Credential / folder resolution in `scripts/upload.py`:

1. `IMAGEKIT_PRIVATE_KEY` / `IMAGEKIT_PRIVATE_API_KEY` in process env
2. Else scan cwd → parents (stops at git / pnpm workspace root) for `.env` then `.env.local` (`.env.local` wins)
3. Or pass `--env-dir apps/3005-ox` to force a directory
4. Folder: `--folder` / positional `folder` > `IMAGEKIT_FOLDER` / `IMAGEKIT_DEFAULT_FOLDER` in env/.env

Never commit private keys. Keep them server-side only.

## Quick Start

From this skill directory:

```bash
python3 scripts/upload.py ./photo.jpg
python3 scripts/upload.py ./photo.jpg /blog/covers
python3 scripts/upload.py ./photo.jpg -f /blog/covers --tags hero,cover
python3 scripts/upload.py ./photo.jpg --env-dir apps/3005-ox
python3 scripts/upload.py https://example.com/image.png --file-name cover.png
python3 scripts/upload.py ./logo.svg --format url
python3 scripts/upload.py ./hero.png /blog/2026/08 --quality 80
python3 scripts/upload.py ./hero.png --image-format keep
python3 scripts/upload.py ./hero.png --no-compress
python3 scripts/upload.py ./hero.png --pre "w-1200,q-75,f-jpg"
```

默认压缩，且 PNG/JPG 转 WebP（`w-1600,h-1600,c-at_max,q-82,f-webp`）。需要原图用 `--no-compress`；只要压缩不要转格式用 `--image-format keep`。

Or raw curl:

```bash
curl -sS -X POST "https://upload.imagekit.io/api/v2/files/upload" \
  -u "$IMAGEKIT_PRIVATE_KEY:" \
  -F "file=@./photo.jpg" \
  -F "fileName=photo.webp" \
  -F "folder=/uploads" \
  -F 'transformation={"pre":"w-1600,h-1600,c-at_max,q-82,f-webp"}'
```

## Agent workflow

1. Ensure `IMAGEKIT_PRIVATE_KEY` exists in process env, or in the app's `.env` / `.env.local`. If the app is not under cwd, pass `--env-dir`.
2. Prefer `scripts/upload.py` over ad-hoc code.
3. Pass a local path or `https://` URL as `source`.
4. If the user names a folder (e.g. `/blog`, `assets/hero`), pass it as positional folder or `-f/--folder`. Paths are normalized to start with `/`.
5. Compression is **on by default** (`w-1600,h-1600,c-at_max,q-82`). PNG/JPG also convert to WebP (`f-webp`, fileName suffix → `.webp`). Only pass `--no-compress` for lossless/original, or `--image-format keep` to compress without format conversion. Do **not** compress locally with Pillow/sips — use the Upload API `transformation.pre`.
6. Return at least: `url`, `fileId`, `name`, `filePath`, and if present `size` / `transformation.pre`.
7. Do **not** print or commit the private key.

## Script options

| Flag | Meaning |
| --- | --- |
| `source` | Local file path or remote `http(s)` URL |
| `folder` (positional) | Optional destination folder, e.g. `/blog/covers` |
| `-f` / `--folder` | Same as positional folder (wins over positional / `IMAGEKIT_FOLDER`) |
| `--file-name` / `--name` | Override Media Library file name |
| `--tags` | Comma-separated tags |
| `--no-unique` | Do not append unique suffix |
| `--overwrite` | Overwrite same name in folder |
| `--private` | Mark file private |
| `--compress` / `--no-compress` | Pre-transform on by default; `--no-compress` keeps original |
| `--quality N` | Maps to `q-N` (default `82` when compressing) |
| `--max-width PX` | Maps to `w-*` (default `1600` when compressing) |
| `--max-height PX` | Maps to `h-*` (optional; with width uses `c-at_max`) |
| `--image-format` | Default: `webp` for png/jpg, else keep. `keep` / `auto` / `jpeg` / `webp` / `png` → ImageKit `f-*` |
| `--pre TRANSFORM` | Raw pre string; overrides the flags above |
| `--format url` | Print only the CDN `url` |
| `--env-dir DIR` | Also load `.env` / `.env.local` from `DIR` (repeatable) |

### Compression (ImageKit pre-transformation)

**On by default.** Uses Upload API field `transformation: { "pre": "..." }` — applied **before** the file is stored in the Media Library ([docs](https://imagekit.io/docs/dam/pre-and-post-transformation-on-upload)). Pass `--no-compress` to skip.

Default for PNG/JPG:

```text
w-1600,h-1600,c-at_max,q-82,f-webp
```

Other types (SVG、GIF、已是 WebP 等) 默认不加 `f-*`，只做尺寸与质量：

```text
w-1600,h-1600,c-at_max,q-82
```

- `c-at_max`：保持比例，装进盒子，**不放大**原图
- `q-82`：有损质量（与 ImageKit 默认优化同一套语法）
- PNG/JPG → 默认追加 `f-webp`，并把 `fileName` 后缀改为 `.webp`
- `--image-format keep`：压缩但不转格式；显式 `jpeg` / `png` / `auto` 等同理追加 `f-*`

Response echo:

```json
"transformation": { "pre": "w-1600,h-1600,c-at_max,q-82,f-webp" }
```

Compare `size` in the upload response to the local file to see savings. Pre-transform for images is synchronous.

## Response fields (common)

```json
{
  "fileId": "...",
  "name": "photo.webp",
  "url": "https://ik.imagekit.io/id/path/photo.webp",
  "thumbnailUrl": "https://ik.imagekit.io/id/...",
  "filePath": "/path/photo.webp",
  "fileType": "image",
  "height": 1200,
  "width": 800,
  "size": 12345
}
```

Use `url` for delivery. Store `fileId` if you may delete/update later.

## URL transforms (after upload)

Append path transforms to the delivered URL (no re-upload needed):

```text
https://ik.imagekit.io/<id>/tr:w-800,h-600,c-at_max,q-80,f-auto/<filePath>
```

Useful params:

| Param | Example | Purpose |
| --- | --- | --- |
| `w` / `h` | `w-800,h-600` | Resize |
| `c` | `c-maintain_ratio`, `c-at_max` | Crop/fit |
| `q` | `q-80` | Quality |
| `f` | `f-auto`, `f-webp` | Format |
| `bl` | `bl-10` | Blur |

Docs: https://imagekit.io/docs/image-transformation

## Security rules

- Never expose `IMAGEKIT_PRIVATE_KEY` in client code, commits, or chat logs.
- Server-side upload only with this skill (Basic auth = private key).
- For browser uploads, generate auth params on a backend; do not put the private key in the frontend.

## When integrating in Next.js / Node

Prefer the official SDK for app code:

```bash
npm i @imagekit/nodejs
```

```ts
import ImageKit from "@imagekit/nodejs";
import fs from "node:fs";

const client = new ImageKit({
  privateKey: process.env.IMAGEKIT_PRIVATE_KEY!,
});

// V2 (beta) — preferred to match this skill
const result = await client.beta.v2.files.upload({
  file: fs.createReadStream("./photo.jpg"),
  fileName: "photo.webp",
  folder: "/uploads",
  transformation: {
    pre: "w-1600,h-1600,c-at_max,q-82,f-webp",
  },
});

// V1 still available as client.files.upload(...)
```

For one-off agent uploads, still use `scripts/upload.py`.

## References

- Platform: https://imagekit.io/
- Upload File V2: https://imagekit.io/docs/api-reference/upload-file/upload-file-v2
- Pre & post upload transformation: https://imagekit.io/docs/dam/pre-and-post-transformation-on-upload
- API keys: https://imagekit.io/docs/api-keys
- Node SDK: https://github.com/imagekit-developer/imagekit-nodejs
