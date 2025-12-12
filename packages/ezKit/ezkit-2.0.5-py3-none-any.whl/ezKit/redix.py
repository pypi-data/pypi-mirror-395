"""Redis Library"""

import random

from os import environ
from typing import Any

import orjson
import redis

from loguru import logger

# --------------------------------------------------------------------------------------------------

DEBUG = environ.get("DEBUG")

# --------------------------------------------------------------------------------------------------


class RedisClient:
    """Redis Client"""

    def __init__(self, url: str, **kwargs):

        self.pool = redis.ConnectionPool.from_url(
            url,
            **{
                "max_connections": 20,  # 生产环境建议设置
                "retry_on_timeout": True,  # 超时重试
                "decode_responses": True,  # 自动解码为字符串
                **kwargs,
            }
        )
        self.client = redis.Redis(connection_pool=self.pool)

    # ---------- String ----------
    def set(self, key: str, value: Any, ex: int | None = None, random_ttl: bool = False):

        try:

            if random_ttl and ex:
                ex = ex + random.randint(1, 300)
            if not isinstance(value, str):
                # value = json.dumps(value)
                # pylint: disable=E1101
                value = orjson.dumps(value).decode()
                # pylint: enable=E1101
            return self.client.set(key, value, ex=ex)

        except Exception as e:
            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)
            return None

    def get(self, key: str):
        try:
            return self.client.get(key)
        except Exception as e:
            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)
            return None

    # ---------- Hash ----------
    def hset(self, key: str, mapping: dict):
        try:
            return self.client.hset(key, mapping=mapping)
        except Exception as e:
            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)
            return None

    def hgetall(self, key: str):
        try:
            return self.client.hgetall(key)
        except Exception as e:
            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)
            return None

    # ---------- List ----------
    def push(self, key: str, *values):
        try:
            return self.client.rpush(key, *values)
        except Exception as e:
            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)
            return None

    def pop(self, key: str):
        try:
            return self.client.lpop(key)
        except Exception as e:
            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)
            return None

    # ---------- Set ----------
    def sadd(self, key: str, *values):
        try:
            return self.client.sadd(key, *values)
        except Exception as e:
            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)
            return None

    def sismember(self, key: str, value):
        try:
            return self.client.sismember(key, value)
        except Exception as e:
            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)
            return None

    # ---------- Atomic ops ----------
    def incr(self, key: str, step: int = 1):
        try:
            return self.client.incrby(key, step)
        except Exception as e:
            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)
            return None

    # ---------- Lock ----------
    def lock(self, key: str, timeout=5):
        try:
            return self.client.lock(key, timeout=timeout)
        except Exception as e:
            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)
            return None

    # ---------- Scan ----------
    def scan(self, pattern: str):

        # for key in self.client.scan_iter(pattern):
        #     yield key

        # https://pylint.readthedocs.io/en/latest/user_guide/messages/refactor/use-yield-from.html
        yield from self.client.scan_iter(pattern)
