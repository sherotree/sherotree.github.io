#!/usr/bin/env python3
"""Upload repo wechat/*.md articles to the Official Account draft box.

Reads WECHAT_APP_ID / WECHAT_APP_SECRET from process env, then .env.local / .env.
Saves drafts only. Does not publish or mass-send.
"""

from __future__ import annotations

import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/stable_token"
MATERIAL_URL = "https://api.weixin.qq.com/cgi-bin/material/add_material"
DRAFT_URL = "https://api.weixin.qq.com/cgi-bin/draft/add"

TITLE_LIMIT = 32
DIGEST_LIMIT = 120

CODE_RE = re.compile(r"`([^`]+)`")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
URL_RE = re.compile(r"https?://[^\s<]+")
TRAILING_PUNCT = ".,;:)]}>，。；：、"


class WeChatError(RuntimeError):
    def __init__(self, payload: dict):
        self.code = payload.get("errcode")
        self.errmsg = str(payload.get("errmsg", ""))
        super().__init__(self.hint())

    def hint(self) -> str:
        base = f"{self.code}: {self.errmsg}"
        if self.code == 40164:
            return (
                base
                + "\n把报错里的 IP 加到微信开发者平台 → 公众号 → 基础信息 → 开发密钥 → API IP 白名单，等几分钟再生效。"
            )
        if self.code == 48001:
            return (
                base
                + "\n这个号没有草稿接口权限。未认证的个人号经常如此，需要改用公众平台后台扫码保存草稿。"
            )
        if self.code in (40001, 40125, 40013):
            return base + "\nAppID 或 AppSecret 不正确。若刚重置过密钥，等一两分钟再试。"
        return base


def find_repo_root(start: Path) -> Path:
    for path in [start, *start.parents]:
        if (path / ".git").exists() or (path / "wechat").is_dir():
            return path
    return start


