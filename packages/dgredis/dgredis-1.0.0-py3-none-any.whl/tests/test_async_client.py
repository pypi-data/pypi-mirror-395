import asyncio

from dgredis import RedisConfig, AsyncRedisClient


async def test_async_client():
    rconf = RedisConfig(
        host="localhost",
        port=6379,
        db=1,
        client_name="dgredis_test"
    )
    async with AsyncRedisClient(cfg=rconf) as client:
        await client.set_key("test_async", "this is a async client test", ttl=60)
        assert await client.get_key("test_async") == "this is a async client test"
        print("assert true")


async def test_async_json_str():
    rconf = RedisConfig(
        host="localhost",
        port=6379,
        db=1,
        client_name="dgredis_test"
    )
    async with (AsyncRedisClient(cfg=rconf) as client):
        await client.set_json_str_key("test_async_json", {"value": 'this is a async client test 2'}, ttl=60)
        v = await client.get_json_str_key("test_async_json")
        assert v and v.get("value") == "this is a async client test 2"
        print("assert true")


async def test_async_json_native():
    rconf = RedisConfig(
        host="localhost",
        port=6379,
        db=1,
        client_name="dgredis_test"
    )
    async with (AsyncRedisClient(cfg=rconf) as client):
        await client.set_json_key("test_async_json_native", {"value": 'this is a async client test 2'}, ttl=60)
        v = await client.get_json_key("test_async_json_native")
        assert v and v.get("value") == "this is a async client test 2"
        print("assert true")


if __name__ == '__main__':
    asyncio.run(test_async_client())
    asyncio.run(test_async_json_str())
    asyncio.run(test_async_json_native())
