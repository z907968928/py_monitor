# encoding: utf-8
import redis
from data_service_monitor.init.init_base import redis_conf


class RedisHandle(object):

    """ 定义一个 Redis 操作类"""
    def __init__(self, redis_name):
        REDIS = redis_conf()
        redis_host = REDIS[redis_name]['HOST']
        redis_port = REDIS[redis_name]['PORT']
        self.Redis = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


def monitor_redis():
    return RedisHandle('default').Redis
    # REDIS = redis_conf()
    # redis_host = REDIS['default']['HOST']
    # redis_port = REDIS['default']['PORT']
    # return redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
