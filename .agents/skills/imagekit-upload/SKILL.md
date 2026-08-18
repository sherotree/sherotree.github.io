---
name: imagekit-upload
description: Upload images (and other media) to ImageKit.io Media Library via server-side Upload File V2 API (POST /api/v2/files/upload), return CDN URLs, and optionally apply URL-based transforms. Use when the user asks to upload to ImageKit, ImageKit CDN, ik.imagekit.io, or host/optimize images with ImageKit.
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
```

Or raw curl:

```bash
curl -sS -X POST "https://upload.imagekit.io/api/v2/files/upload" \
  -u "$IMAGEKIT_PRIVATE_KEY:" \
  -F "file=@./photo.jpg" \
  -F "fileName=photo.jpg" \
  -F "folder=/uploads"
```

## Agent workflow

1. Ensure `IMAGEKIT_PRIVATE_KEY` exists in process env, or in the app's `.env` / `.env.local`. If the app is not under cwd, pass `--env-dir`.
2. Prefer `scripts/upload.py` over ad-hoc code.
3. Pass a local path or `https://` URL as `source`.
4. If the user names a folder (e.g. `/blog`, `assets/hero`), pass it as positional folder or `-f/--folder`. Paths are normalized to start with `/`.
5. Return at least: `url`, `fileId`, `name`, `filePath` from the JSON response.
6. Do **not** print or commit the private key.

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
| `--format url` | Print only the CDN `url` |
| `--env-dir DIR` | Also load `.env` / `.env.local` from `DIR` (repeatable) |

## Response fields (common)

```json
{
  "fileId": "...",
  "name": "photo.jpg",
  "url": "https://ik.imagekit.io/id/path/photo.jpg",
  "thumbnailUrl": "https://ik.imagekit.io/id/...",
  "filePath": "/path/photo.jpg",
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
  fileName: "photo.jpg",
  folder: "/uploads",
});

// V1 still available as client.files.upload(...)
```

For one-off agent uploads, still use `scripts/upload.py`.

## References

- Platform: https://imagekit.io/
- Upload File V2: https://imagekit.io/docs/api-reference/upload-file/upload-file-v2
- API keys: https://imagekit.io/docs/api-keys
- Node SDK: https://github.com/imagekit-developer/imagekit-nodejs
