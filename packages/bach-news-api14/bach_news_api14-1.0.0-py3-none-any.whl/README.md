# News Api14 MCP Server

[English](./README_EN.md) | 简体中文 | [繁體中文](./README_ZH-TW.md)

用于访问 News Api14 API 的 MCP 服务器。

## 🚀 使用 EMCP 平台快速体验

**[EMCP](https://sit-emcp.kaleido.guru)** 是一个强大的 MCP 服务器管理平台，让您无需手动配置即可快速使用各种 MCP 服务器！

### 快速开始：

1. 🌐 访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)**
2. 📝 注册并登录账号
3. 🎯 进入 **MCP 广场**，浏览所有可用的 MCP 服务器
4. 🔍 搜索或找到本服务器（`bach-news_api14`）
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

这是一个 MCP 服务器，用于访问 News Api14 API。

- **PyPI 包名**: `bach-news_api14`
- **版本**: 1.0.0
- **传输协议**: stdio


## 安装

### 从 PyPI 安装:

```bash
pip install bach-news_api14
```

### 从源码安装:

```bash
pip install -e .
```

## 运行

### 方式 1: 使用 uvx（推荐，无需安装）

```bash
# 运行（uvx 会自动安装并运行）
uvx --from bach-news_api14 bach_news_api14

# 或指定版本
uvx --from bach-news_api14@latest bach_news_api14
```

### 方式 2: 直接运行（开发模式）

```bash
python server.py
```

### 方式 3: 安装后作为命令运行

```bash
# 安装
pip install bach-news_api14

# 运行（命令名使用下划线）
bach_news_api14
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
    "bach-news_api14": {
      "command": "uvx",
      "args": ["--from", "bach-news_api14", "bach_news_api14"],
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
    "bach-news_api14": {
      "command": "uvx",
      "args": ["--from", "bach-news_api14", "bach_news_api14"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```


## 可用工具

此服务器提供以下工具:


### `search_publishers`

Find a list of publishers with details like descriptions, logos, languages, categories, and links to their social media.

**端点**: `GET /v2/search/publishers`


**参数**:

- `query` (string) *必需*: Just type what you're looking for.

- `country` (string): 2-letter ISO 3166-1 code of the country.

- `language` (string): 2-letter ISO 3166-1 code of the language.

- `category` (string): Possible options: general, business, entertainment, lifestyle, politics, science, sports, technology.

- `sort` (string): Possible options: popularity, relevancy.



---


### `get_article_content`

This API endpoint provides access to the comprehensive metadata and content of a specific article.

**端点**: `GET /v2/article`


**参数**:

- `url` (string) *必需*: The URL of the article.

- `type` (string): The article content output type can be specified as eitherhtml or plaintext. The default output type is plaintext. Note: The content is accessible only to users who have a valid subscription plan.



---


### `search_articles`

Find articles by keywords and allows you to filter by country, language, publisher, and date to get specific result.

**端点**: `GET /v2/search/articles`


**参数**:

- `query` (string) *必需*: Just type what you're looking for, like cats or weather. If you want to exclude term, just add minus (-) in front of any term (nasa -moon).

- `language` (string) *必需*: example: en, fr, de, zh-Hant. Check out the Supported Languages endpoint to see a list of all the languages you can search for.

- `publisher` (string): A domain of the news source. Example: cnn.com

- `from` (string): Accepts human-readable formats like 1d for 1 day, 1m for 1 month, 1y for 1 year, as well as ISO 8601, RFC 2822, and Unix timestamp formats.

- `to` (string): Accepts human-readable formats like 1d for 1 day, 1m for 1 month, 1y for 1 year, as well as ISO 8601, RFC 2822, and Unix timestamp formats.

- `limit` (number): This parameter controls the maximum number of articles returned on a single page.

- `page` (number): This parameter specifies the page number you want to access. For example, page=2 will return the second page of results.



---


### `get_random_article`

This endpoint gives you the ability to find new and engaging content by randomly selecting an article, with the option to filter by country or language.

**端点**: `GET /v2/article/random`


**参数**:

- `language` (string): example: en, fr, de, zh-Hant. Check out the Supported Languages endpoint to see a list of all the languages you can search for.

- `topic` (string): The topic of interest, example: General, Politics, Sports, or a subtopic Soccer. Check out the Supported Topics endpoint to see a list of all the topics you can search for.

- `type` (string): The article content output type can be specified as eitherhtml or plaintext. The default output type is plaintext. Note: The content is accessible only to users who have a valid subscription plan.



---


### `trending_topics`

This endpoint lets you find the most popular news article for a specific country, language, and topic (like sports or entertainment).

**端点**: `GET /v2/trendings`


**参数**:

- `date` (string): Example value: 

- `topic` (string) *必需*: The topic of interest, example: General, Politics, Sports, or a subtopic Soccer. Check out the Supported Topics endpoint to see a list of all the topics you can search for.

- `language` (string) *必需*: example: en, fr, de, zh-Hant. Check out the Supported Languages endpoint to see a list of all the languages you can search for.

- `country` (string): example: us, in, fr, de, id . Check out the Supported Countries endpoint to see a list of all the countries you can search for.

- `limit` (number): This parameter controls the maximum number of articles returned on a single page.

- `page` (number): This parameter specifies the page number you want to access. For example, page=2 will return the second page of results.



---


### `supported_countries`

This endpoint provides a list of supported countries along with their respective languages.

**端点**: `GET /v2/info/countries`



---


### `supported_languages`

This endpoint provides a list of supported languages.

**端点**: `GET /v2/info/languages`



---


### `supported_topics`

This endpoint provides information about the supported topics. Access to the specific topics may be restricted based on your subscription plan.

**端点**: `GET /v2/info/topics`



---



## 技术栈

- **传输协议**: stdio
- **HTTP 客户端**: httpx


## 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件。

## 开发

此服务器由 [API-to-MCP](https://github.com/BACH-AI-Tools/api-to-mcp) 工具生成。

版本: 1.0.0
