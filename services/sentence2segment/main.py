#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/6 09:46
# @File    : main.py
# @Software: Basebit
# @Description:
import regex

from services.sentence2segment.rule_config import root_node
import utils.funcs as util_func
from utils.structures import CfgStructure


def handle(extract_obj):
    """
    每层的处理逻辑入口
    本层目的：将句子转为segment
    :param extract_obj:
    :return:
    """
    for k, v in extract_obj.paragraphs.items():
        # v：{
        #     'sort': 5,
        #     'paragraph': ' 长期生活于原籍，无烟酒等不良嗜好，无冶游史 \n',
        #     'sentences': ['长期生活于原籍', ',' ,'无烟酒等不良嗜好', ',', '无冶游史']
        # }
        for sentence in v['sentences']:
            classify, sentence = util_func.replace_and_classify_base(sentence, root_node, 'sentence2segment')

            segments = classify.extract(sentence)
            for segment in segments:
                print(segment.segment)
            extract_obj.paragraphs[k].setdefault('segments', [])
            extract_obj.paragraphs[k]['segments'].extend(segments)

    return extract_obj
