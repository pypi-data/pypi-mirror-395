"""
Prompt loader utility module
负责加载和处理 prompt 模板
Responsible for loading and processing prompt templates
"""

import os
from typing import Optional


def load_prompt(base_template: str, env_var_name: str) -> str:
    """
    加载 prompt 模板，支持通过环境变量覆盖或追加
    Load prompt template with support for environment variable override or append
    
    Args:
        base_template: 基础模板内容 / Base template content
        env_var_name: 环境变量名称 / Environment variable name
        
    Returns:
        str: 最终的 prompt 内容 / Final prompt content
    """
    # 获取环境变量中的自定义 prompt
    # Get custom prompt from environment variable
    custom_prompt = os.getenv(env_var_name)
    
    if custom_prompt:
        # 如果环境变量存在，可以选择覆盖或追加
        # If environment variable exists, can choose to override or append
        return custom_prompt
    
    # 返回基础模板
    # Return base template
    return base_template