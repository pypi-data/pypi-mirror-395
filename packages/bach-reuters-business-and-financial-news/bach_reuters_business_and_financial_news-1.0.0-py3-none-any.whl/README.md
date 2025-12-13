# Reuters Business And Financial News MCP Server

[English](./README_EN.md) | 简体中文 | [繁體中文](./README_ZH-TW.md)

用于访问 Reuters Business And Financial News API 的 MCP 服务器。

## 🚀 使用 EMCP 平台快速体验

**[EMCP](https://sit-emcp.kaleido.guru)** 是一个强大的 MCP 服务器管理平台，让您无需手动配置即可快速使用各种 MCP 服务器！

### 快速开始：

1. 🌐 访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)**
2. 📝 注册并登录账号
3. 🎯 进入 **MCP 广场**，浏览所有可用的 MCP 服务器
4. 🔍 搜索或找到本服务器（`bach-reuters_business_and_financial_news`）
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

这是一个 MCP 服务器，用于访问 Reuters Business And Financial News API。

- **PyPI 包名**: `bach-reuters_business_and_financial_news`
- **版本**: 1.0.0
- **传输协议**: stdio


## 安装

### 从 PyPI 安装:

```bash
pip install bach-reuters_business_and_financial_news
```

### 从源码安装:

```bash
pip install -e .
```

## 运行

### 方式 1: 使用 uvx（推荐，无需安装）

```bash
# 运行（uvx 会自动安装并运行）
uvx --from bach-reuters_business_and_financial_news bach_reuters_business_and_financial_news

# 或指定版本
uvx --from bach-reuters_business_and_financial_news@latest bach_reuters_business_and_financial_news
```

### 方式 2: 直接运行（开发模式）

```bash
python server.py
```

### 方式 3: 安装后作为命令运行

```bash
# 安装
pip install bach-reuters_business_and_financial_news

# 运行（命令名使用下划线）
bach_reuters_business_and_financial_news
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
    "bach-reuters_business_and_financial_news": {
      "command": "uvx",
      "args": ["--from", "bach-reuters_business_and_financial_news", "bach_reuters_business_and_financial_news"],
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
    "bach-reuters_business_and_financial_news": {
      "command": "uvx",
      "args": ["--from", "bach-reuters_business_and_financial_news", "bach_reuters_business_and_financial_news"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```


## 可用工具

此服务器提供以下工具:


### `get_all_keywords`

Get all Keywords

**端点**: `GET /keywords/get-all-keywords/{page}`


**参数**:

- `page` (string) *必需*: 20 results per page / starting with page 0



---


### `get_all_n2_tags`

Get all N2 Tags

**端点**: `GET /n2/get-all-n2`



---


### `get_articles_by_date_and_author_id`

Get Articles by date and Author ID

**端点**: `GET /get-articles-by-date-authorId/{date}/{authorId}/{page}/{limit}`


**参数**:

- `date` (string) *必需*: Example value: 2024-01-01

- `authorId` (string) *必需*: Example value: 1510

- `page` (string) *必需*: Example value: 0

- `limit` (string) *必需*: Example value: 20



---


### `get_all_subcategories`

Get all SubCategories

**端点**: `GET /all-category-subcategory`



---


### `get_all_authors`

Get all Authors

**端点**: `GET /authors/get-all-authors`



---


### `get_trending_news`

Get articles by trends

**端点**: `GET /articles-by-trends/{date}/{page}/{limit}`


**参数**:

- `date` (string) *必需*: Example value: 2024-01-31

- `page` (string) *必需*: 20 results per page / starting with page 0

- `limit` (string) *必需*: Example value: 20



---


### `get_articles_by_category_id_and_date_range`

Get Articles by categoryId and time period. This Endpoint has a hard limit set to max 20 result per page

**端点**: `GET /get-articles-category-between-dates/{categoryId}/{fromDate}/{toDate}/{page}/{limit}`


**参数**:

- `categoryId` (string) *必需*: Example value: 239

- `fromDate` (string) *必需*: Example value: 2023-11-01

- `toDate` (string) *必需*: Example value: 2023-11-30

- `page` (string) *必需*: Example value: 0

- `limit` (string) *必需*: Example value: 20



---


### `get_articles_by_date_range`

