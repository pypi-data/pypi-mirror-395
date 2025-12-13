# Whatsapp Profile Pic MCP Server

[English](./README_EN.md) | 简体中文 | [繁體中文](./README_ZH-TW.md)

用于访问 Whatsapp Profile Pic API 的 MCP 服务器。

## 🚀 使用 EMCP 平台快速体验

**[EMCP](https://sit-emcp.kaleido.guru)** 是一个强大的 MCP 服务器管理平台，让您无需手动配置即可快速使用各种 MCP 服务器！

### 快速开始：

1. 🌐 访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)**
2. 📝 注册并登录账号
3. 🎯 进入 **MCP 广场**，浏览所有可用的 MCP 服务器
4. 🔍 搜索或找到本服务器（`bach-whatsapp_profile_pic`）
5. 🎉 点击 **"安装 MCP"** 按钮
6. ✅ 完成！即可在您的应用中使用

### EMCP 平台优势：

- ✨ **零配置**：无需手动编辑配置文件
- 🎨 **可视化管理**：图形界面轻松管理所有 MCP 服务器
- 🔐 **安全可靠**：统一管理 API 密钥和认证信息
- 🚀 **一键安装**：MCP 广场提供丰富的服务器选择
- 📊 **使用统计**：实时查看服务调用情况

立即访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)** 开始您的 MCP 之旅！


---

## 简介

这是一个 MCP 服务器，用于访问 Whatsapp Profile Pic API。

- **PyPI 包名**: `bach-whatsapp_profile_pic`
- **版本**: 1.0.0
- **传输协议**: stdio


## 安装

### 从 PyPI 安装:

```bash
pip install bach-whatsapp_profile_pic
```

### 从源码安装:

```bash
pip install -e .
```

## 运行

### 方式 1: 使用 uvx（推荐，无需安装）

```bash
# 运行（uvx 会自动安装并运行）
uvx --from bach-whatsapp_profile_pic bach_whatsapp_profile_pic

# 或指定版本
uvx --from bach-whatsapp_profile_pic@latest bach_whatsapp_profile_pic
```

### 方式 2: 直接运行（开发模式）

```bash
python server.py
```

### 方式 3: 安装后作为命令运行

```bash
# 安装
pip install bach-whatsapp_profile_pic

# 运行（命令名使用下划线）
bach_whatsapp_profile_pic
```

## 配置

### API 认证

此 API 需要认证。请设置环境变量:

```bash
export API_KEY="your_api_key_here"
```

### 环境变量

| 变量名 | 说明 | 必需 |
|--------|------|------|
| `API_KEY` | API 密钥 | 是 |
| `PORT` | 不适用 | 否 |
| `HOST` | 不适用 | 否 |



### 在 Cursor 中使用

编辑 Cursor MCP 配置文件 `~/.cursor/mcp.json`:


