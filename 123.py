#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/17 22:16
# @File    : 123.py
# @Software: Basebit
# @Description:

# -*- coding:utf-8 -*-
# Author: hankcs
# Date: 2019-12-28 21:25
import time
from hanlp_trie.trie import Trie

import hanlp

t1 = time.time()
print("装入HanLP分词、词性标注、依存句法分析、语义依存分析模型...")
# 分词模型
tokenizer = hanlp.load(hanlp.pretrained.tok.LARGE_ALBERT_BASE)
# 装入词性标注模型
tagger = hanlp.load(hanlp.pretrained.pos.CTB9_POS_ALBERT_BASE)
# 装入依存句法分析模型
syntactic_parser = hanlp.load(hanlp.pretrained.dep.CTB7_BIAFFINE_DEP_ZH)
# 装入语义依存分析模型
semantic_parser = hanlp.load(hanlp.pretrained.sdp.SEMEVAL16_TEXT_BIAFFINE_ZH)
# 用户自定义词典
trie = Trie()
trie.update({
    '自定义词典': 'custom_dict',
    '聪明人': 'smart',
    '。': 'split',
})
t2 = time.time()
print("模型已装入...", t2 - t1)

text = '一般健康状况:一般。疾病史:否认高血压、冠心病等慢性病史。手术外伤史:因“胃息肉”行开腹手术治疗（具体不详）。输血史:否认。传染病史:诉既往曾患“肝炎”（具体不详），诉已愈。'
print('------- 1 ------------')
print(tokenizer(text))


def split_sents(text: str, trie: Trie):
    """
    利用用户自定义词典分句
    :param text:
    :param trie:
    :return:
    """
    words = trie.parse_longest(text)
    sents = []
    pre_start = 0
    offsets = []
    for start, end, value in words:
        if pre_start != start:
            sents.append(text[pre_start: start])
            offsets.append(pre_start)
        pre_start = end
    if pre_start != len(text):
        sents.append(text[pre_start:])
        offsets.append(pre_start)
    return sents, offsets, words


print('------- 2 ------------')
print(split_sents(text, trie))


# def merge_parts(parts, offsets, words):
#     items = [(i, p) for (i, p) in zip(offsets, parts)]
#     items += [(start, [value]) for (start, end, value) in words]
#     return [each for x in sorted(items) for each in x[1]]


parser = hanlp.pipeline().append(
    # 利用用户自定义词典断句
    split_sents, output_key=('parts', 'offsets', 'words'), trie=trie).append(
    # 分词
    tokenizer, input_key='parts', output_key='tokens').append(
    # 词性标注
    tagger, input_key='tokens', output_key='postags').append(
    # 依存句法分析
    syntactic_parser, input_key=('tokens', 'postags'), output_key='syntactic_dependencies').append(
    # 语义依存分析
    semantic_parser, input_key=('tokens', 'postags'), output_key='semantic_dependencies')

print('------- 3 ------------')
print(parser(text))
