"""
模板占位符替换工具 / Template placeholder replacement utility
基于 TypeScript 版本的 generatePrompt 函数移植
Ported from TypeScript version of generatePrompt function
"""

import re
from typing import Dict, Any, Optional


def generate_prompt(
    prompt_template: str,
    params: Optional[Dict[str, Any]] = None
) -> str:
    """
    生成带有占位符替换的 prompt
    Generate prompt with placeholder replacement
    
    使用简单的模板替换方法，将 {paramName} 替换为对应的参数值
    Use simple template replacement method to replace {paramName} with corresponding parameter values
    
    Args:
        prompt_template (str): 包含占位符的模板字符串 / Template string containing placeholders
        params (Optional[Dict[str, Any]]): 参数字典 / Parameter dictionary
        
    Returns:
        str: 替换后的字符串 / String after replacement
        
    Examples:
        >>> template = "Hello {name}, you are {age} years old!"
        >>> params = {"name": "Alice", "age": 25}
        >>> generate_prompt(template, params)
        'Hello Alice, you are 25 years old!'
        
        >>> template = "Welcome {user}! Status: {status}"
        >>> params = {"user": "Bob"}  # missing 'status'
        >>> generate_prompt(template, params)
        'Welcome Bob! Status: '
    """
    # 如果没有提供参数，使用空字典
    # If no parameters provided, use empty dictionary
    if params is None:
        params = {}
    
    result = prompt_template
    
    # 遍历所有参数进行替换
    # Iterate through all parameters for replacement
    for key, value in params.items():
        # 如果值为 None 或 undefined，使用空字符串替换
        # If value is None or undefined, replace with empty string
        replacement_value = "" if value is None else str(value)
        
        # 使用正则表达式替换所有匹配的占位符
        # Use regular expression to replace all matching placeholders
        placeholder_pattern = re.compile(rf'\{{{re.escape(key)}\}}')
        result = placeholder_pattern.sub(replacement_value, result)
    
    return result


def generate_prompt_safe(
    prompt_template: str,
    params: Optional[Dict[str, Any]] = None,
    strict: bool = False
) -> str:
    """
    安全的 prompt 生成函数，支持严格模式
    Safe prompt generation function with strict mode support
    
    Args:
        prompt_template (str): 模板字符串 / Template string
        params (Optional[Dict[str, Any]]): 参数字典 / Parameter dictionary
        strict (bool): 严格模式，如果为 True 且存在未替换的占位符则抛出异常
                      Strict mode, raise exception if unmatched placeholders exist
                      
    Returns:
        str: 替换后的字符串 / String after replacement
        
    Raises:
        ValueError: 当严格模式下存在未替换的占位符时
                   When unmatched placeholders exist in strict mode
    """
    result = generate_prompt(prompt_template, params)
    
    if strict:
        # 检查是否还有未替换的占位符
        # Check if there are still unmatched placeholders
        unmatched_placeholders = re.findall(r'\{[^}]+\}', result)
        if unmatched_placeholders:
            raise ValueError(
                f"未替换的占位符 / Unmatched placeholders: {unmatched_placeholders}"
            )
    
    return result


def extract_placeholders(template: str) -> list[str]:
    """
    从模板中提取所有占位符名称
    Extract all placeholder names from template
    
    Args:
        template (str): 模板字符串 / Template string
        
    Returns:
        list[str]: 占位符名称列表 / List of placeholder names
        
    Examples:
        >>> template = "Hello {name}, you have {count} messages from {sender}!"
        >>> extract_placeholders(template)
        ['name', 'count', 'sender']
    """
    placeholders = re.findall(r'\{([^}]+)\}', template)
    return list(set(placeholders))  # 去重 / Remove duplicates


def validate_template_params(
    template: str,
    params: Dict[str, Any]
) -> Dict[str, list[str]]:
    """
    验证模板参数的完整性
    Validate template parameter completeness
    
    Args:
        template (str): 模板字符串 / Template string
        params (Dict[str, Any]): 参数字典 / Parameter dictionary
        
    Returns:
        Dict[str, list[str]]: 验证结果，包含 'missing' 和 'unused' 键
                             Validation result with 'missing' and 'unused' keys
    """
    required_placeholders = set(extract_placeholders(template))
    provided_params = set(params.keys())
    
    missing = list(required_placeholders - provided_params)
    unused = list(provided_params - required_placeholders)
    
    return {
        'missing': missing,  # 缺失的参数 / Missing parameters
        'unused': unused     # 未使用的参数 / Unused parameters
    }


# 异步版本 / Async version
async def generate_prompt_async(
    prompt_template: str,
    params: Optional[Dict[str, Any]] = None
) -> str:
    """
    异步版本的 prompt 生成函数
    Async version of prompt generation function
    
    Args:
        prompt_template (str): 模板字符串 / Template string
        params (Optional[Dict[str, Any]]): 参数字典 / Parameter dictionary
        
    Returns:
        str: 替换后的字符串 / String after replacement
    """
    # 对于简单的字符串操作，异步版本与同步版本相同
    # For simple string operations, async version is same as sync version
    return generate_prompt(prompt_template, params)


# 为了保持与 TypeScript 版本的命名一致性，提供别名
# Provide alias for consistency with TypeScript version naming
generatePrompt = generate_prompt