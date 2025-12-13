"""
JetTask 系统常量定义

集中管理所有系统级别的常量配置，包括：
- 内部消费者组
- 系统保留关键字
- 默认配置值
- 其他常量
"""

# ============================================================================
# 内部消费者组配置
# ============================================================================

# 内部消费者组前缀列表
# 任何以这些前缀开头的消费者组都会被视为内部消费者组，不会在用户界面显示
INTERNAL_CONSUMER_PREFIXES = [
    'pg_consumer_',      # PostgreSQL 消费者
    'webui_consumer_',   # WebUI 消费者
    'monitor_',          # 监控消费者
    'system_',           # 系统消费者
    '_internal_',        # 通用内部消费者
    '__',                # 双下划线开头的保留消费者
]

# 特定的内部消费者组名称（完全匹配）
INTERNAL_CONSUMER_NAMES = [
    'pg_consumer',       # 默认的 PostgreSQL 消费者
    'webui_consumer',    # 默认的 WebUI 消费者
    'system',            # 系统消费者
]


# ============================================================================
# 辅助函数
# ============================================================================

def is_internal_consumer(consumer_group: str) -> bool:
    """
    判断给定的消费者组是否为内部消费者组
    
    Args:
        consumer_group: 消费者组名称
        
    Returns:
        如果是内部消费者组返回 True，否则返回 False
    """
    if not consumer_group:
        return False
    
    # 转换为小写进行比较
    consumer_group_lower = consumer_group.lower()
    
    # 检查完全匹配（不区分大小写）
    for name in INTERNAL_CONSUMER_NAMES:
        if consumer_group_lower == name.lower():
            return True
    
    # 检查前缀匹配（不区分大小写）
    for prefix in INTERNAL_CONSUMER_PREFIXES:
        if consumer_group_lower.startswith(prefix.lower()):
            return True
    
    # 特殊处理：模糊匹配包含特定关键字的消费者组
    # 例如：pg_consumer 可能以不同格式出现，如 pg_consumer_YYDG_12345
    internal_keywords = [
        'pg_consumer',      # PostgreSQL 消费者的各种变体
        'webui_consumer',   # WebUI 消费者的各种变体
    ]
    
    for keyword in internal_keywords:
        if keyword in consumer_group_lower:
            return True
    
    return False
