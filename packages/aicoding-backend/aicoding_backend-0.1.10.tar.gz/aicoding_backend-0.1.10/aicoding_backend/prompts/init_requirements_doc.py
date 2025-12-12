"""
initRequirementsDoc prompt 生成器
initRequirementsDoc prompt generator
负责将模板和参数组合成最终的 prompt
Responsible for combining templates and parameters into the final prompt
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass
import asyncio
from aicoding_backend.utils.loader import load_prompt


@dataclass
class InitRequirementsDocPromptParams:
    """
    initRequirementsDoc prompt 参数类
    initRequirementsDoc prompt parameters class
    """
    # 目前没有额外参数，未来可按需扩展
    # Currently no additional parameters, can be expanded as needed in the future
    pass


async def get_init_requirements_doc_prompt(
    params: Optional[InitRequirementsDocPromptParams] = None
) -> str:
    """
    获取 initRequirementsDoc 的完整 prompt
    Get the complete prompt for initRequirementsDoc
    
    Args:
        params: prompt 参数（可选）/ prompt parameters (optional)
        
    Returns:
        str: 生成的 prompt / generated prompt
    """
    
    index_template = """
# 需求描述文档

## 目的

**此文件专为 AI Agent 设计，非一般开发者文档。**
**必须生成一个专属于 AI Agent 使用的需求描述文档([根据本次需求命名].md)。**

**必须专注于以下关键目标：**

- 准确识别和描述产品的核心功能特性
- 识别并规避潜在风险和注意事项
- 输出结构清晰、功能完整的需求文档

**强制规定：**

- 完成的规范必须使 AI Agent 能立即理解哪些文件必须参考或修改
- 避免使用模糊不清的需求描述语言
- 使用命令式语言定义规则，避免解释性内容
- 注意事项必须包含具体的风险规避方案
- 参考示例必须来自「examples」文件夹中的产品
- 识别描述中外部依赖，统一调用MCP工具阅读JAR包中源代码

**严重禁止：**

- 禁止包含通用开发知识
- 禁止包含 LLM 已知的通用开发知识
- 进行项目功能解释
- 禁止开始写代码

## 建议结构

请使用以下结构建立需求描述文档文件：

```markdown
## 功能特性:

[在此处插入您的功能特性]

## 参考示例:

[提供并描述您在  `examples/` 文件夹中的示例]

## 参考文档:

[列出开发过程中需要参考的任何文档（网页、MCP 服务器的数据源如 Crawl4AI RAG 等）]

## 注意事项:

[任何其他注意事项或特定要求 - 这里是包含您在项目中经常看到 AI 编程助手遗漏的问题的好地方]

```

## 内容指南

需求描述文档应包含但不限于以下内容：

1. **功能特性** - 简要描述项目功能点描述
2. **参考示例** - 描述主要功能和使用场景
3. **参考文档** - 开发过程中需要参考的任何文档
4. **注意事项** - 任何其他注意事项或特定要求

## 注意事项

1. **面向 AI 优化** - 文档将作为 prompt 提供给 Coding Agent AI，应对 prompt 最佳化
4. **使用命令式语言** - 必须使用直接指令而非描述性语言，减少解释内容
5. **结构化呈现** - 所有内容必须以列表、表格等结构化形式呈现，便于 AI 解析
6. **突出重点标记** - 使用粗体、警告标记等突出关键规则和禁忌
7. **移除通用知识** - 禁止包含 LLM 已知的通用开发知识，仅包含项目特定规则


请根据以上指南，创建一个名为 [根据本次需求命名(使用下划线命名风格)].md 的文件并存放于根目录下「.joycode/docs」目录

## 完成上面的步骤后
**[AI Agent Action]**请呼叫「log_report」工具进行本次工具使用记录上报
    """

    # 加载可能的自定义 prompt (通过环境变量覆盖或追加)
    # Load possible custom prompt (override or append via environment variables)
    return load_prompt(index_template, "INIT_REQUIREMENTS_DOC")