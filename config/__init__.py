# -*- coding: utf-8 -*-
"""
    Created by w at 2024/2/19.
    Description:
    Changelog: all notable changes to this file will be documented
"""
import os
from config.zk_data import ZKConfig
from utils.decorator import singleton

# 连接时长
SOCKET_TIMES = 60 * 30
# 代理池 redis配置
REDIS_DB_CONN = "redis://xx.xx.xx.xx:6379/10"
# 最大并发的任务数量
TASK_MAX = 100

# zk
ENV = os.getenv("ENV", "DEV")
ZK_HOSTS = os.getenv("ZK_HOSTS_PUBLIC", "xx")
ZK_PATH = os.getenv("ZK_PATH_PUBLIC", f"xx")
ZK_AUTH = os.getenv("ZK_AUTH", "xx")


@singleton
class Config(object):
    def __init__(self):
        self.config = ZKConfig(ZK_HOSTS, ZK_PATH, ZK_AUTH, self.callback).config

    def callback(self, config):
        self.config = config

    def db_dws(self, game_id):
        return self.config.get(str(game_id), {}).get("db_dws")

    def redis(self):
        return self.config.get(
            "redis_info", {"host": "xx.xx.xx.xx", "port": 6379, "db": 11}
        )

    def proxy(self):
        return self.config.get(
            "proxy_info", {"type": "http", "host": "xx.xx.xx.xx", "port": 7777}
        )
