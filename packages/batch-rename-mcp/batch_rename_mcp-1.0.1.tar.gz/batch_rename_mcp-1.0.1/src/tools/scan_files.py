"""
文件扫描MCP工具

提供文件扫描和列表功能
"""

import fnmatch
from pathlib import Path
from typing import Dict, Any, List
import logging

from ..utils.security import SecurityValidator

logger = logging.getLogger(__name__)


class ScanFilesHandler:
    """文件扫描处理器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.security = SecurityValidator(config)
    
    async def handle(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理文件扫描请求
        
        Args:
            arguments: MCP工具参数
            
        Returns:
            扫描结果
        """
        try:
            # 提取参数
            path = arguments.get("path")
            recursive = arguments.get("recursive", False)
            filter_pattern = arguments.get("filter", "*")
            max_files = arguments.get("max_files", 100)
            
            # 验证必需参数
            if not path:
                return {
                    "success": False,
                    "message": "Missing required parameter: path",
                    "error_type": "ValidationError"
                }
            
            logger.info(f"Start scanning files: path={path}, recursive={recursive}, filter={filter_pattern}")
            
            # 安全验证
            self.security.validate_path(path)
            
            # 执行扫描
            result = self._scan_directory(path, recursive, filter_pattern, max_files)
            
            # 添加扫描统计信息
            result["scan_info"] = {
                "path": path,
                "recursive": recursive,
                "filter": filter_pattern,
                "max_files": max_files,
                "total_found": len(result.get("files", [])),
                "truncated": result.get("truncated", False)
            }
            
            logger.info(f"File scan completed: found={len(result.get('files', []))}")
            
            return result
            
        except Exception as e:
            logger.error(f"File scan handler failed: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "error_type": type(e).__name__
            }
    
    def _scan_directory(self, path: str, recursive: bool, filter_pattern: str, max_files: int) -> Dict[str, Any]:
        """
        扫描目录
        
        Args:
            path: 目录路径
            recursive: 是否递归
            filter_pattern: 过滤模式
            max_files: 最大文件数
            
        Returns:
            扫描结果
        """
        target_path = Path(path).expanduser().resolve()
        
        if not target_path.exists():
            return {
                "success": False,
                "message": f"Path not found: {path}",
                "files": []
            }
        
        files = []
        directories = []
        truncated = False
        
        try:
            if target_path.is_file():
                # 如果是文件，直接返回文件信息
                if fnmatch.fnmatch(target_path.name, filter_pattern):
                    file_info = self._get_file_info(target_path)
                    files.append(file_info)
            else:
                # 扫描目录
                files, directories, truncated = self._scan_path(
                    target_path, recursive, filter_pattern, max_files
                )
            
            return {
                "success": True,
                "files": files,
                "directories": directories,
                "truncated": truncated,
                "message": f"Found {len(files)} files, {len(directories)} directories"
            }
            
        except PermissionError as e:
            return {
                "success": False,
                "message": f"Permission denied: {str(e)}",
                "files": [],
                "directories": []
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Scan error: {str(e)}",
                "files": [],
                "directories": []
            }
    
    def _scan_path(self, path: Path, recursive: bool, filter_pattern: str, max_files: int) -> tuple:
        """
        递归扫描路径
        
        Returns:
            (files, directories, truncated)
        """
        files = []
        directories = []
        truncated = False
        
        try:
            if recursive:
                # 递归扫描
                for item in path.rglob("*"):
                    if len(files) >= max_files:
                        truncated = True
                        break
                    
                    try:
                        if item.is_file() and fnmatch.fnmatch(item.name, filter_pattern):
                            files.append(self._get_file_info(item))
                        elif item.is_dir():
                            directories.append(self._get_directory_info(item))
                    except (PermissionError, OSError):
                        # 跳过无权限访问的文件/目录
                        continue
            else:
                # 非递归扫描
                for item in path.iterdir():
                    if len(files) >= max_files:
                        truncated = True
                        break
                    
                    try:
                        if item.is_file() and fnmatch.fnmatch(item.name, filter_pattern):
                            files.append(self._get_file_info(item))
                        elif item.is_dir():
                            directories.append(self._get_directory_info(item))
                    except (PermissionError, OSError):
                        # 跳过无权限访问的文件/目录
                        continue
        
        except (PermissionError, OSError) as e:
            logger.warning(f"Error scanning path: {path} - {e}")
        
        return files, directories, truncated
    
    def _get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """获取文件信息"""
        try:
            stat_result = file_path.stat()
            
            return {
                "name": file_path.name,
                "path": str(file_path),
                "size": stat_result.st_size,
                "size_human": self._format_file_size(stat_result.st_size),
                "modified": stat_result.st_mtime,
                "modified_human": self._format_timestamp(stat_result.st_mtime),
                "extension": file_path.suffix,
                "stem": file_path.stem,
                "is_hidden": file_path.name.startswith('.'),
                "permissions": oct(stat_result.st_mode)[-3:],
                "type": "file"
            }
        except OSError as e:
            return {
                "name": file_path.name,
                "path": str(file_path),
                "error": str(e),
                "type": "file"
            }
    
    def _get_directory_info(self, dir_path: Path) -> Dict[str, Any]:
        """获取目录信息"""
        try:
            stat_result = dir_path.stat()
            
            # 尝试计算目录中的文件数量
            try:
                file_count = len(list(dir_path.iterdir()))
            except (PermissionError, OSError):
                file_count = None
            
            return {
                "name": dir_path.name,
                "path": str(dir_path),
                "modified": stat_result.st_mtime,
                "modified_human": self._format_timestamp(stat_result.st_mtime),
                "file_count": file_count,
                "is_hidden": dir_path.name.startswith('.'),
                "permissions": oct(stat_result.st_mode)[-3:],
                "type": "directory"
            }
        except OSError as e:
            return {
                "name": dir_path.name,
                "path": str(dir_path),
                "error": str(e),
                "type": "directory"
            }
    
    def _format_file_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        size = float(size_bytes)
        i = 0
        
        while size >= 1024.0 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
        
        return f"{size:.1f} {size_names[i]}"
    
    def _format_timestamp(self, timestamp: float) -> str:
        """格式化时间戳"""
        from datetime import datetime
        try:
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, OSError):
            return "Unknown"
