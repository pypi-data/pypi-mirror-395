import subprocess
import os
import re
from typing import Optional

def get_repository_name(cwd: Optional[str] = None) -> str:
    """
    获取 Git 仓库名称
    
    Args:
        cwd: 工作目录，默认为当前目录或环境变量指定的目录
        
    Returns:
        仓库名称，如果获取失败则返回 'unknown'
    """
    # 确定工作目录
    working_dir = (
        cwd or 
        os.environ.get('PWD') or 
        os.environ.get('REPO_PATH') or 
        os.getcwd()
    )
    
    try:
        # 执行 git 命令获取远程仓库 URL
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            cwd=working_dir,
            capture_output=True,
            text=True,
            check=True
        )
        
        remote_url = result.stdout.strip()
        
        # 使用正则表达式提取仓库名称
        # 支持 HTTPS 和 SSH 格式
        # https://github.com/user/repo.git   -> repo
        # git@github.com:user/repo.git -> repo
        match = re.search(r'/([^/]+?)(?:\.git)?$', remote_url)
        
        if match:
            return match.group(1)
        else:
            return 'unknown'
            
    except subprocess.CalledProcessError as error:
        print(f"获取仓库名称失败: {error}")
        return 'unknown'
    except Exception as error:
        print(f"获取仓库名称失败: {error}")
        return 'unknown'

# 使用示例
if __name__ == "__main__":
    repo_name = get_repository_name()
    print(f"仓库名称: {repo_name}")