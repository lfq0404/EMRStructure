#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/5 10:44
# @File    : main.py
# @Software: Basebit
# @Description:
import regex

from services.raw2paragraph.config import root_node
from utils.structures import CfgStructure


def handle(extract_obj):
    """
    每层的处理逻辑入口
    本层目的：将原始的文本转为段落
    :param extract_obj:
    :return:
    """
    node = root_node
    classify = None
    while node:
        # 先进行统一的替换
        for cfg in node.replace_cfg:
            patt = cfg['patt']
            repl = cfg['repl']
            extract_obj.raw_text = regex.sub(patt, repl, extract_obj.raw_text)
        # 根据规则分类
        for patt, classify_ in node.classify_cfg:
            match = regex.match(patt, extract_obj.raw_text)
            if match:
                if hasattr(classify_, 'extract'):
                    classify = classify_
                    node = None
                elif isinstance(node, CfgStructure):
                    node = classify_
                else:
                    raise ValueError('raw2paragraph的配置错误：{}'.format(node))
    if not classify:
        raise ValueError('raw2paragraph的配置没有兼容：{}'.format(extract_obj.raw_text))

    return classify.extract(extract_obj)
