# -*- coding: utf-8 -*-
"""
    Created by w at 2024/2/20.
    Description:
    Changelog: all notable changes to this file will be documented
"""


def live_douyin(game_id):
    # from utils.live_log import LiveLog
    from douyin_live.main import run

    # rooms = LiveLog(game_id=game_id).read_live_info(platform="抖音")["roomid"].to_list()
    # print(rooms)
    run(web_ids=[540068631168, 269990234292, 802941556183], game_id=game_id)

def live_bilibili(game_id):
    # from utils.live_log import LiveLog
    from blivedm.sample import blive_run

    # rooms = LiveLog(game_id=game_id).read_live_info(platform="哔哩哔哩")["roomid"].to_list()
    # print(rooms)
    # blive_run(room_ids=[14503677, 6710419, 31861575, 27660854, 9326056], game_id=game_id)
    blive_run(room_ids=[31924968], game_id=game_id)


def start_scheduler():
    """时间调度"""
    from datetime import datetime
    from apscheduler.schedulers.background import BlockingScheduler
    from proxy_pool.scheduler import __runProxyCheck

    scheduler = BlockingScheduler()
    # 容器开启时测试 todo
    # scheduler.add_job(__runProxyCheck, "date", run_date=datetime.now())
    # 半个小时检查一次代理池
    scheduler.add_job(
        __runProxyCheck, "interval", minutes=30, misfire_grace_time=600
    )
    scheduler.start()

if __name__ == "__main__":
    # live_douyin(game_id=2211)
    live_bilibili(game_id=2211)
