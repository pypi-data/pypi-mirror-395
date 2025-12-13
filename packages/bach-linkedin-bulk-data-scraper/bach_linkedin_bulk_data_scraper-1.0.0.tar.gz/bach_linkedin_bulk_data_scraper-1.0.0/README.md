# Linkedin Bulk Data Scraper MCP Server

[English](./README_EN.md) | 简体中文 | [繁體中文](./README_ZH-TW.md)

用于访问 Linkedin Bulk Data Scraper API 的 MCP 服务器。

## 🚀 使用 EMCP 平台快速体验

**[EMCP](https://sit-emcp.kaleido.guru)** 是一个强大的 MCP 服务器管理平台，让您无需手动配置即可快速使用各种 MCP 服务器！

### 快速开始：

1. 🌐 访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)**
2. 📝 注册并登录账号
3. 🎯 进入 **MCP 广场**，浏览所有可用的 MCP 服务器
4. 🔍 搜索或找到本服务器（`bach-linkedin_bulk_data_scraper`）
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

这是一个 MCP 服务器，用于访问 Linkedin Bulk Data Scraper API。

- **PyPI 包名**: `bach-linkedin_bulk_data_scraper`
- **版本**: 1.0.0
- **传输协议**: stdio


## 安装

### 从 PyPI 安装:

```bash
pip install bach-linkedin_bulk_data_scraper
```

### 从源码安装:

```bash
pip install -e .
```

## 运行

### 方式 1: 使用 uvx（推荐，无需安装）

```bash
# 运行（uvx 会自动安装并运行）
uvx --from bach-linkedin_bulk_data_scraper bach_linkedin_bulk_data_scraper

# 或指定版本
uvx --from bach-linkedin_bulk_data_scraper@latest bach_linkedin_bulk_data_scraper
```

### 方式 2: 直接运行（开发模式）

```bash
python server.py
```

### 方式 3: 安装后作为命令运行

```bash
# 安装
pip install bach-linkedin_bulk_data_scraper

# 运行（命令名使用下划线）
bach_linkedin_bulk_data_scraper
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
    "bach-linkedin_bulk_data_scraper": {
      "command": "uvx",
      "args": ["--from", "bach-linkedin_bulk_data_scraper", "bach_linkedin_bulk_data_scraper"],
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
    "bach-linkedin_bulk_data_scraper": {
      "command": "uvx",
      "args": ["--from", "bach-linkedin_bulk_data_scraper", "bach_linkedin_bulk_data_scraper"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```


## 可用工具

此服务器提供以下工具:


### `game_of_thrones`

Returns game of thrones data

**端点**: `GET /goat`



---


### `game_of_thrones_1`

Returns gama of thrones data

**端点**: `POST /goat`



---


### `ip_address`

Returns ip address

**端点**: `POST /ip_address`



---


### `ip_address_1`

Returns ip address

**端点**: `GET /ip_address`



---


### `advice`

Random advice

**端点**: `GET /advice`



---


### `advice_1`

Random advice

**端点**: `POST /advice`



---


### `shuffle`

Shuffles string

**端点**: `GET /shuffle`


**参数**:

- `string` (string): Example value: sama



---


### `shuffle_1`

Shuffles string

**端点**: `POST /shuffle`



---


### `number_facts`

Returns number facts

**端点**: `GET /number_facts`



---


### `nnumber_facts`

Returns Number facts

**端点**: `POST /number_facts`



---


### `joke`

Returns joke

**端点**: `GET /joke`



---


### `joke_1`

Returns joke

**端点**: `POST /joke`



---


### `cat_facts`

Returns cat facts

**端点**: `GET /cat_fact`



---


### `cat_facts_1`

Returns cat facts

**端点**: `POST /cat_fact`



---


### `dog_fact`

Rreturns dog fact

**端点**: `GET /dog_fact`



---


### `dog_fact_1`

Returns dog fact

**端点**: `POST /dog_fact`



---


### `random_dog_image`

Returns dog image

**端点**: `GET /random_dog_image`



---


### `random_dog_image_1`

Returns dog image

**端点**: `POST /random_dog_image`



---


### `random_triva_question`

Returns random triva question

**端点**: `GET /random_triva_question`



---


### `random_triva_question_1`

Returns random triva question

**端点**: `POST /random_triva_question`



---


### `universities_list`

Returns USA university list

**端点**: `GET /universities_list`



---


### `universities_list_1`

Returns USA universities list

**端点**: `POST /universities_list`



---


### `json_placeholder`

Returns json placeholder

**端点**: `POST /json_placeholder`



---


### `json_placeholder_1`

Returns json placeholder

**端点**: `GET /json_placeholder`



---


### `ping`

Checks server health

**端点**: `POST /{ping}`


**参数**:

- `ping` (string) *必需*: Example value: ping



---


### `ping_1`

Check server health

**端点**: `GET /{ping}`


**参数**:

- `ping` (string) *必需*: Example value: ping



---



## 技术栈

- **传输协议**: stdio
- **HTTP 客户端**: httpx


## 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件。

## 开发

此服务器由 [API-to-MCP](https://github.com/BACH-AI-Tools/api-to-mcp) 工具生成。

版本: 1.0.0
