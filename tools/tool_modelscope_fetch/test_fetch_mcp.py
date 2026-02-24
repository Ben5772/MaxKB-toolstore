#!/usr/bin/env python3
"""
ModelScope Fetch MCP 工具测试脚本
"""

import sys
sys.path.insert(0, '/home/ben/fetch-mcp-docker/MaxKB-toolstore/tools/tool_modelscope_fetch/1.0.0')

from fetch_mcp import fetch_mcp_server


def test_basic_usage():
    """测试基础用法"""
    print("=" * 60)
    print("测试 1: 基础用法（只提供 URL）")
    print("=" * 60)
    
    result = fetch_mcp_server(url="https://example.com")
    
    if result["success"]:
        print(f"✓ 成功")
        print(f"  文档名称：{result['document_name']}")
        print(f"  内容长度：{result['content_length']}")
        print(f"  内容预览：{result['content'][:200]}...")
    else:
        print(f"✗ 失败")
        print(f"  错误：{result.get('error', '未知错误')}")
        print(f"  详情：{result.get('details', '')}")
    
    print()


def test_custom_config():
    """测试自定义配置"""
    print("=" * 60)
    print("测试 2: 自定义配置")
    print("=" * 60)
    
    result = fetch_mcp_server(
        url="https://example.com",
        custom_name="测试文档",
        max_length=5000,
        ignore_robots=True
    )
    
    if result["success"]:
        print(f"✓ 成功")
        print(f"  文档名称：{result['document_name']}")
        print(f"  内容长度：{result['content_length']}")
    else:
        print(f"✗ 失败")
        print(f"  错误：{result.get('error', '未知错误')}")
    
    print()


def test_all_parameters():
    """测试所有参数"""
    print("=" * 60)
    print("测试 3: 使用所有参数（完整配置）")
    print("=" * 60)
    
    result = fetch_mcp_server(
        url="https://example.com",
        custom_name="完整配置测试",
        max_length=8000,
        ignore_robots=True,
        mcp_server_url="https://mcp.api-inference.modelscope.net/b13c348780054e/mcp",
        api_key="",  # 如果需要认证，在这里填写
        protocol_version="2024-11-05",
        client_name="maxkb",
        client_version="1.0",
        timeout_init=30,
        timeout_call=60
    )
    
    if result["success"]:
        print(f"✓ 成功")
        print(f"  文档名称：{result['document_name']}")
        print(f"  内容长度：{result['content_length']}")
        print(f"  源 URL: {result['source_url']}")
    else:
        print(f"✗ 失败")
        print(f"  错误：{result.get('error', '未知错误')}")
    
    print()


if __name__ == "__main__":
    print("\n开始运行 ModelScope Fetch MCP 工具测试\n")
    
    try:
        test_basic_usage()
        test_custom_config()
        test_all_parameters()
        
        print("=" * 60)
        print("测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n测试过程中发生异常：{e}")
        import traceback
        traceback.print_exc()
