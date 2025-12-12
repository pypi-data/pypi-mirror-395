"""
操作日志系统

负责记录和管理所有重命名操作，支持撤销功能
"""

import json
import shutil
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

from ..utils.paths import MCPPaths

logger = logging.getLogger(__name__)


class OperationLog:
    """操作日志管理器"""
    
    def __init__(self, log_path: Optional[str] = None):
        # 如果提供了 log_path，使用提供的路径（向后兼容）
        # 否则使用新的标准化路径
        if log_path and log_path != str(MCPPaths.get_logs_dir()):
            logger.warning(f"使用自定义日志路径: {log_path}，建议使用标准路径")
            self.log_path = Path(log_path)
        else:
            # 使用新的标准化路径
            MCPPaths.ensure_directories()
            self.log_path = MCPPaths.get_logs_dir()
            # 尝试迁移旧文件
            migration_results = MCPPaths.migrate_legacy_files()
            if migration_results:
                logger.info(f"文件迁移完成: {migration_results}")
        
        self.log_path.mkdir(exist_ok=True)
        
        # 日志文件路径
        if log_path and log_path != str(MCPPaths.get_logs_dir()):
            self.log_file = self.log_path / "operations.json"
        else:
            self.log_file = MCPPaths.get_operation_log_path()
        
        # 确保日志文件存在
        if not self.log_file.exists():
            self._init_log_file()
    
    def _init_log_file(self) -> None:
        """初始化日志文件"""
        initial_data = {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "operations": []
        }
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, indent=2, ensure_ascii=False)
    
    def start_operation(self, operation_type: str, metadata: Dict[str, Any]) -> str:
        """
        开始一个新操作
        
        Args:
            operation_type: 操作类型
            metadata: 操作元数据
            
        Returns:
            操作ID
        """
        operation_id = str(uuid.uuid4())
        
        operation_data = {
            "id": operation_id,
            "type": operation_type,
            "status": "started",
            "start_time": datetime.now().isoformat(),
            "metadata": metadata,
            "operations": [],
            "result": None
        }
        
        # 读取现有日志
        log_data = self._read_log_file()
        log_data["operations"].append(operation_data)
        
        # 写入日志
        self._write_log_file(log_data)
        
        logger.info(f"Start operation: {operation_type} (ID: {operation_id})")
        
        return operation_id
    
    def complete_operation(self, operation_id: str, result: Dict[str, Any], operations: List[Dict[str, Any]] = None) -> None:
        """
        完成操作

        Args:
            operation_id: 操作ID
            result: 操作结果
            operations: 操作详情列表（可选，避免数据重复）
        """
        log_data = self._read_log_file()

        # 查找操作
        operation = self._find_operation(log_data, operation_id)
        if not operation:
            raise ValueError(f"Operation not found: {operation_id}")

        # 更新操作状态
        operation["status"] = "completed"
        operation["end_time"] = datetime.now().isoformat()
        operation["result"] = result

        # 如果提供了操作列表，保存到operations字段（优化：避免重复）
        if operations:
            operation["operations"] = operations
        elif "operations" in result:
            # 向后兼容：如果result中包含operations，保存它
            operation["operations"] = result["operations"]

        # 写入日志
        self._write_log_file(log_data)

        logger.info(f"操作完成: {operation_id}")
    
    def fail_operation(self, operation_id: str, error: str) -> None:
        """
        标记操作失败
        
        Args:
            operation_id: 操作ID
            error: 错误信息
        """
        log_data = self._read_log_file()
        
        # 查找操作
        operation = self._find_operation(log_data, operation_id)
        if not operation:
            raise ValueError(f"Operation not found: {operation_id}")
        
        # 更新操作状态
        operation["status"] = "failed"
        operation["end_time"] = datetime.now().isoformat()
        operation["error"] = error
        
        # 写入日志
        self._write_log_file(log_data)
        
        logger.error(f"操作失败: {operation_id} - {error}")
    
    def undo_operation(self, operation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        撤销操作
        
        Args:
            operation_id: 操作ID，如果为None则撤销最近的操作
            
        Returns:
            撤销结果
        """
        log_data = self._read_log_file()
        
        if operation_id is None:
            # 找到最近的已完成操作
            operation = self._get_latest_completed_operation(log_data)
            if not operation:
                return {
                    "success": False,
                    "message": "No operations available to undo"
                }
        else:
            operation = self._find_operation(log_data, operation_id)
            if not operation:
                return {
                    "success": False,
                    "message": f"Operation not found: {operation_id}"
                }
        
        # 检查操作是否可撤销
        if operation["status"] != "completed":
            return {
                "success": False,
                "message": f"Operation status does not allow undo: {operation['status']}"
            }
        
        if operation.get("undone", False):
            return {
                "success": False,
                "message": "Operation has already been undone"
            }
        
        # 执行撤销
        try:
            undo_result = self._execute_undo(operation)
            
            if undo_result["success"]:
                # 标记为已撤销
                operation["undone"] = True
                operation["undo_time"] = datetime.now().isoformat()
                operation["undo_result"] = undo_result
                
                # 写入日志
                self._write_log_file(log_data)
                
                logger.info(f"Operation undo succeeded: {operation['id']}")
            
            return undo_result
            
        except Exception as e:
            logger.error(f"Undo operation failed: {e}")
            return {
                "success": False,
                "message": f"Undo failed: {str(e)}",
                "error_type": type(e).__name__
            }
    
    def get_operation_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        获取操作历史
        
        Args:
            limit: 限制返回数量
            
        Returns:
            操作历史列表
        """
        log_data = self._read_log_file()
        operations = log_data["operations"]
        
        # 按时间倒序排列
        operations.sort(key=lambda x: x.get("start_time", ""), reverse=True)
        
        if limit:
            operations = operations[:limit]
        
        # 清理敏感信息，只返回摘要
        summary = []
        for op in operations:
            op_summary = {
                "id": op["id"],
                "type": op["type"],
                "status": op["status"],
                "start_time": op["start_time"],
                "end_time": op.get("end_time"),
                "undone": op.get("undone", False)
            }
            
            # 添加简化的结果信息
            if "result" in op and op["result"]:
                result = op["result"]
                op_summary["files_processed"] = result.get("success_count", 0)
                op_summary["files_failed"] = result.get("failed_count", 0)
            
            summary.append(op_summary)
        
        return summary
    
    def get_operation_details(self, operation_id: str) -> Optional[Dict[str, Any]]:
        """
        获取操作详细信息
        
        Args:
            operation_id: 操作ID
            
        Returns:
            操作详情或None
        """
        log_data = self._read_log_file()
        return self._find_operation(log_data, operation_id)
    
    def clean_old_logs(self, retention_days: int = 30) -> int:
        """
        清理旧日志
        
        Args:
            retention_days: 保留天数
            
        Returns:
            清理的操作数量
        """
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        log_data = self._read_log_file()
        original_count = len(log_data["operations"])
        
        # 过滤掉旧操作
        log_data["operations"] = [
            op for op in log_data["operations"]
            if datetime.fromisoformat(op["start_time"]) > cutoff_date
        ]
        
        cleaned_count = original_count - len(log_data["operations"])
        
        if cleaned_count > 0:
            self._write_log_file(log_data)
            logger.info(f"Cleaned {cleaned_count} old operation records")
        
        return cleaned_count
    
    def _read_log_file(self) -> Dict[str, Any]:
        """读取日志文件"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"读取日志文件失败，重新初始化: {e}")
            self._init_log_file()
            return self._read_log_file()
    
    def _write_log_file(self, data: Dict[str, Any]) -> None:
        """写入日志文件"""
        # 创建备份
        if self.log_file.exists():
            backup_file = self.log_file.with_suffix('.json.bak')
            shutil.copy2(self.log_file, backup_file)
        
        # 写入新数据
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _find_operation(self, log_data: Dict[str, Any], operation_id: str) -> Optional[Dict[str, Any]]:
        """查找操作"""
        for operation in log_data["operations"]:
            if operation["id"] == operation_id:
                return operation
        return None
    
    def _get_latest_completed_operation(self, log_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """获取最近的已完成操作"""
        completed_ops = [
            op for op in log_data["operations"]
            if op["status"] == "completed" and not op.get("undone", False)
        ]
        
        if not completed_ops:
            return None
        
        # 按时间排序，返回最近的
        completed_ops.sort(key=lambda x: x["start_time"], reverse=True)
        return completed_ops[0]
    
    def _execute_undo(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """执行撤销操作"""
        if operation["type"] != "batch_rename":
            return {
                "success": False,
                "message": f"Unsupported undo operation type: {operation['type']}"
            }
        
        # 获取操作中的文件重命名列表
        file_operations = operation.get("operations", [])
        if not file_operations:
            return {
                "success": False,
                "message": "No file operations available to undo"
            }
        
        success_count = 0
        failed_count = 0
        failed_files = []
        
        # 反向执行文件重命名
        for file_op in reversed(file_operations):
            try:
                current_path = Path(file_op["new_path"])
                original_path = Path(file_op["original_path"])
                
                if current_path.exists():
                    # 检查原始文件名是否被占用
                    if original_path.exists() and str(original_path) != str(current_path):
                        # 尝试生成一个临时名称
                        temp_path = original_path.with_suffix(f".temp_{uuid.uuid4().hex[:8]}")
                        current_path.rename(temp_path)
                        temp_path.rename(original_path)
                    else:
                        current_path.rename(original_path)
                    
                    success_count += 1
                    logger.info(f"Undo succeeded: {current_path.name} -> {original_path.name}")
                else:
                    failed_count += 1
                    failed_files.append(f"File not found: {current_path}")
                    
            except Exception as e:
                failed_count += 1
                failed_files.append(f"{file_op['new_path']}: {str(e)}")
                logger.error(f"Undo failed: {file_op['new_path']} - {e}")
        
        result = {
            "success": success_count > 0,
            "files_restored": success_count,
            "files_failed": failed_count,
            "message": f"Successfully restored {success_count} files"
        }
        
        if failed_files:
            result["failed_files"] = failed_files
            result["message"] += f", {failed_count} failed"
        
        return result
