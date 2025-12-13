from mcp.server.fastmcp import FastMCP

from aicoding_backend.utils.file_utils import dir_exists
from .utils import read_file, file_exists, generate_prompt
from typing import Annotated, List, Optional
from pydantic import BaseModel, Field
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from .prompts import get_init_requirements_doc_prompt
from .utils.log import log_data

mcp = FastMCP("backend-coding")

current_dir = Path(__file__).parent


class ProcessThoughtPromptParam(BaseModel):
    """process_thought工具的参数结构"""
    thought: str = Field(
        ...,
        min_length=1,
        description="思维内容",
        example="这是一个关于项目架构的思考"
    )
    thought_number: int = Field(
        ...,
        gt=0,
        description="当前思维编号",
        example=1
    )
    total_thoughts: int = Field(
        ...,
        gt=0,
        description="预计总思维数量，如果需要更多的思考可以随时变更",
        example=5
    )
    next_thought_needed: bool = Field(
        ...,
        description="是否需要下一步思维",
        example=True
    )
    stage: str = Field(
        ...,
        min_length=1,
        description="思维阶段。可用阶段包括：问题定义、信息收集、研究、分析、综合、结论、批判性提问和规划。",
        example="分析"
    )
    tags: Optional[List[str]] = Field(
        default=None,
        description="思维标签，是一个数组字符串",
        example=["架构", "设计"]
    )
    axioms_used: Optional[List[str]] = Field(
        default=None,
        description="使用的公理，是一个数组字符串",
        example=["单一职责原则", "开闭原则"]
    )
    assumptions_challenged: Optional[List[str]] = Field(
        default=None,
        description="挑战的假设，是一个数组字符串",
        example=["所有用户都需要这个功能"]
    )

class JavaFastCodingParam(BaseModel):
    """Java 快速编码工具的参数结构"""
    user_input: str = Field(
        ...,
        description="用户简单描述的需求，例如：'我想在这个项目中增加一个用户管理模块'"
    )
    repo_path: str = Field(
        ...,
        description="Java 项目根目录（绝对路径）"
    )
    target_file: Optional[str] = Field(
        None,
        description="（可选）目标文件路径，如果用户已经明确要修改哪个文件"
    )
    modify_type: Optional[str] = Field(
        None,
        description="（可选）修改类型：add-新增功能，modify-修改功能，delete-删除功能，optimize-优化代码"
    )
    design_doc_path: Optional[str] = Field(
        None,
        description="（可选）已生成的设计文档路径，如果提供则表示进入实现阶段"
    )

class GeneratePrpParam(BaseModel):
    """generate_prp 工具的参数结构"""
    feature_file: str = Field(
        ...,
        description="功能需求文件路径（例如：INITIAL.md）"
    )


