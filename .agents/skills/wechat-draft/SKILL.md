---
name: wechat-draft
description: Upload Markdown articles under wechat/ to the WeChat Official Account draft box via draft/add (covers as permanent image materials). Use when the user asks to publish/upload/sync 公众号草稿, WeChat MP drafts, or process files in wechat/.
---

# WeChat Draft Upload

把仓库根目录 `wechat/*.md` 存进微信公众号**草稿箱**。只存草稿，不群发、不发表。

## Layout

```
wechat/
  YYYY-MM-DD-slug.md      # 必填：# 标题 + ## 正文
  YYYY-MM-DD-slug.jpg     # 必填：同名封面
  covers/                 # 可复用封面库
  drafts.json             # 上传状态（勿提交）
```

凭证写在仓库 `.env.local`（已 gitignore）：

```bash
WECHAT_APP_ID=wx...
WECHAT_APP_SECRET=...
```

密钥在 [微信开发者平台](https://developers.weixin.qq.com/platform/) → 我的业务 → 公众号/服务号 → 基础信息 → 开发密钥。同一页配置 **API IP 白名单**；出口 IP 变动会返回 `40164`。

## Article format

```markdown
# 标题（≤32 字）

## 正文

段落一。

段落二，可含 `code`、[链接](https://example.com) 或裸 URL。
```

- 封面：与 md 同名的 `.jpg`；可从 `wechat/covers/` 复制轮换，说明见该目录 `README.md`。
- 摘要：未单独字段时用正文去空白后前 120 字。
- 已在 `drafts.json` 里的文件会跳过，不会重复上传。

## Commands

在仓库根目录执行：

```bash
python3 .agents/skills/wechat-draft/scripts/upload_drafts.py --dry-run
python3 .agents/skills/wechat-draft/scripts/upload_drafts.py
```

## Agent workflow

1. 确认 `WECHAT_APP_ID` / `WECHAT_APP_SECRET` 在 `.env.local`（或 process env）。
2. 先 `--dry-run` 核对标题字数、封面是否存在、HTML 是否合理。
3. 用户确认后再正式上传；默认只进草稿箱。
4. 若 `40164`：把报错 IP 加进白名单，等几分钟重试。
5. 若 `48001`：账号无草稿接口权限，改用公众平台后台手动存稿，不要死磕接口。
6. 上传成功后提醒用户到公众平台草稿箱核对封面裁切与敏感表述，再点发表。
7. **不要**调用群发 / 发布接口，除非用户明确要求公开发布。

## Notes

- 信息流封面约按 2.35:1 居中裁切，边缘文字可能被切。
- 公开文案勿写私密项目名；发表前在草稿里再扫一眼。
- `drafts.json` 只做本地去重，不进 git。
