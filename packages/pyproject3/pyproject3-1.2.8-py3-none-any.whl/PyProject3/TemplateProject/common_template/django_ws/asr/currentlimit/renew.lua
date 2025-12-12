--[[ 对 session_id 进行续约。

KEYS:
    KEYS[1]，总 session 集合名。
    KEYS[2]，当前 asr app 的 session 集合名。

ARGV:
    ARGV[1]，为 session_id。
    ARGV[2]，过期时长。

return:
    1，续约成功
    -1，续约失败，session_id 已经过期或不存在了。
]]

local cur_time = tonumber(redis.call("TIME")[1])
-- ARGV[2] 秒没续费，说明过期了
if redis.call("ZREMRANGEBYSCORE", KEYS[1], 0, cur_time - tonumber(ARGV[2])) > 0 then
    redis.call("ZREMRANGEBYSCORE", KEYS[2], 0, cur_time - tonumber(ARGV[2]))
end
-- 如何总集合中不存在，说明它以及过期了
if redis.call("ZSCORE", KEYS[1], ARGV[1]) == nil then
    -- 在总集合中不存在，顺便把它从 app_id 的集合中删除
    redis.call("ZREM", KEYS[2], ARGV[1])
    return -1
end
-- 续约，把 session_id 对应的 score 设置为当前时间
redis.call("ZADD", KEYS[1], cur_time, ARGV[1])
redis.call("ZADD", KEYS[2], cur_time, ARGV[1])
return 1