def load_env_file(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def resolve_credentials(root: Path) -> tuple[str, str]:
    merged: dict[str, str] = {}
    for name in (".env", ".env.local"):
        merged.update(load_env_file(root / name))
    app_id = os.environ.get("WECHAT_APP_ID") or merged.get("WECHAT_APP_ID", "")
    app_secret = os.environ.get("WECHAT_APP_SECRET") or merged.get("WECHAT_APP_SECRET", "")
    return app_id, app_secret


def api_json(url: str, payload: dict, token: str | None = None) -> dict:
    if token:
        join = "&" if "?" in url else "?"
        url = f"{url}{join}access_token={token}"
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    return read_response(request)


def read_response(request: urllib.request.Request) -> dict:
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        raw = error.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            raise RuntimeError(f"HTTP {error.code}: {raw[:300]}") from error
    if payload.get("errcode"):
        raise WeChatError(payload)
    return payload


def access_token(app_id: str, app_secret: str) -> str:
    payload = api_json(
        TOKEN_URL,
        {
            "grant_type": "client_credential",
            "appid": app_id,
            "secret": app_secret,
            "force_refresh": False,
        },
    )
    token = payload.get("access_token")
    if not token:
        raise RuntimeError("access_token 缺失")
    return token


def upload_cover(token: str, path: Path) -> str:
    boundary = "----WeChatBoundary" + uuid.uuid4().hex
    head = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{path.name}"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode("utf-8")
    tail = f"\r\n--{boundary}--\r\n".encode("utf-8")
    request = urllib.request.Request(
        f"{MATERIAL_URL}?access_token={token}&type=image",
        data=head + path.read_bytes() + tail,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    payload = read_response(request)
    media_id = payload.get("media_id")
    if not media_id:
        raise RuntimeError(f"封面上传没有返回 media_id：{path.name}")
    return media_id


def parse_article(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    title = ""
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break
    if "## 正文" not in text:
        raise RuntimeError(f"{path.name} 缺少「## 正文」")
    body = text.split("## 正文", 1)[1].strip()
    if not title or not body:
        raise RuntimeError(f"{path.name} 标题或正文为空")
    if len(title) > TITLE_LIMIT:
        raise RuntimeError(
            f"{path.name} 标题 {len(title)} 字，超过公众号 {TITLE_LIMIT} 字限制：{title}"
        )
    return title, body


def inline(text: str) -> str:
    slots: list[str] = []

    def put(fragment: str) -> str:
        slots.append(fragment)
        return f"\x00{len(slots) - 1}\x00"

    text = CODE_RE.sub(lambda match: put(f"<code>{html.escape(match.group(1))}</code>"), text)
    text = MD_LINK_RE.sub(
        lambda match: put(
            f'<a href="{html.escape(match.group(2), quote=True)}">{html.escape(match.group(1))}</a>'
        ),
        text,
    )
    text = html.escape(text)

    def linkify(match: re.Match[str]) -> str:
        url = match.group(0)
        trim = ""
        while url and url[-1] in TRAILING_PUNCT:
            trim = url[-1] + trim
            url = url[:-1]
        return f'<a href="{html.escape(url, quote=True)}">{html.escape(url)}</a>{html.escape(trim)}'

    text = URL_RE.sub(linkify, text)
    for index, fragment in enumerate(slots):
        text = text.replace(f"\x00{index}\x00", fragment)
    return text


def to_html(body: str) -> str:
    parts: list[str] = []
    for block in re.split(r"\n\s*\n", body.strip()):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        parts.append("<p>" + "<br>".join(inline(line) for line in lines) + "</p>")
    return "".join(parts)


def digest_from(body: str) -> str:
    plain = re.sub(r"\s+", "", body)
    plain = plain.replace("`", "")
    plain = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r"\1", plain)
    return plain[:DIGEST_LIMIT]


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"articles": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(path: Path, state: dict) -> None:
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def list_articles(wechat_dir: Path) -> list[Path]:
    return sorted(wechat_dir.glob("*.md"))


def create_draft(token: str, title: str, body: str, thumb_media_id: str) -> str:
    payload = api_json(
        DRAFT_URL,
        {
            "articles": [
                {
                    "article_type": "news",
                    "title": title,
                    "digest": digest_from(body),
                    "content": to_html(body),
                    "thumb_media_id": thumb_media_id,
                    "need_open_comment": 0,
                    "only_fans_can_comment": 0,
                }
            ]
        },
        token=token,
    )
    media_id = payload.get("media_id")
    if not media_id:
        raise RuntimeError(f"草稿接口没有返回 media_id：{title}")
    return media_id


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    root = find_repo_root(Path.cwd())
    wechat_dir = root / "wechat"
    state_path = wechat_dir / "drafts.json"
    if not wechat_dir.is_dir():
        raise RuntimeError(f"找不到内容目录：{wechat_dir}")

    state = load_state(state_path)
    done = {item["file"] for item in state.get("articles", [])}
    pending = [path for path in list_articles(wechat_dir) if path.name not in done]
    if not pending:
        print("没有待上传的文章")
        return 0

    for path in pending:
        title, body = parse_article(path)
        cover = path.with_suffix(".jpg")
        if not cover.exists():
            raise RuntimeError(f"缺少封面：{cover.name}")
        print(f"{path.name}")
        print(f"  标题 {len(title)} 字：{title}")
        print(f"  正文 {len(to_html(body))} 字符，封面 {cover.stat().st_size} 字节")
        if dry_run:
            print(to_html(body))
            print()

    if dry_run:
        return 0

    app_id, app_secret = resolve_credentials(root)
    if not app_id or not app_secret:
        raise RuntimeError("缺少 WECHAT_APP_ID 或 WECHAT_APP_SECRET（写在 .env.local）")

    token = access_token(app_id, app_secret)
    for path in pending:
        title, body = parse_article(path)
        cover = path.with_suffix(".jpg")
        thumb_media_id = upload_cover(token, cover)
        draft_media_id = create_draft(token, title, body, thumb_media_id)
        state.setdefault("articles", []).append(
            {
                "file": path.name,
                "title": title,
                "draft_media_id": draft_media_id,
                "thumb_media_id": thumb_media_id,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        save_state(state_path, state)
        print(f"  已存入草稿 {draft_media_id}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (WeChatError, RuntimeError) as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
