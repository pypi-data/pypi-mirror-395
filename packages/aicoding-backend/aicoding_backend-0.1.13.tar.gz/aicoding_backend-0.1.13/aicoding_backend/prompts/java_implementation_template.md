# Java 快速编码实现指导

## 🎯 核心原则
1. **最小改动原则** - 只改必须改的，能复用就复用，不过度设计
2. **质量优先原则** - 确保正确性和类型安全，每步完成后立即验证
3. **渐进完善原则** - 核心功能 → 边界处理 → 体验优化

## 📋 Java 实现标准流程

### 🔍 步骤 1: 项目结构分析
**必做事项:**
1. 分析现有 Java 项目结构和技术栈
   - 识别 Maven/Gradle 构建工具
   - 确认 Spring Boot 版本和配置
   - 了解数据库访问层（MyBatis/JPA）
   - 检查现有的包结构和命名规范

2. 查找可复用的 Java 组件
   - 搜索类似的 Controller、Service、Repository 实现
   - 找出可直接复用的工具类和配置
   - 确保新代码风格与现有代码一致

### 🏗️ 步骤 2: 分层实现（严格按顺序）

#### 2.1 Entity/DO 层实现
**目标**: 创建/修改数据实体类
**规范要求**:
- 使用 JPA 注解（@Entity, @Table, @Id, @Column）
- 提供无参构造函数，字段使用包装类型
- 使用 Lombok @Getter/@Setter（避免 @Data 与 @Entity 混用）
- 添加 @JSONField 注解控制序列化顺序

**代码模板**:
```java
@Entity
@Table(name = "table_name")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class EntityDO implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @JSONField(ordinal = 1)
    private Long id;
    
    @Column(name = "field_name")
    @JSONField(ordinal = 2)
    @NotBlank(message = "字段不能为空")
    private String fieldName;
    
    @JSONField(ordinal = 100, format = "yyyy-MM-dd HH:mm:ss")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8")
    private LocalDateTime createTime;
}
```

#### 2.2 Repository 层实现
**目标**: 实现数据访问层
**规范要求**:
- 继承 JpaRepository 或使用 MyBatis @Mapper
- 方法命名遵循 Spring Data JPA 规范
- 复杂查询使用 @Query 注解或 XML 配置

**代码模板**:
```java
@Repository
public interface EntityRepository extends JpaRepository<EntityDO, Long> {
    
    List<EntityDO> findByFieldName(String fieldName);
    
    @Query("SELECT e FROM EntityDO e WHERE e.status = :status")
    List<EntityDO> findByStatus(@Param("status") Integer status);
}
```

#### 2.3 DTO/VO 类实现
**目标**: 创建数据传输对象
**规范要求**:
- DTO 用于 API 输入/输出，与 JPA 实体分离
- 使用 Bean Validation 注解进行校验
- 添加序列化注解和字段排序

**代码模板**:
```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class EntityDTO implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    @JSONField(ordinal = 1)
    private Long id;
    
    @JSONField(ordinal = 2)
    @NotBlank(message = "字段不能为空")
    @Size(max = 50, message = "长度不能超过50个字符")
    private String fieldName;
    
    @JSONField(ordinal = 100, format = "yyyy-MM-dd HH:mm:ss")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8")
    private LocalDateTime createTime;
}
```

#### 2.4 Service 层实现
**目标**: 实现业务逻辑层
**规范要求**:
- 使用 @Service 注解
- 通过 @Autowired 注入 Repository
- 实现业务逻辑和数据转换
- 添加事务注解 @Transactional

**代码模板**:
```java
@Service
@Slf4j
public class EntityService {
    
    @Autowired
    private EntityRepository entityRepository;
    
    @Transactional
    public EntityDTO createEntity(EntityDTO entityDTO) {
        try {
            // DTO 转 DO
            EntityDO entityDO = ConvertUtils.convert(entityDTO, EntityDO.class);
            entityDO.setCreateTime(LocalDateTime.now());
            
            // 保存到数据库
            EntityDO savedEntity = entityRepository.save(entityDO);
            
            // DO 转 DTO 返回
            return ConvertUtils.convert(savedEntity, EntityDTO.class);
        } catch (Exception e) {
            log.error("创建实体失败", e);
            throw new BusinessException("创建实体失败");
        }
    }
    
    public List<EntityDTO> findByFieldName(String fieldName) {
        List<EntityDO> entities = entityRepository.findByFieldName(fieldName);
        return ConvertUtils.convertList(entities, EntityDTO.class);
    }
}
```

