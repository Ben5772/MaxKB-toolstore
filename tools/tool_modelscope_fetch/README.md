# ModelScope Fetch MCP 工具

## 一、项目介绍

### 1.1 核心功能
本工具通过调用 ModelScope 云端 MCP（Model Call Protocol）服务，将网页内容抓取并转换为 Markdown 格式。支持完整的 MCP 协议握手流程，包括 Initialize、Initialized 通知和 Tool Call。

### 1.2 适用场景
- **网页内容提取**：将新闻文章、技术文档、博客等网页转换为结构化 Markdown
- **知识库构建**：自动抓取网络资源并转换为 MaxKB 可用的文档格式
- **数据采集**：批量获取网页内容并进行标准化处理
- **内容归档**：保存网页内容为 Markdown 格式，便于版本管理和检索

## 二、环境准备

### 2.1 依赖库

| 依赖库 | 版本要求 | 用途说明 |
|--------|----------|----------|
| `requests` | 任意版本 | HTTP 请求库，用于与 ModelScope MCP 服务通信 |
| `typing` | Python 内置 | 类型注解支持 |
| `re` | Python 内置 | 正则表达式，用于提取网页标题 |
| `urllib.parse` | Python 内置 | URL 解析，提取域名 |

### 2.2 安装依赖

```bash
pip install requests
```

> 注：Python 3.7+ 环境即可运行，其他依赖均为标准库。

## 三、参数说明

### 必需参数

| 参数名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `url` | `str` | 要抓取的网页 URL | `"https://example.com/article"` |

### 可选参数

| 参数名 | 类型 | 默认值 | 说明 | 示例 |
|--------|------|--------|------|------|
| `custom_name` | `str` | `""` | 自定义文档名称，为空则自动生成 | `"AI 技术报告"` |
| `max_length` | `int` | `10000` | 最大字符数限制 | `5000` |
| `ignore_robots` | `bool` | `True` | 是否忽略 robots.txt 限制 | `True` |
| `mcp_server_url` | `str` | `"https://mcp.api-inference.modelscope.net/b13c348780054e/mcp"` | ModelScope MCP 服务器 URL | `"https://your-server.com/mcp"` |
| `api_key` | `str` | `""` | API 密钥（如果服务器需要认证） | `"your-api-key"` |
| `protocol_version` | `str` | `"2024-11-05"` | MCP 协议版本 | `"2024-11-05"` |
| `client_name` | `str` | `"maxkb"` | 客户端名称 | `"maxkb"` |
| `client_version` | `str` | `"1.0"` | 客户端版本 | `"1.0"` |
| `timeout_init` | `int` | `30` | Initialize 超时时间（秒） | `30` |
| `timeout_call` | `int` | `60` | Tool Call 超时时间（秒） | `60` |


## 四、返回结果说明

### 成功响应

```python
{
    "success": True,
    "document_name": "AI 技术报告 [example.com]",
    "content": "# 标题\n\n正文内容...",  # Markdown 格式
    "content_length": 3500,
    "source_url": "https://example.com/article"
}
```

### 失败响应

```python
{
    "success": False,
    "error": "Initialize failed: 401",
    "details": "Unauthorized - Invalid API key"
}
```

## 五、注意事项

1. **MCP 协议版本兼容性**：当前默认使用 `"2024-11-05"` 协议版本，如需使用其他版本请通过 `protocol_version` 参数指定。

2. **认证配置**：如果使用私有 MCP 服务，需通过 `api_key` 参数提供认证信息，工具会自动添加 `Authorization: Bearer <api_key>` 请求头。

3. **超时设置**：
   - `timeout_init`：建议设置为 30-60 秒，用于 MCP 握手初始化
   - `timeout_call`：建议设置为 60-120 秒，用于等待网页抓取和转换

4. **字符数限制**：`max_length` 参数会传递给 MCP 服务，由服务端控制返回内容的最大长度。

5. **robots.txt 处理**：魔搭云端服务无法跳过robot.txt，如需跳过需要自建本地服务，`ignore_robots=True` 时会跳过 robots.txt 检查，直接抓取网页内容。

6. **文档命名规则**：
   - 如果提供 `custom_name`，则使用该名称
   - 否则使用 `网页标题 [域名]` 格式
   - 如果无法提取标题，则使用 `Web Content [域名]`

7. **错误处理**：所有网络错误、协议错误都会返回包含 `error` 字段的字典，便于调试和日志记录。

