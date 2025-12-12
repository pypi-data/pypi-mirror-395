#!/usr/bin/env python3
"""
批量文件重命名MCP服务器

一个功能强大、安全可靠的批量文件重命名MCP（Model Context Protocol）服务器，
提供灵活的重命名模式、操作日志和撤销功能。

主要功能：
- 批量重命名文件
- 操作撤销功能
- 文件扫描和预览
- 安全验证机制
- 详细的操作日志

使用示例：
    from batch_rename_mcp import BatchRenameMCPServer
    
    server = BatchRenameMCPServer()
    # 运行服务器
    import asyncio
    asyncio.run(server.run())
"""

from .server import BatchRenameMCPServer, main
from .core.renamer import Renamer
from .core.pattern_parser import PatternParser
from .core.operation_log import OperationLog

__version__ = "1.0.0"
__author__ = "fengjinchao"
__email__ = "fengjinchao@example.com"
__description__ = "批量文件重命名MCP服务器 - 功能强大、安全可靠的文件重命名工具"

__all__ = [
    "BatchRenameMCPServer",
    "main",
    "Renamer",
    "PatternParser",
    "OperationLog",
    "__version__",
    "__author__",
    "__email__",
    "__description__",
]
