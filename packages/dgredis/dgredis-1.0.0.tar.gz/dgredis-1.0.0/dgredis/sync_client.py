import json
import re
from contextlib import contextmanager
from datetime import date, datetime
from typing import Any

import redis

from .decorator import is_connected
from .conf import RedisConfig
from .encoder import DateTimeEncoder


class RedisClient:
    encoder = DateTimeEncoder()
    iso_date_pattern = re.compile(
        r'^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?)?$'
    )

    def __init__(self, cfg: RedisConfig | None = None):
        self.client: redis.Redis | None = (self.connect(cfg) if cfg else None)
        self.cfg: RedisConfig | None = cfg

    def connect(self, cfg: RedisConfig):
        self.client = redis.Redis(
            host=cfg.host,
            port=cfg.port,
            password=cfg.password,
            decode_responses=True,
            db=cfg.db,
            client_name=cfg.client_name
        )
        return self.client

    @is_connected
    def close(self):
        self.client.close()

    def _serialize(self, value: Any) -> Any:
        if isinstance(value, (dict, list, tuple, set, date, datetime)):
            return json.loads(self.encoder.encode(value))
        return value

    def _deserialize(self, data: Any) -> Any:
        if isinstance(data, str) and self.iso_date_pattern.match(data):
            try:
                if 'T' in data:
                    return datetime.fromisoformat(data.replace('Z', '+00:00'))
                return date.fromisoformat(data)
            except ValueError:
                return data
        elif isinstance(data, dict):
            return {k: self._deserialize(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._deserialize(item) for item in data]
        return data

    @is_connected
    def get_json_key(self, key: str) -> Any:
        result = self.client.json().get(key)
        return self._deserialize(result)

    @is_connected
    def set_json_key(self, key: str, value: Any, ttl: int = None):
        serialized_value = self._serialize(value)
        self.client.json().set(key, "$", serialized_value)
        if ttl:
            self.set_ttl(key, ttl)

    @is_connected
    def get_key(self, key: str) -> Any:
        value = self.client.get(key)
        if value is not None:
            try:
                # Пробуем десериализовать JSON строку
                json_value = json.loads(value)
                return self._deserialize(json_value)
            except json.JSONDecodeError:
                # Если это не JSON, проверяем на дату/время
                return self._deserialize(value)
        return value

    @is_connected
    def set_key(self, key: str, value: Any, ttl: int = None):
        if isinstance(value, (dict, list, tuple, set, date, datetime)):
            value = self.encoder.encode(value)
        return self.client.set(key, value, ex=ttl)

    @is_connected
    def remove_key(self, key: str):
        self.client.delete(key)

    @is_connected
    def get_key_type(self, key: str) -> str:
        return self.client.type(key)

    @is_connected
    def exists(self, key: str) -> bool:
        return self.client.exists(key)

    @is_connected
    def set_ttl(self, key: str, ttl: int):
        self.client.expire(key, ttl)

    @is_connected
    def get_ttl(self, key: str) -> int:
        return self.client.ttl(key)

    @is_connected
    def multiple_set(self, data: dict[str, Any], ttl: int = None):
        self.client.mset(data)
        for k in data.keys():
            self.set_ttl(k, ttl)

    @is_connected
    def multiple_get(self, *args):
        values = self.client.mget(*args)
        return dict(zip(args, values))

    @contextmanager
    def connected(self, cfg: RedisConfig):
        self.client = self.connect(cfg)
        try:
            yield self
        finally:
            self.close()

    def __enter__(self):
        if self.client is None and self.cfg is not None:
            self.connect(self.cfg)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @is_connected
    def set(self, key: str, value: Any, ttl: int = None):
        if isinstance(value, (dict, list, tuple, set)):
            self.set_json_key(key, value, ttl)
        else:
            self.set_key(key, value, ttl)

    @is_connected
    def get(self, key: str) -> Any:
        try:
            value = self.get_json_key(key)
        except redis.exceptions.ResponseError:
            value = self.get_key(key)
        return value
