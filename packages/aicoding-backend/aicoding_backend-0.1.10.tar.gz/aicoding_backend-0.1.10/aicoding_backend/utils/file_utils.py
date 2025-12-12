"""
文件操作工具模块
提供常用的文件和目录操作功能
"""
import os
from pathlib import Path
from typing import Union


def file_exists(file_path: Union[str, Path]) -> bool:
    """
    检查文件是否存在
    
    Args:
        file_path: 文件路径，可以是字符串或Path对象
        
    Returns:
        bool: 如果文件存在返回True，否则返回False
        
    Examples:
        >>> file_exists("test.txt")
        True
        >>> file_exists("/path/to/nonexistent.txt")
        False
    """
    try:
        path = Path(file_path)
        return path.exists() and path.is_file()
    except (OSError, ValueError):
        return False


def dir_exists(dir_path: Union[str, Path]) -> bool:
    """
    检查目录是否存在
    
    Args:
        dir_path: 目录路径，可以是字符串或Path对象
        
    Returns:
        bool: 如果目录存在返回True，否则返回False
    """
    try:
        path = Path(dir_path)
        return path.exists() and path.is_dir()
    except (OSError, ValueError):
        return False


def ensure_dir(dir_path: Union[str, Path]) -> bool:
    """
    确保目录存在，如果不存在则创建
    
    Args:
        dir_path: 目录路径
        
    Returns:
        bool: 成功返回True，失败返回False
    """
    try:
        path = Path(dir_path)
        path.mkdir(parents=True, exist_ok=True)
        return True
    except (OSError, ValueError):
        return False


def get_file_size(file_path: Union[str, Path]) -> int:
    """
    获取文件大小（字节）
    
    Args:
        file_path: 文件路径
        
    Returns:
        int: 文件大小，如果文件不存在返回-1
    """
    try:
        path = Path(file_path)
        if path.exists() and path.is_file():
            return path.stat().st_size
        return -1
    except (OSError, ValueError):
        return -1
    

if __name__=="__main__":
    print(dir_exists("/Users/chenshuren.5/proj/trade-operations-agent"))