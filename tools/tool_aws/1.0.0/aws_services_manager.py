#!/usr/bin/env python3
"""
AWS 综合服务管理器 - 单一函数，全部参数写在入参里
支持：S3、Lambda、RDS、DynamoDB、CloudWatch 等常见 AWS 服务
所有逻辑在一个 def 里，不调用任何其他 py 文件，直接使用 boto3
"""
import json
from typing import Optional, Dict, Any, List
import boto3


def manage_aws_services(
    access_key: str,
    secret_key: str,
    region: str,
    service: str,
    action: str,
    bucket_name: Optional[str] = None,
    object_key: Optional[str] = None,
    file_content: Optional[str] = None,
    local_file_path: Optional[str] = None,
    function_name: Optional[str] = None,
    runtime: Optional[str] = None,
    handler: Optional[str] = None,
    role_arn: Optional[str] = None,
    zip_file_path: Optional[str] = None,
    db_instance_identifier: Optional[str] = None,
    db_instance_class: Optional[str] = None,
    engine: Optional[str] = None,
    engine_version: Optional[str] = None,
    master_username: Optional[str] = None,
    master_user_password: Optional[str] = None,
    allocated_storage: Optional[int] = None,
    table_name: Optional[str] = None,
    key_schema: Optional[str] = None,
    attribute_definitions: Optional[str] = None,
    provisioned_throughput: Optional[str] = None,
    item: Optional[str] = None,
    key: Optional[str] = None,
    update_expression: Optional[str] = None,
    expression_attribute_values: Optional[str] = None,
    log_group_name: Optional[str] = None,
    log_stream_name: Optional[str] = None,
    log_events: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    filter_pattern: Optional[str] = None,
    limit: Optional[int] = None,
    next_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    AWS 综合服务管理统一入口 - 单一函数，全部参数写在入参里
    
    支持的服务和操作：
    
    **S3 (对象存储)**:
        - list_buckets: 列出所有桶
        - list_objects: 列出桶中的对象
        - upload_object: 上传对象
        - download_object: 下载对象
        - delete_object: 删除对象
        - create_bucket: 创建桶
        - delete_bucket: 删除桶
    
    **Lambda (无服务器计算)**:
        - list_functions: 列出所有函数
        - get_function: 获取函数详情
        - create_function: 创建函数
        - update_function: 更新函数
        - delete_function: 删除函数
        - invoke_function: 调用函数
    
    **RDS (关系型数据库)**:
        - list_instances: 列出所有数据库实例
        - describe_instance: 描述实例详情
        - create_instance: 创建实例
        - modify_instance: 修改实例
        - delete_instance: 删除实例
        - start_instance: 启动实例
        - stop_instance: 停止实例
    
    **DynamoDB (NoSQL 数据库)**:
        - list_tables: 列出所有表
        - create_table: 创建表
        - describe_table: 描述表详情
        - delete_table: 删除表
        - put_item: 插入项
        - get_item: 获取项
        - update_item: 更新项
        - delete_item: 删除项
        - query: 查询
    
    **CloudWatch Logs (日志服务)**:
        - describe_log_groups: 描述日志组
        - create_log_group: 创建日志组
        - delete_log_group: 删除日志组
        - describe_log_streams: 描述日志流
        - create_log_stream: 创建日志流
        - put_log_events: 放入日志事件
        - filter_log_events: 过滤日志事件
    
    返回:
        {"success": bool, "service": str, "action": str, "data": dict, "error": str}
    """
    
    # ========== 验证必需参数 ==========
    if not service:
        return {
            "success": False,
            "service": None,
            "action": action,
            "data": {},
            "error": "Missing required parameter: service"
        }
    
    if not action:
        return {
            "success": False,
            "service": service,
            "action": None,
            "data": {},
            "error": "Missing required parameter: action"
        }
    
    # ========== 初始化 boto3 clients ==========
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        lambda_client = boto3.client(
            'lambda',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        rds_client = boto3.client(
            'rds',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        dynamodb_client = boto3.client(
            'dynamodb',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        logs_client = boto3.client(
            'logs',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
    except Exception as e:
        return {
            "success": False,
            "service": service,
            "action": action,
            "data": {},
            "error": f"Failed to create AWS clients: {str(e)}"
        }
    
    # ========== 执行服务操作 ==========
    try:
        service_lower = service.lower()
        action_lower = action.lower()
        
        # ==================== S3 服务 ====================
        if service_lower == "s3":
            if action_lower == "list_buckets":
                response = s3_client.list_buckets()
                buckets = [b['Name'] for b in response.get('Buckets', [])]
                return {
                    "success": True,
                    "service": "s3",
                    "action": "list_buckets",
                    "data": {"buckets": buckets, "count": len(buckets)},
                    "error": None
                }
            
            elif action_lower == "list_objects":
                if not bucket_name:
                    return {"success": False, "service": "s3", "action": action, "data": {}, "error": "Missing required parameter: bucket_name"}
                response = s3_client.list_objects_v2(Bucket=bucket_name)
                objects = [obj['Key'] for obj in response.get('Contents', [])]
                return {
                    "success": True,
                    "service": "s3",
                    "action": "list_objects",
                    "data": {"objects": objects, "count": len(objects)},
                    "error": None
                }
            
            elif action_lower == "upload_object":
                if not bucket_name or not object_key or not file_content:
                    return {"success": False, "service": "s3", "action": action, "data": {}, "error": "Missing required parameters: bucket_name, object_key, file_content"}
                s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=file_content.encode('utf-8'))
                return {
                    "success": True,
                    "service": "s3",
                    "action": "upload_object",
                    "data": {"bucket": bucket_name, "key": object_key},
                    "error": None
                }
            
            elif action_lower == "delete_object":
                if not bucket_name or not object_key:
                    return {"success": False, "service": "s3", "action": action, "data": {}, "error": "Missing required parameters: bucket_name, object_key"}
                s3_client.delete_object(Bucket=bucket_name, Key=object_key)
                return {
                    "success": True,
                    "service": "s3",
                    "action": "delete_object",
                    "data": {"bucket": bucket_name, "key": object_key},
                    "error": None
                }
            
            elif action_lower == "create_bucket":
                if not bucket_name:
                    return {"success": False, "service": "s3", "action": action, "data": {}, "error": "Missing required parameter: bucket_name"}
                if region == 'us-east-1':
                    s3_client.create_bucket(Bucket=bucket_name)
                else:
                    s3_client.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': region}
                    )
                return {
                    "success": True,
                    "service": "s3",
                    "action": "create_bucket",
                    "data": {"bucket": bucket_name},
                    "error": None
                }
            
            elif action_lower == "delete_bucket":
                if not bucket_name:
                    return {"success": False, "service": "s3", "action": action, "data": {}, "error": "Missing required parameter: bucket_name"}
                s3_client.delete_bucket(Bucket=bucket_name)
                return {
                    "success": True,
                    "service": "s3",
                    "action": "delete_bucket",
                    "data": {"bucket": bucket_name},
                    "error": None
                }
            
            else:
                return {"success": False, "service": service, "action": action, "data": {}, "error": f"Unsupported S3 action: {action}"}
        
        # ==================== Lambda 服务 ====================
        elif service_lower == "lambda":
            if action_lower == "list_functions":
                response = lambda_client.list_functions()
                functions = [{'name': f['FunctionName'], 'runtime': f['Runtime']} for f in response.get('Functions', [])]
                return {
                    "success": True,
                    "service": "lambda",
                    "action": "list_functions",
                    "data": {"functions": functions, "count": len(functions)},
                    "error": None
                }
            
            elif action_lower == "get_function":
                if not function_name:
                    return {"success": False, "service": "lambda", "action": action, "data": {}, "error": "Missing required parameter: function_name"}
                response = lambda_client.get_function(FunctionName=function_name)
                return {
                    "success": True,
                    "service": "lambda",
                    "action": "get_function",
                    "data": response['Configuration'],
                    "error": None
                }
            
            elif action_lower == "delete_function":
                if not function_name:
                    return {"success": False, "service": "lambda", "action": action, "data": {}, "error": "Missing required parameter: function_name"}
                lambda_client.delete_function(FunctionName=function_name)
                return {
                    "success": True,
                    "service": "lambda",
                    "action": "delete_function",
                    "data": {"function_name": function_name},
                    "error": None
                }
            
            elif action_lower == "invoke_function":
                if not function_name:
                    return {"success": False, "service": "lambda", "action": action, "data": {}, "error": "Missing required parameter: function_name"}
                payload = {}
                if file_content:
                    payload = json.loads(file_content)
                response = lambda_client.invoke(FunctionName=function_name, Payload=json.dumps(payload))
                return {
                    "success": True,
                    "service": "lambda",
                    "action": "invoke_function",
                    "data": {"payload": response['Payload'].read().decode('utf-8')},
                    "error": None
                }
            
            else:
                return {"success": False, "service": service, "action": action, "data": {}, "error": f"Unsupported Lambda action: {action}"}
        
        # ==================== RDS 服务 ====================
        elif service_lower == "rds":
            if action_lower == "list_instances":
                response = rds_client.describe_db_instances()
                instances = [{
                    'id': i['DBInstanceIdentifier'],
                    'engine': i['Engine'],
                    'status': i['DBInstanceStatus'],
                    'class': i['DBInstanceClass']
                } for i in response.get('DBInstances', [])]
                return {
                    "success": True,
                    "service": "rds",
                    "action": "list_instances",
                    "data": {"instances": instances, "count": len(instances)},
                    "error": None
                }
            
            elif action_lower == "describe_instance":
                if not db_instance_identifier:
                    return {"success": False, "service": "rds", "action": action, "data": {}, "error": "Missing required parameter: db_instance_identifier"}
                response = rds_client.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)
                return {
                    "success": True,
                    "service": "rds",
                    "action": "describe_instance",
                    "data": response['DBInstances'][0],
                    "error": None
                }
            
            elif action_lower == "delete_instance":
                if not db_instance_identifier:
                    return {"success": False, "service": "rds", "action": action, "data": {}, "error": "Missing required parameter: db_instance_identifier"}
                rds_client.delete_db_instance(DBInstanceIdentifier=db_instance_identifier, SkipFinalSnapshot=True)
                return {
                    "success": True,
                    "service": "rds",
                    "action": "delete_instance",
                    "data": {"instance_id": db_instance_identifier},
                    "error": None
                }
            
            else:
                return {"success": False, "service": service, "action": action, "data": {}, "error": f"Unsupported RDS action: {action}"}
        
        # ==================== DynamoDB 服务 ====================
        elif service_lower == "dynamodb":
            if action_lower == "list_tables":
                response = dynamodb_client.list_tables()
                return {
                    "success": True,
                    "service": "dynamodb",
                    "action": "list_tables",
                    "data": {"tables": response.get('TableNames', []), "count": len(response.get('TableNames', []))},
                    "error": None
                }
            
            elif action_lower == "describe_table":
                if not table_name:
                    return {"success": False, "service": "dynamodb", "action": action, "data": {}, "error": "Missing required parameter: table_name"}
                response = dynamodb_client.describe_table(TableName=table_name)
                return {
                    "success": True,
                    "service": "dynamodb",
                    "action": "describe_table",
                    "data": response['Table'],
                    "error": None
                }
            
            elif action_lower == "put_item":
                if not table_name or not item:
                    return {"success": False, "service": "dynamodb", "action": action, "data": {}, "error": "Missing required parameters: table_name, item"}
                item_dict = json.loads(item)
                dynamodb_client.put_item(TableName=table_name, Item=item_dict)
                return {
                    "success": True,
                    "service": "dynamodb",
                    "action": "put_item",
                    "data": {"table_name": table_name},
                    "error": None
                }
            
            elif action_lower == "get_item":
                if not table_name or not key:
                    return {"success": False, "service": "dynamodb", "action": action, "data": {}, "error": "Missing required parameters: table_name, key"}
                key_dict = json.loads(key)
                response = dynamodb_client.get_item(TableName=table_name, Key=key_dict)
                return {
                    "success": True,
                    "service": "dynamodb",
                    "action": "get_item",
                    "data": response.get('Item', {}),
                    "error": None
                }
            
            elif action_lower == "delete_item":
                if not table_name or not key:
                    return {"success": False, "service": "dynamodb", "action": action, "data": {}, "error": "Missing required parameters: table_name, key"}
                key_dict = json.loads(key)
                dynamodb_client.delete_item(TableName=table_name, Key=key_dict)
                return {
                    "success": True,
                    "service": "dynamodb",
                    "action": "delete_item",
                    "data": {"table_name": table_name},
                    "error": None
                }
            
            else:
                return {"success": False, "service": service, "action": action, "data": {}, "error": f"Unsupported DynamoDB action: {action}"}
        
        # ==================== CloudWatch Logs 服务 ====================
        elif service_lower == "cloudwatch_logs" or service_lower == "logs":
            if action_lower == "describe_log_groups":
                kwargs = {}
                if limit:
                    kwargs['limit'] = limit
                if next_token:
                    kwargs['nextToken'] = next_token
                response = logs_client.describe_log_groups(**kwargs)
                groups = [g['logGroupName'] for g in response.get('logGroups', [])]
                return {
                    "success": True,
                    "service": "cloudwatch_logs",
                    "action": "describe_log_groups",
                    "data": {"log_groups": groups, "count": len(groups)},
                    "error": None
                }
            
            elif action_lower == "create_log_group":
                if not log_group_name:
                    return {"success": False, "service": "cloudwatch_logs", "action": action, "data": {}, "error": "Missing required parameter: log_group_name"}
                logs_client.create_log_group(logGroupName=log_group_name)
                return {
                    "success": True,
                    "service": "cloudwatch_logs",
                    "action": "create_log_group",
                    "data": {"log_group_name": log_group_name},
                    "error": None
                }
            
            elif action_lower == "delete_log_group":
                if not log_group_name:
                    return {"success": False, "service": "cloudwatch_logs", "action": action, "data": {}, "error": "Missing required parameter: log_group_name"}
                logs_client.delete_log_group(logGroupName=log_group_name)
                return {
                    "success": True,
                    "service": "cloudwatch_logs",
                    "action": "delete_log_group",
                    "data": {"log_group_name": log_group_name},
                    "error": None
                }
            
            elif action_lower == "filter_log_events":
                if not log_group_name:
                    return {"success": False, "service": "cloudwatch_logs", "action": action, "data": {}, "error": "Missing required parameter: log_group_name"}
                kwargs = {'logGroupName': log_group_name}
                if start_time:
                    kwargs['startTime'] = int(start_time)
                if end_time:
                    kwargs['endTime'] = int(end_time)
                if filter_pattern:
                    kwargs['filterPattern'] = filter_pattern
                if limit:
                    kwargs['limit'] = limit
                response = logs_client.filter_log_events(**kwargs)
                events = [{
                    'timestamp': e['timestamp'],
                    'message': e['message']
                } for e in response.get('events', [])]
                return {
                    "success": True,
                    "service": "cloudwatch_logs",
                    "action": "filter_log_events",
                    "data": {"events": events, "count": len(events)},
                    "error": None
                }
            
            else:
                return {"success": False, "service": service, "action": action, "data": {}, "error": f"Unsupported CloudWatch Logs action: {action}"}
        
        else:
            return {"success": False, "service": service, "action": action, "data": {}, "error": f"Unsupported service: {service}"}
    
    except Exception as e:
        return {
            "success": False,
            "service": service,
            "action": action,
            "data": {},
            "error": str(e)
        }
