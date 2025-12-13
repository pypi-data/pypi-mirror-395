# README生成器 - 产品需求提示文档

## 目标
构建一个智能README.md生成器，能够自动分析Python项目结构，提取项目元数据，并生成符合行业标准的专业README文档。

## 为什么
- **节省时间**：自动生成标准化文档，减少手动编写工作量
- **保持一致性**：确保所有项目文档遵循统一的格式和标准
- **提升质量**：自动提取项目信息，减少人为错误和遗漏
- **标准化**：建立团队文档规范，提高项目可维护性

## 什么
用户可以通过简单的命令或函数调用，自动生成包含项目描述、安装指南、使用方法、项目结构等完整信息的README.md文件。

### 成功标准
- [ ] 自动读取pyproject.toml项目配置
- [ ] 智能分析项目目录结构
- [ ] 识别Python技术栈和依赖
- [ ] 生成标准Markdown格式文档
- [ ] 包含完整的项目信息章节

## 所有必需的上下文

### 文档和参考资料
```yaml
# 必读 - 将这些包含在您的上下文窗口中
- file: pyproject.toml
  why: 包含项目名称、版本、描述、依赖等元数据
  
- file: README.md
  why: 当前文档结构参考，了解现有格式
  
- file: aicoding_backend/main.py
  why: 主程序入口，了解项目架构
  
- file: aicoding_backend/utils/
  why: 工具函数目录，包含文件读取和处理功能
```

### 当前代码库结构
```
aicoding_backend/
├── __init__.py
├── main.py              # 主程序入口
├── prompts/             # 提示模板
├── tools/               # 工具函数
└── utils/               # 通用工具
    ├── file_reader.py   # 文件读取工具
    ├── file_utils.py    # 文件操作工具
    └── template.py      # 模板处理
```

### 期望的代码库结构
```
aicoding_backend/
├── tools/
│   └── readme_generator.py    # 新增README生成器
└── templates/
    └── readme_template.md     # README模板文件
```

## 实施蓝图

### 数据模型和结构
```python
# 项目信息数据模型
@dataclass
class ProjectInfo:
    name: str
    version: str
    description: str
    author: str
    python_version: str
    dependencies: List[str]
    dev_dependencies: List[str]
    project_structure: Dict[str, List[str]]

# README模板数据结构
@dataclass  
class ReadmeTemplate:
    title: str
    description: str
    installation: str
    usage: str
    project_structure: str
    contributing: str
    license: str
```

### 按顺序完成的任务列表

```yaml
任务 1:
创建 aicoding_backend/tools/readme_generator.py:
  - 导入tomllib库读取pyproject.toml
  - 创建ProjectInfo类解析项目元数据
  - 实现读取项目结构的功能

任务 2:
创建 aicoding_backend/templates/readme_template.md:
  - 设计标准README模板
  - 包含所有必要章节
  - 使用Jinja2模板语法

任务 3:
修改 aicoding_backend/tools/__init__.py:
  - 导入新的readme_generator模块
  - 确保模块可被外部访问

任务 4:
创建测试文件 tests/test_readme_generator.py:
  - 测试项目信息提取功能
  - 测试模板渲染功能
  - 验证生成的README格式
```

### 每个任务的伪代码
```python
# 任务 1: readme_generator.py
class ReadmeGenerator:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.project_info = None
    
    def extract_project_info(self) -> ProjectInfo:
        # 读取pyproject.toml
        pyproject_path = self.project_path / "pyproject.toml"
        with open(pyproject_path, 'rb') as f:
            data = tomllib.load(f)
        
        # 提取项目信息
        return ProjectInfo(
            name=data['project']['name'],
            version=data['project']['version'],
            description=data['project']['description'],
            # ... 其他字段
        )
    
    def analyze_project_structure(self) -> Dict[str, List[str]]:
        # 扫描项目目录
        # 识别Python文件、配置文件等
        # 返回结构化信息
        pass
    
    def generate_readme(self) -> str:
        # 加载模板
        # 渲染内容
        # 返回生成的README
        pass
```

### 集成点
```yaml
配置:
  - 添加到: pyproject.toml
  - 模式: "[project.optional-dependencies] 添加 readme-generator"
  
工具导入:
  - 添加到: aicoding_backend/tools/__init__.py
  - 模式: "from .readme_generator import ReadmeGenerator"
  
命令行:
  - 添加到: aicoding_backend/main.py
  - 模式: "添加readme生成命令处理"
```

## 验证循环

### 级别 1: 语法和样式
```bash
# 首先运行这些 - 在继续之前修复任何错误
python -m py_compile aicoding_backend/tools/readme_generator.py
python -m mypy aicoding_backend/tools/readme_generator.py

# 预期: 无错误。如果有错误，阅读错误并修复。
```

### 级别 2: 单元测试
```python
# tests/test_readme_generator.py
def test_extract_project_info():
    generator = ReadmeGenerator(".")
    info = generator.extract_project_info()
    assert info.name == "aicoding-backend"
    assert info.version is not None

def test_generate_readme():
    generator = ReadmeGenerator(".")
    readme = generator.generate_readme()
    assert "# " in readme
    assert "## Installation" in readme
```

```bash
# 运行并迭代直到通过:
python -m pytest tests/test_readme_generator.py -v
```

### 级别 3: 集成测试
```bash
# 生成本项目的README
python -c "from aicoding_backend.tools import ReadmeGenerator; g = ReadmeGenerator('.'); print(g.generate_readme())"

# 验证输出包含关键章节
# 预期: 包含项目名称、描述、安装说明等
```

## 最终验证清单
- [ ] 所有测试通过: `python -m pytest`
- [ ] 无语法错误: `python -m py_compile`
- [ ] 类型检查通过: `python -m mypy`
- [ ] 能正确读取pyproject.toml
- [ ] 生成的README格式正确
- [ ] 包含所有必要章节
- [ ] 文档已更新

## 要避免的反模式
- ❌ 不要硬编码项目路径
- ❌ 不要忽略toml解析错误
- ❌ 不要跳过模板验证
- ❌ 不要生成空章节
- ❌ 不要使用非标准Markdown扩展