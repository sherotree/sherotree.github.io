# 录屏 MP4 怎么做成教程 GIF？浏览器里剪、压、加字幕

写技术博客、做产品说明、给同事演示操作步骤时，一张会动的 GIF 往往比长视频好贴——不用点播放，文档里直接循环展示。

录屏得到的是 MP4 或 MOV，体积大、平台不一定让自动播放。转成 GIF，再适度压缩，就能放进飞书文档、Notion、GitHub README 或 CSDN 文章。

本文讲浏览器里 **视频转 GIF → 裁剪 → 加字幕条** 的完整流程。

![录屏与教程动图](https://ik.imagekit.io/4pjac7gmxh/blog/04-video-hero_C_ErHG6c01.jpg)

---

## 一、什么时候用 GIF，什么时候留视频

**适合 GIF：**

- 操作步骤 3～15 秒，循环看能懂
- 文档 / README 里不能嵌播放器
- 需要「扫一眼就会」的演示

**更适合留 MP4：**

- 超过 20 秒、带旁白
- 需要声音
- 目标平台原生支持视频且可自动静音播放

GIF 的代价是体积和画质。教程动图建议 **宽度 640～800px、时长 10 秒内**，后面再压。

![录屏转 GIF 做教程动图](https://ik.imagekit.io/4pjac7gmxh/blog/04-video-gif-flow_St3YlfKTa.png)

---

## 二、MP4 转 GIF：三步走完

### 2.1 上传录屏并选片段

打开 [视频转 GIF](https://www.uwarp.design/video-to-gif?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=video-gif)，上传 MP4。页面里拖动时间轴，只保留关键操作那一段。

![视频转 GIF 上传界面](https://ik.imagekit.io/4pjac7gmxh/blog/04-video-to-gif-upload_wXwvJduxn.png)

![选段与预览](https://ik.imagekit.io/4pjac7gmxh/blog/04-video-to-gif-result_IvjDJ054W.png)

iPhone 录屏若是 MOV，可用 [MOV 转 GIF](https://www.uwarp.design/mov-to-gif?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=video-gif)，步骤相同。

### 2.2 控制体积：帧率与宽度

导出前注意：

- **宽度**：640px 对文档足够；Retina 截图可试 800px
- **帧率**：10～15fps 通常够用，再高体积涨得快
- **时长**：能短则短，循环 1～2 次即可

若 GIF 仍太大，再用 [GIF 压缩](https://www.uwarp.design/gif-compressor) 或 [改尺寸](https://www.uwarp.design/gif-resizer) 处理。

### 2.3 裁掉多余帧

已经转出 GIF 但头尾多余？用 [GIF 裁剪](https://www.uwarp.design/gif-cutter) 精修时间范围。

![GIF 裁剪工具](https://ik.imagekit.io/4pjac7gmxh/blog/04-gif-cutter-upload_M5cDeCCfr.png)

![裁剪后预览](https://ik.imagekit.io/4pjac7gmxh/blog/04-gif-cutter-result_NNqaGkv_k.png)

### 2.4 加底部字幕条（可选）

演示步骤多时，在 GIF 底部加一行说明更清楚。打开 [GIF 加字幕](https://www.uwarp.design/add-caption-to-gif?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=video-gif)，上传 GIF，输入文字，调整位置后下载。

![GIF 加字幕工具](https://ik.imagekit.io/4pjac7gmxh/blog/04-gif-caption-upload_mK5o_kSq3.png)

![加字幕后的效果](https://ik.imagekit.io/4pjac7gmxh/blog/04-gif-caption-result_lCftaXzgW.png)

---

## 三、用 ffmpeg 批量转（可选）

本地已装 ffmpeg 时，命令行也很快：

```bash
ffmpeg -i demo.mp4 -vf "fps=12,scale=640:-1:flags=lanczos" -t 8 demo.gif
```

上面代码中，`fps=12` 控制帧率，`scale=640:-1` 把宽度缩到 640 像素，`-t 8` 只取前 8 秒。不会 ffmpeg 的同学，用浏览器工具更直观。

---

## 四、常见问题

### 4.1 转完颜色发灰、有噪点？

GIF 只有 256 色，录屏渐变区域容易有色带。可缩短时长、缩小尺寸，或接受一定画质损失。

### 4.2 时长建议多少秒？

教程单步 **3～8 秒** 最好；全流程不超过 **15 秒**，否则请拆成多个 GIF 或直接嵌视频。

### 4.3 和直接嵌视频比，SEO 有影响吗？

文章平台是否收录动图因站而异。技术文档里 GIF 的优势是 **零交互成本**；公开 SEO 页面若可放视频，视频往往更利于停留时长。

### 4.4 带鼠标点击的录屏要注意什么？

录屏前把桌面收拾干净，关闭通知；导出后检查有没有露出邮箱、路径等敏感信息。

### 4.5 处理是在本地吗？

视频转 GIF 在浏览器本地解码处理，适合不想把内部录屏上传到陌生服务器的场景。超大文件可能受浏览器内存限制，建议录屏片段先剪短再上传。

---

## 五、在线工具

| 任务 | 链接 |
|------|------|
| 视频转 GIF | https://www.uwarp.design/video-to-gif?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=video-gif |
| MOV 转 GIF | https://www.uwarp.design/mov-to-gif?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=video-gif |
| GIF 裁剪 | https://www.uwarp.design/gif-cutter?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=video-gif |
| GIF 加字幕 | https://www.uwarp.design/add-caption-to-gif?utm_source=csdn&utm_medium=article&utm_campaign=image-toolkit-cn&utm_content=video-gif |

录屏 → 选段 → 控参数 → 必要时加字幕，教程 GIF 在浏览器里就能做完。

（完）
