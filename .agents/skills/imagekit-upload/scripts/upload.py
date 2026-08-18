#!/usr/bin/env python3
"""
Upload a local file or remote URL to ImageKit Media Library.

Usage:
  python3 scripts/upload.py ./photo.jpg
  python3 scripts/upload.py ./photo.jpg /blog/covers
  python3 scripts/upload.py ./photo.jpg --folder /blog --tags hero,cover
  python3 scripts/upload.py ./photo.jpg --env-dir apps/3005-ox
  python3 scripts/upload.py https://example.com/a.png --file-name cover.png
  python3 scripts/upload.py ./logo.svg --name brand-logo --no-unique

Reads IMAGEKIT_PRIVATE_KEY from process env, else .env / .env.local
(cwd → parents, or --env-dir). Optional default folder: IMAGEKIT_FOLDER.
"""
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import uuid
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

# Upload File V2 (beta): https://imagekit.io/docs/api-reference/upload-file/upload-file-v2
# Server-side: Basic Auth with private key. Client-side would use JWT `token` instead.
UPLOAD_ENDPOINT = "https://upload.imagekit.io/api/v2/files/upload"
KEY_NAMES = ("IMAGEKIT_PRIVATE_KEY", "IMAGEKIT_PRIVATE_API_KEY")
FOLDER_KEY_NAMES = ("IMAGEKIT_FOLDER", "IMAGEKIT_DEFAULT_FOLDER")
ENV_FILENAMES = (".env", ".env.local")


def _strip_quotes(value: str) -> str:
    text = value.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {"'", '"'}:
        return text[1:-1]
    return text


def parse_dotenv(path: Path) -> dict[str, str]:
    """Parse a simple KEY=VALUE .env file (no export/interpolation)."""
    values: dict[str, str] = {}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return values

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if not key:
            continue
        values[key] = _strip_quotes(value)
    return values


def candidate_env_dirs(extra_dirs: list[Path] | None = None) -> list[Path]:
    """cwd → parents, plus any explicit dirs (deduped, existing only)."""
    seen: set[Path] = set()
    dirs: list[Path] = []

    def add(path: Path) -> None:
        resolved = path.expanduser().resolve()
        if resolved in seen or not resolved.is_dir():
            return
        seen.add(resolved)
        dirs.append(resolved)

    for item in extra_dirs or []:
        add(item)

    cwd = Path.cwd()
    add(cwd)
    for parent in cwd.parents:
        add(parent)
        # Stop after repo-ish roots to avoid scanning the whole disk.
        if (parent / ".git").exists() or (parent / "pnpm-workspace.yaml").exists():
            break

    return dirs


def load_dotenv_files(extra_dirs: list[Path] | None = None) -> dict[str, str]:
    """
    Load .env then .env.local from each candidate dir.
    Later files / nearer dirs win: .env.local overrides .env; cwd overrides parents.
    """
    merged: dict[str, str] = {}
    # Parents first, then cwd last so nearer files win.
    for directory in reversed(candidate_env_dirs(extra_dirs)):
        for name in ENV_FILENAMES:
            path = directory / name
            if path.is_file():
                merged.update(parse_dotenv(path))
    return merged


def get_env_value(
    names: tuple[str, ...],
    extra_env_dirs: list[Path] | None = None,
) -> str:
    for name in names:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    file_env = load_dotenv_files(extra_env_dirs)
    for name in names:
        value = file_env.get(name, "").strip()
        if value:
            return value
    return ""


def get_private_key(extra_env_dirs: list[Path] | None = None) -> str:
    key = get_env_value(KEY_NAMES, extra_env_dirs)
    if not key:
        print(
            "error: IMAGEKIT_PRIVATE_KEY not found\n"
            "Set it in the environment, or in .env / .env.local:\n"
            "  IMAGEKIT_PRIVATE_KEY=private_xxx\n"
            "Keys: https://imagekit.io/dashboard/developer/api-keys\n"
            "Tip: run from the app directory, or pass --env-dir path/to/app",
            file=sys.stderr,
        )
        sys.exit(1)
    if not key.startswith("private_"):
        print(
            "warning: IMAGEKIT_PRIVATE_KEY usually starts with 'private_'",
            file=sys.stderr,
        )
    return key


def normalize_folder(folder: str | None) -> str | None:
    """Normalize Media Library folder to `/path` (no trailing slash except root)."""
    if folder is None:
        return None
    text = folder.strip()
    if not text or text == "/":
        return "/"
    text = text.replace("\\", "/")
    while "//" in text:
        text = text.replace("//", "/")
    if not text.startswith("/"):
        text = "/" + text
    return text.rstrip("/") or "/"


def resolve_folder(
    cli_folder: str | None,
    extra_env_dirs: list[Path] | None = None,
) -> str | None:
    """CLI --folder / positional > IMAGEKIT_FOLDER from env/.env."""
    if cli_folder and cli_folder.strip():
        return normalize_folder(cli_folder)
    from_env = get_env_value(FOLDER_KEY_NAMES, extra_env_dirs)
    if from_env:
        return normalize_folder(from_env)
    return None


