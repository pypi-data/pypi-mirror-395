"""
文件读取工具模块
File reading utility module
"""

import os
from pathlib import Path
from typing import Union, Optional, List


async def read_file(file_path: Union[str, Path], filename: Optional[str] = None, encoding: str = 'utf-8') -> str:
    """
    读取文件内容
    Read file content
    
    Args:
        file_path: 文件路径或目录路径 / File path or directory path
        filename: 文件名（可选，当file_path为目录时使用） / Filename (optional, used when file_path is directory)
        encoding: 文件编码，默认utf-8 / File encoding, default utf-8
        
    Returns:
        str: 文件内容 / File content
        
    Raises:
        FileNotFoundError: 文件不存在 / File not found
        PermissionError: 权限不足 / Permission denied
        UnicodeDecodeError: 编码错误 / Encoding error
        
    Examples:
        # 直接传入完整文件路径 / Pass complete file path directly
        content = read_file('/path/to/file.txt')
        
        # 分别传入路径和文件名 / Pass path and filename separately
        content = read_file('/path/to', 'file.txt')
        
        # 使用Path对象 / Use Path object
        content = read_file(Path('/path/to/file.txt'))
    """
    # 处理路径参数 / Handle path parameters
    if filename is not None:
        # 如果提供了filename，则将其与file_path组合
        # If filename is provided, combine it with file_path
        full_path = Path(file_path) / filename
    else:
        # 否则直接使用file_path
        # Otherwise use file_path directly
        full_path = Path(file_path)
    
    # 检查文件是否存在 / Check if file exists
    if not full_path.exists():
        raise FileNotFoundError(f"文件不存在 / File not found: {full_path}")
    
    # 检查是否为文件（而非目录） / Check if it's a file (not directory)
    if not full_path.is_file():
        raise ValueError(f"路径不是文件 / Path is not a file: {full_path}")
    
    try:
        # 读取文件内容 / Read file content
        with open(full_path, 'r', encoding=encoding) as file:
            content = file.read()
        return content
    except PermissionError:
        raise PermissionError(f"权限不足，无法读取文件 / Permission denied to read file: {full_path}")
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(
            e.encoding, e.object, e.start, e.end,
            f"编码错误，无法使用 {encoding} 编码读取文件 / Encoding error, cannot read file with {encoding} encoding: {full_path}"
        )


async def read_file_lines(file_path: Union[str, Path], filename: Optional[str] = None,
                   encoding: str = 'utf-8', strip_newlines: bool = True) -> List[str]:
    """
    按行读取文件内容
    Read file content line by line
    
    Args:
        file_path: 文件路径或目录路径 / File path or directory path
        filename: 文件名（可选） / Filename (optional)
        encoding: 文件编码 / File encoding
        strip_newlines: 是否去除行尾换行符 / Whether to strip newlines
        
    Returns:
        List[str]: 文件行列表 / List of file lines
    """
    content = await read_file(file_path, filename, encoding)
    lines = content.splitlines() if strip_newlines else content.split('\n')
    return lines


async def read_file_safe(file_path: Union[str, Path], filename: Optional[str] = None,
                  encoding: str = 'utf-8', default: str = '') -> str:
    """
    安全读取文件，出错时返回默认值
    Safe file reading, returns default value on error
    
    Args:
        file_path: 文件路径或目录路径 / File path or directory path
        filename: 文件名（可选） / Filename (optional)
        encoding: 文件编码 / File encoding
        default: 默认返回值 / Default return value
        
    Returns:
        str: 文件内容或默认值 / File content or default value
    """
    try:
        return await read_file(file_path, filename, encoding)
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, ValueError):
        return default


def file_exists(file_path: Union[str, Path], filename: Optional[str] = None) -> bool:
    """
    检查文件是否存在
    Check if file exists
    
    Args:
        file_path: 文件路径或目录路径 / File path or directory path
        filename: 文件名（可选） / Filename (optional)
        
    Returns:
        bool: 文件是否存在 / Whether file exists
    """
    if filename is not None:
        full_path = Path(file_path) / filename
    else:
        full_path = Path(file_path)
    
    return full_path.exists() and full_path.is_file()


def get_file_info(file_path: Union[str, Path], filename: Optional[str] = None) -> dict:
    """
    获取文件信息
    Get file information
    
    Args:
        file_path: 文件路径或目录路径 / File path or directory path
        filename: 文件名（可选） / Filename (optional)
        
    Returns:
        dict: 文件信息字典 / File information dictionary
        
    Raises:
        FileNotFoundError: 文件不存在 / File not found
    """
    if filename is not None:
        full_path = Path(file_path) / filename
    else:
        full_path = Path(file_path)
    
    if not full_path.exists():
        raise FileNotFoundError(f"文件不存在 / File not found: {full_path}")
    
    stat = full_path.stat()
    
    return {
        'path': str(full_path.absolute()),
        'name': full_path.name,
        'size': stat.st_size,
        'created': stat.st_ctime,
        'modified': stat.st_mtime,
        'is_file': full_path.is_file(),
        'is_dir': full_path.is_dir(),
        'suffix': full_path.suffix,
        'parent': str(full_path.parent)
    }