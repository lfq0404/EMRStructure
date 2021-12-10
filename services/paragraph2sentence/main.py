#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/6 09:46
# @File    : main.py
# @Software: Basebit
# @Description:
import regex

from services.paragraph2sentence.config import root_node
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
        node = root_node
        classify = None

        # 粗断句
        blocks = get_blocks(v)
        for block in blocks:
            # print('paragraph2sentence预处理的文本：{}'.format(block))
            while node:
                # 先进行统一的替换
                for cfg in node.replace_cfg:
                    patt = cfg['patt']
                    repl = cfg['repl']
                    need_sub = regex.search(patt, block)
                    if need_sub:
                        block = regex.sub(patt, repl, block)
                        # print('paragraph2sentence根据规则 “{}” ，将文本修改为：{}'.format(patt, block))

                # 根据规则分类
                for patt, classify_ in node.classify_cfg:
                    match = regex.match(patt, block)
                    if match:
                        if hasattr(classify_, 'extract'):
                            classify = classify_
                            node = None
                        elif isinstance(node, CfgStructure):
                            node = classify_
                        else:
                            raise ValueError('paragraph2sentence的配置错误：{}'.format(node))
                        break
            if not classify:
                raise ValueError('paragraph2sentence的配置没有兼容：{}'.format(v))

            sentences = classify.extract(block)
            extract_obj.paragraphs[k].setdefault('sentences', [])
            extract_obj.paragraphs[k]['sentences'].extend(sentences)

    return extract_obj


def get_blocks(paragraph):
    """
    粗断句
    :param paragraph: {'sort': 5, 'paragraph': ' 长期生活于原籍，无烟酒等不良嗜好，无冶游史。 \n'}
    :return:
    """
    blocks = ['']
    for i in paragraph['paragraph']:
        blocks[-1] += i
        if i in ['。', '\n']:
            blocks.append('')
    # 此处不能去掉文中的空格，否则有些英文术语会出问题
    blocks = [i.strip() for i in blocks if i.strip()]

    return blocks
