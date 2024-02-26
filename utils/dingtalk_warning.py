#!/usr/bin/env python
# -*- coding: utf -8 -*-
"""
    Created by wq at 2020/7/21.
    Copyright (c) 2013-present, Xiamen Dianchu Technology Co.,Ltd.
    Description:钉钉机器人告警
    Changelog: all notable changes to this file will be documented
"""
import os
from dingtalkchatbot.chatbot import DingtalkChatbot
METADATA_DINGTALK_TOKEN = ""


def dataframe_to_markdown(data):
    """
    dataframe 转为md格式
    :param data:
    :return:
    """
    msg: str = f""
    table_title = "|".join(data.columns)
    msg = f"{msg}|{table_title} |"
    table_divider = "|".join(["---"] * len(data.columns))
    msg = f"{msg}\n |{table_divider} "
    for index, row in data.iterrows():
        temp = ""
        for i in data.columns:
            temp = f"{temp}| {row[i]}"
        msg = f"{msg} |\n {temp}"
    msg = f"""{msg} | """
    return msg


def dingtalk_api_md(
    title: str, text: str, at_mobiles: list = [], token: str = None, is_at_all=False
) -> None:
    """
    Markdown通知
    :return:
    """
    token = token or METADATA_DINGTALK_TOKEN
    webhook = f"https://oapi.dingtalk.com/robot/send?access_token={token}"
    alarm = DingtalkChatbot(webhook)
    env = os.getenv("ENV", "dev")
    print(text)
    # alarm.send_markdown(
    #     title=f"{title}",
    #     text=f"[{env}]{text}",
    #     is_at_all=is_at_all,
    #     at_mobiles=at_mobiles,
    # )
