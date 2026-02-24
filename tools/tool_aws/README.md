# AWS 综合服务管理工具

通过单一接口管理多种 AWS 服务，支持 S3、Lambda、RDS、DynamoDB、CloudWatch Logs 等主流服务。

## 功能特性

### 支持的服务

- ✅ **S3** - 对象存储服务（7 个操作）
- ✅ **Lambda** - 无服务器计算（6 个操作）
- ✅ **RDS** - 关系型数据库（7 个操作）
- ✅ **DynamoDB** - NoSQL 数据库（9 个操作）
- ✅ **CloudWatch Logs** - 日志服务（7 个操作）

### 核心优势

- 🔐 **安全凭证** - AK/SK 通过参数传入，不存储在代码中
- 🎯 **统一接口** - 单一函数管理所有 AWS 服务
- 📝 **完整文档** - 详细的参数说明和使用示例
- ⚡ **即开即用** - 无需额外配置，直接调用

## 输入参数

### 全局必需参数（所有服务都需要）

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_key | string | ✅ | AWS Access Key ID |
| secret_key | string | ✅ | AWS Secret Access Key |
| region | string | ✅ | AWS 区域，如 `us-east-1` |
| service | string | ✅ | 服务名称：`s3`/`lambda`/`rds`/`dynamodb`/`cloudwatch_logs` |
| action | string | ✅ | 操作名称，如 `list_buckets`/`create_function` 等 |

### 各服务特有参数

详见 [AWS_SERVICES_PARAMS.md](AWS_SERVICES_PARAMS.md)，包含每个服务的详细参数说明和必填要求。

## 调用示例

### S3 - 列出所有桶

```python
result = manage_aws_services(
    access_key="AKIAIOSFODNN7EXAMPLE",
    secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    region="us-east-1",
    service="s3",
    action="list_buckets"
)
```

### S3 - 上传对象

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

### Lambda - 列出所有函数

```python
result = manage_aws_services(
    access_key="AKIAIOSFODNN7EXAMPLE",
    secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    region="us-east-1",
    service="lambda",
    action="list_functions"
)
```

### DynamoDB - 插入数据

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

### CloudWatch Logs - 查询日志

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

## 输出结果

所有操作都返回统一格式：

```json
{
    "success": true,
    "service": "s3",
    "action": "list_buckets",
    "data": {
        "buckets": ["bucket1", "bucket2"],
        "count": 2
    },
    "error": null
}
```

失败时：

```json
{
    "success": false,
    "service": "s3",
    "action": "list_buckets",
    "data": {},
    "error": "Missing required parameter: access_key"
}
```

## 依赖安装

```bash
pip install boto3
```

## 文件说明

- `1.0.0/ec2_manager.py` - EC2 管理工具（保留向后兼容）
- `1.0.0/aws_services_manager.py` - AWS 综合服务管理器（新增）
- `AWS_SERVICES_PARAMS.md` - 详细参数说明文档
- `data.yaml` - 工具元数据配置

## 注意事项

1. **权限管理** - 确保提供的凭证具有执行相应操作的最小权限
2. **区域选择** - 不同服务在不同区域的可用性可能不同
3. **JSON 参数** - 复杂参数（如 item、key 等）需要传入 JSON 格式字符串
4. **错误处理** - 建议在使用时添加异常处理逻辑
5. **凭证安全** - 不要将凭证硬编码在代码中，建议使用环境变量
6. **详细文档** - 完整参数说明请查看 [AWS_SERVICES_PARAMS.md](AWS_SERVICES_PARAMS.md)
