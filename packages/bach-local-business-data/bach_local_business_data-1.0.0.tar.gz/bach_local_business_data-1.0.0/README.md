# Local Business Data MCP Server

[English](./README_EN.md) | 简体中文 | [繁體中文](./README_ZH-TW.md)

用于访问 Local Business Data API 的 MCP 服务器。

## 🚀 使用 EMCP 平台快速体验

**[EMCP](https://sit-emcp.kaleido.guru)** 是一个强大的 MCP 服务器管理平台，让您无需手动配置即可快速使用各种 MCP 服务器！

### 快速开始：

1. 🌐 访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)**
2. 📝 注册并登录账号
3. 🎯 进入 **MCP 广场**，浏览所有可用的 MCP 服务器
4. 🔍 搜索或找到本服务器（`bach-local_business_data`）
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

这是一个 MCP 服务器，用于访问 Local Business Data API。

- **PyPI 包名**: `bach-local_business_data`
- **版本**: 1.0.0
- **传输协议**: stdio


## 安装

### 从 PyPI 安装:

```bash
pip install bach-local_business_data
```

### 从源码安装:

```bash
pip install -e .
```

## 运行

### 方式 1: 使用 uvx（推荐，无需安装）

```bash
# 运行（uvx 会自动安装并运行）
uvx --from bach-local_business_data bach_local_business_data

# 或指定版本
uvx --from bach-local_business_data@latest bach_local_business_data
```

### 方式 2: 直接运行（开发模式）

```bash
python server.py
```

### 方式 3: 安装后作为命令运行

```bash
# 安装
pip install bach-local_business_data

# 运行（命令名使用下划线）
bach_local_business_data
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
    "bach-local_business_data": {
      "command": "uvx",
      "args": ["--from", "bach-local_business_data", "bach_local_business_data"],
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
    "bach-local_business_data": {
      "command": "uvx",
      "args": ["--from", "bach-local_business_data", "bach_local_business_data"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```


## 可用工具

此服务器提供以下工具:


### `business_review_details`

Get the details of a specific review by Google Id / Business Id or Google Place Id and Review Author Id.

**端点**: `GET /review-details`


**参数**:

- `business_id` (string) *必需*: The Business Id of the business for which the review belongs. Accepts google_id / business_id or place_id. Examples: 0x880fd393d427a591:0x8cba02d713a995ed ChIJkaUn1JPTD4gR7ZWpE9cCuow

- `review_author_id` (string) *必需*: Review author id (i.e review author_id field). In addition, batching of up to 20 Review Author Ids is supported in a single request using a comma separated list (e.g. review_author_id=id1,id2).

- `region` (string): Query Google Maps from a particular region or country. For a list of supported region/country codes see https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes (Alpha-2 code). Default: us

- `language` (string): Set the language of the results. For a list of supported language codes see https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes . Default: en



---


### `search_in_area`

Search businesses in a specific geographic area defined by a center coordinate point and zoom level. To see it in action, make a query on Google Maps, wait for the results to show, move the map or change the zoom and click \

**端点**: `GET /search-in-area`


**参数**:

- `query` (string) *必需*: Search query / keyword

- `lat` (number) *必需*: Latitude of the center coordinate point of the area to search in.

- `lng` (number) *必需*: Longitude of the center coordinate point of the area to search in.

- `zoom` (string) *必需*: Zoom level on which to make the search (the search area / viewport is determined by lat, lng and zoom on a 1000x1000 screen).

- `limit` (number): Maximum number of businesses to return. Default: 20 Allowed values: 1-500

- `language` (string): Set the language of the results. For a list of supported language codes see https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes . Default: en

- `region` (string): Query Google Maps from a particular region or country. For a list of supported region/country codes see https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes (Alpha-2 code). Default: us

- `subtypes` (string): Find businesses with specific subtypes, specified as a comma separated list of types (business categories). For the complete list of types, see https://daltonluka.com/blog/google-my-business-categories. Examples: Plumber,Carpenter,Electrician Night club,Dance club,Bar,Pub

- `extract_emails_and_contacts` (string): Example value: 

- `fields` (string): A comma separated list of business fields to include in the response (field projection). By default all fields are returned. Example: business_id,type,phone_number,full_address

- `X-User-Agent` (string): Device type for the search. Default desktop.



---


### `autocomplete`

Returns place/address, business and query predictions for text-based geographic queries.

**端点**: `GET /autocomplete`


**参数**:

- `query` (string) *必需*: Search query

- `region` (string): Return results biased to a particular region. For a list of supported region/country codes see https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes (Alpha-2 code). Default: us

- `language` (string): Set the language of the results. For a list of supported language codes see https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 . Default: en

- `coordinates` (string): Geographic coordinates of the location from which the query is applied - recommended to use so that results are biased towards this location. Defaults to some central location in the region (see the region parameter).



---


### `business_photo_details`

