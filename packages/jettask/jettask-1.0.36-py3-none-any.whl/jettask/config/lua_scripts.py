"""
Redis Lua 脚本定义

集中管理所有的 Redis Lua 脚本，用于原子操作和性能优化
"""

# Lua脚本：原子获取并删除结果
# 用于获取任务结果后立即删除，避免多次读取
LUA_SCRIPT_GET_AND_DELETE = """
local key = KEYS[1]
local value = redis.call('GET', key)
if value then
    redis.call('DEL', key)
end
return value
"""

# Lua脚本：批量发送任务（简化版，已被LUA_SCRIPT_NORMAL_TASKS替代）
# 保留用于兼容性
LUA_SCRIPT_BATCH_SEND = """
local stream_key = KEYS[1]
local task_name = ARGV[1]
local count = 0

for i = 2, #ARGV do
    redis.call('XADD', stream_key, '*', 'task_name', task_name, 'message', ARGV[i])
    count = count + 1
end

return count
"""


# Lua脚本：批量发送事件
# 用于 _batch_send_event 和 _batch_send_event_sync 方法
# 批量发送消息到Stream并自动生成offset，同时注册队列
LUA_SCRIPT_BATCH_SEND_EVENT = """
local stream_key = KEYS[1]
local prefix = ARGV[1]
local results = {}

-- 使用Hash存储所有队列的offset
local offsets_hash = prefix .. ':QUEUE_OFFSETS'

-- 从stream_key中提取队列名（去掉prefix:QUEUE:前缀）
local queue_name = string.gsub(stream_key, '^' .. prefix .. ':QUEUE:', '')

-- 将队列添加到全局队列注册表（包括所有队列，包括优先级队列）
local queues_registry_key = prefix .. ':REGISTRY:QUEUES'
redis.call('SADD', queues_registry_key, queue_name)

-- 从ARGV[2]开始，每个参数是一个消息的data
for i = 2, #ARGV do
    local data = ARGV[i]

    -- 使用HINCRBY原子递增offset（如果不存在会自动创建并设为1）
    local current_offset = redis.call('HINCRBY', offsets_hash, queue_name, 1)

    -- 添加消息到Stream（包含offset字段）
    local stream_id = redis.call('XADD', stream_key, '*',
        'data', data,
        'offset', current_offset)

    table.insert(results, stream_id)
end

return results
"""

__all__ = [
    'LUA_SCRIPT_GET_AND_DELETE',
    'LUA_SCRIPT_BATCH_SEND',
    'LUA_SCRIPT_BATCH_SEND_EVENT',
]
