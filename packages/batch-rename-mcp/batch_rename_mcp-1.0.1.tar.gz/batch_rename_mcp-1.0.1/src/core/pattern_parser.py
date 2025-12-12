"""
重命名模式解析器

负责解析和应用各种重命名模式
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class PatternParser:
    """重命名模式解析器"""
    
    def __init__(self):
        self.counter = 1
        self.variables = {
            'counter': self._get_counter,
            'date': self._get_date,
            'time': self._get_time,
            'name': None,  # 由外部设置
            'ext': None,   # 由外部设置
        }
        
    def parse_pattern(self, pattern: str, file_path: Path, counter: int = None) -> str:
        """
        解析重命名模式并生成新的文件名
        
        Args:
            pattern: 重命名模式
            file_path: 原文件路径
            counter: 计数器值（可选）
            
        Returns:
            新的文件名
        """
        if counter is not None:
            self.counter = counter
            
        # 获取文件信息
        file_stem = file_path.stem
        file_ext = file_path.suffix
        
        # 更新变量
        self.variables['name'] = file_stem
        self.variables['ext'] = file_ext.lstrip('.')
        
        # 检查模式类型
        if pattern.startswith('regex:'):
            return self._parse_regex_pattern(pattern, str(file_path.name))
        elif '{' in pattern and '}' in pattern:
            return self._parse_template_pattern(pattern)
        else:
            return self._parse_simple_pattern(pattern, file_stem, file_ext)
    
    def _parse_template_pattern(self, pattern: str) -> str:
        """解析模板变量模式"""
        result = pattern
        
        # 获取原始扩展名
        original_ext = self.variables.get('ext', '')
        
        # 查找所有变量引用
        var_matches = re.findall(r'{([^}]+)}', pattern)
        
        for var_match in var_matches:
            # 检查是否有格式化选项
            if ':' in var_match:
                var_name, format_spec = var_match.split(':', 1)
            else:
                var_name = var_match
                format_spec = None
            
            # 获取变量值
            if var_name in self.variables:
                if callable(self.variables[var_name]):
                    value = self.variables[var_name]()
                else:
                    value = self.variables[var_name]
                
                # 应用格式化
                if format_spec and var_name == 'counter':
                    if format_spec.endswith('d'):
                        # 处理格式如 02d, 03d 等
                        if len(format_spec) > 1 and format_spec[0] == '0':
                            width = int(format_spec[1:-1])
                            value = str(value).zfill(width)
                        else:
                            value = str(value)
                    elif format_spec.isdigit():
                        # 处理纯数字格式如 02, 03
                        width = int(format_spec)
                        if width > 1:
                            value = str(value).zfill(width)
                        else:
                            value = str(value)
                    else:
                        value = str(value)
                
                # 替换变量
                result = result.replace('{' + var_match + '}', str(value))
            else:
                # 未知变量，保持原样
                pass
        
        # 如果结果不包含扩展名且原文件有扩展名，则添加扩展名
        if original_ext and not result.endswith('.' + original_ext):
            result += '.' + original_ext
            
        return result
    
    def _parse_regex_pattern(self, pattern: str, filename: str) -> str:
        """解析正则表达式模式"""
        # 格式: regex:pattern:replacement 或 regex:pattern:replacement:flags
        parts = pattern.split(':', 3)
        if len(parts) < 3:
            raise ValueError("正则表达式模式格式错误，应为 'regex:pattern:replacement' 或 'regex:pattern:replacement:flags'")

        _, regex_pattern, replacement = parts[0], parts[1], parts[2]
        flags = 0

        # 处理可选的标志位
        if len(parts) == 4:
            flag_str = parts[3].lower()
            if 'i' in flag_str:  # 忽略大小写
                flags |= re.IGNORECASE
            if 'm' in flag_str:  # 多行模式
                flags |= re.MULTILINE
            if 's' in flag_str:  # 单行模式（.匹配换行符）
                flags |= re.DOTALL

        try:
            # 应用正则表达式替换
            result = re.sub(regex_pattern, replacement, filename, flags=flags)

            # 验证结果不为空
            if not result.strip():
                raise ValueError(f"正则表达式替换结果为空文件名: '{filename}' -> '{result}'")

            return result
        except re.error as e:
            raise ValueError(f"正则表达式错误: {e}")
        except Exception as e:
            raise ValueError(f"正则表达式处理失败: {e}")
    
    def _parse_simple_pattern(self, pattern: str, file_stem: str, file_ext: str) -> str:
        """解析简单替换模式"""
        # 支持大小写转换
        if pattern.startswith('upper:'):
            base_pattern = pattern[6:]
            if base_pattern == '{name}':
                return file_stem.upper() + file_ext
            else:
                return base_pattern.upper() + file_ext
        elif pattern.startswith('lower:'):
            base_pattern = pattern[6:]
            if base_pattern == '{name}':
                return file_stem.lower() + file_ext
            else:
                return base_pattern.lower() + file_ext
        elif pattern.startswith('title:'):
            base_pattern = pattern[6:]
            if base_pattern == '{name}':
                return file_stem.title() + file_ext
            else:
                return base_pattern.title() + file_ext
        else:
            # 简单字符串，直接添加扩展名
            if not pattern.endswith(file_ext) and file_ext:
                return pattern + file_ext
            return pattern
    
    def _get_counter(self) -> int:
        """获取并递增计数器"""
        value = self.counter
        self.counter += 1
        return value
    
    def _get_date(self) -> str:
        """获取当前日期 YYYYMMDD"""
        return datetime.now().strftime('%Y%m%d')
    
    def _get_time(self) -> str:
        """获取当前时间 HHMMSS"""
        return datetime.now().strftime('%H%M%S')
    
    def reset_counter(self, start_value: int = 1) -> None:
        """重置计数器"""
        self.counter = start_value
    
    def preview_batch(self, pattern: str, file_paths: List[Path]) -> List[Dict[str, str]]:
        """
        批量预览重命名结果
        
        Args:
            pattern: 重命名模式
            file_paths: 文件路径列表
            
        Returns:
            预览结果列表，包含原文件名和新文件名
        """
        self.reset_counter()
        results = []
        
        for i, file_path in enumerate(file_paths, 1):
            try:
                new_name = self.parse_pattern(pattern, file_path, counter=i)
                results.append({
                    'original': str(file_path.name),
                    'new_name': new_name,
                    'status': 'ok'
                })
            except Exception as e:
                results.append({
                    'original': str(file_path.name),
                    'new_name': '',
                    'status': 'error',
                    'error': str(e)
                })
        
        return results
    
    @staticmethod
    def get_available_variables() -> Dict[str, str]:
        """获取可用的模板变量说明"""
        return {
            '{name}': '原文件名（不含扩展名）',
            '{ext}': '文件扩展名',
            '{counter}': '自动递增序号',
            '{counter:03d}': '零填充的3位序号',
            '{date}': '当前日期 (YYYYMMDD)',
            '{time}': '当前时间 (HHMMSS)',
        }
    
    @staticmethod
    def get_pattern_examples() -> List[Dict[str, str]]:
        """获取模式示例"""
        return [
            {
                'pattern': '新文件_{counter:03d}',
                'input': 'old.txt',
                'output': '新文件_001.txt',
                'description': '序号重命名'
            },
            {
                'pattern': 'prefix_{name}',
                'input': 'photo.jpg',
                'output': 'prefix_photo.jpg',
                'description': '添加前缀'
            },
            {
                'pattern': '{name}_backup',
                'input': 'doc.pdf',
                'output': 'doc_backup.pdf',
                'description': '添加后缀'
            },
            {
                'pattern': 'IMG_{date}_{counter}',
                'input': 'image.png',
                'output': 'IMG_20240919_001.png',
                'description': '日期加序号'
            },
            # 正则表达式示例
            {
                'pattern': 'regex:^test:fjc1',
                'input': 'test_image.jpg',
                'output': 'fjc1_image.jpg',
                'description': '将test开头替换为fjc1开头'
            },
            {
                'pattern': 'regex:IMG_(\\d+):PHOTO_$1',
                'input': 'IMG_123.jpg',
                'output': 'PHOTO_123.jpg',
                'description': '正则表达式替换并保留数字'
            },
            {
                'pattern': 'regex:^(.+)_old$:$1_new',
                'input': 'document_old.pdf',
                'output': 'document_new.pdf',
                'description': '将_old后缀替换为_new'
            },
            {
                'pattern': 'regex:(\\d{4})(\\d{2})(\\d{2}):$1-$2-$3',
                'input': '20240919_photo.jpg',
                'output': '2024-09-19_photo.jpg',
                'description': '格式化日期（YYYYMMDD -> YYYY-MM-DD）'
            },
            {
                'pattern': 'regex:test:fjc1:i',
                'input': 'TEST_file.txt',
                'output': 'fjc1_file.txt',
                'description': '忽略大小写替换test为fjc1'
            },
            # 大小写转换示例
            {
                'pattern': 'upper:{name}',
                'input': 'file.txt',
                'output': 'FILE.TXT',
                'description': '转为大写'
            },
            {
                'pattern': 'lower:{name}',
                'input': 'FILE.TXT',
                'output': 'file.txt',
                'description': '转为小写'
            },
            {
                'pattern': 'title:{name}',
                'input': 'my document.pdf',
                'output': 'My Document.pdf',
                'description': '转为标题格式'
            }
        ]