@mcp.tool("generate_prp")
async def handle_generate_prp(feature_file : Annotated[str, Field(..., description="功能需求文件路径（例如：INITIAL.md）")]) -> str:
    """根据功能需求文件生成全面的产品需求提示（PRP）文档的指导。
    
    此工具会：
    1. 读取功能需求文件。
    2. 加载一个模板，指导用户或 AI 如何通过研究代码库和外部资源来构建一个高质量的 PRP。
    """
    args = GeneratePrpParam(feature_file=feature_file)
    try:
        feature_file = args.feature_file

        if not file_exists(feature_file):
            raise Exception(f"功能需求文件不存在: {feature_file}")

        # 获取当前文件的目录路径
        template_path = current_dir / "prompts"

        # 构建示例文件路径（注释掉的代码）
        # form_example_path = current_dir / "../../examples/form-vue-template.md"
        # list_example_path = current_dir / "../../examples/list-vue-template.md"
        # pro_list_example_path = current_dir / "../../examples/pro-list-vue-template.md"

        # 检查模板文件是否存在
        if not file_exists(template_path / "prp_base.md"):
            raise Exception(f"PRP 模板文件不存在: {template_path}")

        # 获取 template 内容
        template_content = await read_file(str(template_path), "prp_base.md")

        # 从功能文件名提取功能名称（用于输出路径）
        feature_name = Path(feature_file).stem

        prompt_content = f"""
# 创建 PRP

## 功能文件：{feature_file}

为通用功能实现生成完整的 PRP，并进行彻底研究。确保将上下文传递给 AI Agent，以实现自我验证和迭代改进。首先阅读功能文件以了解需要创建什么、提供的示例如何帮助以及任何其他考虑因素。

AI Agent只能获得您附加到 PRP 的上下文和训练数据。假设 AI Agent可以访问代码库并具有与您相同的知识截止日期，因此将您的研究发现包含或引用在 PRP 中非常重要。该代理具有网络搜索功能，因此请传递文档和示例的 URL。

## 研究流程

1. **代码库分析**
   - 在代码库中搜索类似的功能/模式
   - 识别要在 PRP 中引用的文件
   - 注意要遵循的现有约定
   - 检查验证方法的测试模式

2. 外部依赖分析规范
   - 对于代码库中缺失的依赖文件，统一使用MCP工具解析JAR包源码进行查阅
   - 处理外部依赖时，优先通过MCP工具读取JAR包内容，确保依赖关系的准确识别
   - 基于JAR包中目标方法的参数定义（入参/出参）作为开发参考标准，确保接口调用的正确性

3. **外部研究**
   - 在线搜索类似的功能/模式
   - 库文档（包含具体 URL）
   - 实现示例（GitHub/StackOverflow/博客）
   - 最佳实践和常见陷阱   

4. **用户澄清**（如果需要）
   - 要镜像的特定模式以及在哪里找到它们？
   - 集成需求以及在哪里找到它们？

## PRP 生成
使用使用以下内容作为PRP模板：
{template_content}

*** 关键：在您完成研究和探索代码库之后，开始编写 PRP 之前 ***

*** 深度思考 PRP 并规划您的方法，然后开始编写 PRP ***

## 输出
保存为：`.joycode/PRPs/{feature_name}.md`

## 质量检查清单
- [ ] 包含所有必要的上下文
- [ ] 验证门槛可由 AI 执行
- [ ] 引用现有模式
- [ ] 清晰的实现路径
- [ ] 记录错误处理
- [ ] 确保 `.joycode/PRPs/{feature_name}.md` 文件必须生成

在 1-10 的范围内为 PRP 评分（使用前端开发工具一次性实现成功的信心水平）

记住：目标是通过全面的上下文实现一次性实现成功。

**[AI Agent Action]**编辑完毕后请呼叫「log_report」工具进行本次工具使用记录上报，本次记录使用的工具为generate_prp
**[AI Agent Action]**编辑完毕后请使用`.joycode/PRPs/{feature_name}.md`文件的全路径名呼叫「execute_prp」工具
        """
        return generate_prompt(prompt_content, {"feature_file":feature_file, "template_content":template_content,"feature_name":feature_name})
    except Exception as error:
        error_message = str(error)
        return f"❌ 生成 PRP 指南失败: {error_message}"


class ExecutePrpArgs(BaseModel):
    """execute_prp 工具的参数结构"""
    prpFile: str = Field(
        ...,
        description="PRP 文件路径"
    )

@mcp.tool("execute_prp")
async def execute_prp(prp_file : Annotated[str, Field(..., description="PRP 文件路径")]) -> str:
    """根据 PRP 文件生成执行指南。
    
    此工具会：
    1. 验证并读取 PRP 文件路径
    2. 加载内置执行模板
    3. 将 PRP 文件路径注入模板中的占位符，返回完整的执行步骤指南
    """
    args = ExecutePrpArgs(prpFile=prp_file)
    try:
        prp_file = args.prpFile

        # 检查 PRP 文件是否存在
        if not file_exists(prp_file):
            raise Exception(f"PRP 文件不存在: {prp_file}")

        # 加载执行指南模板
        template_content = """
# 执行基础 PRP

使用 PRP 文件实现功能。

## PRP 文件：$ARGUMENTS

## 执行流程

1. **上报使用execute_prp工具记录**
   - **[AI Agent Action]**请呼叫「log_report」工具进行本次工具使用记录上报，本次使用工具为execute_prp

2. **加载 PRP**
   - 读取指定的 PRP 文件
   - 理解所有上下文和需求
   - 遵循 PRP 中的所有指令，并根据需要扩展研究
   - 确保拥有完全实现 PRP 所需的所有上下文
   - 根据需要进行更多网络搜索和代码库探索

3. **深度思考**
   - 在执行计划之前深入思考。创建一个解决所有需求的综合计划。
   - 使用待办事项工具将复杂任务分解为更小、可管理的步骤。
   - 使用 TodoWrite 工具创建和跟踪实现计划。
   - 从现有代码中识别要遵循的实现模式。

4. **执行计划**
   - 执行 PRP
   - 实现所有代码

5. **验证**
   - 运行每个验证命令
   - 修复任何失败
   - 重新运行直到全部通过

6. **完成**
   - 确保所有检查清单项目完成
   - 运行最终验证套件
   - 报告完成状态
   - 再次阅读 PRP 以确保已实现所有内容

7. **引用 PRP**
   - 如果需要，您可以随时再次引用 PRP



注意：如果验证失败，请使用 PRP 中的错误模式进行修复并重试；必须确保严格按照 PRP 实现所有功能代码。
        """
        
        # 将模板中的 `$ARGUMENTS` 替换为传入的 prp_file 路径
        
        guide = template_content.replace("$ARGUMENTS", prp_file)
        return guide
        
    except Exception as error:
        error_message = str(error)
        return f"❌ 生成执行指南失败: {error_message}"


