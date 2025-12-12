"""
撤销重命名MCP工具

提供撤销重命名操作的功能
"""

from typing import Dict, Any, List
import logging

from ..core.operation_log import OperationLog

logger = logging.getLogger(__name__)


class UndoRenameHandler:
    """撤销重命名处理器"""
    
    def __init__(self, config: Dict[str, Any], operation_log: OperationLog):
        self.config = config
        self.operation_log = operation_log
    
    async def handle(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理撤销重命名请求
        
        Args:
            arguments: MCP工具参数
            
        Returns:
            操作结果
        """
        try:
            # 提取参数
            operation_id = arguments.get("operation_id")
            
            logger.info(f"开始撤销重命名: operation_id={operation_id}")
            
            # 执行撤销操作
            result = self.operation_log.undo_operation(operation_id)
            
            # 添加额外信息
            if result["success"]:
                result["help"] = self._get_undo_help()
                
                # 如果没有指定operation_id，说明撤销的是最近的操作
                if operation_id is None:
                    result["note"] = "Undid the latest rename operation"
                else:
                    result["note"] = f"Undid specified operation: {operation_id}"
            else:
                # 如果撤销失败，提供帮助信息
                result["help"] = self._get_troubleshooting_help()
                result["available_operations"] = self._get_available_operations()
            
            logger.info(f"撤销重命名完成: success={result.get('success')}")
            
            return result
            
        except Exception as e:
            logger.error(f"撤销重命名处理失败: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "error_type": type(e).__name__,
                "help": self._get_troubleshooting_help()
            }
    
    def _get_undo_help(self) -> Dict[str, Any]:
        """获取撤销操作帮助信息"""
        return {
            "description": "撤销重命名操作说明",
            "usage": {
                "undo_latest": "不提供operation_id参数，撤销最近的操作",
                "undo_specific": "提供operation_id参数，撤销指定的操作"
            },
            "limitations": [
                "只能撤销已完成的批量重命名操作",
                "每个操作只能撤销一次",
                "如果原文件已被修改或移动，撤销可能失败",
                "撤销操作会尝试将文件名恢复到重命名前的状态"
            ],
            "tips": [
                "撤销前建议先查看操作历史",
                "如果撤销部分失败，请检查文件是否被其他程序占用",
                "建议在重要操作前先使用预览模式（dry_run=true）"
            ]
        }
    
    def _get_troubleshooting_help(self) -> Dict[str, Any]:
        """获取故障排除帮助信息"""
        return {
            "common_issues": {
                "no_operations": {
                    "problem": "没有可撤销的操作",
                    "solutions": [
                        "检查是否有已完成的重命名操作",
                        "确认操作没有被撤销过"
                    ]
                },
                "operation_not_found": {
                    "problem": "找不到指定的操作ID",
                    "solutions": [
                        "检查operation_id是否正确",
                        "查看操作历史获取有效的ID"
                    ]
                },
                "partial_failure": {
                    "problem": "撤销部分成功，部分失败",
                    "solutions": [
                        "检查失败文件是否被其他程序占用",
                        "确认文件路径仍然有效",
                        "检查磁盘空间和权限"
                    ]
                }
            },
            "how_to_check": [
                "使用scan_files工具查看目录状态",
                "查看操作历史了解已执行的操作",
                "检查操作日志中的详细信息"
            ]
        }
    
    def _get_available_operations(self) -> List[Dict[str, Any]]:
        """获取可撤销的操作列表"""
        try:
            # 获取最近的操作历史
            history = self.operation_log.get_operation_history(limit=5)
            
            # 过滤出可撤销的操作
            available = []
            for op in history:
                if (op["status"] == "completed" and 
                    not op.get("undone", False) and
                    op["type"] == "batch_rename"):
                    
                    available.append({
                        "id": op["id"],
                        "start_time": op["start_time"],
                        "files_processed": op.get("files_processed", 0),
                        "description": f"批量重命名 {op.get('files_processed', 0)} 个文件"
                    })
            
            return available
            
        except Exception as e:
            logger.warning(f"获取可用操作列表失败: {e}")
            return []
