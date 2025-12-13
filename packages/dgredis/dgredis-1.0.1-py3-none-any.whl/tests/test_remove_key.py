from dgredis import RedisConfig, RedisClient


def test_remove_simple_key():
    rconf = RedisConfig(
        host='localhost',
        port=6379,
        db=1
    )
    with RedisClient().connected(cfg=rconf) as client:
        client.set_key('test', 'this is a test 2 var')
        client.remove_key('test')
        assert client.get_key('test') is None


def test_remove_json_key():
    rconf = RedisConfig(
        host='localhost',
        port=6379,
        db=1
    )
    with RedisClient().connected(cfg=rconf) as client:
        client.set_json_key('test_json', {"value": "this is a test 2 var"})
        client.remove_key('test_json')
        assert client.get_key('test_json') is None


if __name__ == '__main__':
    test_remove_simple_key()
    test_remove_json_key()
