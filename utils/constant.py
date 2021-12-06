#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/2 22:24
# @File    : constant.py
# @Software: Basebit
# @Description: 全局公共常量
from string import punctuation as cn_punc
from zhon.hanzi import punctuation as zh_punc

# 所有中英文的标点符号
PUNCTUATION = cn_punc + zh_punc
