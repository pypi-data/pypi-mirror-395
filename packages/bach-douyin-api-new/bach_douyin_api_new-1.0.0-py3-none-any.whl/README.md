# Douyin Api New MCP Server

[English](./README_EN.md) | 简体中文 | [繁體中文](./README_ZH-TW.md)

用于访问 Douyin Api New API 的 MCP 服务器。

## 🚀 使用 EMCP 平台快速体验

**[EMCP](https://sit-emcp.kaleido.guru)** 是一个强大的 MCP 服务器管理平台，让您无需手动配置即可快速使用各种 MCP 服务器！

### 快速开始：

1. 🌐 访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)**
2. 📝 注册并登录账号
3. 🎯 进入 **MCP 广场**，浏览所有可用的 MCP 服务器
4. 🔍 搜索或找到本服务器（`bach-douyin_api_new`）
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

这是一个 MCP 服务器，用于访问 Douyin Api New API。

- **PyPI 包名**: `bach-douyin_api_new`
- **版本**: 1.0.0
- **传输协议**: stdio


## 安装

### 从 PyPI 安装:

```bash
pip install bach-douyin_api_new
```

### 从源码安装:

```bash
pip install -e .
```

## 运行

### 方式 1: 使用 uvx（推荐，无需安装）

```bash
# 运行（uvx 会自动安装并运行）
uvx --from bach-douyin_api_new bach_douyin_api_new

# 或指定版本
uvx --from bach-douyin_api_new@latest bach_douyin_api_new
```

### 方式 2: 直接运行（开发模式）

```bash
python server.py
```

### 方式 3: 安装后作为命令运行

```bash
# 安装
pip install bach-douyin_api_new

# 运行（命令名使用下划线）
bach_douyin_api_new
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
    "bach-douyin_api_new": {
      "command": "uvx",
      "args": ["--from", "bach-douyin_api_new", "bach_douyin_api_new"],
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
    "bach-douyin_api_new": {
      "command": "uvx",
      "args": ["--from", "bach-douyin_api_new", "bach_douyin_api_new"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```


## 可用工具

此服务器提供以下工具:


### `post`

post

**端点**: `POST /v1/social/douyin/app/user/post`



---


### `profile`

profile

**端点**: `POST /v1/social/douyin/app/user/profile`



---


### `info`

info

**端点**: `POST /v1/social/douyin/app/user/info`



---


### `follower`

follower

**端点**: `POST /v1/social/douyin/app/user/follower`



---


### `hotvideolist`

hotvideolist

**端点**: `POST /v1/social/douyin/web/search/hotvideolist`



---


### `susggestwords`

susggestwords

**端点**: `POST /v1/social/douyin/web/search/susggestwords`



---


### `single`

single

**端点**: `POST /v1/social/douyin/web/search/single`



---


### `item`

item

**端点**: `POST /v1/social/douyin/web/search/item`



---


### `sug`

sug

**端点**: `POST /v1/social/douyin/web/search/sug`



---


### `related`

related

**端点**: `POST /v1/social/douyin/web/aweme/related`



---


### `post_1`

post

**端点**: `POST /v1/social/douyin/web/aweme/post`



---


### `detailurl`

detailUrl

**端点**: `POST /v1/social/douyin/web/aweme/detailurl`



---


### `detail`

detail

**端点**: `POST /v1/social/douyin/web/aweme/detail`



---


### `poi`

poi

**端点**: `POST /v1/social/douyin/app/search/poi`



---


### `detailid`

detailId

**端点**: `POST /v1/social/douyin/app/aweme/detail_id`



---


### `channel`

channel

**端点**: `POST /v1/social/douyin/web/feed/channel`



---


### `list`

list

**端点**: `POST /v1/social/douyin/app/comment/list`



---


### `longvideometa`

longVideoMeta

**端点**: `GET /v1/social/douyin/web/other/long_video_meta`


