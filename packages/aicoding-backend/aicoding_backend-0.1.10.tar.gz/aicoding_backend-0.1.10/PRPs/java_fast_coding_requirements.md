# Java 后端代码快速生成工具 - 产品需求提示 (PRP)

## 目的
该 PRP 专为 AI 代理优化，使其能够通过充分的上下文和自我验证能力，实现 Java 后端快速编码工具的一次性成功实现。该工具将与现有的 TypeScript `fast_coding` 工具功能对等，专门针对 Java 后端开发场景进行优化。

## 核心原则
1. **上下文为王**: 包含所有必要的文档、示例和注意事项
2. **验证循环**: 提供 AI 可运行和修复的可执行测试/检查
3. **信息密集**: 使用代码库中的关键词和模式
4. **渐进式成功**: 从简单开始，验证后再增强
5. **全局规则**: 确保遵循项目开发守则中的所有规范

---

## 目标
构建一个 Java 后端代码快速生成的 MCP 工具，实现与 TypeScript 版本 `fast_coding` 工具相同的功能，但专门针对 Java 后端开发场景进行优化。该工具应支持基于简单用户描述快速生成 Java 后端代码，采用两阶段工作流（设计文档生成 → 代码实现），并智能分析现有代码库以识别可复用的组件和模式。

### 成功标准
- [ ] 成功创建 `java_fast_coding` MCP 工具并在 main.py 中注册
- [ ] 创建完整的提示词模板支持 Java 项目分析和代码生成
- [ ] 工具能够分析现有 Java 项目结构并生成设计文档
- [ ] 工具能够基于设计文档生成标准化的 Java 代码
- [ ] 支持 Controller、Service、Repository 等 Java 组件的生成
- [ ] 通过编译检查和基础功能验证

## 所有必需的上下文

### 文档和参考资料
```yaml
# 必读 - 将这些包含在您的上下文窗口中
- file: .joycode/docs/index.ts
  why: TypeScript fast_coding 工具的完整实现，包含两阶段工作流、参数结构和核心逻辑

- file: templates/java.md  
  why: Java 代码规范，包含 DO/DTO/VO 类创建规范、Alibaba FastJSON 序列化规范、转换工具类规范

- file: aicoding_backend/main.py
  why: MCP 工具注册模式、参数模型定义规范、错误处理模式

- file: aicoding_backend/prompts/prp_base.md
  why: PRP 基础模板结构，了解提示词模板的标准格式

- file: aicoding_backend/prompts/java_test_controller.md
  why: Java Controller 层测试用例编写规则，用于集成测试代码生成

- file: aicoding_backend/prompts/java_test_service.md  
  why: Java Service 层测试规范

- file: aicoding_backend/prompts/java_test_repo.md
  why: Java Repository 层测试规范

- docfile: .joycode/rules/ProjectInfo.mdc
  why: 项目开发守则，包含 MCP 工具开发规范、文件命名规范、代码实现规范
```

### 当前代码库结构
```bash
AICoding-backend/
├── aicoding_backend/
│   ├── main.py                    # MCP 服务器入口，需要注册新工具
│   ├── tools/                     # 工具实现模块
│   │   └── generate_test.py       # 当前为空，需要完善
│   ├── prompts/                   # 提示词模板存储
│   │   ├── prp_base.md           # PRP 基础模板
│   │   ├── java_test_controller.md # Java Controller 测试模板
│   │   ├── java_test_service.md    # Java Service 测试模板  
│   │   └── java_test_repo.md      # Java Repository 测试模板
│   └── utils/                     # 通用工具函数
├── templates/
│   └── java.md                   # Java 代码规范和模板
├── PRPs/                         # 产品需求提示文档存储
└── .joycode/
    ├── docs/
    │   └── index.ts              # TypeScript fast_coding 参考实现
    └── rules/
        └── ProjectInfo.mdc       # 项目开发守则
```

### 期望的代码库结构
```bash
AICoding-backend/
├── aicoding_backend/
│   ├── main.py                           # 新增 JavaFastCodingParam 和 handle_java_fast_coding
│   ├── prompts/
│   │   ├── java_fast_coding.py          # 主要提示词模块 (新增)
│   │   ├── java_design_doc_template.md  # Java 设计文档模板 (新增)
│   │   └── java_implementation_template.md # Java 实现指导模板 (新增)
│   └── tools/
│       └── generate_test.py             # 完善测试代码生成功能
```

