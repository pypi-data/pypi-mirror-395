# B2Bhint MCP Server

[English](./README_EN.md) | 简体中文 | [繁體中文](./README_ZH-TW.md)

用于访问 B2Bhint API 的 MCP 服务器。

## 🚀 使用 EMCP 平台快速体验

**[EMCP](https://sit-emcp.kaleido.guru)** 是一个强大的 MCP 服务器管理平台，让您无需手动配置即可快速使用各种 MCP 服务器！

### 快速开始：

1. 🌐 访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)**
2. 📝 注册并登录账号
3. 🎯 进入 **MCP 广场**，浏览所有可用的 MCP 服务器
4. 🔍 搜索或找到本服务器（`bach-b2bhint`）
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

这是一个 MCP 服务器，用于访问 B2Bhint API。

- **PyPI 包名**: `bach-b2bhint`
- **版本**: 1.0.0
- **传输协议**: stdio


## 安装

### 从 PyPI 安装:

```bash
pip install bach-b2bhint
```

### 从源码安装:

```bash
pip install -e .
```

## 运行

### 方式 1: 使用 uvx（推荐，无需安装）

```bash
# 运行（uvx 会自动安装并运行）
uvx --from bach-b2bhint bach_b2bhint

# 或指定版本
uvx --from bach-b2bhint@latest bach_b2bhint
```

### 方式 2: 直接运行（开发模式）

```bash
python server.py
```

### 方式 3: 安装后作为命令运行

```bash
# 安装
pip install bach-b2bhint

# 运行（命令名使用下划线）
bach_b2bhint
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
    "bach-b2bhint": {
      "command": "uvx",
      "args": ["--from", "bach-b2bhint", "bach_b2bhint"],
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
    "bach-b2bhint": {
      "command": "uvx",
      "args": ["--from", "bach-b2bhint", "bach_b2bhint"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```


## 可用工具

此服务器提供以下工具:


### `search_person_by_name`

Search for a person by parameters will return a list of persons that match your query

**端点**: `GET /api/v1/rapidapi/person/search`


**参数**:

- `q` (string) *必需*: Example value: Elon Musk

- `countryCode` (string): Example value: us



---


### `get_company_full_data`

The Get company details endpoint will return all full company data, including company contacts, financial reports and other data

**端点**: `GET /api/v1/rapidapi/company/full`


**参数**:

- `internationalNumber` (string) *必需*: Example value: 0458.780.306

- `countryCode` (string) *必需*: Example value: be



---


### `search_company_by_name`

Search for a company by parameters will return a list of companies that match your query

**端点**: `GET /api/v1/rapidapi/company/search`


**参数**:

- `q` (string) *必需*: Company name or number or other identifiers

- `countryCode` (string): ISO2 country code



---


### `get_company_basic_data`

The Get company details endpoint will return all basic company data on B2BHint.

**端点**: `GET /api/v1/rapidapi/company/basic`


**参数**:

- `internationalNumber` (string) *必需*: Example value: 0458.780.306

- `countryCode` (string) *必需*: Example value: be



---


### `search_company_by_email`

Search for a company by email will return a list of companies that match the selected email

**端点**: `GET /api/v1/rapidapi/company/search-by-email`


**参数**:

- `email` (string) *必需*: Example value: rsing@tesla.com



---



## 技术栈

- **传输协议**: stdio
- **HTTP 客户端**: httpx


## 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件。

## 开发

此服务器由 [API-to-MCP](https://github.com/BACH-AI-Tools/api-to-mcp) 工具生成。

版本: 1.0.0
