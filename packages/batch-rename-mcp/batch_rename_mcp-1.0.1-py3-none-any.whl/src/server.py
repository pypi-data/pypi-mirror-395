#!/usr/bin/env python3
"""
批量文件重命名MCP服务器

提供批量重命名、撤销操作和文件扫描功能的MCP服务器
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
import mcp.server.stdio
import mcp.types as types

from .tools.batch_rename import BatchRenameHandler
from .tools.undo_rename import UndoRenameHandler
from .tools.scan_files import ScanFilesHandler
from .core.operation_log import OperationLog
from .utils.config_loader import ConfigLoader
from .utils.paths import MCPPaths

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BatchRenameMCPServer:
    """批量重命名MCP服务器"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.server = Server("batch-rename-mcp")
        
        # 确保 MCP 目录结构存在
        MCPPaths.ensure_directories()
        
        # 加载配置
        self.config = ConfigLoader.load_config(config_path)
        
        # 初始化组件（传递 None 以使用新的标准路径）
        self.operation_log = OperationLog()
        
        # 初始化处理器
        self.batch_rename_handler = BatchRenameHandler(self.config, self.operation_log)
        self.undo_rename_handler = UndoRenameHandler(self.config, self.operation_log)
        self.scan_files_handler = ScanFilesHandler(self.config)
        
        self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """设置MCP处理器"""
        
        @self.server.list_resources()
        async def handle_list_resources() -> list[Resource]:
            """返回可用资源列表"""
            return [
                Resource(
                    uri="operation_log://recent",
                    name="最近操作日志",
                    description="显示最近的重命名操作记录",
                    mimeType="application/json",
                ),
                Resource(
                    uri="config://current",
                    name="当前配置",
                    description="显示当前服务器配置",
                    mimeType="application/json",
                ),
                Resource(
                    uri="paths://info",
                    name="路径信息",
                    description="显示 MCP 目录和文件路径信息",
                    mimeType="application/json",
                ),
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """读取资源内容"""
            if uri == "operation_log://recent":
                history = self.operation_log.get_operation_history(limit=10)
                return json.dumps(history, indent=2, ensure_ascii=False)
            elif uri == "config://current":
                return json.dumps(self.config, indent=2, ensure_ascii=False)
            elif uri == "paths://info":
                path_info = MCPPaths.get_path_info()
                return json.dumps(path_info, indent=2, ensure_ascii=False)
            else:
                raise ValueError(f"未知资源: {uri}")
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            """返回可用工具列表"""
            return [
                Tool(
                    name="batch_rename",
                    description="批量重命名文件工具。支持多种重命名模式和安全预览。\n\n必需参数：\n- target: 目标目录路径，如 '/Users/username/photos'\n- pattern: 重命名模式，常用格式：\n  * 模板变量：'test_{counter}' -> test_1.jpg, test_2.jpg\n  * 序号格式：'photo_{counter:02d}' -> photo_01.jpg, photo_02.jpg\n  * 添加前后缀：'{name}_backup' -> 原名_backup.jpg\n  * 日期时间：'IMG_{date}_{counter}' -> IMG_20240919_1.jpg\n  * 正则表达式：'regex:^test:fjc1' -> 将test开头替换为fjc1开头\n  * 正则表达式(忽略大小写)：'regex:test:fjc1:i' -> 将TEST或test替换为fjc1\n  * 正则表达式(复杂)：'regex:IMG_(\\d+):PHOTO_$1' -> IMG_123.jpg变为PHOTO_123.jpg\n  * 大小写转换：'upper:{name}' -> 转为大写\n\n可选参数 options 对象：\n- file_filter: '*.jpg' 或 '*.png' 等\n- dry_run: true(仅预览) 或 false(执行)\n- recursive: 是否包含子目录\n- conflict_resolution: 'auto_number'(自动编号) 'skip'(跳过) 'overwrite'(覆盖)\n\n使用示例：\n1. 替换前缀：{\"target\":\"/path/to/files\",\"pattern\":\"regex:^test:fjc1\",\"options\":{\"dry_run\":true}}\n2. 添加序号：{\"target\":\"/path/to/files\",\"pattern\":\"photo_{counter:03d}\",\"options\":{\"file_filter\":\"*.jpg\"}}\n3. 忽略大小写替换：{\"target\":\"/path/to/files\",\"pattern\":\"regex:test:fjc1:i\",\"options\":{\"dry_run\":true}}",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "target": {
                                "type": "string",
                                "description": "目标目录路径，包含要重命名的文件。例如：'/Users/username/Desktop/photos' 或 '~/Documents/files'"
                            },
                            "pattern": {
                                "type": "string",
                                "description": "重命名模式，支持：\n1. 模板变量：{name}原名 {counter}序号 {date}日期 {time}时间\n2. 正则表达式：regex:pattern:replacement[:flags] (flags: i=忽略大小写)\n3. 大小写转换：upper:{name} lower:{name} title:{name}\n示例：'regex:^test:fjc1' 'photo_{counter:02d}' '{name}_backup'"
                            },
                            "options": {
                                "type": "object",
                                "description": "可选配置参数，控制重命名的行为和范围",
                                "properties": {
                                    "recursive": {
                                        "type": "boolean",
                                        "default": False,
                                        "description": "是否包含子目录中的文件。false=只处理当前目录 true=包含所有子目录"
                                    },
                                    "file_filter": {
                                        "type": "string",
                                        "description": "文件类型过滤器，只处理匹配的文件。例如：'*.jpg'(只处理jpg) '*.png'(只处理png) '*'(所有文件)"
                                    },
                                    "conflict_resolution": {
                                        "type": "string",
                                        "enum": ["skip", "auto_number", "overwrite"],
                                        "default": "auto_number",
                                        "description": "文件名冲突时的处理方式：'skip'跳过冲突文件 'auto_number'自动添加编号 'overwrite'覆盖原文件"
                                    },
                                    "dry_run": {
                                        "type": "boolean",
                                        "default": False,
                                        "description": "是否仅预览效果不实际执行。true=仅显示预览结果 false=实际重命名文件"
                                    }
                                }
                            }
                        },
                        "required": ["target", "pattern"]
                    }
                ),
                Tool(
                    name="undo_rename",
                    description="撤销一次重命名。可选参数 operation_id(字符串)，不传则撤销最近记录。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "operation_id": {
                                "type": "string",
                                "description": "操作ID（可选，默认撤销最近操作）"
                            }
                        }
                    }
                ),
                Tool(
                    name="scan_files",
                    description="扫描指定路径下的文件。必需参数 path，可选 recursive(是否递归)、filter(如 *.jpg)、max_files(默认100)。",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "扫描路径"
                            },
                            "recursive": {
                                "type": "boolean",
                                "default": False,
                                "description": "是否递归扫描"
                            },
                            "filter": {
                                "type": "string",
                                "description": "文件过滤器"
                            },
                            "max_files": {
                                "type": "integer",
                                "default": 100,
                                "description": "最大返回文件数"
                            }
                        },
                        "required": ["path"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
            """处理工具调用"""
            try:
                if name == "batch_rename":
                    result = await self.batch_rename_handler.handle(arguments)
                elif name == "undo_rename":
                    result = await self.undo_rename_handler.handle(arguments)
                elif name == "scan_files":
                    result = await self.scan_files_handler.handle(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2, ensure_ascii=False)
                )]
                
            except Exception as e:
                logger.error(f"Tool call error {name}: {e}")
                return [types.TextContent(
                    type="text", 
                    text=f"Error: {str(e)}"
                )]

    async def run(self) -> None:
        """运行服务器"""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="batch-rename-mcp",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )

def main():
    """主入口函数"""
    import asyncio
    
    logger.info("启动批量文件重命名MCP服务器...")
    
    # 创建服务器实例
    server = BatchRenameMCPServer()
    
    # 运行服务器
    asyncio.run(server.run())

if __name__ == "__main__":
    main()
