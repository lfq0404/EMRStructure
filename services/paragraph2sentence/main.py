#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/6 09:46
# @File    : main.py
# @Software: Basebit
# @Description:
import regex

import utils.funcs as util_func
from services.paragraph2sentence.rule_config import root_node
from utils.structures import CfgStructure, ExtractStructure


def handle(extract_obj):
    """
    每层的处理逻辑入口
    本层目的：将原始的文本转为段落
    :param extract_obj:
    :return:
    """
    # 针对每种史分别进行处理
    for k, v in extract_obj.paragraphs.items():
        # k：个人史
        # v：{'sort': 5, 'paragraph': ' 长期生活于原籍，无烟酒等不良嗜好，无冶游史。 \n'}

        classify, paragraph = util_func.replace_and_classify_base(v['paragraph'], root_node, 'paragraph2sentence')
        if not paragraph:
            continue

        sentences = classify.extract(paragraph)
        extract_obj.paragraphs[k].setdefault('sentences', [])
        extract_obj.paragraphs[k]['sentences'].extend(sentences)

        # # 粗断句
        # blocks = get_blocks(v)
        # for block in blocks:
        #     # 走统一的流程
        #     classify, block = util_func.replace_and_classify_base(block, root_node, 'paragraph2sentence')
        #
        #     sentences = classify.extract(block)
        #     extract_obj.paragraphs[k].setdefault('sentences', [])
        #     extract_obj.paragraphs[k]['sentences'].extend(sentences)

    return extract_obj

# def get_blocks(paragraph):
#     """
#     粗断句
#     :param paragraph: {'sort': 5, 'paragraph': ' 长期生活于原籍，无烟酒等不良嗜好，无冶游史。 \n'}
#     :return:
#     """
#     blocks = ['']
#     for i in paragraph['paragraph']:
#         blocks[-1] += i
#         if i in ['。', '\n']:
#             blocks.append('')
#     # 此处不能去掉文中的空格，否则有些英文术语会出问题
#     blocks = [i.strip() for i in blocks if i.strip()]
#
#     return blocks
