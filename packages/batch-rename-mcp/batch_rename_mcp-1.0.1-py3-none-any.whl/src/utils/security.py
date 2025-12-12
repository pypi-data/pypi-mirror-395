"""
安全验证模块

负责文件操作的安全验证和路径检查
"""

import os
import stat
from pathlib import Path
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class SecurityValidator:
    """安全验证器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.security_settings = config.get("security", {})
        self.general_settings = config.get("settings", {})
        
        # 获取阻止访问的路径
        self.blocked_paths = self.general_settings.get("blocked_paths", [])
        
        # 安全选项
        self.enable_path_validation = self.security_settings.get("enable_path_validation", True)
        self.enable_permission_check = self.security_settings.get("enable_permission_check", True)
        self.max_depth = self.security_settings.get("max_depth", 10)
    
    def validate_path(self, path: str) -> None:
        """
        验证路径安全性
        
        Args:
            path: 要验证的路径
            
        Raises:
            ValueError: 路径不安全时抛出异常
            PermissionError: 权限不足时抛出异常
        """
        if not self.enable_path_validation:
            return
        
        path_obj = Path(path).expanduser().resolve()
        
        # 检查路径是否存在
        if not path_obj.exists():
            raise FileNotFoundError(f"路径不存在: {path}")
        
        # 检查是否在阻止列表中
        self._check_blocked_paths(path_obj)
        
        # 检查路径遍历攻击
        self._check_path_traversal(path_obj)
        
        # 检查权限
        if self.enable_permission_check:
            self._check_permissions(path_obj)
        
        # 检查深度
        self._check_depth(path_obj)
        
        logger.debug(f"路径验证通过: {path_obj}")
    
    def _check_blocked_paths(self, path: Path) -> None:
        """检查是否在阻止路径列表中"""
        path_str = str(path)
        
        for blocked in self.blocked_paths:
            blocked_path = Path(blocked).expanduser().resolve()
            
            # 检查是否是阻止路径或其子路径
            try:
                path.relative_to(blocked_path)
                raise ValueError(f"访问被阻止的路径: {path_str} (阻止: {blocked})")
            except ValueError as e:
                if "访问被阻止的路径" in str(e):
                    raise e
                # relative_to 抛出的正常错误，表示不是子路径，继续检查
                continue
    
    def _check_path_traversal(self, path: Path) -> None:
        """检查路径遍历攻击"""
        path_str = str(path)

        # 检查可疑的路径模式
        suspicious_patterns = [
            "..",
            "~",
        ]

        # 检查路径的各个部分是否包含可疑模式
        for part in path.parts:
            # 检查隐藏文件/目录（除了常见的.DS_Store等）
            if part.startswith('.') and part not in {'.DS_Store', '.gitignore', '.gitkeep'}:
                # 允许用户明确处理隐藏文件，但记录警告
                logger.warning(f"操作隐藏文件/目录: {part} in {path}")

        # 检查是否包含空字节（防止空字节注入）
        if '\x00' in path_str:
            raise ValueError(f"路径包含空字节: {path_str}")

        # 检查路径是否包含Unicode控制字符
        for char in path_str:
            if ord(char) < 32 and char not in {'\t', '\n', '\r'}:
                raise ValueError(f"路径包含控制字符: {repr(char)}")

        # 检查路径长度是否合理
        if len(path_str) > 4096:  # 大多数系统的路径长度限制
            raise ValueError(f"路径过长: {len(path_str)} > 4096")

        # 检查是否试图访问系统关键目录的父目录
        try:
            # 检查是否为系统根目录或接近根目录
            if len(path.parts) <= 2 and path.is_absolute():
                # 对于类似 / 或 /usr 这样的路径要特别小心
                if str(path) in {'/', '/usr', '/bin', '/sbin', '/System', '/private'}:
                    raise ValueError(f"禁止操作系统关键目录: {path}")
        except Exception:
            # 如果路径检查出现异常，为安全起见拒绝操作
            raise ValueError(f"路径验证失败，拒绝操作: {path}")

    
    def _check_permissions(self, path: Path) -> None:
        """检查文件权限"""
        try:
            if path.is_file():
                # 检查文件读写权限
                if not os.access(path, os.R_OK):
                    raise PermissionError(f"没有读取权限: {path}")
                if not os.access(path, os.W_OK):
                    raise PermissionError(f"没有写入权限: {path}")
            elif path.is_dir():
                # 检查目录权限
                if not os.access(path, os.R_OK):
                    raise PermissionError(f"没有读取权限: {path}")
                if not os.access(path, os.W_OK):
                    raise PermissionError(f"没有写入权限: {path}")
                if not os.access(path, os.X_OK):
                    raise PermissionError(f"没有执行权限: {path}")
                    
        except OSError as e:
            raise PermissionError(f"权限检查失败: {path} - {e}")
    
    def _check_depth(self, path: Path) -> None:
        """检查路径深度"""
        parts = path.parts
        if len(parts) > self.max_depth:
            raise ValueError(f"路径深度超过限制: {len(parts)} > {self.max_depth}")
    
    def validate_filename(self, filename: str) -> None:
        """
        验证文件名安全性
        
        Args:
            filename: 文件名
            
        Raises:
            ValueError: 文件名不安全时抛出异常
        """
        if not filename:
            raise ValueError("文件名不能为空")
        
        # 检查长度
        max_length = self.general_settings.get("max_filename_length", 255)
        if len(filename) > max_length:
            raise ValueError(f"文件名过长: {len(filename)} > {max_length}")
        
        # 检查非法字符（Windows和Unix通用）
        illegal_chars = set('<>:"|?*\x00')
        for char in filename:
            if char in illegal_chars:
                raise ValueError(f"文件名包含非法字符: {char}")
        
        # 检查控制字符
        for char in filename:
            if ord(char) < 32:
                raise ValueError(f"文件名包含控制字符: {repr(char)}")
        
        # Windows保留名称检查
        reserved_names = {
            'CON', 'PRN', 'AUX', 'NUL',
            'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
            'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
        }
        
        name_upper = filename.upper()
        # 检查完整名称和不含扩展名的部分
        if name_upper in reserved_names or name_upper.split('.')[0] in reserved_names:
            raise ValueError(f"文件名是Windows保留名称: {filename}")
        
        # 检查以点结尾（Windows不允许）
        if filename.endswith('.'):
            raise ValueError("文件名不能以点结尾")
        
        # 检查以空格开头或结尾
        if filename.startswith(' ') or filename.endswith(' '):
            raise ValueError("文件名不能以空格开头或结尾")
    
    def check_file_access(self, file_path: Path) -> Dict[str, bool]:
        """
        检查文件访问权限
        
        Args:
            file_path: 文件路径
            
        Returns:
            权限字典
        """
        try:
            return {
                "exists": file_path.exists(),
                "readable": os.access(file_path, os.R_OK),
                "writable": os.access(file_path, os.W_OK),
                "executable": os.access(file_path, os.X_OK),
                "is_file": file_path.is_file(),
                "is_dir": file_path.is_dir(),
                "is_symlink": file_path.is_symlink()
            }
        except OSError:
            return {
                "exists": False,
                "readable": False,
                "writable": False,
                "executable": False,
                "is_file": False,
                "is_dir": False,
                "is_symlink": False
            }
    
    def get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """
        获取文件信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件信息字典
        """
        try:
            stat_result = file_path.stat()
            
            return {
                "path": str(file_path),
                "name": file_path.name,
                "size": stat_result.st_size,
                "modified": stat_result.st_mtime,
                "created": stat_result.st_ctime,
                "permissions": oct(stat_result.st_mode)[-3:],
                "owner_uid": stat_result.st_uid,
                "group_gid": stat_result.st_gid,
                "is_file": file_path.is_file(),
                "is_dir": file_path.is_dir(),
                "is_symlink": file_path.is_symlink(),
            }
        except OSError as e:
            return {
                "path": str(file_path),
                "error": str(e)
            }
    
    def validate_operation_safety(self, operation_type: str, file_count: int) -> None:
        """
        验证操作安全性
        
        Args:
            operation_type: 操作类型
            file_count: 文件数量
            
        Raises:
            ValueError: 操作不安全时抛出异常
        """
        # 检查文件数量限制
        max_files = self.general_settings.get("max_files_per_operation", 1000)
        if file_count > max_files:
            raise ValueError(f"操作文件数量超过限制: {file_count} > {max_files}")
        
        # 根据操作类型进行额外检查
        if operation_type == "batch_rename":
            if file_count == 0:
                raise ValueError("没有文件需要重命名")
        
        logger.info(f"操作安全验证通过: {operation_type}, {file_count} 个文件")


class FileUtils:
    """文件操作工具类"""
    
    @staticmethod
    def safe_move(source: Path, destination: Path) -> None:
        """
        安全移动文件
        
        Args:
            source: 源文件路径
            destination: 目标文件路径
        """
        if not source.exists():
            raise FileNotFoundError(f"源文件不存在: {source}")
        
        # 确保目标目录存在
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        # 如果目标文件存在，抛出异常
        if destination.exists():
            raise FileExistsError(f"目标文件已存在: {destination}")
        
        # 执行移动
        source.rename(destination)
    
    @staticmethod
    def safe_copy(source: Path, destination: Path) -> None:
        """
        安全复制文件
        
        Args:
            source: 源文件路径
            destination: 目标文件路径
        """
        import shutil
        
        if not source.exists():
            raise FileNotFoundError(f"源文件不存在: {source}")
        
        # 确保目标目录存在
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        # 执行复制
        shutil.copy2(source, destination)
    
    @staticmethod
    def get_unique_filename(path: Path) -> Path:
        """
        获取唯一的文件名（如果文件已存在则添加序号）
        
        Args:
            path: 原始文件路径
            
        Returns:
            唯一的文件路径
        """
        if not path.exists():
            return path
        
        stem = path.stem
        suffix = path.suffix
        parent = path.parent
        
        counter = 1
        while counter <= 999:
            new_name = f"{stem}_{counter:03d}{suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1
        
        raise ValueError("无法生成唯一文件名，计数器超过限制")
    
    @staticmethod
    def is_safe_extension(filename: str, allowed_extensions: List[str]) -> bool:
        """
        检查文件扩展名是否安全
        
        Args:
            filename: 文件名
            allowed_extensions: 允许的扩展名列表
            
        Returns:
            是否安全
        """
        if "*" in allowed_extensions:
            return True
        
        file_path = Path(filename)
        extension = file_path.suffix.lower()
        
        return extension in [ext.lower() for ext in allowed_extensions]