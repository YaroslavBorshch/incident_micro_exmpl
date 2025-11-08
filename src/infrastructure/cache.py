import redis.asyncio as redis
import json
from datetime import datetime, date
from typing import Optional, Any
from uuid import UUID
from src.core.config import settings


class CacheJSONEncoder(json.JSONEncoder):
    """кастомный JSON encoder для UUID и datetime"""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


class CacheClient:
    def __init__(self):
        self.client: Optional[redis.Redis] = None

    async def initialize(self):
        """подключение к redis"""

        try:
            self.client = await redis.from_url(settings.redis_url)
            await self.client.ping()
            print(f"Cache connected to Redis: {settings.redis_url}")
        except Exception as e:
            print(f"Cache connection failed: {e}")
            self.client = None

    async def close(self):
        """закрытие соединения с redis"""

        if self.client:
            await self.client.close()

    async def get(self, key: str) -> Optional[Any]:
        """получить значение из кеша"""

        if not self.client:
            return None
        try:
            value = await self.client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: int = 300):
        """сохранить значение в кеш"""

        if not self.client:
            print(f"Cache client not initialized")
            return False
        try:
            await self.client.setex(
                key, ttl, json.dumps(value, cls=CacheJSONEncoder)
            )
            return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False

    async def delete(self, key: str):
        """удалить ключ из кеша"""

        if not self.client:
            return False
        try:
            await self.client.delete(key)
            return True
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False


cache_client = CacheClient()
