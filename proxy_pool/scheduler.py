# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxyScheduler
   Description :
   Author :        JHao
   date：          2019/8/5
-------------------------------------------------
   Change Activity:
                   2019/08/05: proxyScheduler
                   2021/02/23: runProxyCheck时,剩余代理少于POOL_SIZE_MIN时执行抓取
-------------------------------------------------
"""
__author__ = "JHao"
from proxy_pool.util.six import Queue
from proxy_pool.helper.fetch import Fetcher
from proxy_pool.helper.check import Checker
from proxy_pool.helper.proxy import Proxy
from proxy_pool.handler.proxyHandler import ProxyHandler


def __runProxyFetch():
    proxy_queue = Queue()
    proxy_fetcher = Fetcher()

    for proxy in proxy_fetcher.run():
        proxy_queue.put(proxy)

    Checker("raw", proxy_queue)


def __runProxyCheck():
    proxy_handler = ProxyHandler()
    proxy_queue = Queue()
    if proxy_handler.db.getCount().get("total", 0) < proxy_handler.conf.poolSizeMin:
        __runProxyFetch()
    for proxy in proxy_handler.getAll():
        proxy_queue.put(proxy)
    Checker("use", proxy_queue)


def pop_proxy(is_https: bool = False):
    proxy_handler = ProxyHandler()
    proxy = proxy_handler.pop(https=is_https)
    return proxy.to_dict if proxy else None


def get_proxy(is_https: bool = False):
    proxy_handler = ProxyHandler()
    proxy = proxy_handler.get(https=is_https)
    return proxy.to_dict if proxy else None


def delete_proxy(proxy):
    proxy_handler = ProxyHandler()
    status = proxy_handler.delete(Proxy(**proxy))
    return {"code": 0, "src": status}


def get_proxy_count():
    proxy_handler = ProxyHandler()
    proxies = proxy_handler.getAll()
    http_type_dict = {}
    source_dict = {}
    for proxy in proxies:
        http_type = "https" if proxy.https else "http"
        http_type_dict[http_type] = http_type_dict.get(http_type, 0) + 1
        for source in proxy.source.split("/"):
            source_dict[source] = source_dict.get(source, 0) + 1
    return {"http_type": http_type_dict, "source": source_dict, "count": len(proxies)}


def get_usable_proxy(platform: str = "douyin"):
    # 测试代理ip
    count = get_proxy_count()["count"]
    proxy_info = None
    for i in range(count):
        proxy_info = get_proxy()
        print("=======代理ip", proxy_info)
        if proxy_info is None:
            break
        from proxy_pool.helper.validator import douyin_validator, bilibili_validator

        if platform == "bilibili":
            is_usable: bool = bilibili_validator(proxy=proxy_info["proxy"])
        else:
            is_usable: bool = douyin_validator(proxy=proxy_info["proxy"])
        # print(is_usable)
        if is_usable:
            return proxy_info
        else:
            delete_proxy(proxy_info)
    if proxy_info is None:
        return None
