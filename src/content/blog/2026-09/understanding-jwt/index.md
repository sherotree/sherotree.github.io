---
title: 理解 JWT：三段分别是什么
date: 2026-09-04
description: 拆开 JSON Web Token 的三段结构：Header、Payload、Signature 各自做什么，以及 JWT 不能解决什么问题。
tags: [JWT, 鉴权, 基础概念, 安全]
draft: true
---

JWT（JSON Web Token）是一种把声明（claims）编码成可传递字符串的方式，常见形态是三段用点号连接的 Base64URL 文本。

登录成功后，前端把一长串 `xxxxx.yyyyy.zzzzz` 塞进请求头，后端验过就认你是谁。资料里又是签名、加密、鉴权、会话，读完仍常不清楚：**三段各自是干什么的，以及它到底防什么**。

下面按结构拆开讲。

![JWT 的 Header、Payload、Signature 三段](./images/jwt-three-parts.png)

## 一、先说一个具体麻烦

接口要求：

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMifQ.signature
```

有人以为：这段字符串是加密的，用户看不懂，所以安全。  
也有人以为：只要有 JWT，就不用 HTTPS，也不用管注销。

两种想法都容易出事。JWT 默认常常是**可解码可读、靠签名防篡改**，不是保险箱；它也不是完整的会话产品方案。

## 二、核心思路：明信片 + 火漆印

简单说，常见的签名型 JWT 更像一张明信片：

（1）正面写着你的声明（谁、什么角色、何时过期）——路人可能读得到  
（2）火漆印证明「内容没被改过，且来自持有密钥的一方」  
（3）没火漆或火漆对不上，接收方直接拒绝

所以 JWT 解决的核心问题是：**在分布式服务之间，传递一份可验证的声明，而不必每次都回中心会话库查同一张表**（具体架构仍可选择有状态黑名单等，那是附加设计）。

## 三、三段分别是什么

标准 JWT 长这样：

```text
header.payload.signature
```

### 3.1 Header（头部）

描述元数据，常见是 JSON，再 Base64URL 编码。

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

上面代码中，`alg` 说明签名算法，`typ` 说明类型。接收方要按约定算法校验，不能盲目信任头部里「声称」的算法而不做白名单约束（历史上有算法混淆类问题，工程上需按安全实践配置）。

### 3.2 Payload（载荷）

放声明。仍是 JSON，再 Base64URL 编码。常见字段：

（1）`sub`：主体，常是用户 id  
（2）`iat` / `exp`：签发时间 / 过期时间  
（3）`iss` / `aud`：签发者 / 受众  
（4）自定义声明：角色、租户 id 等

注意：默认**不是加密**。任何人拿到 token，都能解码 payload 看内容。别把密码、身份证号一类敏感数据塞进去。

### 3.3 Signature（签名）

用密钥（或私钥）对「编码后的 header + payload」计算签名，防止篡改。

直觉公式（HMAC 类）：

```text
signature = HMAC_SHA256(
  base64url(header) + "." + base64url(payload),
  secret
)
```

上面结构中，改 payload 里的 `role` 却不重算合法签名，校验就会失败。这就是「火漆印」的作用。

## 四、一次典型校验流程

![客户端携带 JWT，服务端验签](./images/jwt-flow.png)

（A）用户登录，认证服务签发 JWT  
（B）客户端存储（怎么存是另一话题：内存、HttpOnly Cookie 等各有取舍）  
（C）请求业务 API 时带上  
（D）API 验签名、查 `exp`、查 `iss`/`aud` 等  
（E）通过则按声明授权；失败则 401

验签通过，只说明「声明未被篡改且来自可信签发方」。不自动等于「用户此刻仍应拥有全部权限」——权限回收、强制下线，需要额外机制。

## 五、JWT 不解决什么

（1）**保密性**：默认可读；要保密需走加密型方案（JWE）或根本别放敏感字段  
（2）**传输安全**：仍要 HTTPS，否则 token 会被窃听  
（3）**自动注销**：未过期的 token，在纯无状态模型下仍有效；要作废需黑名单、短过期 + 刷新令牌、或改密钥版本等  
（4）**替代授权设计**：有 token ≠ 权限模型正确；仍要做对象级授权检查

## 六、实践上几条最小建议

（1）payload 只放必要声明，控制体积  
（2）设合理 `exp`；长会话用刷新令牌旋转，而不是超长 access token  
（3）校验时核对算法、签发者、受众、过期时间  
（4）密钥用足够强度的随机值，并支持轮换  
（5）日志里不要完整打印 token

下面是一个解码示意（仅理解结构，生产请用成熟库验签）。

```js
const [h, p] = token.split('.')
const payload = JSON.parse(Buffer.from(p, 'base64url').toString())
console.log(payload.sub, payload.exp)
```

上面代码中，只演示「payload 可读」。缺少签名校验的代码不能当鉴权。

## 七、常见误区

（1）**把 Base64 当成加密**  
编码 ≠ 加密。

（2）**存在 localStorage 就以为万事大吉**  
XSS 可偷 token。存储位置要和威胁模型一起选。

（3）**算法写 `none` 或乱信任 header.alg**  
等于摘掉火漆印。

（4）**token 过长塞进一堆权限快照**  
难轮换、难更新，也更容易泄露面变大。

（5）**401 与 403 分不清**  
token 无效/过期偏 401；token 有效但无权限偏 403。

## 八、小结

JWT 三段里：Header 说明怎么验，Payload 装声明，Signature 防篡改。

它擅长传递可验证的身份与声明；不擅长当加密容器，也不自动提供完善的会话注销。把三段职责分清，后面的安全讨论才有共同语言。

（完）
