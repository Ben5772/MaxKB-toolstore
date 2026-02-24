# AWS 服务参数说明文档

## 必需参数（所有服务都需要）

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| `access_key` | `str` | ✅ 是 | AWS Access Key ID | `"AKIAIOSFODNN7EXAMPLE"` |
| `secret_key` | `str` | ✅ 是 | AWS Secret Access Key | `"wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"` |
| `region` | `str` | ✅ 是 | AWS 区域 | `"us-east-1"`, `"ap-northeast-1"` |
| `service` | `str` | ✅ 是 | 服务名称 | `"s3"`, `"lambda"`, `"rds"`, `"dynamodb"`, `"cloudwatch_logs"` |
| `action` | `str` | ✅ 是 | 操作名称 | `"list_buckets"`, `"create_function"` 等 |

---

## S3 (对象存储服务)

### 基础参数

| 参数名 | 类型 | 必填 | 说明 | 默认值 |
|--------|------|------|------|--------|
| `bucket_name` | `str` | 条件必填 | S3 桶名称 | - |
| `object_key` | `str` | 条件必填 | 对象键（文件路径） | - |
| `file_content` | `str` | 条件必填 | 文件内容（上传时使用） | - |

### 支持的操作

#### 1. list_buckets - 列出所有桶
- **必需参数**: 无（只需要全局必需参数）
- **返回**: 桶列表和数量

#### 2. list_objects - 列出桶中的对象
- **必需参数**: 
  - `bucket_name` (是)
- **返回**: 对象键列表和数量

#### 3. upload_object - 上传对象
- **必需参数**: 
  - `bucket_name` (是)
  - `object_key` (是)
  - `file_content` (是)
- **返回**: 上传成功信息

#### 4. download_object - 下载对象
- **必需参数**: 
  - `bucket_name` (是)
  - `object_key` (是)
- **返回**: 文件内容

#### 5. delete_object - 删除对象
- **必需参数**: 
  - `bucket_name` (是)
  - `object_key` (是)
- **返回**: 删除成功信息

#### 6. create_bucket - 创建桶
- **必需参数**: 
  - `bucket_name` (是)
- **返回**: 创建的桶信息

#### 7. delete_bucket - 删除桶
- **必需参数**: 
  - `bucket_name` (是)
- **返回**: 删除成功信息

---

## Lambda (无服务器计算服务)

### 基础参数

| 参数名 | 类型 | 必填 | 说明 | 默认值 |
|--------|------|------|------|--------|
| `function_name` | `str` | 条件必填 | Lambda 函数名称 | - |
| `runtime` | `str` | 条件必填 | 运行时环境 | - |
| `handler` | `str` | 条件必填 | 函数处理程序 | - |
| `role_arn` | `str` | 条件必填 | IAM 角色 ARN | - |
| `zip_file_path` | `str` | 条件必填 | 部署包路径 | - |

### 支持的操作

#### 1. list_functions - 列出所有函数
- **必需参数**: 无
- **返回**: 函数列表（名称、运行时）

#### 2. get_function - 获取函数详情
- **必需参数**: 
  - `function_name` (是)
- **返回**: 函数配置详情

#### 3. create_function - 创建函数
- **必需参数**: 
  - `function_name` (是)
  - `runtime` (是)
  - `handler` (是)
  - `role_arn` (是)
  - `zip_file_path` (是)
- **返回**: 创建的函数信息

#### 4. update_function - 更新函数
- **必需参数**: 
  - `function_name` (是)
  - `zip_file_path` (是)
- **返回**: 更新后的函数信息

#### 5. delete_function - 删除函数
- **必需参数**: 
  - `function_name` (是)
- **返回**: 删除成功信息

#### 6. invoke_function - 调用函数
- **必需参数**: 
  - `function_name` (是)
- **可选参数**: 
  - `file_content` (否) - 调用 payload（JSON 格式）
- **返回**: 函数执行结果

---

## RDS (关系型数据库服务)

### 基础参数

