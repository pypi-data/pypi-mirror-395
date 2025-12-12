from dgredis import RedisClient, RedisConfig
from time import sleep


def test_context_manager():
    rconf = RedisConfig(
        host='localhost',
        port=6379,
        db=1,
        client_name='dgredis_test'
    )
    with RedisClient().connected(cfg=rconf) as client:
        client.set_key('test', 'this is a context manager test 1', ttl=60)
        assert client.get_key('test') == 'this is a context manager test 1'
        print("assert true")


def test_context_manager2():
    rconf = RedisConfig(
        host='localhost',
        port=6379,
        db=1,
        client_name='dgredis_test'
    )
    with RedisClient(cfg=rconf) as client:
        client.set_key('test', 'this is a context manager test 2', ttl=60)
        assert client.get_key('test') == 'this is a context manager test 2'
        print("assert true")


if __name__ == '__main__':
    test_context_manager()
    test_context_manager2()
