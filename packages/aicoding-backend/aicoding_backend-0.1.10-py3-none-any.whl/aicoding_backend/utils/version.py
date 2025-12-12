import json
import os
from pathlib import Path
from typing import Union
import sys

def get_version() -> str:
    """
    获取 package.json 中的版本号
    
    Returns:
        版本号字符串，如果获取失败则返回 '0.0.0'
    """
    try:
        # 获取当前脚本所在目录
        current_file = Path(__file__).resolve()
        module_dir = current_file.parent
        
        # 构建 package.json 路径 (向上三级目录)
        package_json_path = module_dir / "../../../package.json"
        package_json_path = package_json_path.resolve()
        
        # 读取并解析 package.json
        with open(package_json_path, 'r', encoding='utf-8') as f:
            pkg = json.load(f)
        
        print('版本号获取: ', pkg, file=sys.stderr)
        
        # 获取版本号，如果不存在则返回默认值
        package_json_version = pkg.get('version', '0.0.0')
        return package_json_version
        
    except Exception as error:
        print(f"获取版本号失败: {error}", file=sys.stderr)
        return '0.0.0'

# 使用示例
if __name__ == "__main__":
    version = get_version()
    print(f"版本号: {version}")