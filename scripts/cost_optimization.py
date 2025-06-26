#!/usr/bin/env python3
# 阿里云服务器成本优化工具

import json
import time
import logging
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.ModifyInstanceSpecRequest import ModifyInstanceSpecRequest

# 配置信息
ACCESS_KEY_ID = 'your_access_key_id'
ACCESS_KEY_SECRET = 'your_access_key_secret'
REGION_ID = 'cn-hangzhou'
LOW_USAGE_THRESHOLD = 30  # CPU使用率低于此值被认为是低负载(%)
HIGH_USAGE_THRESHOLD = 70 # CPU使用率高于此值被认为是高负载(%)
CHECK_INTERVAL = 86400    # 检查间隔(秒)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('cost_optimizer')

# 创建AcsClient实例
client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION_ID)

def get_instance_metrics(instance_id):
    """获取实例的性能指标"""
    # 这里应该调用阿里云监控API获取CPU使用率等指标
    # 简化示例，返回模拟数据
    import random
    return {
        'cpu_usage': random.uniform(10, 90),
        'memory_usage': random.uniform(20, 80),
        'disk_usage': random.uniform(10, 60)
    }

def get_instance_info():
    """获取所有实例信息"""
    request = DescribeInstancesRequest()
    request.set_accept_format('json')
    
    try:
        response = client.do_action_with_exception(request)
        instances = json.loads(response)['Instances']['Instance']
        return instances
    except Exception as e:
        logger.error(f"获取实例信息失败: {e}")
        return []

def optimize_instance(instance_id):
    """优化实例配置"""
    metrics = get_instance_metrics(instance_id)
    logger.info(f"实例 {instance_id} - CPU使用率: {metrics['cpu_usage']:.2f}%")
    
    # 根据CPU使用率调整实例规格
    if metrics['cpu_usage'] < LOW_USAGE_THRESHOLD:
        logger.info(f"实例 {instance_id} 负载较低，考虑降低配置")
        # 这里应该实现降低实例规格的逻辑
        # modify_instance_spec(instance_id, 'lower_spec')
    
    elif metrics['cpu_usage'] > HIGH_USAGE_THRESHOLD:
        logger.info(f"实例 {instance_id} 负载较高，考虑提高配置")
        # 这里应该实现提高实例规格的逻辑
        # modify_instance_spec(instance_id, 'higher_spec')
    
    else:
        logger.info(f"实例 {instance_id} 配置合适，无需调整")

def modify_instance_spec(instance_id, new_spec):
    """修改实例规格"""
    request = ModifyInstanceSpecRequest()
    request.set_accept_format('json')
    request.set_InstanceId(instance_id)
    request.set_InstanceType(new_spec)
    
    try:
        response = client.do_action_with_exception(request)
        logger.info(f"实例 {instance_id} 规格已修改为 {new_spec}")
        return json.loads(response)
    except Exception as e:
        logger.error(f"修改实例规格失败: {e}")
        return None

if __name__ == "__main__":
    logger.info("开始成本优化检查...")
    
    while True:
        instances = get_instance_info()
        for instance in instances:
            instance_id = instance['InstanceId']
            optimize_instance(instance_id)
        
        logger.info(f"成本优化检查完成，等待 {CHECK_INTERVAL/3600} 小时后再次检查")
        time.sleep(CHECK_INTERVAL)    