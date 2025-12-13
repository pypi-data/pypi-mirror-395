--[[ 删除 session_id。

KEYS:
    - KEYS[1]，当前 asr app 的 session 集合名。
    - KEYS[2]，总 session 集合名。

ARGV:
    - ARGV[1]，session_id。

return:
    - 1，删除成功
    - 0，删除失败，可能是本来不存在或过期了。
]]

if redis.call("ZREM", KEYS[1], ARGV[1]) > 0 then
    redis.call("ZREM",KEYS[2], ARGV[1])
    return 1
else
    return 0
end
