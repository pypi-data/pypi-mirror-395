#!/usr/bin/python3
# -*- coding: utf-8 -*-


import platform
from datetime import datetime


def set_config(key, value):
    """简要描述函数功能"""
    with open(".env", "w+", encoding="utf-8") as f:
        f.write(f"{key}={value}")
    return {key: value}


def get_nowtime():
    """简要描述函数功能"""
    return datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")


def get_os():
    """简要描述函数功能"""
    return platform.system()
