#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/5 10:36
# @File    : main.py
# @Software: Basebit
# @Description:
from services.resource2raw.config import RESOURCE_TYPE


def handle(resource_type):
    """
    每层的处理逻辑入口
    本层目的：将原始资源转成文本格式
    :return:
    """

    return RESOURCE_TYPE[resource_type].extract()
