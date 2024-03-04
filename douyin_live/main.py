import logging
import time
import multiprocessing
import redis_lock
from douyin_live.config import LIVE_ROOM_URL
from douyin_live.src import dy_live
from douyin_live.src.utils.common import init_global
from douyin_live.src.utils.http_send import send_start
from proxy_pool.scheduler import get_usable_proxy
from utils.dingtalk_warning import dingtalk_api_md
from config import TASK_MAX, SOCKET_TIMES
from utils.redis_helper import RedisHelper


def run_live(web_id, ttwid, game_id):
    # 日志配置
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.ERROR)
    # print("记得修改config.py里面的直播地址啊，不然获取不到数据的！")
    # 初始化要做的事情：比如初始化全局变量
    # init_global()
    # 推送直播点赞等数据
    # send_start()
    dy_live.parseLiveRoomUrl(
        f"{LIVE_ROOM_URL}{web_id}", ttwid=ttwid, game_id=game_id
    )


def run(game_id, ttwid=None):
    redis_obj = RedisHelper()
    lock = redis_lock.Lock(redis_obj.r, "redis-lock-douyin")
    while True:
        # 设置redis锁，操作redis
        if lock.acquire(blocking=False):
            print("Got the lock.")
            web_ids = redis_obj.spop(name="douyin_webids", count=TASK_MAX)
            # 释放lock
            lock.release()
            # 退出循环
            break
        else:
            print("Someone else has the lock douyin.")
            time.sleep(10)

    all_processes = []
    for web_id in web_ids:
        process = multiprocessing.Process(
            target=run_live, args=(int(web_id), ttwid, game_id)
        )
        process.start()
        all_processes.append(process)

    for process in all_processes:
        process.join()

    time.sleep(SOCKET_TIMES)
    for process in all_processes:
        process.terminate()