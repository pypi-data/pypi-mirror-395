"""
路径管理模块

提供统一的 MCP 持久化文件路径管理功能
"""

import os
from pathlib import Path
from typing import Optional


class MCPPaths:
    """MCP 路径管理器"""
    
    MCP_DIR_NAME = ".mcp"
    PROJECT_DIR_NAME = "batch-rename-mcp"
    
    @classmethod
    def get_mcp_base_dir(cls) -> Path:
        """
        获取 MCP 基础目录路径
        
        返回: ~/.mcp/
        """
        return Path.home() / cls.MCP_DIR_NAME
    
    @classmethod
    def get_project_dir(cls) -> Path:
        """
        获取项目专用目录路径
        
        返回: ~/.mcp/batch-rename-mcp/
        """
        return cls.get_mcp_base_dir() / cls.PROJECT_DIR_NAME
    
    @classmethod
    def get_config_dir(cls) -> Path:
        """
        获取配置文件目录
        
        返回: ~/.mcp/batch-rename-mcp/config/
        """
        return cls.get_project_dir() / "config"
    
    @classmethod
    def get_logs_dir(cls) -> Path:
        """
        获取日志文件目录
        
        返回: ~/.mcp/batch-rename-mcp/logs/
        """
        return cls.get_project_dir() / "logs"
    
    @classmethod
    def get_data_dir(cls) -> Path:
        """
        获取数据文件目录
        
        返回: ~/.mcp/batch-rename-mcp/data/
        """
        return cls.get_project_dir() / "data"
    
    @classmethod
    def get_temp_dir(cls) -> Path:
        """
        获取临时文件目录
        
        返回: ~/.mcp/batch-rename-mcp/temp/
        """
        return cls.get_project_dir() / "temp"
    
    @classmethod
    def get_operation_log_path(cls) -> Path:
        """
        获取操作日志文件路径
        
        返回: ~/.mcp/batch-rename-mcp/logs/operations.json
        """
        return cls.get_logs_dir() / "operations.json"
    
    @classmethod
    def get_config_file_path(cls, config_name: str = "config.json") -> Path:
        """
        获取配置文件路径
        
        Args:
            config_name: 配置文件名，默认为 config.json
            
        返回: ~/.mcp/batch-rename-mcp/config/{config_name}
        """
        return cls.get_config_dir() / config_name
    
    @classmethod
    def ensure_directories(cls) -> None:
        """
        确保所有必要目录存在
        """
        directories = [
            cls.get_mcp_base_dir(),
            cls.get_project_dir(),
            cls.get_config_dir(),
            cls.get_logs_dir(),
            cls.get_data_dir(),
            cls.get_temp_dir(),
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_legacy_config_paths(cls) -> list[Path]:
        """
        获取遗留配置文件可能的路径列表（用于兼容性）
        
        返回: 可能的配置文件路径列表
        """
        return [
            Path("mcp_config.json"),
            Path("./mcp_config.json"),
            Path("../mcp_config.json"),
            Path.home() / ".batch_rename_mcp" / "config.json",  # 旧版本路径
        ]
    
    @classmethod
    def migrate_legacy_files(cls) -> dict[str, str]:
        """
        迁移遗留文件到新的路径结构
        
        返回: 迁移结果字典
        """
        results = {}
        
        # 确保新目录存在
        cls.ensure_directories()
        
        # 迁移配置文件
        for legacy_config in cls.get_legacy_config_paths():
            if legacy_config.exists():
                new_config_path = cls.get_config_file_path()
                if not new_config_path.exists():
                    try:
                        import shutil
                        shutil.copy2(legacy_config, new_config_path)
                        results[f"config_from_{legacy_config}"] = f"迁移成功 -> {new_config_path}"
                    except Exception as e:
                        results[f"config_from_{legacy_config}"] = f"迁移失败: {e}"
                break
        
        # 迁移操作日志
        legacy_log_paths = [
            Path("./operation_logs/operations.json"),
            Path("../operation_logs/operations.json"),
            Path("operation_logs/operations.json"),
        ]
        
        for legacy_log in legacy_log_paths:
            if legacy_log.exists():
                new_log_path = cls.get_operation_log_path()
                if not new_log_path.exists():
                    try:
                        import shutil
                        shutil.copy2(legacy_log, new_log_path)
                        results[f"log_from_{legacy_log}"] = f"迁移成功 -> {new_log_path}"
                        
                        # 也复制备份文件（如果存在）
                        legacy_backup = legacy_log.with_suffix('.json.bak')
                        if legacy_backup.exists():
                            new_backup = new_log_path.with_suffix('.json.bak')
                            shutil.copy2(legacy_backup, new_backup)
                            results[f"backup_from_{legacy_backup}"] = f"迁移成功 -> {new_backup}"
                            
                    except Exception as e:
                        results[f"log_from_{legacy_log}"] = f"迁移失败: {e}"
                break
        
        return results
    
    @classmethod
    def get_path_info(cls) -> dict[str, str]:
        """
        获取路径信息（用于调试和显示）
        
        返回: 包含各种路径信息的字典
        """
        cls.ensure_directories()
        
        return {
            "mcp_base_dir": str(cls.get_mcp_base_dir()),
            "project_dir": str(cls.get_project_dir()),
            "config_dir": str(cls.get_config_dir()),
            "logs_dir": str(cls.get_logs_dir()),
            "data_dir": str(cls.get_data_dir()),
            "temp_dir": str(cls.get_temp_dir()),
            "operation_log_file": str(cls.get_operation_log_path()),
            "config_file": str(cls.get_config_file_path()),
        }