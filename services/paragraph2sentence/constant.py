#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/18 14:33
# @File    : constant.py
# @Software: Basebit
# @Description:

# 用户自定义的词性
TAG_SPLIT = 'split'
TAG_CONTACT = 'contact'
# 详见：https://hanlp.hankcs.com/docs/annotations/pos/ctb.html
TAG_PROPER_NOUN = 'NR'  # 专有名词
TAG_COMMON_NOUN = 'NN'  # 其他名词
TAG_PREDICATIVE_ADJECTIVE = 'VA'  # 表语形容词
TAG_TEMPORAL_NOUN = 'NT'  # 时间名词
# CTB的词性：https://hanlp.hankcs.com/docs/annotations/constituency/ctb.html
TAG_NOUN_PHRASE = 'NP'  # 名词短语【以该标志作为segment_key】
