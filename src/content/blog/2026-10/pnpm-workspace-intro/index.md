---
title: pnpm workspace 入门：多包仓库怎么组织
date: 2026-10-16
description: 说明用 pnpm workspace 组织 monorepo：workspace 声明、包之间依赖、以及和多仓库相比解决什么问题。
tags: [pnpm, monorepo, Node.js, 工程]
draft: true
---

pnpm workspace 是用 pnpm 包管理器把多个 package 放进同一仓库协同开发的方式，也就是常见的 monorepo 实践之一。

前端与 Node 项目长大以后，常拆成 `apps/*` 与 `packages/*`。没有 workspace，你会陷入：改共享库要先发版，再在应用里升版本，来回折腾。

![apps 与 packages 组成的 workspace](https://ik.imagekit.io/4pjac7gmxh/blog/2026/10/pnpm-workspace-boxes_IR-AE9J2U.png)

## 一、先说一个具体麻烦

公司有网站 A、网站 B，共用一个 UI 包。若分三个 Git 仓库：

（1）改按钮样式要发 UI 版  
（2）两个网站分别升级  
（3）本地联调要 `npm link` 玄学

workspace 把它们放进一个仓库：改 UI，应用立刻链到本地代码，发布策略可以稍后统一。

## 二、最小结构

根目录常见文件：

```text
pnpm-workspace.yaml
package.json
apps/web/
packages/ui/
```

`pnpm-workspace.yaml` 示例：

```yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

上面配置中，凡匹配目录且含 `package.json` 的，都会成为 workspace 包。

## 三、包之间怎么依赖

在 `apps/web/package.json`：

```json
{
  "dependencies": {
    "@acme/ui": "workspace:*"
  }
}
```

上面代码中，`workspace:*` 表示依赖仓库内的 `@acme/ui`，安装时链到本地包，而不是先去 npm 下旧版。

根目录执行：

```bash
pnpm install
```

pnpm 会处理 workspace 拓扑，并以其硬链/内容寻址方式管理依赖，减少重复拷贝（实现细节可随版本变化，心智模型是「省空间、严开销」）。

![workspace 协议把本地包链接起来](https://ik.imagekit.io/4pjac7gmxh/blog/2026/10/pnpm-link-flow_Gy_O1jenh.png)

## 四、它解决什么，不解决什么

解决：

（1）本地跨包联调  
（2）统一工具链与 CI  
（3）共享代码的原子提交

不自动解决：

（1）权限与代码所有权（仍要约定谁改 packages）  
（2）构建顺序与缓存（常配合 turbo 等，但非必须起步）  
（3）版本发布策略（changeset 等另谈）

## 五、入门建议

（1）先两个包跑通：一个 lib，一个 app  
（2）公共代码进 `packages`，可部署应用进 `apps`  
（3）根脚本用 `pnpm -r` / `--filter` 跑任务  
（4）避免循环依赖

```bash
pnpm --filter web dev
pnpm -r typecheck
```

上面命令中，`--filter` 对准单包；`-r` 递归。

## 六、常见误区

（1）**把一切都塞进一个 package.json**  
失去拆包意义。  
（2）**workspace 包名乱跳**  
与目录名、发布名不一致会乱。  
（3）**在子包私自 npm install 破坏布局**  
统一在根用 pnpm。  
（4）**未声明 workspace 协议却期望本地链接**  
版本号会指向 registry。

## 七、小结

pnpm workspace 用一份仓库、多个 package、workspace 依赖协议，解决多包联调与共享代码的组织问题。先会声明 workspace 与 `workspace:*`，再谈复杂发布与缓存。

（完）
