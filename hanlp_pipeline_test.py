#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/3 15:51
# @File    : hanlp_pipeline_test.py
# @Software: Basebit
# @Description:
import hanlp
import time
from hanlp_trie import Trie

t1 = time.time()
print("装入HanLP分词、词性标注、依存句法分析、语义依存分析模型...")
# 装入分词模型
tokenizer = hanlp.load('LARGE_ALBERT_BASE')
# 装入词性标注模型(获取NN等)
tagger = hanlp.load(hanlp.pretrained.pos.CTB5_POS_RNN_FASTTEXT_ZH)
# 装入依存句法分析模型
syntactic_parser = hanlp.load(hanlp.pretrained.dep.CTB7_BIAFFINE_DEP_ZH)
# 装入语义依存分析模型
semantic_parser = hanlp.load(hanlp.pretrained.sdp.SEMEVAL16_NEWS_BIAFFINE_ZH)
# 装入用户自定义词典
trie = Trie()
trie.update({'电信服务': 'NN', '服务费': 'NN', "合计": "NN", '~~': 'W'})
t2 = time.time()
print("模型已装入...", t2 - t1)


def split_sents(text: str, trie: Trie):
    """
    原自定义词分割函数，来自demo_cws_trie
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


# def split_sents2(text: str, trie: Trie):
#     """
#     更改分割函数，检查一下取词是否输出空串, 抛弃trie树返回的结果中与前一个词有重叠的词
#     :param text:
#     :param trie:
#     :return:
#     """
#     words = trie.parse_longest(text)
#     # print(words)
#     sents = []
#     words2 = []
#     pre_start = 0
#     offsets = []
#     for start, end, value in words:
#         # print(word, value, start, end, pre_start, start)
#         word = text[start:end]
#         if pre_start != start:
#             word2 = text[pre_start: start]
#             if len(word2) > 0:
#                 # print(word2)
#                 sents.append(text[pre_start: start])
#                 words2.append(tuple([word, value, start, end]))
#                 offsets.append(pre_start)
#                 pre_start = end
#             else:
#                 print("自定义词有重叠，跳过:", word, value, start, end)
#         else:
#             print("自定义词首尾相接：", pre_start, start)
#             words2.append(tuple([word, value, start, end]))
#             pre_start = end
#
#     if pre_start != len(text):
#         sents.append(text[pre_start:])
#         offsets.append(pre_start)
#     return sents, offsets, words2


def merge_sents(hlhzs):
    return "~~".join(hlhzs)


def split_pos(postags):
    tpsents = []
    tpsent = []
    for postag in postags:
        if postag[0] == "~~":
            tpsents.append(tpsent)
            tpsent = []
        else:
            tpsent.append(postag)
    tpsents.append(tpsent)
    return tpsents


def merge_parts_old(parts, offsets, words):
    """
    原合并函数，来自demo_cws_trie
    :param parts:
    :param offsets:
    :param words:
    :return:
    """
    items = [(i, p) for (i, p) in zip(offsets, parts)]
    items += [(start, [value]) for (start, end, value) in words]
    return [each for x in sorted(items) for each in x[1]]


def merge_parts(tokens, postags, offsets, words):
    """
    自己的合并函数
    :param tokens:
    :param postags:
    :param offsets:
    :param words:
    :return:
    """
    tps = []
    for i in range(len(tokens)):
        tps2 = [(token, postag) for (token, postag) in zip(tokens[i], postags[i])]
        tps.append(tps2)
    # items = [(i, p) for (i, p) in zip(offsets, tokens)]
    items = [(i, ts) for (i, ts) in zip(offsets, tps)]
    # items += [(start, [word]) for (word, value, start, end) in words]
    # In case you need the tag, use the following line instead
    items += [(start, [(word, value)]) for (word, value, start, end) in words]
    return [each for x in sorted(items) for each in x[1]]


