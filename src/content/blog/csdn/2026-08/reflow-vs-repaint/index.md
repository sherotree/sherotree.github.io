---
title: 重排与重绘：前端性能的两个词
date: 2026-08-13
description: 用白话区分浏览器重排（layout/reflow）与重绘（paint）：几何变化常触发重排，外观颜色变化可能只重绘，并给出少踩坑的写法直觉。
tags: [前端, 性能, 重排, 重绘, 浏览器]
draft: true
---

重排（reflow / layout）与重绘（repaint）是浏览器把 DOM/CSS 变成屏幕像素时的两段常见工作。

性能讨论里这两个词出现频率极高，也极容易被混用。有人改个颜色就说「触发重排」，有人把所有卡顿都归咎于「重绘太多」。分清以后，优化才有靶子。

![从 Layout 到 Paint 再到合成](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/reflow-repaint-pipeline_8J3lzQTUF.png)

## 一、先说一个具体麻烦

一段列表滚动时卡顿。你加了阴影、改了颜色，又用 JS 读 `offsetHeight` 做计算。

若分不清重排与重绘，你会随机删样式，或随机加 `will-change`，像在碰运气。

更有用的问法是：

（1）我是否在逼浏览器重新算几何？  
（2）还是只需要重新画像素？  
（3）是否在读布局结果，造成强制同步布局？

## 二、两个词分别指什么

浏览器渲染管线可以简化成：

（A）算样式  
（B）**Layout（重排）**：算元素几何——大小、位置  
（C）**Paint（重绘）**：把视觉效果画成图层上的像素  
（D）Composite（合成）：图层拼到屏幕（动画常希望主要发生在这里）

所谓重排，重点是几何可能变了，后面的 paint 往往也要跟着来。  
所谓重绘，重点是外观变了，但几何可能不变（例如只改颜色）。

不是每次样式变化都同等代价；也不是「重绘一定比重排便宜到可以无视」。但**改几何通常更重**，这个直觉很管用。

## 三、什么容易触发重排，什么可能只重绘

![几何变化偏重排，颜色变化可能只重绘](https://ik.imagekit.io/4pjac7gmxh/blog/2026/09/reflow-vs-repaint-triggers_bxlHtS44k.png)

更常牵涉重排的（示例，非完整表）：

（1）改 `width` / `height` / `padding` / `margin` / `border`  
（2）改字体大小、文字内容导致换行变化  
（3）显示/隐藏若影响占用（如 `display`）  
（4）读写布局信息：`offsetTop`、`getBoundingClientRect()`、`clientWidth` 等

更常「主要是重绘」的（在几何不变时）：

（1）`color`、`background-color`  
（2）部分阴影、轮廓变化（仍可能不便宜，但不一定先重算整树几何）

`transform` / `opacity` 的动画，现代浏览器常尽量走合成层，避免每帧大布局。这是「为什么动画偏好 transform」的通俗原因。细节因浏览器而异，但方向正确。

## 四、强制同步布局：隐藏的性能坑

典型反模式：在循环里又写样式又读布局。

```js
for (const el of list) {
  el.style.width = '100px'      // 写
  const h = el.offsetHeight     // 读：可能被迫立刻 layout
  doSomething(h)
}
```

上面代码中，浏览器无法把多次写合并后再算，只能穿插同步布局，成本被放大。这叫强制同步布局（forced synchronous layout）一类问题。

更稳的节奏是：先读后写，或批量读、批量写，避免交错。

```js
const heights = list.map((el) => el.offsetHeight) // 先读完
list.forEach((el, i) => {
  el.style.height = heights[i] + 10 + 'px' // 再写
})
```

上面代码中，读取集中，写入集中，给浏览器合并计算的机会。

## 五、优化时怎么用这两个词

（1）先用 Performance / 性能面板看是 Layout 多还是 Paint 多，不要猜  
（2）动画：优先 `transform`/`opacity`，少每帧改宽高  
（3）列表：虚拟化减少 DOM 数量，比纠结单次重绘更有效  
（4）读布局：缓存结果，避免滚动监听里疯狂 `getBoundingClientRect`  
（5）CSS 选择器与层级很深时也会让样式计算变贵——那是上游步骤，但常和卡顿一起出现

重排、重绘是诊断词汇，不是宗教。目标是减少**不必要的工作**，不是消灭一切 paint。

## 六、常见误区

（1）**改任何 CSS 都叫重排**  
不准确；先问是否影响几何。

（2）**`will-change: everything` 当加速器**  
可能浪费内存，用完应撤。

（3）**只看 FPS，不看主线程里 Layout 火焰图**  
会优化错层。

（4）**用 `display: none` 与 `visibility: hidden` 当一回事**  
前者通常更影响布局流，后者占位不同。

（5）**把合成当成永远免费**  
层过多也有代价。

## 七、小结

重排关心几何有没有重算；重绘关心像素有没有重画。几何变化往往更贵；颜色等外观变化可能只走重绘；读写布局交错会逼出强制同步布局。

把两个词分清，前端性能讨论才不会一直在「感觉卡」上空转。

（完）
