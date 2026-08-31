# 视频三平台 · 系列规划

> ⏸ **本期暂缓**。先完成长文 + 短内容（见 [`00-longform-shortform-focus.md`](./00-longform-shortform-focus.md)）；长文 ≥ 30 篇且有可复用口播提纲后再启动本文件。
>
> 覆盖：**B 站**（80 期长视频）· **YouTube 英文**（30 期）· **抖音 / 视频号**（100 期短视频）
> 姊妹计划：[`longform/`](./longform/) 下各 `*-series-plan.md`
> 复用素材：AI 术语 30 篇 · AI 原理 80 篇 · 100-skills 系列
> 三平台原则：**同一次拍摄，剪出三种形态**（不重录），最大化 ROI

---

## 一、B 站 · AI 通识补习班（80 期长视频）

### 定位
面向想搞懂 AI 但被术语劝退的技术 / 半技术观众。

| 项 | 内容 |
|---|---|
| 频道名 | AI 通识补习班（暂定） |
| 时长 | 单集 8-12 分钟 |
| 竞品参考 | 3Blue1Brown · 李永乐 · 林亦 |
| 差异化 | 一次讲透一个概念，不做新闻、不评测 |

### 单集结构
```
0:00-0:30   反常识钩子
0:30-1:30   生活类比（同步画黑板）
1:30-4:00   概念本体
4:00-7:00   真实用法演示（屏幕录制）
7:00-9:00   常见坑 / 误解
9:00-10:00  下期预告 + 三连
```

### 四季 × 20 期 = 80 期

**第一季 · 基础层（20 期）** — 从 AI 术语 30 挑最基础的 20 个
LLM · Token · Prompt · Temperature/Top-p · Embedding · RAG · Fine-tuning · Tool Calling · Agent · MCP · Transformer · Attention · Context Window · System Prompt · Few/Zero-shot · CoT · Hallucination · Vector DB · Inference · Foundation Model

**第二季 · 进阶层（20 期）**
Self-Attention · Positional Encoding · Tokenizer · Sampling · KV Cache · Quantization · Distillation · MoE · 训练 vs 推理 · Streaming · Prompt Caching · Structured Output · Long Context · Lost in the Middle · ReAct · Multi-Agent · Agent Memory · RLHF · DPO · Multimodal

**第三季 · 应用层（20 期）**
Cursor · Claude Code · Copilot · Perplexity · Deep Research · Notion AI · 通义/DeepSeek/Kimi 对比 · v0/Bolt/Lovable · Sora/Runway/Pika · HeyGen/Synthesia · Suno/Udio · Tripo/Meshy · ElevenLabs · DeepL vs LLM 翻译 · AI IDE 分界 · Browser Agent · Coding Agent · AI 面试官 · AI 陪聊 · AI 硬件

**第四季 · 工程与生产（20 期）**
LLM 网关 · 成本模型 · 可观测性 · 幻觉治理 · Prompt Injection · Guardrails · Eval · 部署架构 · 本地部署 · LoRA/QLoRA · Function Calling schema · MCP Server · Agent 上生产 · AI SaaS 技术栈 · Agent 技术栈 · GPU/TPU/NPU · vLLM/TGI · Model Router · AI 能耗 · 100 期总结

### B 站平台规范
- 封面：大字 + 反常识钩子 + 黑板风符号
- 标题：「【AI 通识 · 期 X】<钩子>：一句话讲清 <术语>」
- 分区：科技 → 计算机技术
- 简介：时间戳 + 参考资料

### 生产 SOP · 单集 4-6 小时
脚本（60-90 min · 复用博客素材） → 分镜（30 min · Figma） → 录制（30-45 min · OBS + 罗德） → 剪辑（60-120 min · 剪映专业版） → 封面（15 min）

---

## 二、YouTube 英文 · Build with Me（30 期）

### 定位
面向海外 indie hacker / vibe coder。跟着我一集做一个真实 side project，全程英文。

