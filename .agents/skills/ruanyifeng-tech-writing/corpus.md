# 语料说明

## 重要限制

阮一峰博客**没有**对外公布「全站阅读量 Top 20」实时榜。早期年度总结里有过当年访问量排行，但不足以构成 2026 年精确全站 Top 20。

本 skill 的语料采用替代标准：

1. 中文技术圈长期高频引用、搜索常青的开发者手册类文章  
2. 结构完整、适合提炼「通俗技术文」手法（非周刊链接集）  
3. 实际阅读了全文结构与开篇/论证节奏（WebFetch），用于**风格归纳**，不入库原文

若日后拿到真实访问日志或作者公开榜单，可替换本表权重，但风格规则通常仍适用。

## 精读样本（风格提炼主样本）

| # | 文章 | URL | 提炼重点 |
|---|------|-----|----------|
| 1 | 理解 OAuth 2.0 | https://www.ruanyifeng.com/blog/2014/05/oauth_2_0.html | 场景痛点列表 → 名词 → 思路 → 流程 → 分模式 |
| 2 | OAuth 2.0 的一个简单解释 | https://www.ruanyifeng.com/blog/2019/04/oauth_design.html | 全程生活类比，最后映射回技术 |
| 3 | 函数式编程初探 | https://www.ruanyifeng.com/blog/2012/04/functional_programming.html | 「材料太难 → 我的笔记」开篇；定义→特点→意义 |
| 4 | 理解 RESTful 架构 | https://www.ruanyifeng.com/blog/2011/09/restful.html | 拆词讲解；综述（1）（2）（3）；误区节 |
| 5 | 浏览器同源政策及其规避方法 | https://www.ruanyifeng.com/blog/2016/04/same-origin-policy.html | 概述→限制→分章对策；银行 Cookie 场景 |
| 6 | 跨域资源共享 CORS 详解 | https://www.ruanyifeng.com/blog/2016/04/cors.html | 分类→流程→字段逐条；先概念后报文 |
| 7 | HTTP 协议入门 | https://www.ruanyifeng.com/blog/2016/08/http.html | 按版本演进；每节「是什么→例子→缺点」 |

## 辅助参照（同系长青文，结构校验）

未全文精读每一字，但同属「开发者手册」叙事，用于校验标题与目录习惯：

| 文章 | URL |
|------|-----|
| Fetch API 教程 | https://www.ruanyifeng.com/blog/2020/12/fetch-tutorial.html |
| Cookie 的 SameSite 属性 | https://www.ruanyifeng.com/blog/2019/09/cookie-samesite.html |
| curl 的用法指南 | https://www.ruanyifeng.com/blog/2019/09/curl-reference.html |
| 网页性能管理详解 | https://www.ruanyifeng.com/blog/2015/09/web-page-performance-in-depth.html |
| 函数式编程入门教程 | https://www.ruanyifeng.com/blog/2017/02/fp-tutorial.html |
| OAuth 2.0 的四种方式 | https://www.ruanyifeng.com/blog/2019/04/oauth-grant-types.html |
| 浏览器缓存知识小结等相关缓存文 | 同站「开发者手册」分类 |

合计精读 + 辅助约 **15～20 篇量级**，覆盖其技术文主流写法；**刻意弱化**纯周刊体（链接合集 + 短评），因与 CSDN 工具教程目标不完全一致。

## 从语料抽出的可迁移模式（摘要）

1. 标题动词化理解：`理解` / `详解` / `入门`  
2. 开篇承认「难懂 / 术语多」，承诺「简明」  
3. 先故事或反例，再正式定义  
4. 中文序号分层，叶子节点才上细节字段  
5. **配图**：流程文有示意图；工具/机制文在关键节插图；图下常有说明或承接句  
6. **代码块**：协议/API/配置类高频出现最小报文或片段；节奏为「先说明 → 代码 → 上面代码中……」  
7. 常有「误区 / 对比 / 意义」收束章  
8. 文末 `（完）`

### 语料中的图与代码观察（精读样本）

| 文章类型 | 图 | 代码 |
|----------|----|------|
| OAuth / CORS / HTTP 等协议文 | 流程或结构示意 | 大量最小 HTTP 请求/响应、头字段示例 |
| 函数式编程等概念文 | 相对少，以短代码证明概念 | 短 JS 片段 + 段后解释 |
| 同源政策等「方法并列」文 | 按需 | 每种规避手段配一小段可运行示例 |

结论：其技术文不是「纯叙述」；**能画的流程会画，能演示的接口会给出可对照的代码块**。本 skill 写文时必须继承这一点。

## 版权

文章版权归原作者。本目录只保留**风格描述与自拟示例**，不含其正文拷贝。使用本 skill 产出内容时，须保证题材与表述原创。
