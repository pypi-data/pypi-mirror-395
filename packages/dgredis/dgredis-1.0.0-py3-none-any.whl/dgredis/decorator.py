def is_connected(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        if self.client is None:
            raise RuntimeError('Client is not connected')
        return func(*args, **kwargs)
    return wrapper


def is_connected_async(func):
    async def wrapper(*args, **kwargs):
        self = args[0]
        if self.client is None:
            raise RuntimeError('Client is not connected')
        return await func(*args, **kwargs)
    return wrapper
