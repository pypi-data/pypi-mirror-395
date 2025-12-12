"""
初始化项目规范 MCP 工具
Initialize project specification MCP tool
对应 TypeScript 版本的 Python 实现
Python implementation corresponding to TypeScript version
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import json
from pydantic import BaseModel, Field

from ..prompts.init_project_rules import get_init_project_rules_prompt


class InitProjectRulesSchema(BaseModel):
    """
    初始化项目规范工具的输入参数模式
    Input parameter schema for init project rules tool
    对应 TypeScript 中的 z.object({})
    Corresponds to z.object({}) in TypeScript
    """
    pass  # 空模式，不需要输入参数 / Empty schema, no input parameters needed


@dataclass
class ToolContent:
    """
    工具响应内容结构
    Tool response content structure
    """
    type: str
    text: str


@dataclass
class ToolResponse:
    """
    工具响应结构
    Tool response structure
    """
    content: List[ToolContent]


# 工具配置对象 / Tool configuration object
# 对应 TypeScript 中的 initProjectRulesTool
# Corresponds to initProjectRulesTool in TypeScript
INIT_PROJECT_RULES_TOOL = {
    "name": "init_project_rules",
    "description": "初始化项目规范工具函数",
    # "description": "Initialize project specification tool function",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "additionalProperties": False
    },
}


async def handle_init_project_rules(arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    初始化项目规范工具函数
    Initialize project specification tool function
    提供建立规范文件的指导
    Provide guidance for creating specification documents
    
    Args:
        arguments: 输入参数（当前为空）/ Input arguments (currently empty)
        
    Returns:
        Dict[str, Any]: MCP 标准响应格式 / MCP standard response format
    """
    try:
        # 验证输入参数 / Validate input arguments
        if arguments is None:
            arguments = {}
            
        # 使用 Pydantic 验证参数 / Validate parameters using Pydantic
        schema = InitProjectRulesSchema(**arguments)
        
        # 从生成器获取提示词 / Get prompt from generator
        prompt_content = await get_init_project_rules_prompt()
        
        # 返回成功响应 / Return success response
        return {
            "content": [
                {
                    "type": "text",
                    "text": prompt_content,
                }
            ],
        }
        
    except Exception as error:
        # 错误处理 / Error handling
        error_message = str(error) if error else "未知错误"
        # Unknown error
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"初始化项目规范时发生错误: {error_message}",
                    # Error occurred during project specification initialization: {error_message}
                }
            ],
        }


def handle_init_project_rules_sync(arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    同步版本的工具处理函数
    Synchronous version of the tool handler function
    
    Args:
        arguments: 输入参数（当前为空）/ Input arguments (currently empty)
        
    Returns:
        Dict[str, Any]: MCP 标准响应格式 / MCP standard response format
    """
    import asyncio
    
    try:
        # 尝试获取当前事件循环
        # Try to get current event loop
        loop = asyncio.get_running_loop()
        # 如果已经在事件循环中，直接同步执行
        # If already in event loop, execute synchronously
        return _handle_init_project_rules_sync_internal(arguments)
    except RuntimeError:
        # 如果没有运行的事件循环，使用 asyncio.run
        # If no running event loop, use asyncio.run
        return asyncio.run(handle_init_project_rules(arguments))


def _handle_init_project_rules_sync_internal(arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    内部同步实现，避免事件循环冲突
    Internal sync implementation to avoid event loop conflicts
    """
    try:
        # 验证输入参数 / Validate input arguments
        if arguments is None:
            arguments = {}
            
        # 使用 Pydantic 验证参数 / Validate parameters using Pydantic
        schema = InitProjectRulesSchema(**arguments)
        
        # 直接调用同步版本的 prompt 生成器
        # Directly call sync version of prompt generator
        from ..prompts.init_project_rules import get_init_project_rules_prompt_sync
        prompt_content = get_init_project_rules_prompt_sync()
        
        # 返回成功响应 / Return success response
        return {
            "content": [
                {
                    "type": "text",
                    "text": prompt_content,
                }
            ],
        }
        
    except Exception as error:
        # 错误处理 / Error handling
        error_message = str(error) if error else "未知错误"
        # Unknown error
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"初始化项目规范时发生错误: {error_message}",
                    # Error occurred during project specification initialization: {error_message}
                }
            ],
        }


# 导出工具配置和处理函数 / Export tool configuration and handler functions
__all__ = [
    'InitProjectRulesSchema',
    'INIT_PROJECT_RULES_TOOL',
    'handle_init_project_rules',
    'handle_init_project_rules_sync',
    'ToolContent',
    'ToolResponse'
]