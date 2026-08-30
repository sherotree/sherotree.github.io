# 两张图横竖拼接：做对比图、PRD 附图不用开 PS

写 PRD、做竞品分析、写测评文章时，经常要把 **两张截图拼一起**：左边旧版右边新版，或上面问题下面答案。开 PS 太重，画图工具排版又慢。

浏览器里可以 **左右拼、上下拼、多图宫格、叠水印**。本文讲最常用的拼接场景和步骤。

![数据对比与拼图示意](https://ik.imagekit.io/4pjac7gmxh/blog/10-merge-hero_Poal8ZJjg.jpg)

---

## 一、三种拼接需求

![两张图拼一张：常见用法](https://ik.imagekit.io/4pjac7gmxh/blog/10-merge-flow_VE120ZqyV.png)

（1）**左右 / 上下拼**：两张图对照，适合 before/after、竞品对比。  
（2）**宫格组合**：三四张图排成网格，适合活动晒图、功能罗列。  
（3）**叠图**：一张底图上加标注、水印或半透明覆盖层。

下面分工具说明。

---

## 二、两张图左右或上下拼

打开 [合并图片](https://www.uwarp.design/merge-images?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=merge-images)，上传两张图，选横向或纵向，调间距与对齐，预览后下载。

![合并图片上传界面](https://ik.imagekit.io/4pjac7gmxh/blog/10-merge-images-upload_9uuuo_txz.png)

![拼接结果预览](https://ik.imagekit.io/4pjac7gmxh/blog/10-merge-images-result_oTWveJLDS.png)

写文档时建议：

- 两张截图 **宽度对齐**，阅读体验更好
- 中间留 8～16px 白缝，打印时也不粘在一起
- 导出 PNG 保留 UI 锐度；发邮件可再转 JPG 压体积

若两张图比例差很多，先各自把尺寸调到相同宽度再拼。

---

## 三、多图宫格排版

三四张以上用 [图片组合 / 宫格](https://www.uwarp.design/combine-maker?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=merge-images)，选 2×2、3×3 等模板，拖入图片位置。

![宫格组合工具界面](https://ik.imagekit.io/4pjac7gmxh/blog/10-combine-maker-upload_KSJo2289F.png)

适合运营海报草稿、功能点四宫格。正式印刷仍建议 Figma/PS，快速文档够用。

---

## 四、叠图与水印

要在截图上叠 Logo、箭头说明？可用图片叠加功能，调整上层透明度与位置。

两张 PNG 都有透明区域时，用合并 PNG 类工具保留 Alpha，适合图标、贴纸合成。

---

## 五、常见问题

### 5.1 PNG 透明拼接会铺白底吗？

左右拼接工具通常给透明区铺白或棋盘格预览；要保留透明通道选 PNG 合并类工具，并确认导出格式为 PNG。

### 5.2 拼完太大发不出去？

拼好后压缩图片或转 JPG。文档内展示宽度 1200px 往往足够，不必保留 4K 原拼接。

### 5.3 两张图颜色不一致？

截图前统一系统主题（都浅色或都深色）；拼完后整体调亮度比单张硬拼自然。

### 5.4 竖图拼横图怎么好看？

短边对齐，或中间加标题条说明左右含义，避免读者搞不清顺序。

### 5.5 能拼 GIF 吗？

GIF 合并有专门工具，与静态图合并不同，别混用入口。

---

对比图、PRD 附图：**先对齐尺寸，再拼，最后按需压缩**，比开 PS 快得多。

（完）
