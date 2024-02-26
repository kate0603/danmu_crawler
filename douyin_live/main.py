import logging
import time
import multiprocessing
import requests
from config import SOCKET_TIMES
from douyin_live.config import LIVE_ROOM_URL
from douyin_live.src import dy_live
from douyin_live.src.utils.common import init_global
from douyin_live.src.utils.http_send import send_start
from proxy_pool.scheduler import get_usable_proxy
from utils.dingtalk_warning import dingtalk_api_md


def run_live(web_id, ttwid, proxy_info, game_id):
    # 日志配置
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.ERROR)
    # print("记得修改config.py里面的直播地址啊，不然获取不到数据的！")
    # 初始化要做的事情：比如初始化全局变量
    # init_global()
    # 推送直播点赞等数据
    # send_start()
    # 在config.py配置中修改直播地址: LIVE_ROOM_URL
    dy_live.parseLiveRoomUrl(
        f"{LIVE_ROOM_URL}{web_id}", ttwid=ttwid, proxy_info=proxy_info, game_id=game_id
    )


def run(web_ids, game_id, ttwid=None):
    proxy_info = get_usable_proxy(platform="douyin")
    if proxy_info is None:
        msg = f"""无可用的代理ip"""
        dingtalk_api_md(title="抖音弹幕", text=msg)
        return

    print("代理信息==", proxy_info)

    all_processes = []
    for web_id in web_ids:
        process = multiprocessing.Process(
            target=run_live, args=(web_id, ttwid, proxy_info, game_id)
        )
        process.start()
        all_processes.append(process)

    time.sleep(SOCKET_TIMES)
    for process in all_processes:
        process.terminate()
