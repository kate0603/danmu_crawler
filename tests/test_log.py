# -*- coding: utf-8 -*-
"""
    Created by w at 2024/2/27.
    Description:
    Changelog: all notable changes to this file will be documented
"""
import unittest
from datetime import datetime, timedelta
from utils.live_log import LiveLog


class TestLog(unittest.TestCase):

    def setUp(self) -> None:
        pass

    @unittest.skip("直接跳过测试")
    def test_read_live_chat(self):
        obj = LiveLog(2211)
        print(
            obj.read_live_chat(
                start_time=datetime.now() + timedelta(days=-1), end_time=datetime.now()
            )
        )

    @unittest.skip("直接跳过测试")
    def test_read_live_info(self):
        obj = LiveLog(2211)
        print(obj.read_live_info(platform="抖音"))

    @unittest.skip("直接跳过测试")
    def test_write_chat(self):
        obj = LiveLog(2211)
        data = [
            {
                "platform": "douyin",
                "room_id": "1",
                "user_id": 1,
                "user_name": "t",
                "msg": "test",
                "log_time": datetime.now(),
            }
        ]
        obj.write_chat(data=data)
