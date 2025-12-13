import json
from contextlib import asynccontextmanager
from datetime import date, datetime
from typing import Any

from .sync_client import RedisClient
from .conf import RedisConfig
from .decorator import is_connected_async

import redis.asyncio as redis


class AsyncRedisClient(RedisClient):
    def __init__(self, cfg: RedisConfig | None = None):
        self.client: redis.Redis | None = None
        self.cfg: RedisConfig | None = cfg

    async def connect(self, cfg: RedisConfig | None = None):
        self.client = redis.Redis(
            host=cfg.host,
            port=cfg.port,
            password=cfg.password,
            decode_responses=True,
            db=cfg.db,
            client_name=cfg.client_name
        )
        return self.client

    async def close(self):
        await self.client.close()

    @is_connected_async
    async def get_key(self, key: str) -> Any:
        value = await self.client.get(key)
        if value is not None:
            try:
                # Пробуем десериализовать JSON строку
                json_value = json.loads(value)
                return self._deserialize(json_value)
            except json.JSONDecodeError:
                # Если это не JSON, проверяем на дату/время
                return self._deserialize(value)
        return value

    @is_connected_async
    async def set_key(self, key: str, value: Any, ttl: int = None):
        if isinstance(value, (dict, list, tuple, set, date, datetime)):
            value = self.encoder.encode(value)
        await self.client.set(key, value, ex=ttl)

    @is_connected_async
    async def remove_key(self, key: str):
        await self.client.delete(key)

    def _serialize_to_json_string(self, value: Any) -> str:
        """Сериализация в JSON строку для Redis"""
        if isinstance(value, (dict, list, tuple, set, date, datetime)):
            return self.encoder.encode(value)  # Возвращает строку
        return str(value)

    @is_connected_async
    async def set_json_str_key(self, key: str, value: Any, ttl: int = None):
        serialized_value = self._serialize_to_json_string(value)
        await self.client.set(key, serialized_value)
        if ttl:
            await self.client.expire(key, ttl)

    @is_connected_async
    async def get_json_str_key(self, key: str) -> Any:
        result = await self.client.get(key)
        if result:
            try:
                json_data = json.loads(result)
                return self._deserialize(json_data)
            except json.JSONDecodeError:
                return self._deserialize(result)
        return result

    @is_connected_async
    async def set_json_key(self, key: str, value: Any, ttl: int = None):
        """Установить JSON через RedisJSON (JSON.SET команда)"""
        # RedisJSON ожидает объект Python (dict/list), не строку
        await self.client.json().set(key, "$", value)
        if ttl:
            await self.client.expire(key, ttl)

    @is_connected_async
    async def get_json_key(self, key: str) -> Any:
        """Получить JSON через RedisJSON (JSON.GET команда)"""
        result = await self.client.json().get(key)
        if result is not None:
            return self._deserialize(result)
        return result

    @is_connected_async
    async def get_key_type(self, key: str) -> str:
        return await self.client.type(key)

    @is_connected_async
    async def exists(self, key: str) -> bool:
        return await self.client.exists(key)

    @is_connected_async
    async def set_ttl(self, key: str, ttl: int):
        await self.client.expire(key, ttl)

    @is_connected_async
    async def get_ttl(self, key: str) -> int:
        return await self.client.ttl(key)

    @is_connected_async
    async def multiple_set(self, data: dict[str, Any], ttl: int = None):
        await self.client.mset(data)
        if ttl:
            for k in data.keys():
                await self.set_ttl(k, ttl)

    @is_connected_async
    async def multiple_get(self, *args):
        values = await self.client.mget(*args)
        return dict(zip(args, values))

    @asynccontextmanager
    async def connected(self, cfg: RedisConfig):
        self.client = await self.connect(cfg)
        try:
            yield self
        finally:
            await self.close()

    async def __aenter__(self):
        if self.client is None and self.cfg is not None:
            await self.connect(self.cfg)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    @is_connected_async
    async def set(self, key: str, value: Any, ttl: int = None):
        if isinstance(value, (dict, list, tuple, set)):
            await self.set_json_key(key, value, ttl)
        else:
            await self.set_key(key, value, ttl)

    @is_connected_async
    async def get(self, key: str) -> Any:
        try:
            value = await self.get_json_key(key)
        except redis.exceptions.ResponseError:
            value = await self.get_key(key)
        return value
