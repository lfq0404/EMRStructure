#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/6 17:04
# @File    : main.py
# @Software: Basebit
# @Description:


import regex

from services.sentence2segment.config import root_node
from utils.structures import CfgStructure

"""
拼接segment可能的类型
纯文本
单选
复选
单选+补充
复选+补充
输入框
"""


def handle(extract_obj):
    """
    每层的处理逻辑入口
    本层目的：将句子转为segment
    :param extract_obj:
    :return:
    """
    paragraphs = vars(extract_obj.paragraphs).copy()
    for k, v in paragraphs.items():
        # v：{
        #     'sort': 5,
        #     'paragraph': ' 长期生活于原籍，无烟酒等不良嗜好，无冶游史 \n',
        #     'sentences': ['长期生活于原籍', ',' ,'无烟酒等不良嗜好', ',', '无冶游史']
        #     'segments': [TextSegmentStructure obj, SingleChoiceWithOthersStructure obj]
        # }
        segments_show = []
        for segment in v['segments']:
            segments_show.append(segment.show())
        v['segments_show'] = segments_show

    return extract_obj
