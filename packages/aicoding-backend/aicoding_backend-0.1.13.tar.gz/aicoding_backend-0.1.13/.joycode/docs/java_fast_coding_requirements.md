# Java后端代码快速生成工具需求文档

## 功能特性

### 核心功能描述
**开发一个生成JAVA后端代码的快速模式MCP工具方法**，实现与TypeScript版本`fast_coding`工具相同的功能，但专门针对Java后端开发场景进行优化。

### 主要功能点
- **快速代码生成**: 基于简单的用户描述快速生成Java后端代码
- **两阶段工作流**: 设计文档生成阶段 → 代码实现阶段  
- **智能代码分析**: 自动分析现有代码库，识别可复用的组件和模式
- **模板驱动生成**: 基于预定义模板和规范生成标准化的Java代码
- **增量式开发**: 支持在现有代码基础上进行小幅调整和功能增强

### 适用场景
- ✅ 现有Java项目的功能增强和修改
- ✅ 增加/修改/删除单个Java组件（Controller、Service、Repository等）
- ✅ 业务逻辑的快速实现和调整
- ✅ 标准化代码结构的快速生成
- ❌ 不适合: 大型架构重构、跨模块复杂变更

## 参考示例

### TypeScript实现参考
**主要参考文件**: `.joycode/docs/index.ts`
- **工具名称**: `fast_coding` 
- **核心流程**: 分析 → 文档生成 → 代码实现
- **参数结构**: `userInput`, `repoPath`, `targetFile`, `modifyType`, `designDocPath`

### 现有Java模板参考
**主要参考文件**: `templates/java.md`
- **DO/DTO/VO类创建规范**
- **Alibaba FastJSON序列化规范** 
- **字段注解和验证规范**
- **转换工具类规范**

## 参考文档

### 技术规范文档
- **项目开发守则**: `.joycode/rules/ProjectInfo.mdc`
- **Java代码规范**: `templates/java.md`
- **MCP工具开发规范**: 项目开发守则中的MCP工具开发部分

### 现有工具实现
- **TypeScript Fast Mode实现**: `.joycode/docs/index.ts`
- **现有MCP工具**: `aicoding_backend/main.py`中的工具注册和实现
- **提示词模板**: `aicoding_backend/prompts/`目录下的现有模板

### 外部依赖识别
- **Java项目结构分析**: 需要调用MCP工具分析Java项目的Maven/Gradle结构
- **代码库扫描**: 需要使用代码搜索工具识别现有的Java类和方法
- **依赖管理**: 识别项目中使用的Spring Boot、MyBatis等框架

## 注意事项

### **缺少的关键模板提示词**
1. **Java快速编码主模板** - 缺少`java_fast_coding.py`或对应的提示词文件
2. **Java设计文档生成模板** - 缺少Java项目特定的设计文档模板
3. **Java代码实现指导模板** - 缺少基于设计文档的Java代码实现指导
4. **Java项目结构分析模板** - 缺少Java项目特定的代码库分析提示词
5. **Java组件生成模板** - 缺少Controller、Service、Repository等组件的生成模板

### **技术实现风险**
- **框架适配**: 必须适配Spring Boot、MyBatis、Maven/Gradle等Java生态工具
- **代码规范一致性**: 生成的代码必须符合项目现有的编码规范和架构模式
- **依赖管理**: 自动识别和处理Java项目的依赖关系和版本兼容性
- **测试代码生成**: 必须同时生成对应的JUnit测试代码

### **关键实现要求**
- **必须在`aicoding_backend/main.py`中注册新的MCP工具**
- **必须创建`aicoding_backend/prompts/java_fast_coding.py`提示词文件**
- **必须支持Java项目的Maven/Gradle构建工具**
- **必须集成现有的Java测试模板**(`java_test_*.md`)
- **必须遵循项目的异步函数和错误处理规范**

### **质量保证要求**  
- **代码生成质量**: 生成的Java代码必须通过编译和基础测试
- **模板变量替换**: 所有模板中的占位符必须被实际内容替换
- **错误处理**: 必须包含完整的异常处理和用户友好的错误消息
- **日志记录**: 必须调用`log_report`工具记录使用情况

### **开发优先级**
1. **高优先级**: 创建基础的Java快速编码工具和核心提示词模板
2. **中优先级**: 实现Java项目结构分析和代码复用识别功能  
3. **低优先级**: 优化生成代码的质量和添加高级功能特性