# -*- coding: utf-8 -*-
"""
    Created by w at 2024/2/27.
    Description:
    Changelog: all notable changes to this file will be documented
"""
import unittest
from utils.redis_helper import RedisHelper


class TestRedis(unittest.TestCase):

    def setUp(self) -> None:
        pass

    @unittest.skip("直接跳过测试")
    def test_sadd(self):
        obj = RedisHelper()
        obj.sadd(name="douyin_webids", value=[5, 3, 5, 6])

    @unittest.skip("直接跳过测试")
    def test_spop(self):
        obj = RedisHelper()
        print(obj.spop(name="douyin_webids", count=2))

    @unittest.skip("直接跳过测试")
    def test_flushall(self):
        obj = RedisHelper()
        obj.flushall()