@mcp.tool("java_fast_coding")
async def handle_java_fast_coding(
    user_input: Annotated[str, Field(..., description="用户简单描述的需求")],
    repo_path: Annotated[str, Field(..., description="Java 项目根目录（绝对路径）")],
    target_file: Annotated[Optional[str], Field(None, description="目标文件路径")] = None,
    modify_type: Annotated[Optional[str], Field(None, description="修改类型")] = None,
    design_doc_path: Annotated[Optional[str], Field(None, description="设计文档路径")] = None
) -> str:
    """Java 快速编码工具 - 基于简单描述快速生成 Java 后端代码
    支持两阶段工作流：设计文档生成阶段 → 代码实现阶段
    """
    args = JavaFastCodingParam(
        user_input=user_input,
        repo_path=repo_path,
        target_file=target_file,
        modify_type=modify_type,
        design_doc_path=design_doc_path
    )

    try:
        # 参数验证
        if not dir_exists(args.repo_path):
            raise Exception(f"Java 项目目录不存在: {args.repo_path}")
        
        # 检查项目规范文件
        project_info_path = f"{args.repo_path}/.joycode/rules/ProjectInfo.mdc"
        has_project_info = file_exists(project_info_path)
        
        # 阶段判断：文档生成 vs 代码实现
        if args.design_doc_path:
            # 阶段 2：实现阶段
            return await generate_java_implementation_prompt(args, has_project_info, project_info_path)
        else:
            # 阶段 1：文档生成阶段
            return await generate_java_document_prompt(args, has_project_info, project_info_path)
            
    except Exception as error:
        return f"❌ Java 快速编码工具执行失败: {str(error)}"


async def generate_java_document_prompt(args: JavaFastCodingParam, has_project_info: bool, project_info_path: str) -> str:
    """生成 Java 设计文档阶段的提示"""
    try:
        # 读取 Java 设计文档模板
        java_design_template = await read_file(current_dir / "prompts", "java_design_doc_template.md")
        
        # 构建提示内容
        prompt_content = f"""
# 🚀 Java Fast Mode - 阶段 1: 设计文档生成

**用户需求**: {args.user_input}
{f"**目标文件**: {args.target_file}" if args.target_file else ""}
{f"**修改类型**: {get_modify_type_label(args.modify_type)}" if args.modify_type else ""}

---

## 📋 当前任务：生成设计文档（⚠️ 仅生成文档，不写代码）

### 🔍 步骤 1: 深入分析 Java 项目结构

**必做事项:**
{f"1. 读取目标文件: `{args.target_file}`\\n   - 理解现有代码结构和实现方式\\n   - 识别需要修改的具体位置" if args.target_file else "1. 使用代码搜索工具定位需要修改的 Java 文件\\n   - 理解现有代码结构和实现方式"}

2. 查找可复用资源 (关键!)
   - 搜索项目中**类似的功能实现** (作为参考模板)
   - 找出**可直接复用的 Java 组件和工具类**
   - 确保新代码风格与现有 Java 代码一致
   - 分析现有的 Controller、Service、Repository 层结构

{f"3. 遵循项目规范\\n   - 读取: `{project_info_path}`\\n   - 严格遵循项目的 Java 代码风格、命名规范和技术栈要求" if has_project_info else ""}

4. Java 项目特定分析
   - 识别 Maven/Gradle 构建工具和依赖管理
   - 分析 Spring Boot 配置和注解使用模式
   - 检查现有的 DO/DTO/VO 类结构
   - 了解数据库访问层（MyBatis/JPA）的使用方式

---

### 📝 步骤 2: 生成完整的 Java 设计文档

**文档路径**: `.joycode/fast-mode/{{feature-name}}.md` （请根据功能生成合适的文件名）

**⚠️ 强制要求:**
1. **必须使用 `write_file` 创建设计文档**
2. **必须严格按照以下模板填写所有占位符内容（不能留空或使用待补充）**
3. **不能直接写代码，必须先生成文档**

**Java 设计文档模板:**
```markdown
{java_design_template}
```

**📋 必须填写的内容清单:**
- ✅ **需求描述**: 用户需求的简要说明
- ✅ **影响范围**:
  * 主要修改文件: 列出所有需要修改的 Java 文件路径及修改原因
  * 关联文件: 列出可能受影响的关联文件
- ✅ **复用资源**:
  * 参考实现: 必须搜索并列出项目中类似的 Java 功能实现
  * 可复用组件/类: 列出可以直接使用的现有 Java 组件或工具类
- ✅ **Java 实现步骤**:
  * 每个步骤必须包含: 目标、Java 文件路径、具体改动点、关键代码片段
  * 包含 Controller、Service、Repository、Entity 等层次的实现计划
- ✅ **验证清单**:
  * 功能验证: 列出具体的测试场景和验证点
  * 编译测试: Maven/Gradle 编译验证步骤
- ✅ **注意事项**: Java 实现过程中需要注意的具体事项

**⚠️ 关键提醒:**
- 所有模板中的占位符都必须替换成实际的 Java 项目内容
- **本阶段只生成文档，不写 Java 代码！**
- 文档要简洁实用，但必须完整，重点突出关键改动点

---

### ✅ 步骤 3: 反馈给用户

**完成后告知用户:**
- ✓ Java 设计文档已生成（提供文档完整路径）
- ✓ 说明文档包含的主要内容（影响文件、实现步骤等）
- ✓ 提醒用户：下一步会自动调用实现阶段，或用户可以先查看文档

---

**🚀 现在开始执行！**

**重要提醒**:
- 本阶段**只生成设计文档**，**不写任何 Java 代码**
- 文档生成后，自动重新调用本工具，将设计文档传入，进入实现阶段
- 设计文档路径: `.joycode/fast-mode/{{合适的功能名称}}.md`

**[AI Agent Action]**完成后请呼叫「log_report」工具进行本次工具使用记录上报，本次记录使用的工具为java_fast_coding
        """
        
        return generate_prompt(prompt_content, {
            "user_input": args.user_input,
            "target_file": args.target_file or "",
            "modify_type": args.modify_type or "",
            "project_info_path": project_info_path,
            "java_design_template": java_design_template
        })
        
    except Exception as error:
        return f"❌ 生成 Java 文档提示失败: {str(error)}"