Get extra details about a business photo - caption, owner name and avatar, and more information. Supports batching of up to 20 Photo Ids.

**端点**: `GET /photo-details`


**参数**:

- `business_id` (string) *必需*: The Business Id of the business for which the photo belongs. Accepts google_id / business_id or place_id. Examples: 0x880fd393d427a591:0x8cba02d713a995ed ChIJkaUn1JPTD4gR7ZWpE9cCuow

- `photo_id` (string) *必需*: Photo Id of the photo to fetch. In addition, batching of up to 20 Photo Ids is supported in a single request using a comma separated list (e.g. photo_id=id1,id2).



---


### `business_posts`

Get all / paginate Business Owner Posts (\

**端点**: `GET /business-posts`


**参数**:

- `business_id` (string) *必需*: Unique Business Id. Accepts google_id / business_id or place_id. Examples: 0x880fd393d427a591:0x8cba02d713a995ed ChIJkaUn1JPTD4gR7ZWpE9cCuow

- `cursor` (string): Specify the cursor obtained from the previous request to get the next of result page (use for pagination).

- `region` (string): Query Google Maps from a particular region or country. For a list of supported region/country codes see https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes (Alpha-2 code). Default: us

- `language` (string): Set the language of the results. For a list of supported language codes see https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes . Default: en



---


### `reverse_geocoding`

Get the details of a place or address in a specific geographic location by latitude and longitude (reverse geocoding). This endpoint implements the \

**端点**: `GET /reverse-geocoding`


**参数**:

- `lat` (number) *必需*: Example value: 40.6958453

- `lng` (number) *必需*: Example value: -73.9799119

- `region` (string): Query Google Maps from a particular region or country. For a list of supported region/country codes see https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes (Alpha-2 code). Default: us

- `language` (string): Set the language of the results. For a list of supported language codes see https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes . Default: en

- `fields` (string): A comma separated list of business fields to include in the response (field projection). By default all fields are returned. Example: business_id,type,phone_number,full_address



---


### `search_nearby`

Search businesses near by specific geographic coordinates. To see it in action, right click on a specific point in the map on Google Maps and select \

**端点**: `GET /search-nearby`


**参数**:

- `query` (string) *必需*: Search query / keyword Examples: Bars and pubs Plumbers

- `lat` (number) *必需*: Latitude of the geographic coordinates to search near by.

- `lng` (number) *必需*: Longitude of the geographic coordinates to search near by.

- `limit` (number): Maximum number of businesses to return. Default: 20 Allowed values: 1-500

- `language` (string): Set the language of the results. For a list of supported language codes see https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes . Default: en

- `region` (string): Query Google Maps from a particular region or country. For a list of supported region/country codes see https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes (Alpha-2 code). Default: us

- `subtypes` (string): Find businesses with specific subtypes, specified as a comma separated list of types (business categories). For the complete list of types, see https://daltonluka.com/blog/google-my-business-categories. Examples: Plumber,Carpenter,Electrician Night club,Dance club,Bar,Pub

- `extract_emails_and_contacts` (string): Example value: 

- `fields` (string): A comma separated list of business fields to include in the response (field projection). By default all fields are returned. Example: business_id,type,phone_number,full_address

- `X-User-Agent` (string): Device type for the search. Default desktop.



---


### `business_photos`

Get business photos by Business Id.

**端点**: `GET /business-photos`


**参数**:

- `business_id` (string) *必需*: Unique Business Id. Accepts google_id / business_id or place_id. Examples: 0x880fd393d427a591:0x8cba02d713a995ed ChIJkaUn1JPTD4gR7ZWpE9cCuow

- `limit` (number): Maximum number of business photos to return. Default: 20 Allowed values: 1-100

- `cursor` (string): Specify the cursor obtained from the previous request to get the next of result page (use for pagination).

- `is_video` (string): Example value: 

- `region` (string): Query Google Maps from a particular region or country. For a list of supported region/country codes see https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes (Alpha-2 code). Default: us

- `fields` (string): A comma separated list of review fields to include in the response (field projection). By default all fields are returned. Example: type,photo_url



---


### `search`

Search local businesses on Google Maps with an option to pull emails and social profile links from their website (see the `extract_emails_and_contacts` parameter below).

**端点**: `GET /search`


**参数**:

- `query` (string) *必需*: Search query / keyword Examples: Plumbers near New-York, USA Bars in 94102, USA

- `limit` (number): Maximum number of businesses to return. Default: 20 Allowed values: 1-500

- `lat` (number): Latitude of the coordinates point from which the query is applied - recommended to use so that results are biased towards this location. Defaults to some central location in the region (see the region parameter).

- `lng` (number): Longitude of the coordinates point from which the query is applied - recommended to use so that results are biased towards this location. Defaults to some central location in the region (see the region parameter).

- `zoom` (string): Zoom level on which to make the search (the viewport is determined by lat, lng and zoom). Default: 13

- `language` (string): Set the language of the results. For a list of supported language codes see https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes . Default: en

- `region` (string): Query Google Maps from a particular region or country. For a list of supported region/country codes see https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes (Alpha-2 code). Default: us

- `subtypes` (string): Find businesses with specific subtypes, specified as a comma separated list of types (business categories). For the complete list of types, see https://daltonluka.com/blog/google-my-business-categories. Examples: Plumber,Carpenter,Electrician Night club,Dance club,Bar,Pub

- `verified` (string): Example value: 

- `business_status` (string): Find businesses with specific status, specified as a comma separated list of the following values: OPEN, CLOSED_TEMPORARILY, CLOSED. Examples: OPEN CLOSED_TEMPORARILY,CLOSED

- `fields` (string): A comma separated list of business fields to include in the response (field projection). By default all fields are returned. Example: business_id,type,phone_number,full_address

- `extract_emails_and_contacts` (string): Example value: 

- `X-User-Agent` (string): Device type for the search. Default desktop.



---


### `bulk_search`

Search local businesses on Google Maps. Batching of up to 20 queries is supported in a single request.

**端点**: `POST /search`


**参数**:

- `X-User-Agent` (string): Device type for the search. Default desktop.



---


### `business_details`

Get full business details including emails and social contacts. Supports batching of up to 20 Business Ids.

**端点**: `GET /business-details`


**参数**:

- `business_id` (string) *必需*: Unique Business Id. Accepts google_id / business_id or place_id. Examples: 0x880fd393d427a591:0x8cba02d713a995ed ChIJkaUn1JPTD4gR7ZWpE9cCuow In addition, batching of up to 20 Business Ids is supported in a single request using a comma separated list (e.g. business_id=id1,id2).

- `extract_emails_and_contacts` (string): Example value: 

- `extract_share_link` (string): Example value: 

- `fields` (string): A comma separated list of business fields to include in the response (field projection). By default all fields are returned. Example: business_id,type,phone_number,full_address

- `region` (string): Query Google Maps from a particular region or country. For a list of supported region/country codes see https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes (Alpha-2 code). Default: us

- `language` (string): Set the language of the results. For a list of supported language codes see https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes . Default: en

- `coordinates` (string): Geographic coordinates of the location from which the query is applied - recommended to use so that results are biased towards this location. Defaults to some central location in the region (see the region parameter).



---


### `business_reviews_v2`

Get business reviews by Business Id with pagination support.

**端点**: `GET /business-reviews-v2`


**参数**:

- `business_id` (string) *必需*: Unique Business Id. Accepts google_id / business_id or place_id. Examples: 0x880fd393d427a591:0x8cba02d713a995ed ChIJkaUn1JPTD4gR7ZWpE9cCuow

- `limit` (number): Maximum number of business reviews to return. Default: 20 Allowed values: 1-1000

- `cursor` (string): The cursor value from the previous response to get the next set of results (scrolling / pagination).

- `translate_reviews` (string): Example value: 

- `query` (string): Return reviews matching a text query.

- `sort_by` (string): How to sort the reviews in the results. Default: most_relevant Allowed values: most_relevant, newest, highest_ranking, lowest_ranking

- `fields` (string): A comma separated list of review fields to include in the response (field projection). By default all fields are returned. Example: review_id,review_text,rating

- `region` (string): Query Google Maps from a particular region or country. For a list of supported region/country codes see https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes (Alpha-2 code). Default: us

- `language` (string): Set the language of the results. For a list of supported language codes see https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes . Default: en



---


### `business_reviews`

Get business reviews by Business Id with pagination support.

**端点**: `GET /business-reviews`


**参数**:

- `business_id` (string) *必需*: Unique Business Id. Accepts google_id / business_id or place_id. Examples: 0x880fd393d427a591:0x8cba02d713a995ed ChIJkaUn1JPTD4gR7ZWpE9cCuow

- `limit` (number): Maximum number of business reviews to return. Default: 20 Allowed values: 1-1000

- `offset` (number): Number of business reviews to skip (for pagination/scrolling). Default: 0

- `translate_reviews` (string): Example value: 

- `query` (string): Return reviews matching a text query.

- `sort_by` (string): How to sort the reviews in the results. Default: most_relevant Allowed values: most_relevant, newest, highest_ranking, lowest_ranking

- `fields` (string): A comma separated list of review fields to include in the response (field projection). By default all fields are returned. Example: review_id,review_text,rating

- `region` (string): Query Google Maps from a particular region or country. For a list of supported region/country codes see https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes (Alpha-2 code). Default: us

- `language` (string): Set the language of the results. For a list of supported language codes see https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes . Default: en



---



## 技术栈

- **传输协议**: stdio
- **HTTP 客户端**: httpx


## 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件。

## 开发

此服务器由 [API-to-MCP](https://github.com/BACH-AI-Tools/api-to-mcp) 工具生成。

版本: 1.0.0
