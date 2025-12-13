#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Server - 文本文件对比工具
通过 stdio 方式与客户端通信，提供双向文本文件逐行对比功能
"""

import json
import sys
import asyncio
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# 创建 MCP Server 实例
app = Server("file-comparison-server")


def compare_files(file1_content: str, file2_content: str) -> Dict[str, Any]:
    """
    双向文本文件逐行对比功能
    
    Args:
        file1_content: 第一个文件的完整文本内容
        file2_content: 第二个文件的完整文本内容
    
    Returns:
        包含对比结果的字典
    """
    # 按行分割文件内容
    file1_lines = file1_content.splitlines()
    file2_lines = file2_content.splitlines()
    
    # 创建行内容集合以加速查找
    file1_set = set(file1_lines)
    file2_set = set(file2_lines)
    
    # 正向对比：找出仅存在于 file1 中的行
    only_in_file1 = []
    for line_num, line in enumerate(file1_lines, start=1):
        if line not in file2_set:
            only_in_file1.append({
                "line_number": line_num,
                "content": line
            })
    
    # 反向对比：找出仅存在于 file2 中的行
    only_in_file2 = []
    for line_num, line in enumerate(file2_lines, start=1):
        if line not in file1_set:
            only_in_file2.append({
                "line_number": line_num,
                "content": line
            })
    
    # 生成对比结果
    result = {
        "only_in_file1": only_in_file1,
        "only_in_file2": only_in_file2,
        "summary": {
            "file1_total_lines": len(file1_lines),
            "file2_total_lines": len(file2_lines),
            "unique_to_file1": len(only_in_file1),
            "unique_to_file2": len(only_in_file2)
        }
    }
    
    return result


@app.list_tools()
async def list_tools() -> List[Tool]:
    """
    向客户端返回可用工具列表
    """
    return [
        Tool(
            name="compare_text_files",
            description="双向文本文件逐行对比工具。以第一个文件为准找出与第二个文件的差异，"
                        "同时以第二个文件为准找出与第一个文件的差异，返回 JSON 格式结果。",
            inputSchema={
                "type": "object",
                "properties": {
                    "file1_content": {
                        "type": "string",
                        "description": "第一个文件的完整文本内容"
                    },
                    "file2_content": {
                        "type": "string",
                        "description": "第二个文件的完整文本内容"
                    }
                },
                "required": ["file1_content", "file2_content"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """
    处理工具调用请求
    
    Args:
        name: 工具名称
        arguments: 工具参数
    
    Returns:
        工具执行结果
    """
    if name != "compare_text_files":
        raise ValueError(f"未知工具: {name}")
    
    # 参数验证
    if not isinstance(arguments, dict):
        raise ValueError("参数必须是字典类型")
    
    file1_content = arguments.get("file1_content")
    file2_content = arguments.get("file2_content")
    
    if file1_content is None:
        raise ValueError("缺少必需参数: file1_content")
    if file2_content is None:
        raise ValueError("缺少必需参数: file2_content")
    
    if not isinstance(file1_content, str):
        raise ValueError("file1_content 必须是字符串类型")
    if not isinstance(file2_content, str):
        raise ValueError("file2_content 必须是字符串类型")
    
    # 执行文件对比
    try:
        result = compare_files(file1_content, file2_content)
        
        # 将结果转换为格式化的 JSON 字符串
        result_json = json.dumps(result, ensure_ascii=False, indent=2)
        
        return [TextContent(
            type="text",
            text=result_json
        )]
    except Exception as e:
        raise RuntimeError(f"文件对比过程中发生错误: {str(e)}")


async def main():
    """
    MCP Server 主入口
    """
    # 通过 stdio 启动 Server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


def main() -> None:
    asyncio.run(main())