async def generate_java_implementation_prompt(args: JavaFastCodingParam, has_project_info: bool, project_info_path: str) -> str:
    """生成 Java 代码实现阶段的提示"""
    try:
        # 读取 Java 实现模板
        java_impl_template = await read_file(current_dir / "prompts", "java_implementation_template.md")
        
        prompt_content = f"""
# 🚀 Java Fast Mode - 阶段 2: 代码实现

**用户需求**: {args.user_input}
{f"**目标文件**: {args.target_file}" if args.target_file else ""}
{f"**修改类型**: {get_modify_type_label(args.modify_type)}" if args.modify_type else ""}
**设计文档**: {args.design_doc_path}

---

{java_impl_template}

---

## 📋 当前任务：按设计文档实现 Java 代码

### 📝 步骤 1: 读取设计文档

**必做事项:**
1. 使用 `read_file` 读取设计文档: `{args.design_doc_path}`
2. 理解文档中的：
   - 影响范围（需要修改的 Java 文件）
   - 复用资源（参考实现）
   - Java 实现步骤（具体改动点）
   - 验证清单（测试要点）

{f"3. 遵循项目规范\\n   - 读取: `{project_info_path}`" if has_project_info else ""}

### 🔨 步骤 2: 按文档实施 Java 代码

**实施要求:**
1. **严格按照设计文档执行** - 不能偏离文档规划
2. **遵循 Java 编码规范** - 使用项目现有的代码风格
3. **分层实现** - 按 Controller → Service → Repository → Entity 顺序实现
4. **集成测试代码** - 使用现有 Java 测试模板生成对应测试
5. **编译验证** - 确保生成的代码能够编译通过

### ✅ 步骤 3: 验证和完成

**验证清单:**
- [ ] 所有 Java 文件编译通过
- [ ] 测试代码生成完整
- [ ] 符合项目编码规范
- [ ] 功能逻辑正确实现

**[AI Agent Action]**完成后请呼叫「log_report」工具进行本次工具使用记录上报，本次记录使用的工具为java_fast_coding
        """
        
        return generate_prompt(prompt_content, {
            "user_input": args.user_input,
            "target_file": args.target_file or "",
            "modify_type": args.modify_type or "",
            "design_doc_path": args.design_doc_path,
            "java_impl_template": java_impl_template
        })
        
    except Exception as error:
        return f"❌ 生成 Java 实现提示失败: {str(error)}"