| 参数名 | 类型 | 必填 | 说明 | 默认值 |
|--------|------|------|------|--------|
| `db_instance_identifier` | `str` | 条件必填 | 数据库实例标识符 | - |
| `db_instance_class` | `str` | 条件必填 | 实例类型 | `"db.t2.micro"` |
| `engine` | `str` | 条件必填 | 数据库引擎 | - |
| `engine_version` | `str` | 条件必填 | 引擎版本 | - |
| `master_username` | `str` | 条件必填 | 主用户名 | - |
| `master_user_password` | `str` | 条件必填 | 主用户密码 | - |
| `allocated_storage` | `int` | 条件必填 | 存储大小 (GB) | - |

### 支持的操作

#### 1. list_instances - 列出所有数据库实例
- **必需参数**: 无
- **返回**: 实例列表（ID、引擎、状态、类型）

#### 2. describe_instance - 描述实例详情
- **必需参数**: 
  - `db_instance_identifier` (是)
- **返回**: 实例完整配置

#### 3. create_instance - 创建实例
- **必需参数**: 
  - `db_instance_identifier` (是)
  - `db_instance_class` (是)
  - `engine` (是)
  - `master_username` (是)
  - `master_user_password` (是)
  - `allocated_storage` (是)
- **可选参数**: 
  - `engine_version` (否)
- **返回**: 创建的实例信息

#### 4. modify_instance - 修改实例
- **必需参数**: 
  - `db_instance_identifier` (是)
  - `db_instance_class` (是)
- **返回**: 修改后的实例信息

#### 5. delete_instance - 删除实例
- **必需参数**: 
  - `db_instance_identifier` (是)
- **返回**: 删除成功信息

#### 6. start_instance - 启动实例
- **必需参数**: 
  - `db_instance_identifier` (是)
- **返回**: 启动成功信息

#### 7. stop_instance - 停止实例
- **必需参数**: 
  - `db_instance_identifier` (是)
- **返回**: 停止成功信息

---

## DynamoDB (NoSQL 数据库服务)

### 基础参数

| 参数名 | 类型 | 必填 | 说明 | 默认值 |
|--------|------|------|------|--------|
| `table_name` | `str` | 条件必填 | 表名 | - |
| `key_schema` | `str` | 条件必填 | 键模式（JSON 格式） | - |
| `attribute_definitions` | `str` | 条件必填 | 属性定义（JSON 格式） | - |
| `provisioned_throughput` | `str` | 条件必填 | 预置吞吐量（JSON 格式） | - |
| `item` | `str` | 条件必填 | 项数据（JSON 格式） | - |
| `key` | `str` | 条件必填 | 主键（JSON 格式） | - |
| `update_expression` | `str` | 条件必填 | 更新表达式 | - |
| `expression_attribute_values` | `str` | 条件必填 | 表达式属性值（JSON 格式） | - |

### 支持的操作

#### 1. list_tables - 列出所有表
- **必需参数**: 无
- **返回**: 表名列表和数量

#### 2. create_table - 创建表
- **必需参数**: 
  - `table_name` (是)
  - `key_schema` (是)
  - `attribute_definitions` (是)
  - `provisioned_throughput` (是)
- **返回**: 创建的表信息

#### 3. describe_table - 描述表详情
- **必需参数**: 
  - `table_name` (是)
- **返回**: 表完整配置

#### 4. delete_table - 删除表
- **必需参数**: 
  - `table_name` (是)
- **返回**: 删除成功信息

#### 5. put_item - 插入项
- **必需参数**: 
  - `table_name` (是)
  - `item` (是) - JSON 格式
- **返回**: 插入成功信息

#### 6. get_item - 获取项
- **必需参数**: 
  - `table_name` (是)
  - `key` (是) - JSON 格式
- **返回**: 项数据

#### 7. update_item - 更新项
- **必需参数**: 
  - `table_name` (是)
  - `key` (是)
  - `update_expression` (是)
  - `expression_attribute_values` (是)
- **返回**: 更新后的项信息

#### 8. delete_item - 删除项
- **必需参数**: 
  - `table_name` (是)
  - `key` (是)
- **返回**: 删除成功信息

#### 9. query - 查询
- **必需参数**: 
  - `table_name` (是)
  - `key` (是)
- **返回**: 查询结果列表

---

## CloudWatch Logs (日志服务)

### 基础参数

