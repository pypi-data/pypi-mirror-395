"""
核心重命名器模块

负责文件重命名的核心逻辑实现
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

from .pattern_parser import PatternParser
from .operation_log import OperationLog
from ..utils.security import SecurityValidator

logger = logging.getLogger(__name__)


class Renamer:
    """文件重命名核心类"""
    
    def __init__(self, config: Dict[str, Any], operation_log: OperationLog):
        self.config = config
        self.operation_log = operation_log
        self.pattern_parser = PatternParser()
        self.security = SecurityValidator(config)
        
    def batch_rename(
        self,
        target: str,
        pattern: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        批量重命名文件
        
        Args:
            target: 目标路径
            pattern: 重命名模式
            options: 选项字典
            
        Returns:
            操作结果
        """
        options = options or {}
        
        try:
            # 安全验证
            self.security.validate_path(target)
            
            # 获取文件列表
            files = self._get_file_list(target, options)
            
            if not files:
                return {
                    "success": False,
                    "message": "No matching files found",
                    "files_processed": 0
                }
            
            # 限制处理文件数量
            max_files = self.config.get("settings", {}).get("max_files_per_operation", 1000)
            if len(files) > max_files:
                return {
                    "success": False,
                    "message": f"File count exceeds limit ({len(files)} > {max_files})",
                    "files_found": len(files)
                }
            
            # 验证重命名操作
            rename_plan = self._create_rename_plan(files, pattern)
            validation_result = self._validate_rename_plan(rename_plan)
            
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "message": "Rename plan validation failed",
                    "errors": validation_result["errors"]
                }
            
            # 检查是否为预览模式
            if options.get("dry_run", False):
                return {
                    "success": True,
                    "message": "Preview mode",
                    "preview": rename_plan["preview"],
                    "files_to_process": len(files)
                }
            
            # 执行重命名
            result = self._execute_rename(rename_plan, options)
            
            return result
            
        except Exception as e:
            logger.error(f"Batch rename failed: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "error_type": type(e).__name__
            }
    
    def _get_file_list(self, target: str, options: Dict[str, Any]) -> List[Path]:
        """获取文件列表"""
        target_path = Path(target).expanduser().resolve()
        
        if not target_path.exists():
            raise FileNotFoundError(f"目标路径不存在: {target}")
        
        files = []
        
        if target_path.is_file():
            files.append(target_path)
        elif target_path.is_dir():
            # 扫描目录
            recursive = options.get("recursive", False)
            file_filter = options.get("file_filter", "*")
            
            if recursive:
                pattern = f"**/{file_filter}"
                files.extend(target_path.glob(pattern))
            else:
                files.extend(target_path.glob(file_filter))
            
            # 只保留文件，过滤掉目录
            files = [f for f in files if f.is_file()]
        
        return sorted(files)
    
    def _create_rename_plan(self, files: List[Path], pattern: str) -> Dict[str, Any]:
        """创建重命名计划"""
        self.pattern_parser.reset_counter()
        
        rename_operations = []
        preview = []
        
        for i, file_path in enumerate(files, 1):
            try:
                # 生成新文件名
                new_name = self.pattern_parser.parse_pattern(pattern, file_path, counter=i)
                new_path = file_path.parent / new_name
                
                # 验证新文件名
                self.security.validate_filename(new_name)
                
                operation = {
                    "original_path": str(file_path),
                    "new_path": str(new_path),
                    "original_name": file_path.name,
                    "new_name": new_name
                }
                
                rename_operations.append(operation)
                
                preview.append({
                    "original": file_path.name,
                    "new_name": new_name,
                    "status": "ready"
                })
                
            except Exception as e:
                logger.warning(f"Failed to process file {file_path}: {e}")
                preview.append({
                    "original": str(file_path.name),
                    "new_name": "",
                    "status": "error",
                    "error": str(e)
                })
        
        return {
            "operations": rename_operations,
            "preview": preview
        }
    
    def _validate_rename_plan(self, rename_plan: Dict[str, Any]) -> Dict[str, Any]:
        """验证重命名计划"""
        errors = []
        operations = rename_plan["operations"]
        
        # 检查文件名冲突
        new_paths = [op["new_path"] for op in operations]
        duplicates = self._find_duplicates(new_paths)
        
        if duplicates:
            errors.append(f"Duplicate new filenames found: {', '.join(duplicates)}")
        
        # 检查目标文件是否已存在
        existing_files = []
        for operation in operations:
            new_path = Path(operation["new_path"])
            if new_path.exists() and str(new_path) != operation["original_path"]:
                existing_files.append(str(new_path))
        
        if existing_files:
            errors.append(f"Target files already exist: {', '.join(existing_files[:5])}")
            if len(existing_files) > 5:
                errors.append(f"... and {len(existing_files) - 5} more files")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def _execute_rename(self, rename_plan: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """执行重命名操作"""
        operations = rename_plan["operations"]
        conflict_resolution = options.get("conflict_resolution", "auto_number")

        success_count = 0
        failed_operations = []
        successful_operations = []
        operation_lock = []  # 用于原子性回滚的操作锁

        # 开始操作
        operation_id = self.operation_log.start_operation("batch_rename", {
            "pattern": options.get("pattern", ""),
            "total_files": len(operations),
            "conflict_resolution": conflict_resolution
        })

        try:
            for operation in operations:
                try:
                    original_path = Path(operation["original_path"])
                    new_path = Path(operation["new_path"])

                    # 处理冲突
                    if new_path.exists() and str(new_path) != str(original_path):
                        new_path = self._resolve_conflict(new_path, conflict_resolution)
                        operation["new_path"] = str(new_path)
                        operation["new_name"] = new_path.name

                    # 创建操作锁记录（用于回滚）
                    lock_record = {
                        "original_path": str(original_path),
                        "new_path": str(new_path),
                        "backup_created": False,
                        "operation_completed": False
                    }
                    operation_lock.append(lock_record)

                    # 执行重命名
                    original_path.rename(new_path)
                    lock_record["operation_completed"] = True

                    # 记录成功的操作（减少数据重复，只存储关键信息）
                    successful_operations.append({
                        "original_path": operation["original_path"],
                        "new_path": operation["new_path"],
                        "original_name": operation["original_name"],
                        "new_name": operation["new_name"]
                    })
                    success_count += 1

                    logger.info(f"重命名成功: {original_path.name} -> {new_path.name}")

                except Exception as e:
                    error_info = {
                        "file": operation["original_path"],
                        "error": str(e)
                    }
                    failed_operations.append(error_info)
                    logger.error(f"重命名失败: {operation['original_path']} - {e}")

            # 记录操作结果（优化：减少重复数据）
            self.operation_log.complete_operation(operation_id, {
                "success_count": success_count,
                "failed_count": len(failed_operations),
                "has_operations": len(successful_operations) > 0  # 用标志位代替完整数据
            }, successful_operations)  # 单独传递操作数据

            result = {
                "success": True,
                "operation_id": operation_id,
                "message": f"Successfully renamed {success_count} files",
                "files_processed": success_count,
                "files_failed": len(failed_operations)
            }

            if failed_operations:
                result["failed_operations"] = failed_operations
                result["message"] += f", {len(failed_operations)} failed"

            return result

        except Exception as e:
            # 操作失败，使用改进的回滚机制
            self.operation_log.fail_operation(operation_id, str(e))

            if operation_lock:
                self._atomic_rollback_operations(operation_lock)

            raise e
    
    
    def _find_duplicates(self, items: List[str]) -> List[str]:
        """查找重复项"""
        seen = set()
        duplicates = set()
        
        for item in items:
            if item in seen:
                duplicates.add(item)
            seen.add(item)
        
        return list(duplicates)
    
    def _resolve_conflict(self, path: Path, strategy: str) -> Path:
        """解决文件名冲突"""
        if strategy == "skip":
            raise ValueError(f"File exists, skipping: {path}")
        elif strategy == "overwrite":
            return path
        elif strategy == "auto_number":
            return self._get_unique_path(path)
            else:
                raise ValueError(f"Unknown conflict resolution strategy: {strategy}")
    
    def _get_unique_path(self, path: Path) -> Path:
        """获取唯一的文件路径"""
        if not path.exists():
            return path
        
        stem = path.stem
        suffix = path.suffix
        parent = path.parent
        
        counter = 1
        while True:
            new_name = f"{stem}_{counter:03d}{suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1
            
            if counter > 999:
                raise ValueError("Unable to generate unique filename")
    
    def _atomic_rollback_operations(self, operation_lock: List[Dict[str, Any]]) -> None:
        """原子性回滚操作"""
        logger.info(f"开始原子性回滚 {len(operation_lock)} 个操作...")

        rollback_count = 0
        rollback_errors = []

        # 反向回滚已完成的操作
        for lock_record in reversed(operation_lock):
            if not lock_record["operation_completed"]:
                continue

            try:
                current_path = Path(lock_record["new_path"])
                original_path = Path(lock_record["original_path"])

                if current_path.exists():
                    # 检查原始路径是否被占用
                    if original_path.exists() and str(original_path) != str(current_path):
                        # 生成临时路径进行安全回滚
                        import uuid
                        temp_path = original_path.with_suffix(f".rollback_temp_{uuid.uuid4().hex[:8]}")
                        current_path.rename(temp_path)

                        # 如果原始位置有文件，先移动到临时位置
                        if original_path.exists():
                            conflict_temp = original_path.with_suffix(f".conflict_{uuid.uuid4().hex[:8]}")
                            original_path.rename(conflict_temp)
                            logger.warning(f"回滚时发现冲突文件，已移动到: {conflict_temp}")

                        # 回滚到原始位置
                        temp_path.rename(original_path)
                    else:
                        # 直接回滚
                        current_path.rename(original_path)

                    rollback_count += 1
                    logger.info(f"回滚成功: {current_path.name} -> {original_path.name}")
                else:
                    logger.warning(f"回滚时文件不存在: {current_path}")

            except Exception as e:
                error_msg = f"回滚失败: {lock_record['new_path']} -> {lock_record['original_path']}: {e}"
                rollback_errors.append(error_msg)
                logger.error(error_msg)

        if rollback_errors:
            logger.error(f"回滚完成，成功 {rollback_count} 个，失败 {len(rollback_errors)} 个")
            for error in rollback_errors:
                logger.error(f"  - {error}")
        else:
            logger.info(f"原子性回滚完成，成功回滚 {rollback_count} 个操作")

    def _rollback_operations(self, operations: List[Dict[str, Any]]) -> None:
        """回滚操作（保留旧方法以兼容）"""
        logger.info(f"回滚 {len(operations)} 个操作...")

        for operation in reversed(operations):
            try:
                current_path = Path(operation["new_path"])
                original_path = Path(operation["original_path"])

                if current_path.exists():
                    current_path.rename(original_path)
                    logger.info(f"回滚成功: {current_path.name} -> {original_path.name}")

            except Exception as e:
                logger.error(f"回滚失败: {operation} - {e}")
