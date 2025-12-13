import dataclasses


@dataclasses.dataclass
class RedisConfig:
    host: str
    port: int
    password: str | None = None
    db: int = 0
    client_name: str = 'dgredis'