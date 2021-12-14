#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/2 22:24
# @File    : constant.py
# @Software: Basebit
# @Description: 全局公共常量
import os
from string import punctuation as cn_punc
from zhon.hanzi import punctuation as zh_punc

BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# 所有中英文的标点符号
PUNCTUATION = cn_punc + zh_punc

# 选项的分割线。以下相隔的文本视为选项
OPTION_SPLITS = ['/', '或', '、', '；']

# 不断句的标点符号
NOT_BROKEN_PUNC = ['°', ' ', '(', ')', '（', '）', '+', '-', '’', '：', ':'] + OPTION_SPLITS

# 用于断句的标点符号
BROKEN_PUNC = ''.join([i for i in PUNCTUATION if i not in NOT_BROKEN_PUNC])
