from dgredis.conf import RedisConfig
from dgredis import RedisClient


def test_db_index():
    rconf = RedisConfig(
        host='localhost',
        port=6379,
        db=1
    )
    client = RedisClient(cfg=rconf)
    client.set_key("test", "this is a test", ttl=60)
    assert client.get_key("test") == "this is a test"

if __name__ == '__main__':
    test_db_index()
