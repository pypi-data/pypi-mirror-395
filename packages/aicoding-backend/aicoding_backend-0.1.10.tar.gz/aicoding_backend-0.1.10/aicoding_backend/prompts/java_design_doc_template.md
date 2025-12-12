# Java 快速编码设计文档

## 需求描述
**用户需求**: {user_input}
**修改类型**: {modify_type}

## 影响范围

### 主要修改文件
- **{main_file_1}**: {main_file_1_reason}
- **{main_file_2}**: {main_file_2_reason}
- **{main_file_3}**: {main_file_3_reason}

### 关联文件
- **{related_file_1}**: {related_file_1_reason}
- **{related_file_2}**: {related_file_2_reason}

## 复用资源

### 参考实现
- **{reference_file_1}**: {reference_description_1}
- **{reference_file_2}**: {reference_description_2}

### 可复用组件/类
- **{reusable_component_1}**: {component_description_1}
- **{reusable_component_2}**: {component_description_2}

## Java 实现步骤

### 步骤 1: Entity/DO 层实现
**目标**: 创建/修改数据实体类
**文件**: {entity_file_path}
**改动点**:
- {entity_change_1}
- {entity_change_2}

**关键代码片段**:
```java
{entity_code_snippet}
```

### 步骤 2: Repository 层实现
**目标**: 实现数据访问层
**文件**: {repository_file_path}
**改动点**:
- {repository_change_1}
- {repository_change_2}

**关键代码片段**:
```java
{repository_code_snippet}
```

### 步骤 3: Service 层实现
**目标**: 实现业务逻辑层
**文件**: {service_file_path}
**改动点**:
- {service_change_1}
- {service_change_2}

**关键代码片段**:
```java
{service_code_snippet}
```

### 步骤 4: Controller 层实现
**目标**: 实现控制器层
**文件**: {controller_file_path}
**改动点**:
- {controller_change_1}
- {controller_change_2}

**关键代码片段**:
```java
{controller_code_snippet}
```

### 步骤 5: DTO/VO 类实现
**目标**: 创建数据传输对象
**文件**: {dto_file_path}
**改动点**:
- {dto_change_1}
- {dto_change_2}

**关键代码片段**:
```java
{dto_code_snippet}
```

## 验证清单

### 功能验证
- [ ] {functional_test_1}
- [ ] {functional_test_2}
- [ ] {functional_test_3}

### 编译测试
- [ ] Maven/Gradle 编译通过: `{compile_command}`
- [ ] 单元测试执行: `{test_command}`
- [ ] 集成测试验证: `{integration_test}`

### 手动测试场景
1. **{test_scenario_1}**
   - 操作: {test_operation_1}
   - 预期结果: {test_expected_1}

2. **{test_scenario_2}**
   - 操作: {test_operation_2}
   - 预期结果: {test_expected_2}

## 注意事项

### Java 编码规范
- {coding_standard_1}
- {coding_standard_2}
- {coding_standard_3}

### 框架特定注意事项
- **Spring Boot**: {spring_boot_note}
- **MyBatis/JPA**: {orm_note}
- **Maven/Gradle**: {build_tool_note}

### 依赖管理
- **新增依赖**: {new_dependency}
- **版本兼容性**: {version_compatibility}
- **配置文件修改**: {config_changes}

## 技术栈信息

### 当前项目技术栈
- **构建工具**: {build_tool}
- **Java 版本**: {java_version}
- **Spring Boot 版本**: {spring_boot_version}
- **数据库**: {database}
- **ORM 框架**: {orm_framework}

### 项目结构
```
{project_structure}