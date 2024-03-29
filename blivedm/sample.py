# -*- coding: utf-8 -*-
import time
import redis_lock
import asyncio
import http.cookies
from typing import *
import aiohttp
import aiohttp_proxy
from datetime import datetime
import blivedm
import blivedm.models.web as web_models
from utils.live_log import LiveLog
from utils.redis_helper import RedisHelper

# 直播间一直存在，因此设定一个结束时间
from config import SOCKET_TIMES as TIMEOUT, TASK_MAX

# 这里填一个已登录账号的cookie。不填cookie也可以连接，但是收到弹幕的用户名会打码，UID会变成0
SESSDATA = "a2dc5e52%2C1722578108%2Cb6fb0%2A21CjDyvQ46HT-03Oy1s-CD9CwnqDVkOp--hRNKGYuU7T8MuRk_Ehulm5XAvXR7RIQ8m9ESVlpYczF3Rm5GU3QxOTJleEV1SzY1WHJEMUwyNzQzeHVQei1wWlRpNjIteFVERWdmeGpwN0NTaFlNZ1hjRl9uWUNwRnN4YUp5dGphaGF5ZUZhVEIwaG93IIEC"

session: Optional[aiohttp.ClientSession] = None


async def main(room_ids: list, game_id, sessdata=None):
    init_session(sessdata)
    try:
        await run_multi_clients(room_ids, game_id)
    finally:
        await session.close()


def init_session(sessdata):
    from config import Config

    proxy = Config().proxy()
    proxy_url = f"""{proxy["type"]}://{proxy["host"]}:{proxy["port"]}"""
    print("===bilibili代理地址", proxy_url)

    proxy = aiohttp_proxy.ProxyConnector.from_url(proxy_url)

    cookies = http.cookies.SimpleCookie()
    cookies["SESSDATA"] = sessdata or SESSDATA
    cookies["SESSDATA"]["domain"] = "bilibili.com"

    global session
    session = aiohttp.ClientSession(connector=proxy, trust_env=True)
    # session = aiohttp.ClientSession()
    session.cookie_jar.update_cookies(cookies)


async def run_multi_clients(room_ids, game_id):
    """
    演示同时监听多个直播间
    """
    clients = [blivedm.BLiveClient(room_id, session=session) for room_id in room_ids]
    handler = MyHandler(game_id)
    for client in clients:
        client.set_handler(handler)
        client.start()

    try:
        # await asyncio.gather(*(
        #     client.join() for client in clients
        # ))
        await asyncio.wait([client.join() for client in clients], timeout=TIMEOUT)
    finally:
        await asyncio.gather(*(client.stop_and_close() for client in clients))


class MyHandler(blivedm.BaseHandler):
    # # 演示如何添加自定义回调
    # _CMD_CALLBACK_DICT = blivedm.BaseHandler._CMD_CALLBACK_DICT.copy()
    #
    # # 入场消息回调
    # def __interact_word_callback(self, client: blivedm.BLiveClient, command: dict):
    #     print(f"[{client.room_id}] INTERACT_WORD: self_type={type(self).__name__}, room_id={client.room_id},"
    #           f" uname={command['data']['uname']}")
    # _CMD_CALLBACK_DICT['INTERACT_WORD'] = __interact_word_callback  # noqa
    def __init__(self, game_id):
        # super.__init__(blivedm.BaseHandler)
        self.game_id = game_id

    def _on_heartbeat(
        self, client: blivedm.BLiveClient, message: web_models.HeartbeatMessage
    ):
        # print(f"[{client.room_id}] 心跳")
        pass

    def _on_danmaku(
        self, client: blivedm.BLiveClient, message: web_models.DanmakuMessage
    ):
        # print(f"[{client.room_id}] {message.uname}：{message.msg}")
        LiveLog(game_id=self.game_id).write_chat(
            data={
                "platform": "bilibili",
                "room_id": client.room_id,
                "user_id": message.uid,
                "user_name": message.uname,
                "msg": message.msg,
                "log_time": datetime.now(),
            }
        )

    def _on_gift(self, client: blivedm.BLiveClient, message: web_models.GiftMessage):
        # print(
        #     f"[{client.room_id}] {message.uname} 赠送{message.gift_name}x{message.num}"
        #     f" （{message.coin_type}瓜子x{message.total_coin}）"
        # )
        pass

    def _on_buy_guard(
        self, client: blivedm.BLiveClient, message: web_models.GuardBuyMessage
    ):
        # print(f"[{client.room_id}] {message.username} 购买{message.gift_name}")
        pass

    def _on_super_chat(
        self, client: blivedm.BLiveClient, message: web_models.SuperChatMessage
    ):
        # print(
        #     f"[{client.room_id}] 醒目留言 ¥{message.price} {message.uname}：{message.message}"
        # )
        pass


def blive_run(game_id, sessdata: str = None):
    import sys

    if (
        sys.platform.startswith("win")
        and sys.version_info[0] == 3
        and sys.version_info[1] >= 8
    ):
        policy = asyncio.WindowsSelectorEventLoopPolicy()
        asyncio.set_event_loop_policy(policy)
    redis_obj = RedisHelper()
    lock = redis_lock.Lock(redis_obj.r, "redis-lock-bilibili")
    while True:
        # 设置redis锁，操作redis
        if lock.acquire(blocking=False):
            print("Got the lock.")
            room_ids = redis_obj.spop(name="bilibili_roomids", count=TASK_MAX)
            # 释放lock
            lock.release()
            # 退出循环
            break
        else:
            print("Someone else has the lock bilibili.")
            time.sleep(10)

    asyncio.run(main(room_ids=room_ids, game_id=game_id, sessdata=sessdata))
