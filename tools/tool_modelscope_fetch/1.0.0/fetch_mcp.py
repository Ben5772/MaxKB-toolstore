"""
MaxKB Tools - ModelScope Fetch MCP 客户端（精简版）
专为 MaxKB sandbox 设计，通过 HTTP 调用 ModelScope 云端 MCP 服务

外部参数:
    url: str - 要抓取的网页 URL
    custom_name: str - 自定义文档名称（可选）
    max_length: int - 最大字符数限制（可选，默认 10000）
    ignore_robots: bool - 是否忽略 robots.txt（可选，默认 True）
    mcp_server_url: str - ModelScope MCP 服务器 URL（可选，默认使用官方服务）
    api_key: str - API 密钥（可选，如果服务器需要认证）
    protocol_version: str - MCP 协议版本（可选，默认 "2024-11-05"）
    client_name: str - 客户端名称（可选，默认 "maxkb"）
    client_version: str - 客户端版本（可选，默认 "1.0"）
    timeout_init: int - Initialize 超时时间（可选，默认 30 秒）
    timeout_call: int - Tool Call 超时时间（可选，默认 60 秒）

返回:
    {
        "success": bool,
        "document_name": str,
        "content": str,  # Markdown 内容
        "content_length": int,
        "source_url": str
    }
"""

import requests
from typing import Dict, Any, Optional
import re


def fetch_mcp_server(
    url: str,
    custom_name: str = "",
    max_length: int = 10000,
    ignore_robots: bool = True,
    mcp_server_url: str = "https://mcp.api-inference.modelscope.net/b13c348780054e/mcp",
    api_key: str = "",
    protocol_version: str = "2024-11-05",
    client_name: str = "maxkb",
    client_version: str = "1.0",
    timeout_init: int = 30,
    timeout_call: int = 60
) -> Dict[str, Any]:
    """
    获取网页内容并转换为 Markdown
    
    Args:
        url: 目标网页 URL
        custom_name: 自定义文档名称
        max_length: 最大字符数限制
        ignore_robots: 是否忽略 robots.txt 限制
        mcp_server_url: ModelScope MCP 服务器 URL
        api_key: API 密钥（如果需要认证）
        protocol_version: MCP 协议版本
        client_name: 客户端名称
        client_version: 客户端版本
        timeout_init: Initialize 超时时间（秒）
        timeout_call: Tool Call 超时时间（秒）
        
    Returns:
        包含 Markdown 内容的字典
    """
    
    # ModelScope MCP Server 配置（可通过参数自定义）
    server_url = mcp_server_url
    
    try:
        # 步骤 1: Initialize
        session = requests.Session()
        init_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": protocol_version,
                "capabilities": {},
                "clientInfo": {"name": client_name, "version": client_version}
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream,application/json"
        }
        
        # 如果提供了 API 密钥，添加认证头
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        response = session.post(server_url, headers=headers, json=init_payload, timeout=timeout_init)
        if response.status_code != 200:
            return {
                "success": False,
                "error": f"Initialize failed: {response.status_code}",
                "details": response.text[:200]
            }
        
        # 获取 Session ID
        session_id = response.headers.get('mcp-session-id')
        if not session_id:
            return {"success": False, "error": "No session-id returned"}
        
        # 步骤 2: Initialized notification
        init_notification = {"jsonrpc": "2.0", "method": "notifications/initialized"}
        session.post(server_url, headers={**headers, "mcp-session-id": session_id}, 
                    json=init_notification, timeout=10)
        
        # 步骤 3: Call fetch tool
        fetch_params = {
            "url": url,
            "max_length": max_length
        }
        
        if ignore_robots:
            fetch_params["args"] = ["--ignore-robots-txt"]
        
        tool_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "fetch",
                "arguments": fetch_params
            }
        }
        
        response = session.post(
            server_url,
            headers={**headers, "mcp-session-id": session_id},
            json=tool_payload,
            timeout=timeout_call
        )
        
        if response.status_code != 200:
            return {
                "success": False,
                "error": f"Tool call failed: {response.status_code}",
                "details": response.text[:200]
            }
        
        # 解析响应
        result = response.json()
        if "error" in result:
            return {
                "success": False,
                "error": result["error"].get("message", "Unknown error")
            }
        
        # 提取内容
        result_data = result.get("result", {})
        content_data = result_data.get("content", {})
        
        # 处理列表格式的 content
        if isinstance(content_data, list) and len(content_data) > 0:
            text_content = ""
            for item in content_data:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_content += item.get("text", "")
            fetched_content = text_content
        else:
            fetched_content = content_data.get("content", "") if isinstance(content_data, dict) else str(content_data)
        
        # 提取标题
        fetched_title = result_data.get("title", "")
        if not fetched_title:
            # 从内容中提取第一个标题
            match = re.search(r'^#\s+(.+)$', fetched_content, re.MULTILINE)
            if match:
                fetched_title = match.group(1)
        
        # 构建文档名称
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        document_name = custom_name if custom_name else (f"{fetched_title} [{domain}]" if fetched_title else f"Web Content [{domain}]")
        
        return {
            "success": True,
            "document_name": document_name,
            "content": fetched_content,
            "content_length": len(fetched_content),
            "source_url": url
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Request error: {str(e)}",
            "details": str(e)[:200]
        }
