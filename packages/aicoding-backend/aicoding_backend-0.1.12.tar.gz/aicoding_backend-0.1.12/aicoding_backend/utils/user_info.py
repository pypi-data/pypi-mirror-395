from typing import Dict, Optional
import os

def get_user_info(cwd: Optional[str] = None) -> Dict[str, str]:
    """
    使用 GitPython 获取 Git 用户信息
    """
    try:
        import git
    except ImportError:
        print("GitPython 未安装，运行: pip install GitPython")
        return {'name': 'unknown', 'email': 'unknown', 'cwd': cwd or os.getcwd()}
    
    if cwd is None:
        cwd = os.getcwd()
    
    try:
        # 打开 Git 仓库
        repo = git.Repo(cwd, search_parent_directories=True)
        
        # 获取配置
        config = repo.config_reader()
        
        try:
            name = config.get('user', 'name')
        except (git.exc.ConfigError, ValueError):
            name = 'unknown'
        
        try:
            email = config.get('user', 'email')
        except (git.exc.ConfigError, ValueError):
            email = 'unknown'
        
        print(f"[DataStatistics] 解析用户信息: name={name}, email={email}, cwd={cwd}")
        return {'name': name, 'email': email, 'cwd': cwd}
    
    except Exception as error:
        print(f"获取用户信息失败: {error}")
        return {'name': 'unknown', 'email': 'unknown', 'cwd': cwd}

if __name__ == "__main__":
    user_info = get_user_info("/Users/chenshuren.5/proj/coze-studio")
    print(f"用户名: {user_info['name']}")
    print(f"邮箱: {user_info['email']}")
    print(f"工作目录: {user_info['cwd']}")