```json
{
  "mcpServers": {
    "bach-whatsapp_profile_pic": {
      "command": "uvx",
      "args": ["--from", "bach-whatsapp_profile_pic", "bach_whatsapp_profile_pic"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### 在 Claude Desktop 中使用

编辑 Claude Desktop 配置文件 `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "bach-whatsapp_profile_pic": {
      "command": "uvx",
      "args": ["--from", "bach-whatsapp_profile_pic", "bach_whatsapp_profile_pic"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```


## 可用工具

此服务器提供以下工具:


### `is_a_business`

Requests to this endpoint will return `true` if the number is a Whatsapp for Business account, or `false` if it is not.

**端点**: `GET /isbiz`


**参数**:

- `phone` (number) *必需*: The WhatsApp number must be written as: countrycode and number; do NOT include any non-number character, spaces, or anything which is not a number. Otherwise, the request will not be processed. Examples of correct numbers are: 34123456789 (for Spain) 491234567890 (for Germany) TIPS: Do NOT include '+' before your countrycode. Do NOT include a '-', or any other character or space (anything which is not a number) as part of your phone number. If you do not know which is your country code, check th



---


### `verified_name`

Fetch the verified name of the whatsapp business number. Non whatsapp business numbers will not have a verified name.

**端点**: `GET /bizname`


**参数**:

- `phone` (number) *必需*: Example value: 13022612667



---


### `about`

Gather user's own about description.

**端点**: `GET /about`


**参数**:

- `phone` (number) *必需*: The WhatsApp number must be written as: countrycode and number; do NOT include any non-number character, spaces, or anything which is not a number. Otherwise, the request will not be processed. Examples of correct numbers are: 34123456789 (for Spain) 491234567890 (for Germany) TIPS: Do NOT include '+' before your countrycode. Do NOT include a '-', or any other character or space (anything which is not a number) as part of your phone number. If you do not know which is your country code, check th



---


### `business_info`

Fetchs: `description`, `website`, `email`, `business hours`, `address` and `category`; if the number is a whatsapp for business account.

**端点**: `GET /bizinfo`


**参数**:

- `phone` (number) *必需*: The WhatsApp number must be written as: countrycode and number; do NOT include any non-number character, spaces, or anything which is not a number. Otherwise, the request will not be processed. Examples of correct numbers are: 34123456789 (for Spain) 491234567890 (for Germany) TIPS: Do NOT include '+' before your countrycode. Do NOT include a '-', or any other character or space (anything which is not a number) as part of your phone number. If you do not know which is your country code, check th



---


### `whatsapp_number_checker`

Enter the number you want to validate if it exists on the whatsapp network.

**端点**: `GET /wchk`


**参数**:

- `phone` (number) *必需*: The WhatsApp number must be written as: countrycode and number; do NOT include any non-number character, spaces, or anything which is not a number. Otherwise, the request will not be processed. Examples of correct numbers are: 34123456789 (for Spain) 491234567890 (for Germany) TIPS: Do NOT include '+' before your countrycode. Do NOT include a '-', or any other character or space (anything which is not a number) as part of your phone number. If you do not know which is your country code, check th



---


### `double_check`

This endpoint will return if the number is registered on whatsapp; if yes, it tells if the profile picture is public, and if it is, the response will include the public url of the picture.

**端点**: `GET /wspic/dck`


**参数**:

- `phone` (number) *必需*: The WhatsApp number must be written as: countrycode and number; do NOT include any non-number character, spaces, or anything which is not a number. Otherwise, the request will not be processed. Examples of correct numbers are: 34123456789 (for Spain) 491234567890 (for Germany) TIPS: Do NOT include '+' before your countrycode. Do NOT include a '-', or any other character or space (anything which is not a number) as part of your phone number. If you do not know which is your country code, check th



---


### `picture_uri`

Returns a whatsapp number profile picture as url encoded data uri

**端点**: `GET /wspic/uri`


**参数**:

- `phone` (number) *必需*: The WhatsApp number must be written as: countrycode and number; do NOT include any non-number character, spaces, or anything which is not a number. Otherwise, the request will not be processed. Examples of correct numbers are: 34123456789 (for Spain) 491234567890 (for Germany) TIPS: Do NOT include '+' before your countrycode. Do NOT include a '-', or any other character or space (anything which is not a number) as part of your phone number. If you do not know which is your country code, check th



---


### `picture_base64`

Fetch the base64 encoded file of a whatsapp number profile picture.

**端点**: `GET /wspic/b64`


**参数**:

- `phone` (number) *必需*: The WhatsApp number must be written as: countrycode and number; do NOT include any non-number character, spaces, or anything which is not a number. Otherwise, the request will not be processed. Examples of correct numbers are: 34123456789 (for Spain) 491234567890 (for Germany) TIPS: Do NOT include '+' before your countrycode. Do NOT include a '-', or any other character or space (anything which is not a number) as part of your phone number. If you do not know which is your country code, check th



---


### `picture_jpg`

Get the whatsapp's number profile picture as a jpg file.

**端点**: `GET /wspic/png`


**参数**:

- `phone` (number) *必需*: The WhatsApp number must be written as: countrycode and number; do NOT include any non-number character, spaces, or anything which is not a number. Otherwise, the request will not be processed. Examples of correct numbers are: 34123456789 (for Spain) 491234567890 (for Germany) TIPS: Do NOT include '+' before your countrycode. Do NOT include a '-', or any other character or space (anything which is not a number) as part of your phone number. If you do not know which is your country code, check th



---


### `picture_url`

Fetchs the url of a whatsapp number profile picture.

**端点**: `GET /wspic/url`


**参数**:

- `phone` (number) *必需*: The WhatsApp number must be written as: countrycode and number; do NOT include any non-number character, spaces, or anything which is not a number. Otherwise, the request will not be processed. Examples of correct numbers are: 34123456789 (for Spain) 491234567890 (for Germany) TIPS: Do NOT include '+' before your countrycode. Do NOT include a '-', or any other character or space (anything which is not a number) as part of your phone number. If you do not know which is your country code, check th



---



## 技术栈

- **传输协议**: stdio
- **HTTP 客户端**: httpx


## 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件。

## 开发

此服务器由 [API-to-MCP](https://github.com/BACH-AI-Tools/api-to-mcp) 工具生成。

版本: 1.0.0