| 项 | 内容 |
|---|---|
| 频道名 | Build with Me · Vibecoding for Non-Devs |
| 时长 | 主视频 15-20 分钟 · Shorts 30-60 秒 |
| 竞品参考 | Fireship（快节奏） · Theo（Web dev） · Nicholas Renotte（AI）|
| 差异化 | 不是 tutorial，是「一起动手」（Coding with Me）|

### 单集结构
```
0:00-0:20   Hook（today we're building X in 20 minutes）
0:20-1:00   Why it matters（真实场景）
1:00-14:00  Live build（关键节点加速快剪）
14:00-17:00 Deploy + Demo
17:00-19:00 What can go wrong + What's next
19:00-20:00 CTA（订阅 + 项目仓库）
```

### 30 期排期

**Season 1 · Vibecoding Foundations（10 期）**
1. What is vibecoding · 2. Bolt vs Lovable vs v0 · 3. First Web App in 30 min · 4. From idea to landing · 5. Adding auth without code · 6. Adding payments in 15 min · 7. Deploy to production · 8. Adding your custom domain · 9. Adding analytics · 10. When AI gets stuck: 3 rescue moves

**Season 2 · AI-Native Projects（10 期）**
11. Build a RAG chatbot in 20 min · 12. Build a browser agent · 13. Build a Twitter automation · 14. Build a YouTube summarizer · 15. Build a résumé generator · 16. Build a meeting notes tool · 17. Build an AI translator page · 18. Build an AI music player · 19. Build a personal AI wiki · 20. Build a Chrome extension in 20 min

**Season 3 · Level Up（10 期）**
21. Move from Bolt to Cursor · 22. Add a database properly · 23. Fix your first real bug without reading code · 24. Ship to Product Hunt in 24 hours · 25. Adding SEO to your vibecoded site · 26. Getting your first 10 users · 27. Charging money · 28. When to hire a real developer · 29. The vibecoding ceiling · 30. 30 projects, 30 lessons

### YouTube 平台规范
- 缩略图：大字英文 + face reaction + 项目截图三分法
- 标题：`I built X in Y minutes with $0`（Fireship 式）
- 时长：主 15-20 分 + 每期剪 3-5 个 Shorts
- 描述：Chapters + Repo + Sponsor 位

### Shorts 引流策略
主视频剪 3-5 个 30-60 秒 Shorts：
- 「最爽的那一刻」（AI 一次做对）
- 「最糟的那一刻」（AI 崩了怎么救）
- 「最终成品 demo」
- 「30 秒讲清 idea」
- 「一个我踩过的坑」

---

## 三、抖音 / 视频号 · AI 骚操作 60 秒（100 期）

### 定位
面向下沉市场 + 中年 + 非技术用户。**每天一个具体应用场景**，不解释原理、不推销工具。

| 项 | 内容 |
|---|---|
| 账号名 | AI 骚操作（暂定） |
| 时长 | 15-60 秒（追 30 秒） |
| 竞品参考 | AI 学长小明 · AI 疯狂制造 · 数字生命卡兹克（抖音号）|
| 差异化 | 只演示、不推广。「原来 AI 还能这么用」的震撼感 |

### 单集结构（30 秒模板）
```
0-3s   悬念钩子（如「教我妈用 AI 一分钟搞定这件事」）
3-15s  演示过程（无解说 / 快节奏）
15-25s 结果展示
25-30s 一句话价值 + 关注引导
```

### 100 期分区

**分区 A · 生活场景（30 期）** — 破圈爆款潜力最大
1. 一键翻译菜单 · 2. 拍照识别植物 · 3. 语音写日记 · 4. AI 修复老照片 · 5. AI 给爸妈讲电影 · 6. AI 讲故事哄睡 · 7. AI 陪练英语 · 8. AI 讲论文 · 9. AI 做菜谱 · 10. AI 装修灵感 · 11. AI 出旅游攻略 · 12. AI 写年终总结 · 13. AI 回复家长群消息 · 14. AI 写情书 · 15. AI 出面试题 · 16. AI 写辞职信 · 17. AI 讲专业术语 · 18. AI 帮孩子写作业（争议向） · 19. AI 分析家庭消费 · 20. AI 出商务方案 · 21. AI 出健身计划 · 22. AI 陪谈心 · 23. AI 做心理测试 · 24. AI 解梦 · 25. AI 出穿搭 · 26. AI 出发型 · 27. AI 拍简历照 · 28. AI 出品牌名 · 29. AI 找房子 · 30. AI 讲历史故事

