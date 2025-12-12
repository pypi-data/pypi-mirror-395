"""
配置加载器模块

负责加载和管理MCP服务器配置
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

from .paths import MCPPaths


class ConfigLoader:
    """配置加载器"""
    
    DEFAULT_CONFIG = {
        "name": "batch-rename-mcp",
        "version": "1.0.0",
        "description": "批量文件重命名MCP服务器",
        "settings": {
            "max_files_per_operation": 1000,
            "log_retention_days": 30,
            "allowed_extensions": ["*"],
            "blocked_paths": ["/System", "/usr", "/bin", "/sbin", "/private"],
            "auto_backup": True,
            "operation_log_path": str(MCPPaths.get_logs_dir()),
            "max_filename_length": 255,
            "allowed_pattern_types": ["template", "regex", "simple"]
        },
        "security": {
            "enable_path_validation": True,
            "enable_permission_check": True,
            "max_depth": 10,
            "require_confirmation": True
        },
        "paths": {
            "config_dir": str(MCPPaths.get_config_dir()),
            "logs_dir": str(MCPPaths.get_logs_dir()),
            "data_dir": str(MCPPaths.get_data_dir()),
            "temp_dir": str(MCPPaths.get_temp_dir())
        }
    }
    
    @classmethod
    def load_config(cls, config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        加载配置文件
        
        Args:
            config_path: 配置文件路径，如果为None则使用默认配置
            
        Returns:
            配置字典
        """
        # 确保目录存在
        MCPPaths.ensure_directories()
        
        if config_path is None:
            # 优先使用新的标准配置路径
            standard_config = MCPPaths.get_config_file_path()
            if standard_config.exists():
                config_path = str(standard_config)
            else:
                # 尝试查找旧的配置文件（向后兼容）
                legacy_paths = MCPPaths.get_legacy_config_paths()
                for path in legacy_paths:
                    if path.exists():
                        config_path = str(path)
                        # 尝试迁移旧配置文件
                        try:
                            import shutil
                            shutil.copy2(path, standard_config)
                            print(f"配置文件已迁移: {path} -> {standard_config}")
                            config_path = str(standard_config)
                        except Exception as e:
                            print(f"配置文件迁移失败: {e}")
                        break
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                # 合并默认配置和用户配置
                merged_config = cls._merge_configs(cls.DEFAULT_CONFIG, config)
                
                # 确保路径信息是最新的
                merged_config['paths'] = {
                    "config_dir": str(MCPPaths.get_config_dir()),
                    "logs_dir": str(MCPPaths.get_logs_dir()),
                    "data_dir": str(MCPPaths.get_data_dir()),
                    "temp_dir": str(MCPPaths.get_temp_dir())
                }
                
                return merged_config
                    
            except (json.JSONDecodeError, IOError) as e:
                print(f"配置文件加载失败，使用默认配置: {e}")
                
        return cls.DEFAULT_CONFIG.copy()
    
    @classmethod
    def _merge_configs(cls, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """
        合并默认配置和用户配置
        
        Args:
            default: 默认配置
            user: 用户配置
            
        Returns:
            合并后的配置
        """
        result = default.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = cls._merge_configs(result[key], value)
            else:
                result[key] = value
                
        return result
    
    @classmethod
    def validate_config(cls, config: Dict[str, Any]) -> bool:
        """
        验证配置文件的有效性
        
        Args:
            config: 配置字典
            
        Returns:
            配置是否有效
        """
        required_keys = ["name", "settings"]
        
        for key in required_keys:
            if key not in config:
                return False
                
        # 验证设置项
        settings = config.get("settings", {})
        if not isinstance(settings.get("max_files_per_operation"), int):
            return False
            
        if settings.get("max_files_per_operation", 0) <= 0:
            return False
            
        return True