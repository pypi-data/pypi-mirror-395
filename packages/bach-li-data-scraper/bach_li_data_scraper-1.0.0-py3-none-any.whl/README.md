# Li Data Scraper MCP Server

[English](./README_EN.md) | 简体中文 | [繁體中文](./README_ZH-TW.md)

用于访问 Li Data Scraper API 的 MCP 服务器。

## 🚀 使用 EMCP 平台快速体验

**[EMCP](https://sit-emcp.kaleido.guru)** 是一个强大的 MCP 服务器管理平台，让您无需手动配置即可快速使用各种 MCP 服务器！

### 快速开始：

1. 🌐 访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)**
2. 📝 注册并登录账号
3. 🎯 进入 **MCP 广场**，浏览所有可用的 MCP 服务器
4. 🔍 搜索或找到本服务器（`bach-li_data_scraper`）
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

这是一个 MCP 服务器，用于访问 Li Data Scraper API。

- **PyPI 包名**: `bach-li_data_scraper`
- **版本**: 1.0.0
- **传输协议**: stdio


## 安装

### 从 PyPI 安装:

```bash
pip install bach-li_data_scraper
```

### 从源码安装:

```bash
pip install -e .
```

## 运行

### 方式 1: 使用 uvx（推荐，无需安装）

```bash
# 运行（uvx 会自动安装并运行）
uvx --from bach-li_data_scraper bach_li_data_scraper

# 或指定版本
uvx --from bach-li_data_scraper@latest bach_li_data_scraper
```

### 方式 2: 直接运行（开发模式）

```bash
python server.py
```

### 方式 3: 安装后作为命令运行

```bash
# 安装
pip install bach-li_data_scraper

# 运行（命令名使用下划线）
bach_li_data_scraper
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
    "bach-li_data_scraper": {
      "command": "uvx",
      "args": ["--from", "bach-li_data_scraper", "bach_li_data_scraper"],
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
    "bach-li_data_scraper": {
      "command": "uvx",
      "args": ["--from", "bach-li_data_scraper", "bach_li_data_scraper"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```


## 可用工具

此服务器提供以下工具:


### `get_public_profile_data_by_url`

Enrich public profile data

**端点**: `GET /get-profile-data-by-url`



---


### `get_company_details`

The endpoint returns enrich company details

**端点**: `GET /get-company-details`



---


### `get_company_by_domain`

Enrich company data by domain. **1 credit per successful request.**

**端点**: `GET /get-company-by-domain`



---


### `search_people`

You may see less than 10 results per page. This is because not all profiles as public, sometimes hiding profiles. The endpoint automatically filters these profiles from the result

**端点**: `GET /search-people`



---


### `about_the_profile`

Get profile verification details, profile’s joined, contact information updated, and profile photo updated date

**端点**: `GET /about-this-profile`



---


### `get_profile_data_and_connection_u0026_follower_count`

Get Profile Data and Connection \u0026 Follower Count

**端点**: `GET /data-connection-count`



---


### `get_post_comment_reaction`

Get post comment Reaction

**端点**: `POST /posts/comments/reactions`



---


### `search_post_by_keyword`

Search Post by Keyword

**端点**: `POST /search-posts`



---


### `get_post_reactions`

Get profiles that reacted to the post

**端点**: `POST /get-post-reactions`



---


### `get_profile_post_and_comments`

Get profile post and comments of the post

**端点**: `GET /get-profile-post-and-comments`



---


### `get_profiles_comments`

Get last 50 comments of a profile. 1 credit per call

**端点**: `GET /get-profile-comments`



---


### `get_company_jobs`

Get company jobs

**端点**: `POST /company-jobs`



---


### `ping`

Ping

**端点**: `GET /health`



---


### `get_profile_recent_activity_time`

Get the time of the profile's last activity

**端点**: `GET /get-profile-recent-activity-time`



---


### `get_profile_reactions`

Find out what posts a profile reacted to

**端点**: `GET /get-profile-likes`



---


### `get_profile_post_comment`

Get 50 comments of a profile post  (activity)

**端点**: `GET /get-profile-posts-comments`



---


### `get_profiles_posts`

Get last 50 posts of a profile. 1 credit per call

**端点**: `GET /get-profile-posts`



---


### `search_post_by_hashtag`

Search Post by Hashtag

**端点**: `POST /search-posts-by-hashtag`



---


### `get_company_post_comments`

Get comments of a company post

**端点**: `GET /get-company-post-comments`



---


### `get_companys_post`

Get last 50 posts of a company. 1 credit per call

**端点**: `GET /get-company-posts`



---



## 技术栈

- **传输协议**: stdio
- **HTTP 客户端**: httpx


## 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件。

## 开发

此服务器由 [API-to-MCP](https://github.com/BACH-AI-Tools/api-to-mcp) 工具生成。

版本: 1.0.0
