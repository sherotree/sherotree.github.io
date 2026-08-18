---
title: 理解 img2threejs：一张图如何变成 Three.js 模型
date: 2026-08-13
description: 说明开源技能 img2threejs 如何把参考图重建成可 diff、可动画的程序化 Three.js 工厂函数，以及它与 mesh 导出路线的差别。
tags: [Three.js, 图像到3D, Agent, 程序化建模]
series: browser-graphics
draft: false
---

img2threejs 是一套给 Agent 用的开源技能（Skill）：你给它一张物体参考图，它尽量用 **TypeScript + Three.js 原语 / 程序材质** 写出一个 `THREE.Group` 工厂函数，而不是导出一大坨 mesh 文件。

网上说「图像到 3D」的工具很多。有的走摄影测量，有的下载资产包，有的让模型一口气吐出几千行几何代码。img2threejs 的取舍不同：它强调 **用代码重建**、**分阶段过质量门**、**尽量省 token**。

下面按我读仓库与官方文档后的理解，把它在干什么、怎么跑、边界在哪讲清楚。

![常见 mesh 路线与 img2threejs 代码重建对照](https://ik.imagekit.io/4pjac7gmxh/blog/2026/08/img2threejs-two-paths_TBZPUTKvt.png)

## 一、先说一个具体麻烦

你手头有一张耳机、自行车或道具的产品图，想在浏览器里转一转、做一点开合动画。

常见几条路：

（1）找现成 GLB / 资产包——有时找不到同款，有时授权不清  
（2）用摄影测量或「图生 mesh」——文件大，难进 Git，也难改结构  
（3）让聊天模型直接写 Three.js——容易一次生成整坨，难验收，也容易把隐藏面瞎编圆

真正卡人的，往往不是「能不能出个像」，而是：**结果能不能进仓库、能不能改关节、下一轮改动会不会把上下文烧光**。

img2threejs 正是冲着这类工程问题来的。官方仓库：[img2threejs/img2threejs](https://github.com/img2threejs/img2threejs)。在线展览馆里的模型，也是生成代码在浏览器里跑： [img2threejs-showcase](https://img2threejs.github.io/img2threejs-showcase/)。

![img2threejs showcase 展览馆：相机、电钻等可拆组件模型](https://ik.imagekit.io/4pjac7gmxh/blog/2026/08/img2threejs-showcase-gallery_mlTWJKK0m.png)

展览馆里的条目会标出类别和组件数。点进去可以在浏览器里检视层级、拆开装配，而不是只看一张静帧。

## 二、核心思路：用图纸重建，而不是扫描成一块实心木

简单说，可以把两条路想成两种交付家具的方式。

一种是把整张桌子锯成一块实心木，运到你家——沉、难改、版本管理也麻烦。  
另一种是先写装配图：桌腿、台面、铰链、油漆编号，再按图在工地上组装。改高度改颜色，改的是图纸和工序，不是把整块木头磨掉重来。

img2threejs 偏第二种。

所谓「code-only / procedural」，指的是：输出主要是 **可 diff 的 TypeScript** 和一份结构化规格 `ObjectSculptSpec`（JSON），几何来自原语、生成几何和程序着色器，而不是把照片「抠」成不可读的三角网包。

它明确不是摄影测量，也不靠下载美术包凑数。单张图看不见的背面，它宁可标低置信度或镜像推断，也不假装「全知」。

## 三、流水线怎么走

整体是一条带闸门的雕刻流水线。

（A）探测参考图，做适合性检查  
（B）写评估与 `ObjectSculptSpec`：组件树、材质、插槽等  
（C）严格质量门：规格太浅就挡住，先别生成代码  
（D）按阶段只生成「当前解锁」的那一关工厂代码  
（E）浏览器渲染，打出一张参考图 vs 渲染的对比页  
（F）Agent 用视觉判分：过关则继续，不过则改规格或改代码

![img2threejs 从参考图到模型的流水线](https://ik.imagekit.io/4pjac7gmxh/blog/2026/08/img2threejs-pipeline_TnSDP-CvA.png)

这里有一个设计重心：**Python 脚本负责机械活，模型只负责看图判断**。

校验 JSON、打包对比图、管关卡状态、写规格脚手架，都尽量丢给纯标准库脚本（官方强调 Python 3.10+ stdlib，不额外 pip 一堆依赖）。模型的 token，主要花在「这一侧像不像参考」和「这一关该怎么改代码」。

## 四、八个雕刻阶段

模型不是一次雕完，而是固定顺序解锁：

`blockout → structural → form → material → surface → lighting → interaction → optimization`

可以粗读成：先搭块、再定结构、再修形体、再材质表面、再灯光、再交互，最后优化。

![八个雕刻阶段依次解锁](https://ik.imagekit.io/4pjac7gmxh/blog/2026/08/img2threejs-passes_mAU-kteul.png)

每一关要通过，通常得有：真实渲染、对比页、视觉分数够线，以及身份相关细节各自过阈值。不过关，Agent 只能选有限动作，例如 `continue`、`refine-spec`、`refine-code`、`request-input`、`stop`——不是无限糊墙式重试。

生成器也是 fail-closed：严格门不过，就不写工厂文件，而是返回 `BLOCKED` 和原因。这比「先吐五千行再发现规格空心」更省。

## 五、最小上手步骤

它挂在 Claude Code、Codex、OpenCode 一类 Agent 宿主上，作为 skill 目录使用。官方示例是克隆到 skills 目录（多宿主可用同一份 checkout，再 symlink）：

```bash
git clone https://github.com/img2threejs/img2threejs.git ~/.claude/skills/img2threejs
```

上面命令中，关键是把技能目录放到宿主能发现的位置；多编辑器共用时，用符号链接指向同一仓库，避免几份拷贝版本漂移。

附上参考图后，用类似下面的指令启动（以 Claude Code 为例）：

```text
/img2threejs Rebuild this object as a Three.js model, keep the proportions, angles, and colours.
```

上面这段里，技能会自己做主体分类、细节清单，并把各关卡按门禁往前推。你已经知道「正确」长什么样时，也可以把保真度、材质、运行时插槽、严格门等要求写清楚——这些不是形容词装饰，而是对应流水线里真实会检查的项。

脚本本身也可单独跑。例如探测图片、写评估、写规格、校验、再生成工厂：

```bash
python3 forge/stage1_intake/probe_image.py <image>
python3 forge/stage2_spec/new_pre_spec_assessment.py "Name" --image <image> --out assessment.json
python3 forge/stage2_spec/new_sculpt_spec.py "Name" --image <image> --assessment assessment.json --out spec.json
python3 forge/stage2_spec/validate_sculpt_spec.py spec.json --strict-quality
python3 forge/stage3_build/generate_threejs_factory.py spec.json --out src/createObjectModel.ts
```

上面代码中，前几步都在「还没写 Three.js」时把规格做扎实；`validate_sculpt_spec.py --strict-quality` 是关键闸门——浅规格在这里就该停。

跨会话重建时，可用 `forge/state.py` / `forge/next.py --state` 记住清单进度；但过关权威仍是规格、渲染证据与审查记录，状态文件不能「开后门」。

## 六、你最终拿到什么

典型交付是三样东西：

（1）`ObjectSculptSpec` JSON：组件、材质、重复系统、插槽，以及各关审查历史  
（2）TypeScript 工厂，例如 `createXxxModel(spec, options)`，返回 `THREE.Group`  
（3）各关渲染与对比页，方便回看「哪一关过了、哪一关凑合」

展览馆里的 Sony 耳机示例，工厂开头大致是这样组织的（节选）：

```ts
import * as THREE from "three";

export interface SonyWf1000xm3Options {
  shadows?: boolean;
}

const COL = {
  bodyBlack: 0x1b1b1e,
  copper: 0xe3b184,
  gold: 0xc9a24b,
  // ...
};

const CASE_LEN = 2.62;
const CASE_DEP = 1.12;
```

上面代码中，颜色与尺寸不是「凭感觉起名」，而是从参考量出来的常数；后面才会用原语拼出盒盖、耳塞、触点，并挂上可循环的开合动画。根节点上还会通过 `userData.sculptRuntime` 暴露节点、插槽、碰撞体等，方便接动画，而不是一块不能动的摆件。

## 七、为什么说它「省 token」

多数「图生 3D」Agent 循环，会把机械劳动也塞进模型上下文：反复通读整份模型、手算像素、口头校验 JSON、重复已经做过的步骤。

img2threejs 的对策可以概括成几条：

（1）脚本强制执行，模型只判视觉  
（2）零额外依赖，少在对话里排环境故障  
（3）按关生成，不每次重生整模  
（4）规格浅就 fail-fast，别先 codegen  
（5）每关只看一张打包好的对比图  
（6）交付文本（TS + JSON），而不是巨型二进制 mesh

效果是：你仍然在做「从图到三维」，但昂贵的模型上下文，尽量留给判断与写码，而不是簿记。

## 八、边界与常见误区

官方自己写得很直白：单张图不可能保证隐藏面精确，也不能保证人物 100% 像。硬表面物体更强；角色偏风格化重建。说「这张图达不到你要的保真度」是合法结果，不是失败话术。

容易踩的坑：

（1）把它当成「一键摄影测量」——目标产物是代码工厂，不是扫描 mesh  
（2）关掉严格门赶进度——省一时，后面渲染和 token 更贵  
（3）用漂亮贴图掩盖结构空洞——项目里对武器等路线还有专门门禁，防止「贴图像、结构空」  
（4）期望背面细节与正面同精度——看不见的区域应标低置信度，而不是编造

可选地，仓库也接 SAM2、Depth Anything、MediaPipe 等参考保真工具；它们提供证据，不替代过关判决。

## 九、小结

img2threejs 解决的是：在 Agent 工作流里，把一张参考图重建成 **可进仓库、可审查、可动画** 的 Three.js 程序模型，并用脚本把门、用模型看图，压住 token 浪费。

若你做的是浏览器展示、可交互道具、需要版本管理的三维资产，值得先打开官方 showcase 转一转现成 demo，再按 skill 挂到自己的宿主里试一张硬表面物体图。

它不替代 DCC 工作流，也不是万能 mesh 生成器。把它理解成「带质量门的程序化雕刻流水线」，预期会准很多。

（完）
