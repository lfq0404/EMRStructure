#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/16 15:38
# @File    : config.py
# @Software: Basebit
# @Description:
import services.paragraph2sentence.constant as cons

# 分词
# 强制校正【慎用】
TOK_DICT_FORCE = {
    '全身麻醉'
}
# 软校正
TOK_DICT_COMBINE = set(
)

# 词性
POS_DICT_TAGS = {
    ('一般', '健康', '状况'): (cons.TAG_COMMON_NOUN, cons.TAG_COMMON_NOUN, cons.TAG_COMMON_NOUN),

    '。': cons.TAG_SPLIT,

    '、': cons.TAG_CONTACT,
    '°': cons.TAG_CONTACT,
    ' ': cons.TAG_CONTACT,
    '(': cons.TAG_CONTACT,
    ')': cons.TAG_CONTACT,
    '（': cons.TAG_CONTACT,
    '）': cons.TAG_CONTACT,
    '+': cons.TAG_CONTACT,
    '-': cons.TAG_CONTACT,
    '’': cons.TAG_CONTACT,
    '：': cons.TAG_CONTACT,
    ':': cons.TAG_CONTACT,

    '吸烟': cons.TAG_NOUN_PHRASE,

    '一般': cons.TAG_PREDICATIVE_ADJECTIVE,
}

# 实体命名
# 自定义单个实体命名。不管在什么情况下，都以该名单对实体命名
NER_DICT_WHITELIST = {
    '午饭后': 'TIME',
}
# 根据上下文自定义实体命名
NER_DICT_TAGS = {
    ('名字', '叫', '金华'): ('O', 'O', 'S-PERSON'),
}
