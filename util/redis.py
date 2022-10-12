import redis
import util.config as config

class RedisDB():
    def __init__(self):
        redis_pool = redis.ConnectionPool(host=config.REDIS_HOST, port=config.REDIS_PORT)
        self.__strict_redis = redis.StrictRedis(connection_pool=redis_pool)

    def set(self, key, value, expiry):
        self.__strict_redis.set(name=key, value=value, ex=expiry)

    def get(self, key):
        return self.__strict_redis.get(key)

    def ttl(self, key):
        return self.__strict_redis.ttl(key)


redis_db = RedisDB()