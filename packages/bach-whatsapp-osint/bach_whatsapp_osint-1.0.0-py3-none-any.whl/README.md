# Whatsapp Osint MCP Server

[English](./README_EN.md) | 简体中文 | [繁體中文](./README_ZH-TW.md)

用于访问 Whatsapp Osint API 的 MCP 服务器。

## 🚀 使用 EMCP 平台快速体验

**[EMCP](https://sit-emcp.kaleido.guru)** 是一个强大的 MCP 服务器管理平台，让您无需手动配置即可快速使用各种 MCP 服务器！

### 快速开始：

1. 🌐 访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)**
2. 📝 注册并登录账号
3. 🎯 进入 **MCP 广场**，浏览所有可用的 MCP 服务器
4. 🔍 搜索或找到本服务器（`bach-whatsapp_osint`）
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

这是一个 MCP 服务器，用于访问 Whatsapp Osint API。

- **PyPI 包名**: `bach-whatsapp_osint`
- **版本**: 1.0.0
- **传输协议**: stdio


## 安装

### 从 PyPI 安装:

```bash
pip install bach-whatsapp_osint
```

### 从源码安装:

```bash
pip install -e .
```

## 运行

### 方式 1: 使用 uvx（推荐，无需安装）

```bash
# 运行（uvx 会自动安装并运行）
uvx --from bach-whatsapp_osint bach_whatsapp_osint

# 或指定版本
uvx --from bach-whatsapp_osint@latest bach_whatsapp_osint
```

### 方式 2: 直接运行（开发模式）

```bash
python server.py
```

### 方式 3: 安装后作为命令运行

```bash
# 安装
pip install bach-whatsapp_osint

# 运行（命令名使用下划线）
bach_whatsapp_osint
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
    "bach-whatsapp_osint": {
      "command": "uvx",
      "args": ["--from", "bach-whatsapp_osint", "bach_whatsapp_osint"],
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
    "bach-whatsapp_osint": {
      "command": "uvx",
      "args": ["--from", "bach-whatsapp_osint", "bach_whatsapp_osint"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```


## 可用工具

此服务器提供以下工具:


### `business_insights`

This endpoint returns business status and verified name for an array of WhatsApp numbers.

**端点**: `POST /bizos`



---


### `status`

Whatsapp user's status info.

**端点**: `GET /about`


**参数**:

- `phone` (number) *必需*: Enter phone number with country code and no special characters.



---


### `devices`

Returns the number of linked devices. Max number of linked devices is 4.

**端点**: `GET /devices`


**参数**:

- `phone` (number) *必需*: Provide the phone number in international format without the + sign (as required by Meta/WhatsApp). Use digits only—no spaces or symbols. Example: 34911222333 (ES), 13022612667 (US), 447911123456 (UK). The result will show how many devices are linked to this WhatsApp account (up to 4).



---


### `privacy_settings`

Fetch user privacy settings

**端点**: `GET /privacy`


**参数**:

- `phone` (number) *必需*: Provide the phone number in international format without the + sign and using digits only—no spaces or symbols. Examples: 34911222333 (ES), 13022612667 (US), 447911123456 (UK). The response returns the account’s current privacy settings. Privacy settings depend on the user configuration.



---


### `base64_encoded_profile`

Fetch the base64 encoded file of a whatsapp number profile picture.

**端点**: `GET /wspic/b64`


**参数**:

- `phone` (number) *必需*: Enter phone number with country code, without special characters.



---


### `fetch_osint_info`

This endpoint adeptly determines whether a given number is registered on WhatsApp. In the affirmative case, it provides insights into the visibility of the profile picture, and if accessible, furnishes the public URL of the image in the response.

**端点**: `GET /wspic/dck`


**参数**:

- `phone` (number) *必需*: The whatsapp number must be written as countrycode and number, no special characters.



---



## 技术栈

- **传输协议**: stdio
- **HTTP 客户端**: httpx


## 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件。

## 开发

此服务器由 [API-to-MCP](https://github.com/BACH-AI-Tools/api-to-mcp) 工具生成。

版本: 1.0.0
