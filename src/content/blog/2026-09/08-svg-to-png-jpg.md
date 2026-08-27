# SVG 图标导出 PNG/JPG：模糊、透明底、尺寸怎么设

前端拿到设计师的 SVG 图标，要放进 PPT、交 Android 资源、或发运营做推文——对方往往只要 PNG/JPG。直接改扩展名不行，需要 **栅格化**：按指定像素宽高渲染成位图。

导出最常见的坑是 **尺寸太小发虚**，或 **该透明却铺了白底**。本文用浏览器工具讲清 SVG 查看、定倍率、选格式。

![SVG 矢量与栅格导出](https://ik.imagekit.io/4pjac7gmxh/blog/08-svg-hero_oxjdHE1nGo.jpg)

---

## 一、SVG 和 PNG 的本质区别

SVG 是矢量：放大不糊，由路径和公式描述。PNG/JPG 是栅格：固定像素格子，尺寸不够就虚。

你可以把它想成「无限放大的地图」和「固定分辨率的卫星照片」。要插入 Word 或老后台，对方只收照片，就得先定好要多清晰的「照片」。

![SVG 导出栅格图别发虚](https://ik.imagekit.io/4pjac7gmxh/blog/08-svg-export-flow_YQTuosxBc.png)

---

## 二、导出前先预览 SVG

上传前用 [SVG 查看器](https://www.uwarp.design/svg-viewer?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=svg-raster) 打开文件，确认路径、留白、颜色是否符合预期。

![SVG 查看器上传](https://ik.imagekit.io/4pjac7gmxh/blog/08-svg-viewer-upload_IyXAQatUd.png)

![SVG 预览效果](https://ik.imagekit.io/4pjac7gmxh/blog/08-svg-viewer-result_1cEMk4tI5.png)

有些 SVG 自带 `viewBox` 很大但图形很小，导出前可用 [调整 SVG 尺寸](https://www.uwarp.design/resize-svg) 规范化画布，避免导出一片留白。

---

## 三、SVG 转 PNG：要透明底时

打开 [SVG 转 PNG](https://www.uwarp.design/svg-to-png?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=svg-raster)，上传 SVG，设置输出宽度（高度常按比例）。

![SVG 转 PNG 上传](https://ik.imagekit.io/4pjac7gmxh/blog/08-svg-to-png-upload_hXtrnL3UT.png)

![SVG 转 PNG 预览](https://ik.imagekit.io/4pjac7gmxh/blog/08-svg-to-png-result_vMFlsdgs3.png)

**倍率建议：**

| 用途 | 参考宽度 |
|------|----------|
| 网页 `@1x` 图标 24px | 导出 24～48px |
| Retina `@2x` | 设计稿尺寸 × 2 |
| PPT / 文档插图 | 400～800px |
| App 商店图 | 按平台规范表 |

图标设计稿 24×24，给 Retina 屏至少导出 **48×48**；再小放大就会糊。

---

## 四、SVG 转 JPG：不需要透明时

发邮件、插不支持透明的系统，用 [SVG 转 JPG](https://www.uwarp.design/svg-to-jpg?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=svg-raster)。JPG 会铺底色（通常白），体积一般小于 PNG。

---

## 五、用命令行导出（可选）

已装 Inkscape 时：

```bash
inkscape icon.svg --export-type=png --export-width=96 -o icon@2x.png
```

上面代码中，`--export-width=96` 控制输出宽度。没有 Inkscape 时，浏览器工具零安装更方便。

---

## 六、常见问题

### 6.1 导出发虚怎么办？

加大输出宽度。24px 图标至少导出 48px 或 72px，别直接用 CSS 把小图拉大。

### 6.2 要不要留透明底？

要叠在彩色背景、做 App 图标：**PNG**。要最小体积、背景本来就是白色：**JPG**。

### 6.3 颜色和设计稿不一致？

检查 SVG 里是否写死 `#000`；是否用了 `currentColor` 依赖外层 CSS。独立导出时选查看器里最终呈现的颜色为准。

### 6.4 带 `<image>` 外链的 SVG？

若 SVG 引用外部位图，离线导出可能缺图。请设计 embed 或提供完整文件。

### 6.5 字体图标 SVG？

文字转路径（outline）再导出最稳；否则依赖系统字体，换电脑字形可能变。

---

## 七、在线工具

| 任务 | 链接 |
|------|------|
| SVG 转 PNG | https://www.uwarp.design/svg-to-png?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=svg-raster |
| SVG 转 JPG | https://www.uwarp.design/svg-to-jpg?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=svg-raster |
| SVG 查看器 | https://www.uwarp.design/svg-viewer?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=svg-raster |
| 调整 SVG 尺寸 | https://www.uwarp.design/resize-svg?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=svg-raster |

记住：**先预览、再定 2x/3x 宽度、最后选 PNG 还是 JPG**，图标导出就不容易糊。

（完）
