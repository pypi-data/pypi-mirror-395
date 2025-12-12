import json
from typing import Any, Optional
from cachetools import TTLCache


DEFAULT_TTL = 3600


class BaseCache:
    """缓存接口"""
    is_async = False

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        raise NotImplementedError

    def get(self, key: str) -> Any:
        raise NotImplementedError

    def delete(self, key: str):
        raise NotImplementedError


# ---------------------
# 内存缓存
# ---------------------
class MemoryCache(BaseCache):
    is_async = False

    def __init__(self, maxsize: int = 1000, ttl: int = DEFAULT_TTL):
        self._cache = TTLCache(maxsize=maxsize, ttl=ttl)

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        # cachetools TTLCache 不支持 per-key TTL, 所以只使用全局 TTL
        self._cache[key] = value

    def get(self, key: str) -> Any:
        return self._cache.get(key)

    def delete(self, key: str):
        self._cache.pop(key, None)


# ---------------------
# Redis 缓存
# ---------------------
class RedisCache(BaseCache):
    """同步 Redis"""
    is_async = False

    def __init__(self, redis_client, ttl: int = DEFAULT_TTL):
        self.redis = redis_client
        self.ttl = ttl

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        ttl = ttl or self.ttl
        self.redis.setex(key, ttl, json.dumps(value))

    def get(self, key: str) -> Any:
        data = self.redis.get(key)
        if data:
            return json.loads(data)
        return None

    def delete(self, key: str):
        self.redis.delete(key)


class AsyncRedisCache(BaseCache):
    """异步 Redis"""
    is_async = True

    def __init__(self, redis_client, ttl: int = DEFAULT_TTL):
        self.redis = redis_client
        self.ttl = ttl

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        ttl = ttl or self.ttl
        await self.redis.setex(key, ttl, json.dumps(value))

    async def get(self, key: str) -> Any:
        data = await self.redis.get(key)
        if data:
            return json.loads(data)
        return None

    async def delete(self, key: str):
        await self.redis.delete(key)

