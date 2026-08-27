# CSDN 引流计划 — Image Conversion（10 篇）

> 站点：`https://www.uwarp.design/`  
> 工具目录：`app/(tools)/(image-conversion)/(hosted)/`  
> 关键词地图：[`KEYWORD-MAP.md`](../../app/(tools)/(image-conversion)/KEYWORD-MAP.md)  
> 外链总计划：[`backlink-plan.md`](../backlink-plan.md)  
> 姊妹计划（英文站）：[`dev.to/image-conversion-traffic-plan.md`](../dev.to/image-conversion-traffic-plan.md)  
> 平台：`https://blog.csdn.net`（中文投稿 / 偏百度检索）  
> 状态：规划中 · 2026-08-25

---

## 目标

用 **10 篇** CSDN 中文教程，把国内开发者 / 前端 / 运营 / 学生流量导到 Uwarp **具体 hosted 工具页**（不是首页）。

成功标准（建议 4–6 周后复盘）：

| 指标 | 目标（起步） |
|------|-------------|
| 单篇阅读 | ≥ 800（CSDN 检索流量通常高于冷启动 Dev.to） |
| 文内点击到 uwarp | GA `utm_source=csdn` / referral |
| 百度可见性 | 目标关键词能进 CSDN 站内搜 / 外搜前几页 |
| 外链 | 每篇至少 1 条可点击工具子页链接 |

---

## 与 Dev.to 的差异（必读）

| 维度 | Dev.to | CSDN |
|------|--------|------|
| 语言 | 英文 | **中文** |
| 动机 | 社区讨论、技术品味 | **搜索解题**（百度 → CSDN 排名） |
| 标题 | 场景 / 观点型 | **「怎么转 / 在线 / 免费 / 不安装」** 意图清晰 |
| 硬广容忍度 | 低，少 listicle | **可适度工具推荐**，但仍要有步骤与坑点 |
| 本地场景 | GitHub README、Discord | **微信/钉钉、交作业、简历、文档、小红书尺寸** |
| 系列名 | Browser Image Toolkit | **浏览器里搞定图片**（或「不装 PS 的图片工具箱」） |

**错开原则：** 与 Dev.to 可共享底层工具能力，但 **标题、场景、关键词不要中英一一翻译照搬**，避免同质化与自我竞争叙事。本计划优先覆盖 **中文高检索意图**，Dev.to 未覆盖或弱覆盖的线（透明 PNG、PSD、拼图、证件照、微信发图体积等）。

---

## 原则

1. **链到具体工具页**，不要只堆首页。
2. 标题带主关键词：`格式A转格式B` / `在线XXX` / `免费`（实事求是）。
3. 结构：**场景 → 为什么会出问题 → 分步截图/步骤 → 常见坑 → 工具链接**。
4. 文中 1–2 处工具链 + 文末「在线工具」小节；锚文本用中文任务词轮换。
5. 节奏：**每周 1–2 篇**；同账号短时间连发 10 篇易触发低质判定。
6. 正文可写「国外免费工具 / 浏览器本地处理」等信任话术，**勿夸大「最大/最好」**。
7. 发布后用百度普通收录推工具页（见 [`baidu-index.md`](../baidu-index.md)），文章与落地页互相促进。

### 刻意先不做

- 纯「十大在线转换器」无步骤水文
- 与工具无关的 AI 绘画站外引流文
- 一工具一文、每篇不足 800 字的薄内容刷量

---

## 每篇统一结构

1. 开头 3 句说清场景（交作业 / 发钉钉 / 上线网页 / 写文档）
2. 格式或限制说明（体积、透明、兼容）
3. **步骤 1–N**（浏览器操作，可附可选命令行）
4. 常见问题（FAQ 3–5 条，利于百度 featured / 站内搜）
5. **在线工具**：链到 `https://www.uwarp.design/{slug}`
6. 文末互链本系列已发文章（养站内权重）

**UTM 模板：**

```text
https://www.uwarp.design/{slug}?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content={post-slug}
```

**分类建议（CSDN）：** 前端、JavaScript、工具资源、经验分享（按账号习惯选 1–2 个）。

---

## 发布顺序与主题