### 已知的代码库陷阱和库怪癖
```java
// 关键: MCP 工具必须遵循项目开发守则中的严格规范
// 示例: 所有 MCP 工具函数必须是异步函数，使用 await read_file() 进行文件读取
// 示例: 必须使用 Pydantic BaseModel 定义参数结构，Field() 提供参数描述
// 示例: 错误响应必须以 ❌ 开头，成功响应使用 generate_prompt() 格式化长文本
// 示例: 所有工具必须在 main.py 中注册，提示词文件必须提供 get_{tool_name}_prompt() 函数
// 示例: Java 命名规范：类名 PascalCase，方法和变量 camelCase，常量 UPPER_SNAKE_CASE
// 示例: Spring Boot 中 @ConfigurationProperties 类必须提供 setter 方法
// 示例: Hibernate 实体类必须提供无参构造函数，字段应使用包装类型（如 Integer 而非 int）
// 示例: 使用 Lombok 时，@Data 与 @Entity 混用可能导致 Hibernate 代理问题，建议改用 @Getter/@Setter
// 示例: Optional 仅用于返回值，不应用于字段或方法参数
// 示例: Alibaba FastJSON 序列化需要 @JSONField 注解控制字段顺序和格式
```

## 实施蓝图

### 数据模型和结构

定义清晰、封装良好、类型安全的核心数据模型，确保与 MCP 协议和 FastMCP 框架兼容。

```python
# 参数模型设计 - 参考 TypeScript 版本的参数结构
class JavaFastCodingParam(BaseModel):
    """Java 快速编码工具的参数结构"""
    user_input: str = Field(..., description="用户简单描述的需求，例如：'我想在这个项目中增加一个用户管理模块'")
    repo_path: str = Field(..., description="Java 项目根目录（绝对路径）")
    target_file: Optional[str] = Field(None, description="（可选）目标文件路径，如果用户已经明确要修改哪个文件")
    modify_type: Optional[str] = Field(None, description="（可选）修改类型：add-新增功能，modify-修改功能，delete-删除功能，optimize-优化代码")
    design_doc_path: Optional[str] = Field(None, description="（可选）已生成的设计文档路径，如果提供则表示进入实现阶段")
```

### 按顺序完成 PRP 所需完成的任务列表

```yaml
任务 1: 创建 Java 快速编码主工具
  文件: aicoding_backend/main.py
  - 添加 JavaFastCodingParam 参数模型类
  - 实现 handle_java_fast_coding 异步函数
  - 使用 @mcp.tool("java_fast_coding") 装饰器注册工具
  - 实现两阶段工作流：文档生成阶段和代码实现阶段
  - 添加完整的错误处理和日志记录

任务 2: 创建 Java 快速编码提示词模块
  文件: aicoding_backend/prompts/java_fast_coding.py
  - 实现 get_java_fast_coding_prompt() 函数
  - 提供文档生成阶段和实现阶段的提示词模板
  - 包含 Java 项目结构分析指导
  - 集成现有 Java 代码规范和测试模板引用

任务 3: 创建 Java 设计文档模板
  文件: aicoding_backend/prompts/java_design_doc_template.md
  - 基于 TypeScript 版本设计文档模板进行 Java 化改造
  - 包含 Java 项目特有的模块结构（Controller、Service、Repository、Entity）
  - 添加 Maven/Gradle 依赖管理考虑
  - 包含 Spring Boot 框架特定的配置要求

任务 4: 创建 Java 实现指导模板  
  文件: aicoding_backend/prompts/java_implementation_template.md
  - 提供基于设计文档的 Java 代码实现指导
  - 集成现有 Java 测试模板的引用
  - 包含编译验证和基础测试指导
  - 添加 Java 特有的代码质量检查要求

任务 5: 完善测试代码生成功能
  文件: aicoding_backend/tools/generate_test.py  
  - 实现基于现有 Java 测试模板的代码生成逻辑
  - 支持 Controller、Service、Repository 三层测试生成
  - 集成到 java_fast_coding 工具的工作流中
  - 确保生成的测试代码符合项目规范

任务 6: 集成测试和验证
  - 测试工具注册和参数验证
  - 验证两阶段工作流的正确性
  - 测试 Java 项目结构分析功能
  - 验证生成的设计文档和代码的质量
```

### 每个任务所需的伪代码