**分区 B · 职场场景（30 期）**
Excel 一键透视 · PPT 一句话生成 · 会议纪要 · 周报生成 · 邮件回复 · 简历优化 · 面试模拟 · 数据分析 · 图表美化 · 竞品调研 · 用户画像 · 广告文案 · 商务谈判 · 客户回访 · 会议同传 · 文档翻译 · 报销单整理 · 合同摘要 · 培训内容 · 内部沟通 · 提案生成 · 时间管理 · 目标拆解 · 跨部门协作 · 项目复盘 · 招聘 JD · 绩效沟通 · 离职谈话 · 员工手册 · 团建活动

**分区 C · 内容创作（20 期）**
写公众号 · 起小红书标题 · 做小红书封面 · 抖音脚本 · B 站选题 · 播客大纲 · 播客剪辑 · 视频封面 · 视频剪辑 · 配音 · 音乐配乐 · 音效搜索 · 素材寻找 · 版权检查 · AI 出图 · 抠图去水印 · 视频字幕 · 数字人主播 · 直播脚本 · 直播复盘

**分区 D · 家庭 / 教育（20 期）**
给爸妈用 · 给孩子用 · 给孩子做绘本 · AI 讲十万个为什么 · 讲古诗 · 讲英语单词 · 讲数学题 · 陪玩游戏 · 讲科普 · 讲纪录片 · 家庭旅行规划 · 家庭财务 · 健康问答 · 用药说明 · 老人陪伴 · 家庭菜单 · 家庭作业检查 · 家庭矛盾调解（趣味） · 家庭活动策划 · 长辈生日祝福

### 抖音 / 视频号平台规范
- 封面：三段式（问题 + AI 图标 + 结果）
- 标题：**具体场景 + 意外结果**（如「教我妈用 AI 一分钟搞定这件事，她眼睛都亮了」）
- BGM：抖音热榜 BGM（每周刷新）
- 更新时间：抖音 12:00 / 19:00 · 视频号 8:00 / 20:00
- 变现路径：橱窗 · 直播 · 小店 · 私域引流

### 生产 SOP · 单集 30-60 分钟
选题（5 min） → 脚本（10 min） → 拍摄 / 录屏（10-20 min） → 剪辑（15-30 min · 剪映）

---

## 三平台联动策略

| 内容源 | B 站 | YouTube | 抖音 |
|---|---|---|---|
| AI 术语 30 篇 | 主脚本 | 挑 15 期改英文版 | 15 秒剪辑版 |
| 100-skills 系列 | 每季末 1 期综述 | Skill of the Week | 每天一个 skill demo |
| Vibecoding 项目 | 少量露出 | 主脚本 | 项目 demo 剪辑 |
| Solopreneur 数据 | 不发 | 主脚本（Build in Public） | 数据爆点视频 |

**核心：一次拍摄，三次剪辑，三个平台。**

---

## 进度追踪

| 平台 | 计划 | 已完成 | 进度 |
|---|---|---|---|
| B 站 · AI 通识 | 80 | 0 | ⬜ |
| YouTube · Build with Me | 30 | 0 | ⬜ |
| 抖音 / 视频号 · AI 骚操作 | 100 | 0 | ⬜ |
| **合计** | **210** | **0** | **0%** |

---

## 下一步待办

- [ ] 三个平台账号注册 + 头像 + banner + 频道简介
- [ ] 视觉统一：片头 / 片尾 / 字幕 / 封面模板
- [ ] 拍摄环境：黑板 / 手绘板 / 屏幕录制路径三种统一
- [ ] 前 3 期各拍 1 期样片（不上线）
- [ ] 建立选题池：Notion 一张表管三个平台
- [ ] 决定：是否请人剪辑 / 什么时候开始