**参数**:

- `episode_id_current` (string): Example value: 

- `album_id` (number): Example value: 7316087737772147251

- `aweme_id_current` (string): Example value: 



---


### `hotlist`

hotList

**端点**: `POST /v1/social/douyin/web/search/live`



---


### `reply`

reply

**端点**: `POST /v1/social/douyin/app/comment/listreply`



---


### `discover`

discover

**端点**: `POST /v1/social/douyin/app/search/discover`



---


### `list_1`

list

**端点**: `POST /v1/social/douyin/app/mix/list`



---


### `getpcbanner`

getPcBanner

**端点**: `GET /v1/social/douyin/web/other/getPcBanner`



---


### `brandweeklylist`

brandWeeklyList

**端点**: `POST /v1/social/douyin/app/hot/brand_weekly_list`



---


### `single_1`

single

**端点**: `POST /v1/social/douyin/app/search/single`



---


### `seokeywordrelated`

seoKeywordRelated

**端点**: `GET /v1/social/douyin/web/other/seo_keyword_related`


**参数**:

- `id` (number): Example value: 6984256064577441061



---


### `following`

following

**端点**: `POST /v1/social/douyin/app/user/following`



---


### `city`

city

**端点**: `GET /v1/social/douyin/app/poi/city`



---


### `aweme`

aweme

**端点**: `POST /v1/social/douyin/app/music/aweme`



---


### `webshorten`

webShorten

**端点**: `GET /v1/social/douyin/web/other/web_shorten`



---


### `emojilist`

emojiList

**端点**: `GET /v1/social/douyin/web/other/emoji_list`



---


### `chart`

chart

**端点**: `POST /v1/social/douyin/app/music/chart`



---


### `aweme_1`

aweme

**端点**: `POST /v1/social/douyin/app/challenge/aweme`



---


### `music`

music

**端点**: `POST /v1/social/douyin/app/search/music`



---


### `challenge`

challenge

**端点**: `POST /v1/social/douyin/app/search/challenge`



---


### `index`

index

**端点**: `GET /v1/social/douyin/app/feed/index`


**参数**:

- `max_cursor` (number): Example value: 0



---


### `item_1`

item

**端点**: `POST /v1/social/douyin/app/search/item`



---


### `wallpaper`

wallpaper

**端点**: `POST /v1/social/douyin/web/feed/wallpaper`



---


### `brandbillboard`

brandBillboard

**端点**: `POST /v1/social/douyin/app/hot/brand_billboard`



---


### `mediumrelated`

mediumRelated

**端点**: `POST /v1/social/douyin/web/feed/medium_related`



---


### `nearby`

nearby

**端点**: `GET /v1/social/douyin/app/feed/nearby`


**参数**:

- `max_cursor` (number): Example value: 3

- `city` (number): Example value: 8616124



---


### `tab`

tab

**端点**: `POST /v1/social/douyin/web/feed/tab`



---


### `lvideotheater`

lvideoTheater

**端点**: `POST /v1/social/douyin/web/feed/lvideo_theater`



---


### `follow`

follow

**端点**: `POST /v1/social/douyin/web/feed/follow`



---


### `detail_1`

detail

**端点**: `POST /v1/social/douyin/app/poi/detail`



---


### `detail_2`

detail

**端点**: `POST /v1/social/douyin/app/challenge/detail`



---


### `module`

module

**端点**: `POST /v1/social/douyin/web/feed/module`



---


### `searchlist`

searchList

**端点**: `GET /v1/social/douyin/app/hot/search_list`


**参数**:

- `detail_list` (number): Example value: 1



---


### `appointlivelist`

appointLiveList

**端点**: `GET /v1/social/douyin/web/other/appoint_live_list`



---


### `queryaccounttype`

queryAccountType

**端点**: `GET /v1/social/douyin/web/other/query_account_type`


**参数**:

