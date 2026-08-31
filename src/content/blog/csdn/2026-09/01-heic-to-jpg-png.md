# iPhone 拍的 HEIC 怎么转 JPG/PNG？交作业、发钉钉不用再求人

HEIC（High Efficiency Image Container）是 iPhone 近几年默认的拍照格式。同样一张图，它比 JPG 更小，画质往往还更好。

麻烦在于：很多场景并不认这个格式。老师收作业的系统只收 JPG；同事用 Windows 电脑打不开你 AirDrop 过来的照片；钉钉、邮件附件有时也会提示「格式不支持」。你明明有图，对方却看不见。

本文用浏览器在线工具，把 iPhone 拍的 HEIC 转成通用的 JPG 或 PNG。全程不用安装 Photoshop，也不用把照片上传到陌生服务器——解码在本地浏览器里完成。

![iPhone 拍照与 HEIC 格式](https://ik.imagekit.io/4pjac7gmxh/blog/iphone-photo-hero_91bPqI8_-.jpg)

---

## 一、HEIC 是什么，为什么 Windows 经常打不开

简单说，HEIC 是苹果推的高效图片容器。iPhone 拍完照，相册里存的往往不是 `.jpg`，而是 `.heic`（或扩展名写成 `.heif`，本质同类）。

你可以把它想成「精装外文书」：内容很好，体积也省，但不少「只收平装稿」的系统读不了。Windows 10/11 默认没有好用的 HEIC 查看器；学校教务网、公司 OA、老版本 Word 也常常只认 JPG/PNG。

下面三种格式怎么选，一张图概括：

![HEIC、JPG、PNG 格式对比](https://ik.imagekit.io/4pjac7gmxh/blog/heic-format-compare_bU9MDTROG.png)

（1）**HEIC**：省空间、画质好，但兼容性差。  
（2）**JPG**：兼容性最好，适合发群、交作业、插 PPT。有损压缩，不支持透明。  
（3）**PNG**：无损，适合还要二次修图、或需要透明底的场景；体积通常更大。

---

## 二、什么时候转 JPG，什么时候转 PNG

多数日常场景，**转 JPG 就够了**：

- 钉钉 / 微信 / 邮件发图
- 学校、单位系统上传附件
- 简历、文档里插图
- 网页后台上传（后台往往限制 JPG/PNG）

下面这些情况，**优先考虑 PNG**：

- 照片里有人像抠图、Logo 等，你后面还要做透明底
- 需要无损保存，不想 JPG 压缩带来额外损失
- 设计同事明确要求 PNG

如果拿不准：先转 JPG 发出去；对方说「糊了」或「要透明底」，再换 PNG。

---

## 三、浏览器里转 HEIC：三步走完

整体路径如下。不用装客户端，打开网页、上传、下载即可。

![iPhone 照片转通用格式的常见路径](https://ik.imagekit.io/4pjac7gmxh/blog/heic-convert-flow_A6e_IOZ-z.png)

下面分 JPG 和 PNG 两条线说明。两条线的操作几乎一样，只是输出格式不同。

### 3.1 HEIC 转 JPG（交作业、发钉钉）

**步骤 1：** 在电脑浏览器打开 [HEIC 转 JPG 在线工具](https://www.uwarp.design/heic-to-jpg?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=heic-jpg)。

![HEIC 转 JPG 上传界面](https://ik.imagekit.io/4pjac7gmxh/blog/heic-to-jpg-upload_eXIpRjAte.png)

**步骤 2：** 点击上传区，选中 iPhone 导出的 `.heic` 文件。也可以把文件拖进页面。

照片从 iPhone 弄到电脑，常见做法有：

- **AirDrop** 到 Mac，再从「照片」或「文件」里导出
- **数据线连接**，用「照片」应用导入
- **微信 / 钉钉传原图**（注意：部分渠道会自动压成 JPG，若已是 JPG 就不必再转）

**步骤 3：** 上传后右侧会出现预览。中间有**质量滑块**（默认大约 92%），可以边拖边看体积与清晰度。满意后点下载，得到 `.jpg` 文件。

![HEIC 转 JPG 预览与下载](https://ik.imagekit.io/4pjac7gmxh/blog/heic-to-jpg-result_v_25ZxeFJ.png)

上面流程里，解码和转码都在浏览器本地完成，文件不会传到网站服务器。单张大小限制为 **50 MB**，一般手机照片足够用。

### 3.2 HEIC 转 PNG（无损、方便后续修图）

需要 PNG 时，打开 [HEIC 转 PNG 在线工具](https://www.uwarp.design/heic-to-png?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=heic-jpg)，同样上传 HEIC，预览无误后下载即可。

![HEIC 转 PNG 上传界面](https://ik.imagekit.io/4pjac7gmxh/blog/heic-to-png-upload_YsJ01-DFK.png)

![HEIC 转 PNG 预览与下载](https://ik.imagekit.io/4pjac7gmxh/blog/heic-to-png-result_FYokJG_bZ.png)

PNG 没有质量滑块，因为本身是无损导出。如果下载后文件太大，可以再用图片压缩工具处理。

---

## 四、和命令行比，浏览器方案适合谁

如果你会写脚本，macOS 上也可以用 `sips` 或 ImageMagick 批量转。下面是一条 macOS 自带的例子，把当前目录所有 HEIC 转成 JPG：

```bash
for f in *.HEIC *.heic; do
  [ -f "$f" ] || continue
  sips -s format jpeg "$f" --out "${f%.*}.jpg"
done
```

上面代码中，`sips` 是 macOS 内置命令；`--out` 指定输出文件名。Windows 用户通常没有这条命令，需要额外装工具。

浏览器方案的好处是：**零安装、跨平台**。你在公司 Windows、家里 Mac、甚至 Linux 上，打开同一个链接就能转，适合偶尔处理几张图的同学和同事。

---

## 五、常见问题

### 5.1 Windows 双击 HEIC 打不开，一定要转吗？

不一定，但**要给别人看**时，转成 JPG 最省事。Windows 10/11 可以在「应用商店」安装「HEIF 图像扩展」，装完能预览，但很多网页上传入口仍然只收 JPG/PNG。要交作业、发钉钉，直接转 JPG 少扯皮。

### 5.2 转完 JPG 发钉钉还是很大，怎么办？

HEIC 转 JPG 不会自动把图「压到很小」。如果钉钉提示体积超限，可以：

（1）在工具里把 JPG **质量滑块**往低调一点（例如 80～85），一般肉眼差别不大。  
（2）用图片压缩或改尺寸工具再处理。  
（3）发「文件」而不是直接贴图，有时限制更宽松——以你所在群/组织的实际规则为准。

### 5.3 转 PNG 比 JPG 大很多，正常吗？

正常。PNG 无损，体积通常大于 JPG。若不需要透明底、也不打算反复编辑，发图用 JPG 更合适。

### 5.4 要不要再转成 WebP？

WebP 适合**你自己管的前端页面**，能省流量。但交作业、发钉钉、给同事看图，**JPG 兼容性仍然最好**。

### 5.5 上传后提示解码失败？

常见原因：（1）文件损坏或不是标准 HEIC；（2）超过 50 MB 限制；（3）Live Photo 包了一层特殊结构。可以换一张从相册「导出原图」的文件重试；若是 Live Photo，需要先在相册里导出静态帧再转换。

---

HEIC 是 iPhone 省空间的好格式，但协作场景认的是 JPG/PNG。记住两条线：日常发图转 **JPG**，要无损或后续修图转 **PNG**；打开浏览器上传、预览、下载，不用求人装软件。

（完）
