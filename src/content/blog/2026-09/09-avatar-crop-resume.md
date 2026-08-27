# 简历头像、微信头像一次裁方/裁圆（含常见尺寸）

投简历、换微信头像、填报名系统，上传框往往写着：**「请上传正方形照片」「尺寸 295×413」「文件小于 2MB」**。手机相册里大多是竖构图全身或半身，比例不对直接被拒。

其实不需要开 PS。浏览器里 **裁方 → 裁圆 → 按像素导出**，几分钟搞定。

![证件照与头像裁剪](https://ik.imagekit.io/4pjac7gmxh/blog/09-avatar-hero_G0WH0qxXx.jpg)

---

## 一、常见尺寸对照（参考）

不同平台规则会变，投稿前以官网为准。下面数字供裁剪时参考：

![常见头像尺寸参考](https://ik.imagekit.io/4pjac7gmxh/blog/09-avatar-sizes_Nwafg0kcH.png)

| 场景 | 常见尺寸 | 说明 |
|------|----------|------|
| 微信头像 | 400×400 | 方形，建议 < 2MB |
| 简历证件照（1 寸） | 295×413 px | 约 2.5×3.5 cm @300dpi |
| 简历证件照（2 寸） | 413×579 px | 约 3.5×4.9 cm |
| 网站个人头像 | 256～512 方形 | 圆形展示常见 |
| linkedin / 招聘 App | 400×400 或 800×800 | 以平台提示为准 |

---

## 二、第一步：裁成方形

打开 [方形裁剪](https://www.uwarp.design/square-crop?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=avatar-crop) 或 [头像裁剪器](https://www.uwarp.design/pfp-cropper?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=avatar-crop)，上传照片，拖动取景框对准脸部，导出正方形。

![头像裁剪器上传](https://ik.imagekit.io/4pjac7gmxh/blog/09-pfp-cropper-upload_FrvkkGvKg.png)

![方形裁剪预览](https://ik.imagekit.io/4pjac7gmxh/blog/09-pfp-cropper-result_ExLOyYPSA.png)

证件照构图建议：头顶留一点空，眼睛在画面上 1/3 附近，背景尽量纯色（白/蓝）。

---

## 三、第二步：需要圆形头像时

个人站、论坛、部分 App 展示圆形头像，但文件仍可能是方形 PNG。用 [圆形裁剪](https://www.uwarp.design/circle-crop-image?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=avatar-crop)，导出 **带透明角的圆图**，叠在任意背景上不突兀。

![圆形裁剪上传](https://ik.imagekit.io/4pjac7gmxh/blog/09-circle-crop-upload_SvMyQ-eHN.png)

![圆形裁剪结果](https://ik.imagekit.io/4pjac7gmxh/blog/09-circle-crop-result__UAq3Vi3G.png)

若平台自己会裁圆（如微信），上传 **方形** 即可，让平台裁；需要你自己控边缘时，再导出圆形 PNG。

---

## 四、证件照与简历专用

部分报名系统要固定比例竖图。可用 [证件照 / 简历照片](https://www.uwarp.design/profile-photo?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=avatar-crop) 按模板比例裁剪，再导出 JPG 控制体积。

裁完后若超过 2MB，用 JPG 压缩或略降质量，别靠微信「发原图再保存」——那次序往往越弄越糊。

---

## 五、常见问题

### 5.1 圆裁导出是否带透明？

圆形裁剪工具通常导出 **圆内保留、圆外透明** 的 PNG。JPG 不支持透明，圆外会变成白底或黑底。

### 5.2 微信头像为什么发糊？

多次转发压缩所致。用裁剪工具 **直接导出目标尺寸**，一次上传，少经聊天压缩。

### 5.3 1 寸和 2 寸怎么记？

记像素比记厘米省事：295×413（1 寸）、413×579（2 寸）是国内简历常见电子版参考。

### 5.4 戴眼镜、刘海要露耳朵吗？

严格证件照有规定；一般简历 / 社交头像：**面部清晰、光线均匀** 即可，不必公安级标准。

### 5.5 能批量裁吗？

在线工具适合 1～几张。班级集体照裁剪建议用脚本或桌面软件批量；单人求职场景浏览器足够。

---

## 六、在线工具

| 任务 | 链接 |
|------|------|
| 头像裁剪器 | https://www.uwarp.design/pfp-cropper?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=avatar-crop |
| 方形裁剪 | https://www.uwarp.design/square-crop?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=avatar-crop |
| 圆形裁剪 | https://www.uwarp.design/circle-crop-image?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=avatar-crop |
| 证件照 / 简历照片 | https://www.uwarp.design/profile-photo?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=avatar-crop |

先 **裁方**，要圆再 **圆裁**，对照平台尺寸表导出，头像上传就不容易被打回。

（完）
