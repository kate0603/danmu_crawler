# -*- coding: utf-8 -*-
"""
    Created by w at 2024/2/27.
    Description:
    Changelog: all notable changes to this file will be documented
"""
import unittest


class TestProxyPool(unittest.TestCase):

    def setUp(self) -> None:
        pass

    @unittest.skip("直接跳过测试")
    def test_check(self):
        from proxy_pool.scheduler import __runProxyCheck

        __runProxyCheck()

    @unittest.skip("直接跳过测试")
    def test_proxy_count(self):
        from proxy_pool.scheduler import get_proxy_count

        print(get_proxy_count())

    @unittest.skip("直接跳过测试")
    def test_proxy_count(self):
        from proxy_pool.scheduler import delete_proxy

        proxy = {
            "proxy": "8.219.97.248:80",
            "https": True,
            "fail_count": 0,
            "region": "中国 中国  阿里云",
            "anonymous": "",
            "source": "freeProxy11",
            "check_count": 5,
            "last_status": True,
            "last_time": "2024-02-22 09:49:06",
        }
        delete_proxy(proxy=proxy)
