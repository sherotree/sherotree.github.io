# 不会用 Photoshop？PSD 直接转 JPG/PNG 给同事

设计同事发来 `.psd`，你电脑没装 Photoshop，双击打不开。邮件里写「请导出 JPG」，对方忙起来又要等半天。

其实不少场景只需要 **一张扁平化的出图**：海报定稿、Banner 预览、给开发切临时参考图。不必开 PS，浏览器里就能把 PSD 转成 JPG 或 PNG 下载。

本文讲在线转换步骤，以及 **能力边界**——哪些 PSD 能完美转，哪些要降低预期。

![设计稿与 PSD 文件](https://ik.imagekit.io/4pjac7gmxh/blog/07-psd-hero_AYok1SzNC.jpg)

---

## 一、PSD 为什么别人打不开

PSD 是 Adobe Photoshop 的专有格式，里面可能有 dozens 个图层、智能对象、调整图层、蒙版。普通看图软件只认「最终结果」，不认图层结构。

你可以把它想成「带全部施工图纸的精装房模型」：业主只想看效果图，不需要进工地。在线转换器做的是 **渲染合成后的平面图**（JPG/PNG），不是可编辑的 PSD。

---

## 二、浏览器里 PSD 转 JPG / PNG

### 2.1 转 JPG（体积小、发邮件方便）

打开 [PSD 转 JPG](https://www.uwarp.design/psd-to-jpg?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=psd-export)，上传 PSD，预览合成效果，调 JPG 质量后下载。

![PSD 转 JPG 上传界面](https://ik.imagekit.io/4pjac7gmxh/blog/07-psd-to-jpg-upload_hwSa8GTmH.png)

适合：发钉钉预览、插 PPT、给非设计同事过目。

### 2.2 转 PNG（无损、可能要透明）

需要无损或保留透明区域时，用 [PSD 转 PNG](https://www.uwarp.design/psd-to-png?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=psd-export)。PNG 体积更大，但适合再进其他设计工具或网页。

---

## 三、能力边界（诚实说明）

在线 PSD 解析 **不能 100% 复刻 Photoshop**。下面情况可能和设计师本机导出不一致：

（1）**复杂图层样式**：特殊混合模式、高级渐变可能偏差  
（2）**智能对象**：嵌套过深时可能 rasterize 异常  
（3）**字体**：你电脑没有的字体，会替换成默认字形  
（4）**3D、视频图层**：多数在线工具不支持

若用于 **正式印刷、品牌交付**，仍请设计师在 PS 里「导出为 Web」或「存储为副本」。在线工具适合 **快速预览、内部沟通、临时占位**。

---

## 四、和设计师协作的小技巧

- 让对方同时发 **PDF 或 PNG 定稿**，PSD 作备档
- 只要某一图层？请设计 **单独导出该图层 PNG**，比你自己在 PSD 里找图层省事
- 文件超过 50 MB 时，先让设计「合并可见图层」另存较小 PSD

---

## 五、常见问题

### 5.1 图层会丢吗？

导出 JPG/PNG 是 **合成后的单张图**，图层信息本来就会丢。这是格式决定的，不是工具 bug。

### 5.2 转出来颜色发灰？

检查 PSD 是否 CMYK 色彩模式；部分工具按 sRGB 预览。印刷稿请以设计稿为准。

### 5.3 透明背景能保留吗？

转 PNG 时，若 PSD 最上层合成结果带透明，有机会保留；带背景色的稿则是实心底。

### 5.4 批量转换？

一次处理一个文件最稳。批量建议设计用 PS 动作，或 IT 用 ImageMagick 等（支持有限）。

### 5.5 文件安全吗？

浏览器本地解析的方案，文件不上传服务器，适合不方便把客户稿传到公网转换器的场景。超大或机密文件仍建议内网工具。

---

没装 PS 也能把 PSD 变成通用图片；正式交付仍找设计师原文件导出最稳。

（完）