| # | 发布序 | 工作标题（中文检索向） | 主搜意图 | 引流工具（优先） | 与 Dev.to 关系 |
|---|--------|------------------------|----------|------------------|----------------|
| 1 | 第 1 篇 | iPhone 拍的 HEIC 怎么转 JPG/PNG？交作业、发钉钉不用再求人 | HEIC转JPG / HEIC转PNG | `/heic-to-jpg` `/heic-to-png` | 同能力，场景改中文办公 |
| 2 | 第 2 篇 | PNG 透明图转 JPG 变黑底？白底填充与格式选择一次说清 | PNG转JPG / 透明PNG | `/png-to-jpg` `/fill-transparent-png` `/check-if-png-is-transparent` | Dev.to 未单列 |
| 3 | 第 3 篇 | 微信/文档里 GIF 发不出去：在线压缩、改尺寸、调速度 | GIF压缩 / GIF太大 | `/gif-compressor` `/gif-resizer` `/gif-speed-changer` `/shorten-gif` | 近 Dev.to#1，渠道改微信 |
| 4 | 第 4 篇 | 录屏 MP4 怎么做成教程 GIF？浏览器里剪、压、加字幕 | 视频转GIF / MP4转GIF | `/video-to-gif` `/mov-to-gif` `/gif-cutter` `/add-caption-to-gif` | 近 Dev.to#5，标题更检索 |
| 5 | 第 5 篇 | 网页要上 WebP：JPG/PNG 怎么转，以及何时别转 | JPG转WebP / PNG转WebP | `/jpg-to-webp` `/png-to-webp` `/webp-to-jpg` `/webp-to-png` | 近 Dev.to#4 |
| 6 | 第 6 篇 | 截图发群前先打码：模糊、马赛克、去 EXIF 三件套 | 截图打码 / 去除EXIF | `/censor-photo-blur-pixelate` `/image-censor` `/remove-exif-data` `/view-metadata` | EXIF+打码合并，更本土 |
| 7 | 第 7 篇 | 不会用 Photoshop？PSD 直接转 JPG/PNG 给同事 | PSD转JPG / PSD转PNG | `/psd-to-jpg` `/psd-to-png` | Dev.to 未覆盖 |
| 8 | 第 8 篇 | SVG 图标导出 PNG/JPG：模糊、透明底、尺寸怎么设 | SVG转PNG / SVG转JPG | `/svg-to-png` `/svg-to-jpg` `/svg-viewer` `/resize-svg` | 近 Dev.to#8 |
| 9 | 第 9 篇 | 简历头像、微信头像一次裁方/裁圆（含常见尺寸） | 头像裁剪 / 圆形头像 | `/pfp-cropper` `/square-crop` `/circle-crop-image` `/profile-photo` | 替 Dev.to Discord 线 |
| 10 | 第 10 篇 | 两张图横竖拼接：做对比图、PRD 附图不用开 PS | 图片拼接 / 合并图片 | `/merge-images` `/combine-maker` `/overlay-images` `/merge-png` | Dev.to 未覆盖 |

---

## 各篇工作笔记

### 1 — HEIC 转 JPG/PNG

- **标题备选：** `iPhone 照片 HEIC 转 JPG/PNG 最省事的方法（浏览器在线）`
- **FAQ 种子：** Windows 打不开 HEIC？转完发钉钉还是很大？要不要再压成 WebP？
- **锚文本：** HEIC转JPG在线、免费HEIC转PNG
- **状态：** `draft` · 稿：`01-heic-to-jpg-png.md`

### 2 — 透明 PNG → JPG

- **标题备选：** `PNG 转 JPG 黑底/花屏？透明通道处理与白底填充`
- **FAQ 种子：** 为什么 JPG 没有透明？需要透明该用什么格式？
- **锚文本：** PNG转JPG、填充透明PNG
- **状态：** `draft` · 稿：`02-png-to-jpg-transparent.md`

### 3 — GIF 体积（微信/文档）

- **标题备选：** `GIF 太大发不了微信？压缩、缩小尺寸、加快速度 checklist`
- **FAQ 种子：** 压完糊了怎么办？循环次数？裁掉片头片尾？
- **锚文本：** 在线压缩GIF、GIF改尺寸
- **状态：** `draft` · 稿：`03-gif-compress-wechat.md`

### 4 — 视频 → GIF 教程

- **标题备选：** `MP4/录屏转 GIF 做技术文档动图（可加字幕条）`
- **FAQ 种子：** 和直接嵌视频比何时用 GIF？时长建议多少秒？
- **锚文本：** 视频转GIF、GIF加字幕
- **状态：** `draft` · 稿：`04-video-to-gif-tutorial.md`

### 5 — WebP

- **标题备选：** `前端性能：JPG/PNG 转 WebP 实操与兼容回退`
- **FAQ 种子：** Safari 老版本？动画 WebP vs GIF？
- **锚文本：** JPG转WebP、PNG转WebP在线
- **状态：** `draft` · 稿：`05-jpg-png-to-webp.md`

### 6 — 打码 + EXIF

- **标题备选：** `开发者截图防泄密：打码 + 去掉 EXIF 位置信息`
- **FAQ 种子：** 只涂鸦够不够？GPS 在哪看？
- **锚文本：** 图片打码在线、去除EXIF
- **状态：** `draft` · 稿：`06-screenshot-censor-exif.md`