| 参数名 | 类型 | 必填 | 说明 | 默认值 |
|--------|------|------|------|--------|
| `log_group_name` | `str` | 条件必填 | 日志组名称 | - |
| `log_stream_name` | `str` | 条件必填 | 日志流名称 | - |
| `log_events` | `str` | 条件必填 | 日志事件（JSON 格式） | - |
| `start_time` | `str` | 条件必填 | 开始时间（毫秒时间戳） | - |
| `end_time` | `str` | 条件必填 | 结束时间（毫秒时间戳） | - |
| `filter_pattern` | `str` | 条件必填 | 过滤模式 | - |
| `limit` | `int` | 条件必填 | 返回数量限制 | - |
| `next_token` | `str` | 条件必填 | 分页令牌 | - |

### 支持的操作

#### 1. describe_log_groups - 描述日志组
- **必需参数**: 无
- **可选参数**: 
  - `limit` (否)
  - `next_token` (否)
- **返回**: 日志组列表和数量

#### 2. create_log_group - 创建日志组
- **必需参数**: 
  - `log_group_name` (是)
- **返回**: 创建成功信息

#### 3. delete_log_group - 删除日志组
- **必需参数**: 
  - `log_group_name` (是)
- **返回**: 删除成功信息

#### 4. describe_log_streams - 描述日志流
- **必需参数**: 
  - `log_group_name` (是)
- **可选参数**: 
  - `limit` (否)
  - `next_token` (否)
- **返回**: 日志流列表

#### 5. create_log_stream - 创建日志流
- **必需参数**: 
  - `log_group_name` (是)
  - `log_stream_name` (是)
- **返回**: 创建成功信息

#### 6. put_log_events - 放入日志事件
- **必需参数**: 
  - `log_group_name` (是)
  - `log_stream_name` (是)
  - `log_events` (是) - JSON 格式数组
- **返回**: 放入成功信息

#### 7. filter_log_events - 过滤日志事件
- **必需参数**: 
  - `log_group_name` (是)
- **可选参数**: 
  - `start_time` (否)
  - `end_time` (否)
  - `filter_pattern` (否)
  - `limit` (否)
- **返回**: 过滤后的日志事件列表

---

## 使用示例

### 示例 1: S3 - 列出所有桶
```python
result = manage_aws_services(
    access_key="AKIAIOSFODNN7EXAMPLE",
    secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    region="us-east-1",
    service="s3",
    action="list_buckets"
)
```

### 示例 2: S3 - 上传对象
```python
result = manage_aws_services(
    access_key="AKIAIOSFODNN7EXAMPLE",
    secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    region="us-east-1",
    service="s3",
    action="upload_object",
    bucket_name="my-bucket",
    object_key="path/to/file.txt",
    file_content="Hello, World!"
)
```

### 示例 3: Lambda - 列出所有函数
```python
result = manage_aws_services(
    access_key="AKIAIOSFODNN7EXAMPLE",
    secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    region="us-east-1",
    service="lambda",
    action="list_functions"
)
```

### 示例 4: DynamoDB - 插入项
```python
result = manage_aws_services(
    access_key="AKIAIOSFODNN7EXAMPLE",
    secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    region="us-east-1",
    service="dynamodb",
    action="put_item",
    table_name="Users",
    item='{"id": {"S": "123"}, "name": {"S": "John"}}'
)
```

### 示例 5: CloudWatch Logs - 查询日志
```python
result = manage_aws_services(
    access_key="AKIAIOSFODNN7EXAMPLE",
    secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    region="us-east-1",
    service="cloudwatch_logs",
    action="filter_log_events",
    log_group_name="/aws/lambda/my-function",
    start_time="1609459200000",
    end_time="1609545600000",
    filter_pattern="ERROR"
)
```

---

## 错误处理

所有操作都会返回统一格式的响应：

```python
{
    "success": True/False,
    "service": "服务名称",
    "action": "操作名称",
    "data": {...},  # 成功时返回数据
    "error": None/"错误信息"  # 失败时包含错误信息
}
```

---

## 注意事项

1. **凭证安全**: 不要将 AWS 凭证硬编码在代码中，建议使用环境变量或 AWS 配置文件
2. **权限管理**: 确保提供的凭证具有执行相应操作的最小权限
3. **区域选择**: 不同服务在不同区域的可用性可能不同
4. **JSON 参数**: 复杂的参数（如 item、key、key_schema 等）需要传入 JSON 格式的字符串
5. **异常处理**: 建议在使用时添加 try-except 块来捕获可能的异常
