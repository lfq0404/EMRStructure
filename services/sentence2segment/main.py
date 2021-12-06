#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/6 09:46
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
    for k, v in vars(extract_obj.paragraphs).items():
        # v：{
        #     'sort': 5,
        #     'paragraph': ' 长期生活于原籍，无烟酒等不良嗜好，无冶游史 \n',
        #     'sentences': ['长期生活于原籍', ',' ,'无烟酒等不良嗜好', ',', '无冶游史']
        # }
        for sentence in v['sentences']:
            node = root_node
            classify = None
            while node:
                # 先进行统一的替换
                print('sentence2segment预处理的文本：{}'.format(sentence))
                for cfg in node.replace_cfg:
                    patt = cfg['patt']
                    repl = cfg['repl']
                    need_sub = regex.search(patt, sentence)
                    if need_sub:
                        sentence = regex.sub(patt, repl, sentence)
                        print('根据规则 “{}” ，将文本修改为：{}'.format(patt, sentence))

                # 根据规则分类
                for patt, classify_ in node.classify_cfg:
                    match = regex.match(patt, sentence)
                    if match:
                        if hasattr(classify_, 'extract'):
                            classify = classify_
                            node = None
                        elif isinstance(node, CfgStructure):
                            node = classify_
                        else:
                            raise ValueError('paragraph2sentence的配置错误：{}'.format(node))
            if not classify:
                raise ValueError('paragraph2sentence的配置没有兼容：{}'.format(v))

            segments = classify.extract(sentence)
            getattr(extract_obj.paragraphs, k).setdefault('segments', [])
            getattr(extract_obj.paragraphs, k)['segments'].extend(segments)

    return extract_obj
