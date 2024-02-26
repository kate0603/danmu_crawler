# -*- coding: utf-8 -*-
import logging
import os

import json
from kazoo.protocol.states import EventType, KazooState

from .zk_sdk import ServiceRegister


class ZKConfig:
    NODE_ERROR = "zk:get config error"
    NODE_ERROR_CHANGE = "zk:change config error"
    NODE_LOSE = "zk:restart get config error"
    NODE_SUSPENDED = "zk:suspended get config error"
    service = None

    def __init__(self, ZK_HOSTS, ZK_PATH, ZK_AUTH, callback):
        self.ZK_HOSTS = ZK_HOSTS
        self.ZK_PATH = ZK_PATH
        self.ZK_AUTH = ZK_AUTH
        self.callback = callback
        self.config = self.get_zk_config()

    def get_zk_config(self):
        try:
            self.service = ServiceRegister(self.ZK_HOSTS, auth_data=self.ZK_AUTH, read_only=True)
            data, ver = self.service.get(self.ZK_PATH, self.watcher)
            config = json.loads(data)
            return config
        except Exception as e:
            logging.error(self.NODE_ERROR)
            os._exit(0)

    # 当数据发生变化时会调用，data为新的数据
    def watcher(self, data, stat, event):
        if event is None:
            return
        if event.type == EventType.CHANGED:
            try:
                self.config = json.loads(data)
                self.callback(self.config)
            except Exception as e:
                logging.warning(self.NODE_ERROR_CHANGE)
        if event.state == KazooState.LOST or event.state == KazooState.SUSPENDED:
            try:
                self.service = ServiceRegister(self.ZK_HOSTS, auth_data=self.ZK_AUTH, read_only=True)
            except Exception:
                if event.state == KazooState.LOST:
                    logging.warning(self.NODE_LOSE)
                else:
                    logging.warning(self.NODE_SUSPENDED)
