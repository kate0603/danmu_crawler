# -*- coding: utf-8 -*-
"""
    Created by w at 2024/2/20.
    Description:
    Changelog: all notable changes to this file will be documented
"""
from datetime import datetime, timedelta


def cut_words(game_id: int, start_time: datetime = None, end_time: datetime = None):
    import jieba.analyse
    import pandas as pd
    from collections import Counter
    from utils.live_log import LiveLog

    end_time = end_time or datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    start_time = start_time or end_time + timedelta(days=-1, microseconds=1)
    log_obj = LiveLog(game_id=game_id)
    for platform in ["douyin", "bilibili"]:
        data = log_obj.read_live_chat(
            platform=platform, start_time=start_time, end_time=end_time
        )
        msgs: list = data["msg"].to_list()

        # jieba.enable_parallel(4) # windows不支持
        results = []
        for str in msgs:
            seg_list = jieba.analyse.extract_tags(str)
            results.extend(seg_list)

        def counter(arr):
            return Counter(arr)

        words = pd.DataFrame(list(counter(results).items()), columns=["word", "num"])
        log_obj.write_chat_word(
            data=words, log_date=start_time.date(), platform=platform
        )


def live_douyin(game_id):
    from douyin_live.main import run

    run(game_id=game_id)


def live_bilibili(game_id):
    from blivedm.sample import blive_run

    blive_run(game_id=game_id)


def redis_put_ids(name: str, value: list):
    """
    :param name: douyin_webids/bilibili_roomids
    :param value:
    :return:
    """
    from utils.redis_helper import RedisHelper

    obj = RedisHelper()
    obj.sadd(name=name, value=value)


def redis_lock_release(lock_name: str = "redis-lock-douyin"):
    import redis_lock
    from utils.redis_helper import RedisHelper

    redis_obj = RedisHelper()

    lock = redis_lock.Lock(redis_obj.r, lock_name)
    lock.reset()


def start_scheduler():
    """时间调度"""
    from datetime import datetime
    from apscheduler.schedulers.background import BlockingScheduler

    #

    scheduler = BlockingScheduler()
    # 容器开启时测试 todo
    scheduler.add_job(
        func=live_douyin, trigger="date", args=(2211,), run_date=datetime.now()
    )
    scheduler.add_job(
        func=live_bilibili, trigger="date", args=(2211,), run_date=datetime.now()
    )
    # 半个小时检查一次代理池
    # scheduler.add_job(__runProxyCheck, "interval", minutes=30, misfire_grace_time=600)
    scheduler.start()


if __name__ == "__main__":
    start_scheduler()