Get Articles by time period. This Endpoint has a hard limit set to max 20 result per page

**端点**: `GET /get-articles-between-dates/{fromDate}/{toDate}/{page}/{limit}`


**参数**:

- `fromDate` (string) *必需*: Example value: 2023-11-01

- `toDate` (string) *必需*: Example value: 2023-11-30

- `page` (string) *必需*: 20 results per page / starting with page 0

- `limit` (string) *必需*: Example value: 20



---


### `get_articles_by_keyword`

Get Articles by Keyword name  Example of internal request: Where keyword_name like 'Microsoft%'

**端点**: `GET /get-articles-by-keyword-name/{keywordName}/{page}/{limit}`


**参数**:

- `keywordName` (string) *必需*: Example value: Microsoft

- `page` (string) *必需*: 20 results per page / starting with page 0

- `limit` (string) *必需*: Example value: 20



---


### `get_articles_by_keyword_u0026_date_range`

Get Articles by Date Range and Keyword name  Example of internal request: Where keyword_name like 'Microsoft%'

**端点**: `GET /get-articles-by-keyword-name-date-range/{fromDate}/{toDate}/{keywordName}/{page}/{limit}`


**参数**:

- `fromDate` (string) *必需*: Example value: 2025-01-01

- `toDate` (string) *必需*: Example value: 2025-01-30

- `keywordName` (string) *必需*: Example value: Microsoft

- `page` (string) *必需*: 20 results per page / starting with page 0

- `limit` (string) *必需*: Example value: 20



---


### `get_markets_rics_by_asset_id_and_category_id`

Get Markets Rics by Asset ID and Category ID

**端点**: `GET /market-rics/list-rics-by-asset-and-category/{marketAssetId}/{marketCategoryId}`


**参数**:

- `marketAssetId` (string) *必需*: Example value: 1

- `marketCategoryId` (string) *必需*: Example value: 1



---


### `get_rics_data_by_assetid_and_categoryid`

Get Rics Data By AssetId and CategoryId

**端点**: `GET /market-data/list-data-by-asset-and-category/{marketAssetId}/{marketCategoryId}`


**参数**:

- `marketAssetId` (string) *必需*: Example value: 1

- `marketCategoryId` (string) *必需*: Example value: 1



---


### `get_all_market_categories`

Get all Market Categories

**端点**: `GET /market-category/list`



---


### `get_categories_by_market_asset_id`

Get Categories by market Asset id

**端点**: `GET /market-category/list-by-market-asset-id/{marketAssetId}`


**参数**:

- `marketAssetId` (string) *必需*: Example value: 1



---


### `get_all_tags`

Get all tags

**端点**: `GET /tags/get-all-tags`



---


### `get_articles_by_date`

Get Articles by  Date This Endpoint has a hard limit set to max 20 result per page

**端点**: `GET /article-date/{date}/{page}/{limit}`


**参数**:

- `date` (string) *必需*: Example value: 2024-01-01

- `page` (string) *必需*: 20 results per page / starting with page 0

- `limit` (string) *必需*: Example value: 20



---


### `get_all_market_assets`

Get all Market Assets

**端点**: `GET /market-assets/list`



---


### `search_keywords`

Search a keyword by name  Example of internal request: Where keyword_name like 'Microsoft%'

**端点**: `GET /keywords/search-keyword-by-name/{keywordName}`


**参数**:

- `keywordName` (string) *必需*: Example value: Microsoft



---


### `get_all_categories`

Get all Categories

**端点**: `GET /all-category`



---


### `get_article_by_category_id_and_date`

Get Article by category id and article date ex :/api/v1/category-id-8/article-date-11-04-2021  category - category id from Category endpoint date-{day-month-year}

**端点**: `GET /category-id/{category}/article-date/{date}/{page}/{limit}`


**参数**:

- `category` (string) *必需*: Example value: 240

- `date` (string) *必需*: Example value: 2024-01-01

- `page` (string) *必需*: Example value: 0

- `limit` (string) *必需*: Example value: 20



---



## 技术栈

- **传输协议**: stdio
- **HTTP 客户端**: httpx


## 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件。

## 开发

此服务器由 [API-to-MCP](https://github.com/BACH-AI-Tools/api-to-mcp) 工具生成。

版本: 1.0.0