#### 2.5 Controller 层实现
**目标**: 实现控制器层
**规范要求**:
- 使用 @RestController 注解
- RESTful API 设计规范
- 统一返回格式
- 参数校验和异常处理

**代码模板**:
```java
@RestController
@RequestMapping("/api/entities")
@Slf4j
public class EntityController {
    
    @Autowired
    private EntityService entityService;
    
    @PostMapping
    public Result<EntityDTO> createEntity(@Valid @RequestBody EntityDTO entityDTO) {
        try {
            EntityDTO result = entityService.createEntity(entityDTO);
            return Result.success(result);
        } catch (Exception e) {
            log.error("创建实体接口异常", e);
            return Result.error("创建失败");
        }
    }
    
    @GetMapping
    public Result<List<EntityDTO>> getEntities(@RequestParam String fieldName) {
        try {
            List<EntityDTO> results = entityService.findByFieldName(fieldName);
            return Result.success(results);
        } catch (Exception e) {
            log.error("查询实体列表异常", e);
            return Result.error("查询失败");
        }
    }
}
```

### 🧪 步骤 3: 测试代码生成
**必做事项**:
1. 使用现有 Java 测试模板生成对应测试
2. 生成 Controller、Service、Repository 三层测试
3. 确保测试代码覆盖主要业务场景

**测试生成命令**:
- Controller 测试：参考 `aicoding_backend/prompts/java_test_controller.md`
- Service 测试：参考 `aicoding_backend/prompts/java_test_service.md`  
- Repository 测试：参考 `aicoding_backend/prompts/java_test_repo.md`

### ✅ 步骤 4: 编译和验证
**验证清单**:
1. **编译检查**
   ```bash
   # Maven 项目
   mvn clean compile
   mvn test
   
   # Gradle 项目  
   ./gradlew build
   ./gradlew test
   ```

2. **代码质量检查**
   - 确保所有类都有适当的注解
   - 验证字段类型和验证注解
   - 检查异常处理和日志记录

3. **功能验证**
   - API 接口测试
   - 数据库操作验证
   - 业务逻辑正确性检查

## 🚨 Java 特有注意事项

### 编码规范
- **类名**: PascalCase (UserController, UserService)
- **方法和变量**: camelCase (getUserById, userName)
- **常量**: UPPER_SNAKE_CASE (MAX_SIZE, DEFAULT_VALUE)
- **包名**: 小写，用点分隔 (com.example.service)

### Spring Boot 特定注意事项
- @ConfigurationProperties 类必须提供 setter 方法
- @Component 扫描确保包路径正确
- 配置文件优先级：application-{profile}.yml > application.yml

### Hibernate/JPA 注意事项  
- 实体类必须提供无参构造函数
- 字段应使用包装类型（Integer 而非 int）
- 避免在实体类中使用 @Data 注解，建议使用 @Getter/@Setter

### MyBatis 注意事项
- Mapper 接口使用 @Mapper 注解
- XML 文件路径与接口包路径对应
- 参数使用 @Param 注解明确参数名

### 序列化注意事项
- 使用 @JSONField 控制字段序列化顺序
- 时间字段统一格式：yyyy-MM-dd HH:mm:ss
- 敏感字段使用 serialize = false 隐藏

## 🔧 工具类和配置

### 转换工具类使用
```java
// 单个对象转换
EntityDTO dto = ConvertUtils.convert(entityDO, EntityDTO.class);

// 列表转换  
List<EntityDTO> dtoList = ConvertUtils.convertList(doList, EntityDTO.class);

// 手动映射（复杂逻辑）
EntityVO vo = ConvertUtils.toVO(entityDO);
```

### 统一返回格式
```java
// 成功返回
return Result.success(data);

// 失败返回
return Result.error("错误信息");

// 分页返回
return Result.success(pageData, total);
```

## 📝 完成检查清单

### 代码质量
- [ ] 所有类都有适当的注解
- [ ] 异常处理完整
- [ ] 日志记录合理
- [ ] 代码格式规范

### 功能完整性  
- [ ] Entity/DO 层实现完整
- [ ] Repository 层数据访问正确
- [ ] Service 层业务逻辑正确
- [ ] Controller 层 API 设计规范
- [ ] DTO/VO 类数据传输正确

### 测试覆盖
- [ ] Controller 层测试
- [ ] Service 层测试  
- [ ] Repository 层测试
- [ ] 集成测试通过

### 编译验证
- [ ] Maven/Gradle 编译通过
- [ ] 单元测试执行成功
- [ ] 代码质量检查通过
- [ ] API 接口可正常访问

**[AI Agent Action]** 完成所有步骤后，请呼叫「log_report」工具进行本次工具使用记录上报