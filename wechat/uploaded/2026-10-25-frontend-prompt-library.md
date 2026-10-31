# 重复问了三次的前端提示词，我干脆推进仓库了

- 素材日：2026-10-25
- 交稿日：2026-10-26

## 正文

以前我用 ChatGPT，像投币买罐可乐：要个 hook 投一次，要个 PR 总结再投一次。每次都从零交代技术栈、约定、「怎样算写完」。回过来的东西能跑，但跟我们仓库里最近几份 PR 总对不齐，下次还得再讲一遍。

浪费的不是 token，是同一套前端规矩被重复口述。

昨天我在 Dev.to 写了这篇：[From One-Off ChatGPT Asks to a Reusable Frontend Prompt Library](https://dev.to/sherotree/from-one-off-chatgpt-asks-to-a-reusable-frontend-prompt-library-3f11)。核心就一件事：把常问的前端活，当成代码来管——有文件名、进 git、改了走 PR。

我现在的做法很土：仓库里放一个 `prompts/frontend/`，每个文件只干一件事。比如 `new-component.md`、`accessible-react.md`、`pr-review-ai.md`、`design-token-change.md`。一个月用不到两次的，不配占一个文件，继续当聊天里的便利贴就行。

每个文件我强制同一种骨架：什么时候用、要贴什么上下文、硬规矩、输出必须有哪些段、「完成」长什么样。模型最会填空，你不给空，它就给你编气氛。

接线也很简单：Cursor / Copilot 指到这个目录，PR 机器人加载 `pr-review-ai.md`，需要脚手架时用 `@new-component` 展开。不需要搞提示词 CMS，Markdown 够用。

独立开发或副业项目里，这招特别值：你一个人又写产品又审代码，脑子里那套「Modal 要焦点陷阱 / Escape / 回焦」很容易在第三次粘贴时漏掉。提示词进仓库之后，记忆在 git 里，不在聊天滚动条里。

今晚不用做三十个。挑你最近两周重复问过三次的三件事，各写成一个 md，丢进仓库。下次别再开空白对话框，打开对应文件粘一次就行。