def guess_filename(source: str, override: str | None) -> str:
    if override:
        return override
    if source.startswith(("http://", "https://")):
        path = urlparse(source).path
        name = Path(path).name or "upload.bin"
        return name
    return Path(source).name


def build_multipart(
    fields: dict[str, str],
    file_field: str | None,
    file_name: str | None,
    file_bytes: bytes | None,
    content_type: str | None,
) -> tuple[bytes, str]:
    boundary = f"----ImageKitBoundary{uuid.uuid4().hex}"
    lines: list[bytes] = []

    for key, value in fields.items():
        lines.append(f"--{boundary}".encode())
        lines.append(f'Content-Disposition: form-data; name="{key}"'.encode())
        lines.append(b"")
        lines.append(value.encode())

    if file_field and file_name is not None and file_bytes is not None:
        ctype = content_type or "application/octet-stream"
        lines.append(f"--{boundary}".encode())
        lines.append(
            (
                f'Content-Disposition: form-data; name="{file_field}"; '
                f'filename="{file_name}"'
            ).encode()
        )
        lines.append(f"Content-Type: {ctype}".encode())
        lines.append(b"")
        lines.append(file_bytes)

    lines.append(f"--{boundary}--".encode())
    lines.append(b"")
    body = b"\r\n".join(lines)
    return body, f"multipart/form-data; boundary={boundary}"


def upload(
    source: str,
    *,
    file_name: str | None = None,
    folder: str | None = None,
    tags: list[str] | None = None,
    use_unique: bool = True,
    is_private: bool = False,
    overwrite: bool = False,
    env_dirs: list[Path] | None = None,
) -> dict[str, Any]:
    private_key = get_private_key(env_dirs)
    resolved_name = guess_filename(source, file_name)
    resolved_folder = resolve_folder(folder, env_dirs)

    fields: dict[str, str] = {
        "fileName": resolved_name,
        "useUniqueFileName": "true" if use_unique else "false",
        "isPrivateFile": "true" if is_private else "false",
    }
    if resolved_folder:
        fields["folder"] = resolved_folder
    if tags:
        # V2 expects array[string]; multipart sends JSON array string.
        fields["tags"] = json.dumps(tags)
    if overwrite:
        fields["overwriteFile"] = "true"
        fields["useUniqueFileName"] = "false"

    file_field: str | None = None
    file_bytes: bytes | None = None
    content_type: str | None = None

    if source.startswith(("http://", "https://")):
        fields["file"] = source
    else:
        path = Path(source).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"file not found: {path}")
        file_bytes = path.read_bytes()
        file_field = "file"
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if not file_name:
            fields["fileName"] = path.name

    body, content_type_header = build_multipart(
        fields,
        file_field,
        resolved_name if file_field else None,
        file_bytes,
        content_type,
    )

    auth = base64.b64encode(f"{private_key}:".encode()).decode()
    req = Request(
        UPLOAD_ENDPOINT,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": content_type_header,
            "Accept": "application/json",
        },
    )

    try:
        with urlopen(req, timeout=120) as resp:
            raw = resp.read().decode()
            return json.loads(raw)
    except HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise RuntimeError(f"ImageKit upload failed ({exc.code}): {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"ImageKit upload network error: {exc}") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload a file or remote URL to ImageKit"
    )
    parser.add_argument(
        "source",
        help="Local file path or remote https URL",
    )
    parser.add_argument(
        "folder_pos",
        nargs="?",
        metavar="folder",
        help="Optional destination folder, e.g. /blog/covers (same as --folder)",
    )
    parser.add_argument(
        "--file-name",
        "--name",
        dest="file_name",
        help="Override fileName in Media Library",
    )
    parser.add_argument(
        "-f",
        "--folder",
        dest="folder",
        help="Destination folder path, e.g. /blog/covers (overrides IMAGEKIT_FOLDER)",
    )
    parser.add_argument(
        "--tags",
        help="Comma-separated tags, e.g. hero,cover",
    )
    parser.add_argument(
        "--no-unique",
        action="store_true",
        help="Do not append unique suffix to fileName",
    )
    parser.add_argument(
        "--private",
        action="store_true",
        help="Mark uploaded file as private",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing file with same name+folder",
    )
    parser.add_argument(
        "--format",
        choices=("json", "url"),
        default="json",
        help="Output full JSON (default) or only url",
    )
    parser.add_argument(
        "--env-dir",
        action="append",
        default=[],
        metavar="DIR",
        help="Also load .env / .env.local from DIR (repeatable)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    env_dirs = [Path(d) for d in args.env_dir]
    # --folder wins over positional folder
    folder = args.folder if args.folder is not None else args.folder_pos

    try:
        result = upload(
            args.source,
            file_name=args.file_name,
            folder=folder,
            tags=tags or None,
            use_unique=not args.no_unique,
            is_private=args.private,
            overwrite=args.overwrite,
            env_dirs=env_dirs or None,
        )
    except Exception as exc:  # noqa: BLE001 - CLI boundary
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.format == "url":
        url = result.get("url")
        if not url:
            print("error: response missing url", file=sys.stderr)
            print(json.dumps(result, ensure_ascii=False, indent=2), file=sys.stderr)
            sys.exit(1)
        print(url)
        return

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
