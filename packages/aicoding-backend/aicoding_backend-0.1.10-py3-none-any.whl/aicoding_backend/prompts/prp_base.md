名称: "基础 PRP 模板 v2 - 上下文丰富且带验证循环"
描述: |

## 目的
该模板专为 AI 代理优化，使其能够通过充分的上下文和自我验证能力，通过迭代改进实现可工作的代码。

## 核心原则
1. **上下文为王**: 包含所有必要的文档、示例和注意事项
2. **验证循环**: 提供 AI 可运行和修复的可执行测试/检查
3. **信息密集**: 使用代码库中的关键词和模式
4. **渐进式成功**: 从简单开始，验证后再增强
5. **全局规则**: 确保遵循 CLAUDE.md 中的所有规则

---

## 目标
[需要构建什么 - 明确说明最终状态和期望]

### 成功标准
- [ ] [具体的可衡量结果]

## 所有必需的上下文

### 文档和参考资料（列出实现功能所需的所有上下文）
```yaml
# 必读 - 将这些包含在您的上下文窗口中
- url: [官方 API 文档 URL]
  why: [您需要的具体章节/方法]
  
- file: [path/to/example.java]
  why: [要遵循的模式，要避免的陷阱]
  
- doc: [库文档 URL] 
  section: [关于常见陷阱的具体章节]
  critical: [防止常见错误的关键见解]

- docfile: [PRPs/ai_docs/file.md]
  why: [用户粘贴到项目中的文档]

```

### 当前代码库结构（在项目根目录运行 `tree` 命令）以获取代码库概览
```bash

```

### 期望的代码库结构（包含要添加的文件及文件职责）
```bash

```

### 已知的代码库陷阱和库怪癖  
```java
// 关键: [库名称] 需要 [特定设置/使用约定]
// 示例: Spring Boot 中 @ConfigurationProperties 类必须提供 setter 方法
// 示例: Hibernate 实体类必须提供无参构造函数，字段应使用包装类型（如 Integer 而非 int）
// 示例: 使用 Lombok 时，@Data 与 @Entity 混用可能导致 Hibernate 代理问题，建议改用 @Getter/@Setter
// 示例: Java 命名规范：类名 PascalCase，方法和变量 camelCase，常量 UPPER_SNAKE_CASE
// 示例: Optional 仅用于返回值，不应用于字段或方法参数
```

## 实施蓝图

### 数据模型和结构  

定义清晰、封装良好、类型安全的核心数据模型，确保与序列化和持久化框架兼容。

```java
示例:
 - 使用普通 Java 类（POJO）定义 DTO 和实体，提供 public 无参构造函数
 - 使用 Lombok @Getter/@Setter
 - 使用 enum 定义状态或分类常量，禁止使用字符串字面量
 - 实体类使用 JPA 注解（如 @Entity、@Table、@Id、@Column）
 - DTO 类用于 API 输入/输出，与 JPA 实体分离
 - 使用 Bean Validation 注解（如 @NotNull、@NotBlank、@Email）进行校验
 - 避免在模型中使用 Java 8 之后的语言特性（如 records、sealed classes）
```

### 按顺序完成 PRP 所需完成的任务列表

```yaml
任务 1:
修改 jd.gms.item.site.web/src/main/java/jd/gms/item/site/controller/task/TaskControllerNew.java:
  - 在addTaskV2方法中，submitTaskService.submitTask4File调用成功后
  - 添加缓存记录逻辑：RedisCacheUtil.hIncrBy("task:usage:stat:" + getUserCodeLowerCase(), type, 1L)
  - 添加try-catch块确保缓存失败不影响主流程
  - 添加适当的日志记录

任务 N:
...

```

### 每个任务所需的伪代码（根据需要添加到每个任务）
```java

// 任务 1 - 修改addTaskV2方法
public SiteResult addTaskV2(...) {
    // ... 现有代码 ...
    
    TaskResult taskResult = submitTaskService.submitTask4File(...);
    
    // 新增：记录任务使用统计
    try {
        if (taskResult.isSuccess()) {
            taskUsageStatService.recordTaskUsage(getUserCodeLowerCase(), type);
        }
    } catch (Exception e) {
        log.warn("记录任务使用统计失败，不影响主流程, erp={}, type={}", getUserCodeLowerCase(), type, e);
    }
    
    // ... 现有代码 ...
}
```

### 集成点
```yaml
缓存配置:
  - 使用现有RedisCacheUtil工具类
  - 缓存过期时间：30天
  - key命名规范：task:usage:stat:{erp}
  
依赖注入:
  - 在TaskControllerNew中添加TaskUsageStatService注入
  - 使用现有@Autowired注解模式
  
接口规范:
  - 查询接口：GET /new/task/getUsageStat?erp={erp}
  - 返回格式：SiteResult<TaskUsageStatDTO>
```

## 验证循环

### 级别 1: 语法和样式
```bash
# 编译检查
mvn compile -pl [本次生成、修改的代码文件]
# 预期: 无编译错误
```

```

## 最终验证清单
- [ ] 无 lint 错误
- [ ] 无类型错误
- [ ] 错误情况得到优雅处理
- [ ] 日志信息丰富但不冗长
- [ ] 文档已更新（如需要）

---

## 要避免的反模式
- ❌ 当现有模式有效时不要创建新模式
- ❌ 不要因为"应该可以工作"而跳过验证
- ❌ 不要忽略失败的测试 - 修复它们
- ❌ 不要在异步上下文中使用同步函数
- ❌ 不要硬编码应该是配置的值
- ❌ 不要捕获所有异常 - 要具体
- ❌ 忠实地理解用户所提出的需求，不要自主添加其他功能
