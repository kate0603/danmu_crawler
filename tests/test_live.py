# -*- coding: utf-8 -*-
"""
    Created by w at 2024/2/27.
    Description:
    Changelog: all notable changes to this file will be documented
"""
import unittest
from datetime import datetime

class TestLive(unittest.TestCase):

    def setUp(self) -> None:
        pass

    @unittest.skip("直接跳过测试")
    def test_cut_words(self):
        from live_main import cut_words

        cut_words(game_id=2211, start_time=datetime(2024, 2,27), end_time=datetime(2024, 2, 28))

    @unittest.skip("直接跳过测试")
    def test_redis_lock_release(self):
        from live_main import redis_lock_release

        redis_lock_release(lock_name="redis-lock-douyin")
        # redis_lock_release(lock_name="redis-lock-bilibili")

    @unittest.skip("直接跳过测试")
    def test_redis_put_ids(self):
        from live_main import redis_put_ids

        redis_put_ids(
            name="douyin_webids",
            value=[
                207569091371,

            ],
        )
        # redis_put_ids(
        #     name="bilibili_roomids",
        #     value=[
        #         31875914,
        #     ],
        # )

    @unittest.skip("直接跳过测试")
    def test_live(self):
        from live_main import live_douyin, live_bilibili

        live_douyin(game_id=2211)
        # live_bilibili(game_id=2211)
