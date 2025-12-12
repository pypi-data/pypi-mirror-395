"""
批量重命名MCP工具

提供批量重命名文件的功能
"""

from typing import Dict, Any
import logging

from ..core.renamer import Renamer
from ..core.operation_log import OperationLog
from ..core.pattern_parser import PatternParser

logger = logging.getLogger(__name__)


class BatchRenameHandler:
    """批量重命名处理器"""
    
    def __init__(self, config: Dict[str, Any], operation_log: OperationLog):
        self.config = config
        self.operation_log = operation_log
        self.renamer = Renamer(config, operation_log)
    
    async def handle(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理批量重命名请求
        
        Args:
            arguments: MCP工具参数
            
        Returns:
            操作结果
        """
        try:
            # 提取参数
            target = arguments.get("target")
            pattern = arguments.get("pattern")
            options = arguments.get("options", {})
            
            # 验证必需参数
            if not target:
                return {
                    "success": False,
                    "message": "Missing required parameter: target",
                    "error_type": "ValidationError"
                }
            
            if not pattern:
                return {
                    "success": False,
                    "message": "Missing required parameter: pattern",
                    "error_type": "ValidationError"
                }
            
            logger.info(f"开始批量重命名: target={target}, pattern={pattern}")
            
            # 添加pattern到options中，供日志使用
            options["pattern"] = pattern
            
            # 执行批量重命名
            result = self.renamer.batch_rename(target, pattern, options)
            
            # 如果是预览模式，添加额外信息
            if options.get("dry_run", False):
                result["help"] = self._get_pattern_help()
                result["examples"] = PatternParser.get_pattern_examples()
            
            logger.info(f"Batch rename finished: success={result.get('success')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Batch rename handler failed: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "error_type": type(e).__name__
            }
    
    def _get_pattern_help(self) -> Dict[str, Any]:
        """获取模式帮助信息"""
        return {
            "description": "Rename pattern syntax",
            "template_variables": PatternParser.get_available_variables(),
            "special_patterns": {
                "regex:pattern:replacement": "Regex replacement",
                "upper:{name}": "Convert to uppercase",
                "lower:{name}": "Convert to lowercase",
                "title:{name}": "Convert to title case"
            },
            "conflict_resolution": {
                "auto_number": "Auto add sequence to avoid conflicts (default)",
                "skip": "Skip conflicting files",
                "overwrite": "Overwrite existing files"
            }
        }