### 7 — PSD 转出图

- **标题备选：** `没有 Photoshop 怎么打开 PSD？在线转 JPG/PNG`
- **FAQ 种子：** 图层会丢吗？复杂效果糊了怎么办？（诚实说明能力边界）
- **锚文本：** PSD转JPG、PSD转PNG免费
- **状态：** `draft` · 稿：`07-psd-to-jpg-png.md`

### 8 — SVG 导出

- **标题备选：** `前端切图：SVG 转 PNG/JPG 避免发虚的设置清单`
- **FAQ 种子：** 2x/3x 怎么导？要不要留透明底？
- **锚文本：** SVG转PNG在线、SVG查看器
- **状态：** `draft` · 稿：`08-svg-to-png-jpg.md`

### 9 — 头像裁剪

- **标题备选：** `简历/微信头像尺寸怎么裁？方形与圆形在线裁剪`
- **FAQ 种子：** 常见像素表；圆裁导出是否带透明
- **锚文本：** 头像裁剪、圆形裁剪图片
- **状态：** `draft` · 稿：`09-avatar-crop-resume.md`

### 10 — 拼图 / 合并

- **标题备选：** `两张图左右/上下拼接：竞品对比图、文档附图快速搞定`
- **FAQ 种子：** PNG 透明拼接？多图宫格用哪个？
- **锚文本：** 在线合并图片、图片拼接工具
- **状态：** `draft` · 稿：`10-merge-images-combine.md`

---

## 追踪表

| # | 标题（终稿） | CSDN URL | 发布日 | 主要工具页 | UTM content | 阅读 | 状态 |
|---|--------------|----------|--------|------------|-------------|------|------|
| 1 | iPhone 拍的 HEIC 怎么转 JPG/PNG？交作业、发钉钉不用再求人 | | | `/heic-to-jpg` `/heic-to-png` | heic-jpg | | draft |
| 2 | PNG 透明图转 JPG 变黑底？白底填充与格式选择一次说清 | | | `/png-to-jpg` `/fill-transparent-png` | png-jpg-alpha | | draft |
| 3 | 微信/文档里 GIF 发不出去：在线压缩、改尺寸、调速度 | | | `/gif-compressor` `/gif-resizer` | gif-wechat | | draft |
| 4 | 录屏 MP4 怎么做成教程 GIF？浏览器里剪、压、加字幕 | | | `/video-to-gif` `/gif-cutter` | video-gif | | draft |
| 5 | 网页要上 WebP：JPG/PNG 怎么转，以及何时别转 | | | `/jpg-to-webp` `/png-to-webp` | webp-frontend | | draft |
| 6 | 截图发群前先打码：模糊、马赛克、去 EXIF 三件套 | | | `/censor-photo-blur-pixelate` `/remove-exif-data` | censor-exif | | draft |
| 7 | 不会用 Photoshop？PSD 直接转 JPG/PNG 给同事 | | | `/psd-to-jpg` `/psd-to-png` | psd-export | | draft |
| 8 | SVG 图标导出 PNG/JPG：模糊、透明底、尺寸怎么设 | | | `/svg-to-png` `/svg-to-jpg` | svg-raster | | draft |
| 9 | 简历头像、微信头像一次裁方/裁圆（含常见尺寸） | | | `/pfp-cropper` `/circle-crop-image` | avatar-crop | | draft |
| 10 | 两张图横竖拼接：做对比图、PRD 附图不用开 PS | | | `/merge-images` `/combine-maker` | merge-images | | draft |

状态：`todo` → `draft` → `published` → `reviewed`

---

## 复盘清单（满 6 周或发完）

1. 按 `utm_source=csdn` 看 Top 3 引流工具页，反推是否加站内中文 blog
2. 高阅读低点击：检查外链是否被 CSDN 转短链/nofollow、CTA 是否太靠后
3. 低阅读：改标题关键词（补「在线」「免费」「转XXX」）再发修订版或新开篇
4. 与 Dev.to 对照：同一能力线哪边 ROI 更高，决定第二批平台重心
5. 工具页配合 [`baidu-index.md`](../baidu-index.md) 补推收录

---

## 下一步

- [ ] 准备 CSDN 账号专栏（建议专栏名与系列一致）
- [x] 写第 1 篇（HEIC）稿 `01-heic-to-jpg-png.md`
- [x] 写第 2–10 篇稿 `02-` … `10-*.md`
- [ ] 发布到 CSDN，回填 URL 与发布日
- [ ] 每篇发布后：站内互链 + 对应工具页百度推送
- [ ] （可选）高表现篇同步改写进 `uwarp.design` 中文说明或英文 blog（注意勿重复堆砌）