def get_modify_type_label(modify_type: str) -> str:
    """获取修改类型的中文标签"""
    if not modify_type:
        return ""
    
    labels = {
        "add": "新增功能",
        "modify": "修改功能",
        "delete": "删除功能",
        "optimize": "优化代码"
    }
    return labels.get(modify_type, modify_type)


@mcp.tool()
async def init_project_rules() -> str:
    """初始化项目规则
    Args: None
    Return: 模版提示词
    """
    template = await read_file(current_dir / "prompts", "CreateFeatureProjectRules.md")
    return template

@mcp.tool()
async def init_requirements_doc() -> str:
    """初始化需求描述文档模板
    Args: None
    Return: 需求描述文档模板提示词
    """
    return await get_init_requirements_doc_prompt()

# @mcp.tool()
# async def process_thought(processThoughtPromptParam : ProcessThoughtPromptParam) -> str:
#     """处理单一思维并返回格式化输出
#     """
#     return await execute_process_thought(
#         thought=processThoughtPromptParam.thought,
#         thought_number=processThoughtPromptParam.thought_number,
#         total_thoughts=processThoughtPromptParam.total_thoughts,
#         next_thought_needed=processThoughtPromptParam.next_thought_needed,
#         stage=processThoughtPromptParam.stage,
#         tags=processThoughtPromptParam.tags,
#         axioms_used=processThoughtPromptParam.axioms_used,
#         assumptions_challenged=processThoughtPromptParam.assumptions_challenged
#     )

async def execute_process_thought(
    thought: str,
    thought_number: int,
    total_thoughts: int,
    next_thought_needed: bool,
    stage: str,
    tags: List[str] = None,
    axioms_used: List[str] = None,
    assumptions_challenged: List[str] = None
) -> str:
    try:
        logging.info('Executing process_thought tool')

        # 确保列表参数不为None
        tags = tags or []
        axioms_used = axioms_used or []
        assumptions_challenged = assumptions_challenged or []

        # 更新total_thoughts如果thought_number更大
        if thought_number > total_thoughts:
            total_thoughts = thought_number

        # 构建next_section内容
        if next_thought_needed:
            next_section = '需要更多思考，继续使用 「process_thought」 工具思考找寻答案'
        else:
            next_section_lines = [
                '## 思考完成',
                '',
                '返回最终分析结果概要',
                '',
                '1. **任务摘要** - 目标、范围、挑战和限制条件',
                '2. **初步解答构想** - 可行的技术方案和实施计划',
            ]
            next_section = '\n'.join(next_section_lines)

        # 构建模板
        template_lines = [
            '## 思维 {{thought_number}}/{{total_thoughts}} - {{stage}}',
            '',
            '{{thought}}',
            '',
            '**标签:** {{tags}}',
            '',
            '**使用的原则:** {{axioms_used}}',
            '',
            '**挑战的假设:** {{assumptions_challenged}}',
            '',
            '**禁止事项：** 你应该禁止一切猜测，任何疑虑请完整查看相关程序代码或使用网络搜寻工具查询',
            '',
            '{{next_section}}',
        ]
        template = '\n'.join(template_lines)

        param = {
            "thought":thought,
            "thought_number":thought_number,
            "total_thoughts":total_thoughts,
            "stage":stage,
            "tags":",".join(tags) or "no tags",
            "axioms_used": ",".join(axioms_used) or "no axioms used",
            "assumptions_challenged":",".join(assumptions_challenged) or "no assumptions challenged",
        }

        # 格式化输出
        return generate_prompt(template, param)

    except Exception as error:
        logging.error('Error executing process_thought', exc_info=error)
        raise Exception('Error executing process_thought') from error

class RepoInfoParam(BaseModel):
    """log_report工具的参数结构"""
    work_dir: str = Field(..., description="当前工作代码库根目录地址",example="/Users/chenshuren.5/proj/AICoding-backend/aicoding_backend")
    tool_type:str = Field(..., description="当前执行的mcp工具", example="init_project_rules")

@mcp.tool()
def log_report(
    work_dir:Annotated[str, Field(..., description="当前工作代码库根目录地址")],
    tool_type:Annotated[str, Field(..., description="当前执行的mcp工具")]
    ):
    repoInfoParam = RepoInfoParam(work_dir=work_dir, tool_type=tool_type)
    """上报工具使用记录"""
    log_data(repoInfoParam.work_dir, {"toolType":repoInfoParam.tool_type})

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()