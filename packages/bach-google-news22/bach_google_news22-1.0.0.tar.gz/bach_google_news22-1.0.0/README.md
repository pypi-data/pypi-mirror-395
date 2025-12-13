# Google News22 MCP Server

[English](./README_EN.md) | 简体中文 | [繁體中文](./README_ZH-TW.md)

用于访问 Google News22 API 的 MCP 服务器。

## 🚀 使用 EMCP 平台快速体验

**[EMCP](https://sit-emcp.kaleido.guru)** 是一个强大的 MCP 服务器管理平台，让您无需手动配置即可快速使用各种 MCP 服务器！

### 快速开始：

1. 🌐 访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)**
2. 📝 注册并登录账号
3. 🎯 进入 **MCP 广场**，浏览所有可用的 MCP 服务器
4. 🔍 搜索或找到本服务器（`bach-google_news22`）
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

这是一个 MCP 服务器，用于访问 Google News22 API。

- **PyPI 包名**: `bach-google_news22`
- **版本**: 1.0.0
- **传输协议**: stdio


## 安装

### 从 PyPI 安装:

```bash
pip install bach-google_news22
```

### 从源码安装:

```bash
pip install -e .
```

## 运行

### 方式 1: 使用 uvx（推荐，无需安装）

```bash
# 运行（uvx 会自动安装并运行）
uvx --from bach-google_news22 bach_google_news22

# 或指定版本
uvx --from bach-google_news22@latest bach_google_news22
```

### 方式 2: 直接运行（开发模式）

```bash
python server.py
```

### 方式 3: 安装后作为命令运行

```bash
# 安装
pip install bach-google_news22

# 运行（命令名使用下划线）
bach_google_news22
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
    "bach-google_news22": {
      "command": "uvx",
      "args": ["--from", "bach-google_news22", "bach_google_news22"],
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
    "bach-google_news22": {
      "command": "uvx",
      "args": ["--from", "bach-google_news22", "bach_google_news22"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```


## 可用工具

此服务器提供以下工具:


### `search_by_topic_headlines`

This endpoint lets you find the most popular news article for a specific country, language, and topic (like sports or entertainment).

**端点**: `GET /v2/topic-headlines`


**参数**:

- `country` (string) *必需*: 2-letter ISO 3166-1 code of the country.

- `language` (string) *必需*: 2-letter ISO 639-1 code of the article language.

- `topic` (string) *必需*: The topic field specifies the category of interest for the content you are requesting. Access Levels Basic and Pro users can access popular, general topics like: General Entertainment World Business Health Sports Science Technology Ultra and Mega users have access to all available topics, including the more specialized categories: General Autos Beauty Business Cryptocurrency Economy Education Entertainment Finance Gadgets Gaming Health Lifestyle Markets Movies Music Politics Science Soccer Sport

- `date` (string): Example value: 

- `page` (number): Example value: 



---


### `search_by_keyword`

Find articles by keywords and allows you to filter by country, language, source, and date to get specific result.

**端点**: `GET /v2/search`


**参数**:

- `q` (string) *必需*: Keywords: Enter single or multiple keywords to search for articles containing those terms. Example: q=technology will search for articles related to technology. Phrases: Enclose phrases in double quotes to search for the exact phrase. Example: q=\\\"climate change\\\" will search for articles containing the exact phrase \"climate change\". Boolean Operators: Use boolean operators like AND, OR, and NOT to refine your search. Example: q=education AND technology will search for articles that contai

- `country` (string) *必需*: 2-letter ISO 3166-1 code of the country.

- `language` (string) *必需*: 2-letter ISO 639-1 code of the language.

- `source` (string): A domain of the news source. Example: cnn.com

- `from` (string): Example value: 

- `to` (string): Example value: 

- `limit` (number): This parameter controls the maximum number of articles returned on a single page.

- `page` (number): Example value: 



---


### `search_by_geolocation`

This endpoint lets you find the most popular news article in a specific geographical location.

**端点**: `GET /v2/geolocation`


**参数**:

- `country` (string) *必需*: 2-letter ISO 3166-1 code of the country.

- `language` (string) *必需*: 2-letter ISO 639-1 code of the article language.

- `location` (string) *必需*: Specify the geographical location for which you want to retrieve news

- `page` (number): Example value: 



---


### `search_by_top_headlines`

This endpoint lets you find the most popular news article for a specific country, language.

**端点**: `GET /v2/top-headlines`


**参数**:

- `country` (string) *必需*: 2-letter ISO 3166-1 code of the country.

- `language` (string) *必需*: 2-letter ISO 639-1 code of the article language.

- `page` (number): Example value: 



---



## 技术栈

- **传输协议**: stdio
- **HTTP 客户端**: httpx


## 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件。

## 开发

此服务器由 [API-to-MCP](https://github.com/BACH-AI-Tools/api-to-mcp) 工具生成。

版本: 1.0.0