if __name__ == '__main__':
    # parser = hanlp.pipeline() \
    #     .append(split_sents, output_key=('parts', 'offsets', 'words'), trie=trie) \
    #     .append(tokenizer, input_key='parts', output_key='tokens')
    #
    # parser2 = parser.append(tagger, input_key='tokens', output_key='postags')
    #
    # # 测试文本
    # text = "增值电信服务费"
    #
    # # 执行出错
    # res2 = parser2(text)
    # # 执行通过，所以问题在tagger的执行
    # res = parser(text)
    # # 打印分词的结果
    # print(res['tokens'])  # [['增值'], []]
    # print(res['words'])  # [('电信服务', 'NN', 2, 6), ('服务费', 'NN', 4, 7)]
    # # 单独执行每个token的词性标注都可以
    # print(tagger(res['tokens'][0]))  # ['NN']
    # print(tagger(res['tokens'][1]))  # []
    # # 一起执行就有错，应该上传入的二维列表中有空的子列表，
    # # 但上一行print(tagger(res['tokens'][1]))对空的列表执行tagger是可以的。
    # print(tagger(res['tokens']))
    #
    # # 所以原因应该是split_sents()中取自定义词输出了空串，
    # # 在这种存在多种匹配分词可能的情况下，text[pre_start: start]出现了pre_start>start的情况
    # print(res['parts'])  # ['增值', '']

    # 测试GPU并行
    text = [
        # "原价合计", "增值电信服务费", "折扣额合计",
        '一般健康状况:一般。疾病史:否认高血压、冠心病等慢性病史。手术外伤史:因“胃息肉”行开腹手术治疗（具体不详）。输血史:否认。传染病史:诉既往曾患“肝炎”（具体不详），诉已愈。',
    ]

    # 测试自定义词分割，通过
    # res = split_sents2(merge_sents(text), trie)
    # print(res)
    # # 分词及词性标注
    # parser3 = hanlp.pipeline() \
    #     .append(merge_sents, output_key="sents") \
    #     .append(split_sents2, input_key="sents", output_key=('parts', 'offsets', 'words'), trie=trie) \
    #     .append(tokenizer, input_key='parts', output_key='tokens') \
    #     .append(tagger, input_key='tokens', output_key='postags') \
    #     .append(merge_parts, input_key=('tokens', 'postags', 'offsets', 'words'), output_key='merged')
    # # 执行通过
    # res3 = parser3(text)
    # print(res3)
    # # 依存句法分析
    # parser4 = hanlp.pipeline() \
    #     .append(merge_sents, output_key="sents") \
    #     .append(split_sents2, input_key="sents", output_key=('parts', 'offsets', 'words'), trie=trie) \
    #     .append(tokenizer, input_key='parts', output_key='tokens') \
    #     .append(tagger, input_key='tokens', output_key='postags') \
    #     .append(merge_parts, input_key=('tokens', 'postags', 'offsets', 'words'), output_key='merged') \
    #     .append(split_pos, input_key="merged", output_key="splits") \
    #     .append(syntactic_parser, input_key='splits', output_key='syntactic_dependencies')
    # # 执行通过
    # res4 = parser4(text)
    # print(res4)
    # # 语义依存分析
    text = '一般健康状况:一般。疾病史:否认高血压、冠心病等慢性病史。手术外伤史:因“胃息肉”行开腹手术治疗（具体不详）。输血史:否认。传染病史:诉既往曾患“肝炎”（具体不详），诉已愈。'

    # 语义依存分析
    parser5 = hanlp.pipeline() \
        .append(merge_sents, output_key="sents") \
        .append(split_sents2, input_key="sents", output_key=('parts', 'offsets', 'words'), trie=trie) \
        .append(tokenizer, input_key='parts', output_key='tokens') \
        .append(tagger, input_key='tokens', output_key='postags') \
        .append(merge_parts, input_key=('tokens', 'postags', 'offsets', 'words'), output_key='merged') \
        .append(split_pos, input_key="merged", output_key="splits") \
        .append(semantic_parser, input_key='splits', output_key='semantic_dependencies')
    # 执行通过
    res5 = parser5(text)
    print(res5)
    # parser6 = hanlp.pipeline() \
    #     .append(split_sents, output_key=('parts', 'offsets', 'words'), trie=trie) \
    #     .append(tokenizer, input_key='parts', output_key='tokens') \
    #     .append(merge_parts_old, input_key=('tokens', 'offsets', 'words'), output_key='merged') \
    #     .append(split_pos, input_key="merged", output_key="splits") \
    #     .append(syntactic_parser, input_key='splits', output_key='syntactic_dependencies')
    #
    # res6 = parser6(text)
    # print(res6)
