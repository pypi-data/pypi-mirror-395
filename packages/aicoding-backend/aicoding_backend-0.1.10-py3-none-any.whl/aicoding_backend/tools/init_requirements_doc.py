"""
初始化需求描述文档 MCP 工具
Initialize requirements document MCP tool
对应 TypeScript 版本的 Python 实现
Python implementation corresponding to TypeScript version
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import json
import asyncio
from pydantic import BaseModel, Field

from ..prompts.init_requirements_doc import get_init_requirements_doc_prompt


class InitRequirementsDocSchema(BaseModel):
    """
    初始化需求描述文档工具的输入参数模式
    Input parameter schema for init requirements doc tool
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
# 对应 TypeScript 中的 initRequirementsDocTool
# Corresponds to initRequirementsDocTool in TypeScript
INIT_REQUIREMENTS_DOC_TOOL = {
    "name": "init_requirements_doc",
    "description": "初始化需求描述文档模板",
    # "description": "Initialize requirements document template",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "additionalProperties": False
    },
}


async def handle_init_requirements_doc(arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    初始化需求描述文档工具函数
    Initialize requirements document tool function
    提供建立需求描述文档的指导
    Provide guidance for creating requirements documents
    
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
        schema = InitRequirementsDocSchema(**arguments)
        
        # 从生成器获取提示词 / Get prompt from generator
        prompt_content = await get_init_requirements_doc_prompt()
        
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
                    "text": f"初始化需求描述文档时发生错误: {error_message}",
                    # Error occurred during requirements document initialization: {error_message}
                }
            ],
        }


def handle_init_requirements_doc_sync(arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    同步版本的工具处理函数
    Synchronous version of the tool handler function
    
    Args:
        arguments: 输入参数（当前为空）/ Input arguments (currently empty)
        
    Returns:
        Dict[str, Any]: MCP 标准响应格式 / MCP standard response format
    """
    try:
        # 使用 asyncio.run 运行异步函数 / Use asyncio.run to run async function
        return asyncio.run(handle_init_requirements_doc(arguments))
    except Exception as error:
        # 错误处理 / Error handling
        error_message = str(error) if error else "未知错误"
        # Unknown error
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"初始化需求描述文档时发生错误: {error_message}",
                    # Error occurred during requirements document initialization: {error_message}
                }
            ],
        }