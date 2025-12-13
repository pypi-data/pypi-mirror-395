import json
import time
from datetime import datetime
from typing import Any, Dict
import urllib.request
import urllib.error
import sys
from aicoding_backend.utils.user_info import get_user_info  
from aicoding_backend.utils.git_info import get_repository_name  
from aicoding_backend.utils.version import get_version  

def format_datetime() -> str:
    """
    格式化日期时间为 YYYY-MM-DD HH:mm:ss 格式
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def log_data(cwd:str, log_data: Any) -> None:
    """
    上报日志数据
    
    Args:
        log_data: 要上报的日志数据
    """
    try:
        headers = {
            "User-Agent": "TO-CE/1.0.0",
            "Accept": "application/json",
            "Content-Type": "application/json;charset=UTF-8",
        }
        
        # 在方法内部组装 uuid: toolType_时间戳_userName
        timestamp = int(time.time() * 1000)  # 毫秒时间戳
        git_user_info = get_user_info(cwd)
        repo_name = get_repository_name(cwd=cwd)
        version = get_version()
        # 格式化 upTime 为 YYYY-MM-DD HH:mm:ss 格式
        up_time = format_datetime()
        uuid = f"coding_{timestamp}_{git_user_info['name'] or 'unknown'}"
        
        final_log_data = {
            "toolType": "coding",
            "action": "coding_to_backend_log",
            "version": version,
            "ext": json.dumps(log_data, ensure_ascii=False),
            "userName": git_user_info['name'],  # erp
            "userEmail": git_user_info['email'],  # 邮箱
            "repoName": repo_name,  # 仓库名称
            "uuid": uuid,
            "upTime": up_time
        }
        
        
        # 准备请求数据
        json_data = json.dumps(final_log_data, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(
            "http://11.58.76.189/site/aiCoding/reportLog",
            data=json_data,
            headers=headers,
            method="POST"
        )
        
        # 发送请求
        response = urllib.request.urlopen(req)
        
    except urllib.error.URLError as e:
        print(f"log上报失败: {e}", file=sys.stderr)
    except Exception as error:
        print(f"log上报失败: {error}", file=sys.stderr)

# 使用示例
if __name__ == "__main__":
    sample_log_data = {"repoPath": "/path/to/repo", "someKey": "someValue"}
    log_data(cwd="/Users/chenshuren.5/proj/coze-studio", log_data=sample_log_data)