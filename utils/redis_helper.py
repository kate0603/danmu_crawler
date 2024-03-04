# -*- coding: utf-8 -*-
"""
    Created by w at 2024/2/26.
    Description:
    Changelog: all notable changes to this file will be documented
"""
import redis
from config import Config


class RedisHelper(object):
    def __init__(self):
        redis_info: dict = Config().redis()
        pool = redis.ConnectionPool(
            host=redis_info["host"],
            port=redis_info["port"],
            decode_responses=True,
            db=redis_info["db"],
        )
        self.r = redis.Redis(connection_pool=pool)

    def append(self, name: str, value):
        self.r.append(key=name, value=value)

    def set(self, name: str, value):
        self.r.set(name=name, value=value)

    def get(self, name: str):
        return self.r.get(name=name)

    def rpush(self, name: str, value):
        self.r.rpush(name, value)

    def rpop(self, name: str):
        return self.r.rpop(name=name)

    def flushall(self):
        self.r.flushall()

    def sadd(self, name: str, value: list):
        self.r.sadd(name, *value)

    def spop(self, name: str, count: int = 10):
        return self.r.spop(name=name, count=count)
