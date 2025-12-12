from dgredis import RedisConfig, RedisClient


def test_auto_get_dict():
    rconf = RedisConfig(
        host='localhost',
        port=6379,
        db=1,
        client_name='dgredis_test'
    )
    with RedisClient(cfg=rconf) as client:
        client.set('test_json', {'value': 'test'}, ttl=60)
        res = client.get('test_json')
        assert res and res.get('value') == 'test'
        assert isinstance(res, dict)


def test_auto_get_list():
    rconf = RedisConfig(
        host='localhost',
        port=6379,
        db=1,
        client_name='dgredis_test'
    )
    with RedisClient(cfg=rconf) as client:
        client.set('test_list', [1, 2, 3], ttl=60)
        res = client.get('test_list')
        assert res and res == [1, 2, 3]
        assert isinstance(res, list)


if __name__ == '__main__':
    test_auto_get_dict()
    test_auto_get_list()