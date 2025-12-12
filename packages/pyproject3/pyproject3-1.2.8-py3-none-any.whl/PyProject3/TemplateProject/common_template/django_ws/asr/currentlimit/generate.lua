--[[ 为当前 asr app 申请 session_id。
KEYS:
    KEYS[1]，总 session 集合名。
    KEYS[2]，当前 asr app 的 session 集合名。
    KEYS[3]，会话计数用的 key 名。

ARGV:
    ARGV[1]，app 的最大并发数。
    ARGV[2]，最大总并发数。
    ARGV[3]，整数，过期时长，单位秒。

return：
    字符串，session_id。
    -1，超过 app 的并发数。
    -2，超过总的并发数。
]]

local cur_time = tonumber(redis.call("TIME")[1])
-- 单个 app 的并发数限制
redis.call("ZREMRANGEBYSCORE", KEYS[2], 0, cur_time - tonumber(ARGV[3]))
local app_sessions = redis.call("ZCARD", KEYS[2])
if app_sessions >= tonumber(ARGV[1]) then
    return -1
end
-- 最大并发数限制
redis.call("ZREMRANGEBYSCORE", KEYS[1], 0, cur_time - tonumber(ARGV[3]))
local total_sessions = redis.call("ZCARD", KEYS[1])
if total_sessions >= tonumber(ARGV[2]) then
    return -2
end
-- 为 app 生成 session id，用当前时间 + 自增计数保证生成的 session_id 唯一
local sessions = redis.call("INCR", KEYS[3])
local session_id = string.format("%d-%d", cur_time, sessions)
redis.call("ZADD", KEYS[1], cur_time, session_id)
redis.call("ZADD", KEYS[2], cur_time, session_id)
return session_id