```python
# 任务 1 - Java 快速编码主工具实现
@mcp.tool("java_fast_coding")
async def handle_java_fast_coding(args: JavaFastCodingParam) -> str:
    """Java 快速编码工具 - 基于简单描述快速生成 Java 后端代码"""
    try:
        # 参数验证
        if not file_exists(args.repo_path):
            raise Exception(f"Java 项目目录不存在: {args.repo_path}")
        
        # 检查项目规范文件
        project_info_path = os.path.join(args.repo_path, ".joycode/rules/ProjectInfo.mdc")
        has_project_info = file_exists(project_info_path)
        
        # 阶段判断：文档生成 vs 代码实现
        if args.design_doc_path:
            # 阶段 2：实现阶段
            return await generate_java_implementation_prompt(args, has_project_info)
        else:
            # 阶段 1：文档生成阶段  
            return await generate_java_document_prompt(args, has_project_info)
            
    except Exception as error:
        return f"❌ Java 快速编码工具执行失败: {str(error)}"

# 任务 2 - 提示词模块实现
def get_java_fast_coding_prompt(stage: str, **kwargs) -> str:
    """获取 Java 快速编码提示词"""
    if stage == "document":
        return generate_prompt("java_design_doc_template.md", kwargs)
    elif stage == "implementation": 
        return generate_prompt("java_implementation_template.md", kwargs)
    else:
        raise ValueError(f"未知的阶段: {stage}")
```

### 集成点
```yaml
MCP 工具注册:
  - 在 main.py 中注册 java_fast_coding 工具
  - 遵循现有工具的注册模式和错误处理规范
  - 集成 log_report 工具进行使用记录上报

提示词模板集成:
  - 引用现有 Java 测试模板 (java_test_*.md)
  - 集成 Java 代码规范 (templates/java.md)  
  - 复用 PRP 基础模板的结构模式

文件操作集成:
  - 使用项目 utils 模块的 read_file、file_exists、generate_prompt 函数
  - 遵循异步文件操作规范
  - 确保路径操作的安全性和正确性

测试代码生成集成:
  - 调用完善后的 generate_test.py 工具
  - 支持多层级测试代码生成
  - 确保生成的测试代码符合项目测试规范
```

## 验证循环

### 级别 1: 语法和样式检查
```bash
# Python 代码检查
python -m py_compile aicoding_backend/main.py
python -m py_compile aicoding_backend/prompts/java_fast_coding.py
# 预期: 无编译错误

# 工具注册验证
python -c "from aicoding_backend.main import mcp; print('java_fast_coding' in [tool.name for tool in mcp.list_tools()])"
# 预期: 输出 True
```

## 最终验证清单
- [ ] java_fast_coding 工具成功注册到 MCP 服务器
- [ ] 工具参数验证正确，错误处理完善
- [ ] 文档生成阶段能够分析 Java 项目结构并生成设计文档
- [ ] 实现阶段能够基于设计文档生成 Java 代码和测试代码
- [ ] 生成的代码符合 Java 编码规范和项目规范
- [ ] 集成现有 Java 测试模板，生成的测试代码完整可用
- [ ] 工具使用记录正确上报到 log_report
- [ ] 所有提示词模板格式正确，变量替换功能正常
- [ ] 错误情况得到优雅处理，用户友好的错误消息
- [ ] 文档已更新，包含工具使用说明和最佳实践

---

## 要避免的反模式
- ❌ 不要直接复制 TypeScript 版本代码，必须根据 Python MCP 框架进行适配
- ❌ 不要忽略项目开发守则中的 MCP 工具开发规范
- ❌ 不要跳过参数验证和错误处理，这是 MCP 工具的基本要求
- ❌ 不要忘记集成现有的 Java 测试模板和代码规范
- ❌ 不要硬编码文件路径，使用相对路径和配置化方式
- ❌ 不要忽略异步函数要求，所有 MCP 工具函数必须是异步的
- ❌ 忠实地理解用户所提出的需求，不要自主添加其他功能

## PRP 质量评分: 9/10
**信心水平**: 在 1-10 的范围内，我对使用这个 PRP 一次性成功实现 Java 快速编码工具的信心水平是 9。

**评分理由**:
- ✅ 包含完整的上下文信息，引用了所有相关的现有代码和文档
- ✅ 详细的实施蓝图，明确的任务分解和伪代码指导
- ✅ 完善的验证循环，从语法检查到功能验证到集成测试
- ✅ 遵循项目开发守则，确保实现符合现有规范
- ✅ 集成现有资源，复用 Java 测试模板和代码规范
- ⚠️ 扣 1 分：需要对 TypeScript 版本进行深度理解和 Python 适配，存在一定实现复杂度