# 网页要上 WebP：JPG/PNG 怎么转，以及何时别转

前端做性能优化时，常听到「把图片换成 WebP」。同样画质下，WebP 往往比 JPG 小 25%～35%；带透明的 PNG 转 WebP 也能省不少流量。

但 WebP 不是万能的。交作业、发微信、老系统后台上传，仍然只认 JPG/PNG。本文讲 **什么时候转、怎么在浏览器里转、以及如何做兼容回退**。

![网页性能与图片格式](https://ik.imagekit.io/4pjac7gmxh/blog/05-webp-hero_eFbSEpRXz.jpg)

---

## 一、WebP 是什么，为什么前端爱用

WebP 是 Google 推的图片格式，支持有损、无损和动画。对网站来说，更小的图片意味着更快的 LCP（最大内容绘制）和更少的 CDN 流量。

你可以把它想成「压缩更好的包装盒」：同样一件货，盒子更小，运输更便宜。但收件人那边得认这个盒子——不认的话，还得备一份 JPG 老包装。

![WebP：什么时候转、什么时候别转](https://ik.imagekit.io/4pjac7gmxh/blog/05-webp-when_0TUEeVWYW.png)

---

## 二、什么时候转 WebP，什么时候别转

**适合转：**

- 你自己部署的网站 / 博客静态资源
- 能用 `<picture>` 或 CDN 做格式协商
- 移动端 H5 页面，目标浏览器较新

**先别转：**

- 学校、单位系统上传附件
- 微信、钉钉直接发图
- 邮件正文插图给不确定环境的收件人

**收到 WebP 要插 PPT？** 先转回 JPG 或 PNG，再插入 Office。

---

## 三、浏览器里转换

### 3.1 JPG 转 WebP

打开 [JPG 转 WebP](https://www.uwarp.design/jpg-to-webp?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=webp-frontend)，上传照片，调质量，预览后下载。

![JPG 转 WebP 上传](https://ik.imagekit.io/4pjac7gmxh/blog/05-jpg-to-webp-upload_DUwLniSiB.png)

![JPG 转 WebP 预览](https://ik.imagekit.io/4pjac7gmxh/blog/05-jpg-to-webp-result_17PEyjuc3.png)

### 3.2 PNG 转 WebP（含透明）

Logo、带 Alpha 的 UI 切图，用 [PNG 转 WebP](https://www.uwarp.design/png-to-webp?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=webp-frontend)。透明通道可保留（视工具实现与导出选项而定），体积通常小于 PNG。

![PNG 转 WebP 上传](https://ik.imagekit.io/4pjac7gmxh/blog/05-png-to-webp-upload_dGXkg08al.png)

![PNG 转 WebP 预览](https://ik.imagekit.io/4pjac7gmxh/blog/05-png-to-webp-result_sT3XAUFDh.png)

转换在浏览器本地完成，适合处理少量素材，不必把源文件传到第三方服务器。

---

## 四、上线时怎么做兼容回退

网站不能只有 WebP。常见写法是用 `<picture>` 让浏览器自己选：

```html
<picture>
  <source srcset="hero.webp" type="image/webp" />
  <img src="hero.jpg" alt="首页横幅" width="1200" height="630" />
</picture>
```

上面代码中，支持 WebP 的浏览器加载 `.webp`；不支持的回退到 `.jpg`。Next.js、Vercel 等框架也提供自动图片优化，上传 JPG/PNG 由 CDN 按需输出 WebP。

Safari 很早版本对 WebP 支持不完整；2020 年后的 iOS/macOS 一般没问题。面向企业内网老浏览器时，务必保留 JPG/PNG 回退。

---

## 五、常见问题

### 5.1 Safari 老版本打不开 WebP？

iOS 14+、macOS Big Sur+ 原生支持较好。更老系统用 `<picture>` 回退 JPG，或服务端按 `Accept` 头内容协商。

### 5.2 动画 WebP 和 GIF 怎么选？

动画 WebP 体积通常小于 GIF，但 IM 软件、旧编辑器未必支持。网站内动画优先 WebP；表情包、文档里仍常用 GIF。

### 5.3 转完反而变大？

极小图标、简单 PNG 有时 WebP 不一定更小。以实际文件大小为准，不要迷信格式名。

### 5.4 无损 WebP 和 PNG 比呢？

无损 WebP 常比 PNG 小，但设计软件导出链路未必顺。设计交付仍常要 PNG，网站上再转 WebP 服务用户。

### 5.5 批量转换怎么办？

少量图用在线工具；整站素材可用 `cwebp` 命令行或构建脚本批量处理。在线工具适合快速验证质量再写进流水线。

---

网站性能优化用 WebP；人际协作发图仍用 JPG/PNG。两套场景分开，就不容易踩坑。

（完）
