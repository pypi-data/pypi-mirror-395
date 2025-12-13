# Coding Agent - DO/VO/DTO 类创建规范

## 1. 分层架构规范

### 1.1 DO (Data Object) - 数据对象
- **职责**: 与数据库表结构一一对应，用于数据持久化
- **命名规则**: `实体名DO` (如 UserDO, OrderDO)
- **位置**: `com.xxx.entity` 或 `com.xxx.domain`

### 1.2 DTO (Data Transfer Object) - 数据传输对象
- **职责**: 用于服务层之间数据传输，可能包含多个DO的组合
- **命名规则**: `实体名DTO` (如 UserDTO, OrderDTO)
- **位置**: `com.xxx.dto`

### 1.3 VO (Value Object) - 视图对象
- **职责**: 用于向前端展示，通常包含格式化后的数据
- **命名规则**: `实体名VO` (如 UserVO, OrderVO)
- **位置**: `com.xxx.vo`

### 1.4 BO (Business Object) - 业务对象
- **职责**: 封装业务逻辑，用于业务层
- **命名规则**: `实体名BO` (如 UserBO, OrderBO)
- **位置**: `com.xxx.bo`

## 2. 类结构规范

### 2.1 基础类结构模板

```java
import com.alibaba.fastjson.annotation.JSONField;
import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import javax.validation.constraints.*;
import java.io.Serializable;
import java.time.LocalDateTime;
import java.util.Date;

/**
 * 用户数据对象
 * @author Auto-Generated
 * @date 2025-01-01
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserDO implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    /**
     * 主键ID
     */
    @JSONField(ordinal = 1)
    private Long id;
    
    /**
     * 用户名
     */
    @JSONField(ordinal = 2)
    @NotBlank(message = "用户名不能为空")
    @Size(max = 50, message = "用户名长度不能超过50个字符")
    private String username;
    
    /**
     * 创建时间
     */
    @JSONField(ordinal = 100, format = "yyyy-MM-dd HH:mm:ss")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8")
    private LocalDateTime createTime;
    
    /**
     * 更新时间
     */
    @JSONField(ordinal = 101, format = "yyyy-MM-dd HH:mm:ss")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8")
    private LocalDateTime updateTime;
}
```

### 2.2 字段注解规范

```java
public class ExampleDTO {
    
    // 主键字段
    @JSONField(ordinal = 1)
    private Long id;
    
    // 必填字段
    @JSONField(ordinal = 2)
    @NotBlank(message = "字段不能为空")
    private String requiredField;
    
    // 可选字段
    @JSONField(ordinal = 3)
    private String optionalField;
    
    // 时间字段
    @JSONField(ordinal = 4, format = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createTime;
    
    // 隐藏字段（序列化时忽略）
    @JSONField(serialize = false)
    private String password;
    
    // 重命名字段
    @JSONField(name = "new_field_name")
    private String oldFieldName;
    
    // 格式化数字
    @JSONField(ordinal = 5, format = "#.##")
    private BigDecimal amount;
}
```

## 3. Alibaba FastJSON 序列化规范

### 3.1 依赖配置
```xml
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>fastjson</artifactId>
    <version>[具体的版本]</version>
</dependency>
```

### 3.2 序列化配置

```java
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.serializer.SerializeConfig;
import com.alibaba.fastjson.serializer.SerializerFeature;
import com.alibaba.fastjson.serializer.SimpleDateFormatSerializer;

public class JsonUtils {
    
    private static final SerializeConfig config = new SerializeConfig();
    
    static {
        // 配置日期格式
        config.put(LocalDateTime.class, new SimpleDateFormatSerializer("yyyy-MM-dd HH:mm:ss"));
        config.put(Date.class, new SimpleDateFormatSerializer("yyyy-MM-dd HH:mm:ss"));
    }
    
    /**
     * 对象转JSON字符串
     */
    public static String toJSONString(Object obj) {
        return JSON.toJSONString(obj, 
            config, 
            SerializerFeature.WriteMapNullValue,
            SerializerFeature.WriteNullStringAsEmpty,
            SerializerFeature.WriteNullListAsEmpty,
            SerializerFeature.DisableCircularReferenceDetect
        );
    }
    
    /**
     * JSON字符串转对象
     */
    public static <T> T parseObject(String json, Class<T> clazz) {
        return JSON.parseObject(json, clazz);
    }
    
    /**
     * JSON字符串转列表
     */
    public static <T> List<T> parseArray(String json, Class<T> clazz) {
        return JSON.parseArray(json, clazz);
    }
}
```