- `sec_user_id` (string): Example value: MS4wLjABAAAAIqOcUlkHRYn3R9QrxuXwCrQbarxTKLqYNDByv_hGbGU



---


### `aweme_2`

aweme

**端点**: `POST /v1/social/douyin/app/poi/aweme`



---


### `index_1`

index

**端点**: `POST /v1/social/douyin/app/shorten/index`



---


### `trans`

trans

**端点**: `POST /v1/social/douyin/app/schema/trans`



---


### `live`

live

**端点**: `POST /v1/social/douyin/app/search/live`



---


### `sug_1`

sug

**端点**: `GET /v1/social/douyin/app/search/sug`


**参数**:

- `keyword` (string): Example value: anime



---


### `poi_1`

poi

**端点**: `GET /v1/social/douyin/app/feed/poi`


**参数**:

- `id` (number): Example value: 6601124549775853572

- `cursor` (number): Example value: 0

- `count` (number): Example value: 10



---


### `reply_1`

reply

**端点**: `POST /v1/social/douyin/web/comment/listreply`



---


### `list_2`

list

**端点**: `POST /v1/social/douyin/web/comment/list`



---


### `social`

social

**端点**: `POST /v1/social/douyin/web/search/social`



---


### `recommend`

recommend

**端点**: `POST /v1/social/douyin/web/mix/recommend`



---


### `detail_3`

detail

**端点**: `POST /v1/social/douyin/web/mix/detail`



---


### `list_3`

list

**端点**: `POST /v1/social/douyin/web/mix/list`



---


### `ab`

ab

**端点**: `POST /v1/social/douyin/web/search/ab`



---


### `aweme_3`

aweme

**端点**: `POST /v1/social/douyin/web/mix/aweme`



---


### `brandcategory`

brandCategory

**端点**: `GET /v1/social/douyin/app/hot/brand_category`



---


### `aweme_4`

aweme

**端点**: `POST /v1/social/douyin/web/music/aweme`



---


### `detail_4`

detail

**端点**: `POST /v1/social/douyin/web/user/detail`



---


### `favorite`

favorite

**端点**: `POST /v1/social/douyin/app/aweme/favorite`



---


### `detailurl_1`

detailUrl

**端点**: `POST /v1/social/douyin/app/aweme/detail_url`



---


### `searchvideolist`

searchVideoList

**端点**: `POST /v1/social/douyin/app/hot/search_video_list`



---


### `billboardaweme`

billboardAweme

**端点**: `GET /v1/social/douyin/app/hot/billboard_aweme`



---


### `detail_5`

detail

**端点**: `POST /v1/social/douyin/web/music/detail`



---


### `aweme_5`

aweme

**端点**: `POST /v1/social/douyin/app/mix/aweme`



---


### `self`

self

**端点**: `POST /v1/social/douyin/web/user/self`



---


### `index_2`

index

**端点**: `GET /v1/social/douyin/app/hashtag/index`


**参数**:

- `id` (number): Example value: 7023579918135008293

- `offset` (number): Example value: 0

- `limit` (number): Example value: 20



---


### `detail_6`

detail

**端点**: `POST /v1/social/douyin/app/mix/detail`



---


### `detail_7`

detail

**端点**: `POST /v1/social/douyin/app/music/detail`



---


### `suggestwords`

suggestWords

**端点**: `GET /v1/social/douyin/app/search/suggest_words`


**参数**:

- `keyword` (string): Example value: anime

- `business_id` (number): Example value: 30003

- `from_group_id` (string): Example value: 



---


### `seoinnerlink`

seoInnerLink

**端点**: `GET /v1/social/douyin/web/other/seo_inner_link`



---



## 技术栈

- **传输协议**: stdio
- **HTTP 客户端**: httpx


## 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件。

## 开发

此服务器由 [API-to-MCP](https://github.com/BACH-AI-Tools/api-to-mcp) 工具生成。

版本: 1.0.0
