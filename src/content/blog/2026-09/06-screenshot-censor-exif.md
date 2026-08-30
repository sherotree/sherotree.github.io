# 截图发群前先打码：模糊、马赛克、去 EXIF 三件套

开发者、运营、测试同学发截图到钉钉群、微信群里，最怕两件事：**敏感信息没挡住**，以及 **照片里藏着拍摄位置**。

手机号、API Key、后台 URL、客户数据——涂鸦两笔不一定盖干净。更隐蔽的是 EXIF：很多手机拍屏或拍文档的照片，元数据里带着 GPS、设备型号，发原图等于间接报地址。

本文讲浏览器里 **打码 + 查看元数据 + 去除 EXIF** 的组合操作，发群前过一遍更安心。

![截图与隐私安全](https://ik.imagekit.io/4pjac7gmxh/blog/06-censor-hero_zwCECwY3F.jpg)

---

## 一、只涂鸦够不够？

不够。随手画黑块，有时边缘漏字；放大仍能猜出内容。模糊和马赛克会把像素混在一起，更难还原。

EXIF 是另一回事：画面上看不出，但「另存为」或元数据工具一读，拍摄时间、GPS、相机型号都可能还在。发客户群、公开社区前，建议 **打码 + 去 EXIF** 一起做。

![截图发群前的两道保险](https://ik.imagekit.io/4pjac7gmxh/blog/06-censor-exif-flow_L_6gdjtFz.png)

---

## 二、打码：模糊与马赛克

### 2.1 选区域打码

打开 [图片打码（模糊/像素化）](https://www.uwarp.design/censor-photo-blur-pixelate?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=censor-exif)，上传截图，在敏感区域框选，选模糊或马赛克强度，预览后下载。

![打码工具上传界面](https://ik.imagekit.io/4pjac7gmxh/blog/06-censor-blur-upload_vhNAm-9ia.png)

![打码后预览](https://ik.imagekit.io/4pjac7gmxh/blog/06-censor-blur-result_4HXLMW1WO.png)

需要更自由涂抹时，可用涂鸦式打码功能，手指或鼠标涂哪遮哪。

打码要点：

- 密钥、Token 要完全盖住，留首尾字符也可能被猜
- 地址栏 URL 常含内部域名，整行遮
- 聊天窗口注意头像、群名是否涉密

---

## 三、EXIF：先查看，再删除

### 3.1 查看照片里有什么元数据

上传前先用图片元数据查看功能看一眼。

![查看元数据工具](https://ik.imagekit.io/4pjac7gmxh/blog/06-view-metadata-upload_ttHfUYgNg.png)

![元数据读取结果](https://ik.imagekit.io/4pjac7gmxh/blog/06-view-metadata-result_U4xLbengX.png)

常见字段包括：拍摄时间、相机/手机型号、GPS 经纬度、方向信息。电脑截图一般是 PNG，EXIF 较少；**手机拍屏、拍纸质文档** 更要查。

### 3.2 去除 EXIF

确认要清理时，打开 [去除 EXIF 数据](https://www.uwarp.design/remove-exif-data?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=censor-exif)，上传图片，下载「干净」版本再发群。

![去除 EXIF 工具](https://ik.imagekit.io/4pjac7gmxh/blog/06-remove-exif-upload_E3TbYssV1.png)

![处理完成预览](https://ik.imagekit.io/4pjac7gmxh/blog/06-remove-exif-result_mrswZ5stE.png)

处理在浏览器本地完成，适合不想把含内部信息的原图上传到不可信服务器的场景。

---

## 四、推荐发群前 checklist

（1）放大检查：打码区域是否漏边  
（2）查看元数据：有没有 GPS、设备序列号  
（3）去 EXIF 后另存新文件，不要原图直发  
（4）仍不放心：关键信息改用文字口述，别出现在图里

---

## 五、常见问题

### 5.1 打码后能恢复吗？

强模糊、大块马赛克很难恢复；简单半透明黑条有可能被调高对比度看清。涉密内容用高强度马赛克。

### 5.2 GPS 在哪看？

在元数据工具的 EXIF 区找 `GPSLatitude` / `GPSLongitude`，或中文界面里的「位置」字段。没有不一定是好事——有些 App 发图时会自动剥 EXIF，但仍建议显式检查。

### 5.3 截图 PNG 有 EXIF 吗？

纯软件截图通常没有 GPS，但可能有 DPI、色彩配置。去 EXIF 一键清理无副作用，发外面前做一次不亏。

### 5.4 打码和压缩顺序？

先打码，再压缩。先压再打码，边缘可能出现压缩伪影。

### 5.5 视频怎么打码？

本文针对静态图。视频需用视频编辑工具或专用打码功能，不在此展开。

---

发群前：**挡住该挡的像素，删掉该删的元数据**，比事后撤回省事得多。

（完）