### 3.3 序列化注解使用规范

```java
public class UserVO {
    
    // 字段排序
    @JSONField(ordinal = 1)
    private Long id;
    
    // 日期格式化
    @JSONField(format = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createTime;
    
    // 忽略序列化
    @JSONField(serialize = false)
    private String password;
    
    // 忽略反序列化
    @JSONField(deserialize = false)
    private String computedField;
    
    // 自定义字段名
    @JSONField(name = "user_name")
    private String username;
    
    // 空值处理
    @JSONField(serialzeFeatures = SerializerFeature.WriteNullStringAsEmpty)
    private String description;
}
```

## 4. 转换工具类规范

### 4.1 DO/DTO/VO 转换工具

```java
import org.springframework.beans.BeanUtils;
import java.util.List;
import java.util.stream.Collectors;

public class ConvertUtils {
    
    /**
     * 单个对象转换
     */
    public static <T> T convert(Object source, Class<T> targetClass) {
        if (source == null) {
            return null;
        }
        try {
            T target = targetClass.newInstance();
            BeanUtils.copyProperties(source, target);
            return target;
        } catch (Exception e) {
            throw new RuntimeException("对象转换失败", e);
        }
    }
    
    /**
     * 列表转换
     */
    public static <T> List<T> convertList(List<?> sourceList, Class<T> targetClass) {
        if (sourceList == null || sourceList.isEmpty()) {
            return Collections.emptyList();
        }
        return sourceList.stream()
                .map(item -> convert(item, targetClass))
                .collect(Collectors.toList());
    }
    
    /**
     * 手动映射转换（复杂逻辑）
     */
    public static UserVO toVO(UserDO userDO) {
        if (userDO == null) {
            return null;
        }
        UserVO vo = new UserVO();
        vo.setId(userDO.getId());
        vo.setUsername(userDO.getUsername());
        vo.setCreateTime(userDO.getCreateTime());
        // 复杂转换逻辑
        vo.setStatusDesc(getStatusDescription(userDO.getStatus()));
        return vo;
    }
    
    private static String getStatusDescription(Integer status) {
        // 状态描述转换逻辑
        return switch (status) {
            case 1 -> "正常";
            case 0 -> "禁用";
            default -> "未知";
        };
    }
}
```

## 5. 命名规范

### 5.1 类命名
- DO: `实体名DO` (UserDO, OrderDO)
- DTO: `实体名DTO` (UserDTO, OrderDTO)  
- VO: `实体名VO` (UserVO, OrderVO)
- BO: `实体名BO` (UserBO, OrderBO)

### 5.2 字段命名
- 使用驼峰命名法
- Boolean字段避免使用is前缀
- 时间字段: `createTime`, `updateTime`, `deleteTime`
- 版本字段: `version`
- 乐观锁: `version`

## 6. 验证注解规范

```java
public class UserDTO {
    
    // 字符串验证
    @NotBlank(message = "用户名不能为空")
    @Size(max = 50, message = "用户名长度不能超过50个字符")
    private String username;
    
    // 数字验证
    @Min(value = 0, message = "年龄不能小于0")
    @Max(value = 150, message = "年龄不能大于150")
    private Integer age;
    
    // 邮箱验证
    @Email(message = "邮箱格式不正确")
    private String email;
    
    // 手机号验证
    @Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")
    private String phone;
    
    // 集合验证
    @Size(min = 1, max = 10, message = "列表大小必须在1-10之间")
    private List<String> tags;
    
    // 自定义验证
    @ValidStatus
    private Integer status;
}
```

## 7. 最佳实践

### 7.1 分层使用场景
- **DO**: 数据库操作、JPA实体
- **DTO**: Service层间调用、API入参
- **VO**: Controller返回给前端
- **BO**: 业务逻辑封装

### 7.2 序列化注意事项
- 始终实现`Serializable`接口
- 设置`serialVersionUID`
- 敏感字段使用`@JSONField(serialize = false)`
- 时间字段统一格式化

### 7.3 性能优化建议
- 使用Lombok减少样板代码
- 合理使用`@JSONField(ordinal)`优化序列化性能
- 避免循环引用导致的序列化问题

这个规范确保了代码的一致性、可维护性和性能，同时遵循了业界最佳实践。