# Whatsapp Number Validators MCP Server

[English](./README_EN.md) | 简体中文 | [繁體中文](./README_ZH-TW.md)

用于访问 Whatsapp Number Validators API 的 MCP 服务器。

## 🚀 使用 EMCP 平台快速体验

**[EMCP](https://sit-emcp.kaleido.guru)** 是一个强大的 MCP 服务器管理平台，让您无需手动配置即可快速使用各种 MCP 服务器！

### 快速开始：

1. 🌐 访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)**
2. 📝 注册并登录账号
3. 🎯 进入 **MCP 广场**，浏览所有可用的 MCP 服务器
4. 🔍 搜索或找到本服务器（`bach-whatsapp_number_validators`）
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

这是一个 MCP 服务器，用于访问 Whatsapp Number Validators API。

- **PyPI 包名**: `bach-whatsapp_number_validators`
- **版本**: 1.0.0
- **传输协议**: stdio


## 安装

### 从 PyPI 安装:

```bash
pip install bach-whatsapp_number_validators
```

### 从源码安装:

```bash
pip install -e .
```

## 运行

### 方式 1: 使用 uvx（推荐，无需安装）

```bash
# 运行（uvx 会自动安装并运行）
uvx --from bach-whatsapp_number_validators bach_whatsapp_number_validators

# 或指定版本
uvx --from bach-whatsapp_number_validators@latest bach_whatsapp_number_validators
```

### 方式 2: 直接运行（开发模式）

```bash
python server.py
```

### 方式 3: 安装后作为命令运行

```bash
# 安装
pip install bach-whatsapp_number_validators

# 运行（命令名使用下划线）
bach_whatsapp_number_validators
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
    "bach-whatsapp_number_validators": {
      "command": "uvx",
      "args": ["--from", "bach-whatsapp_number_validators", "bach_whatsapp_number_validators"],
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
    "bach-whatsapp_number_validators": {
      "command": "uvx",
      "args": ["--from", "bach-whatsapp_number_validators", "bach_whatsapp_number_validators"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```


## 可用工具

此服务器提供以下工具:


### `ping`

Ping Validation Test

**端点**: `GET /ping`



---


### `check_if_number_is_business_via_post_request`

Verify whether a given number is registered on WhatsApp and determine if it belongs to WhatsApp Business. To obtain the status of a particular number, please provide the number along with the corresponding country code.

**端点**: `POST /v1/wa_id/business`



---


### `check_if_number_is_business_via_get_request`

Verify whether a given number is registered on WhatsApp and determine if it belongs to WhatsApp Business. To obtain the status of a particular number, please provide the number along with the corresponding country code.

**端点**: `GET /v1/wa_id/business`


**参数**:

- `number` (string) *必需*: Example value: 919879879876



---


### `bulk_validation`

Verify up to 25 numbers in once call. For each number, verify whether this number is registered on WhatsApp and determine if it belongs to WhatsApp Business. To obtain the status of these numbers, please provide all numbers along with the corresponding country code.

**端点**: `POST /v1/bulk_validate/wa_id`



---


### `validate_single_number_via_post_request`

Verify whether a given number is registered on WhatsApp and determine if it belongs to WhatsApp Business. To obtain the status of a particular number, please provide the number along with the corresponding country code.

**端点**: `POST /v1/validate/wa_id`



---


### `validate_single_number_via_get_request`

Verify whether a given number is registered on WhatsApp and determine if it belongs to WhatsApp Business. To obtain the status of a particular number, please provide the number along with the corresponding country code.

**端点**: `GET /v1/validate/wa_id`


**参数**:

- `number` (string) *必需*: Example value: 919879879876



---


### `phone_number_validation_via_post_request`

You can utilize a phone number validator to verify the validity of a given number. In case the number is invalid, the validator will provide alternative valid phone numbers for different countries associated with the given number.

**端点**: `POST /v1/validate/phone`



---


### `phone_number_validation_via_get_request`

You can utilize a phone number validator to verify the validity of a given number. In case the number is invalid, the validator will provide alternative valid phone numbers for different countries associated with the given number.

**端点**: `GET /v1/validate/phone`


**参数**:

- `number` (string) *必需*: Example value: 919879879876



---



## 技术栈

- **传输协议**: stdio
- **HTTP 客户端**: httpx


## 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件。

## 开发

此服务器由 [API-to-MCP](https://github.com/BACH-AI-Tools/api-to-mcp) 工具生成。

版本: 1.0.0
