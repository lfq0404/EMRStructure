#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/6 09:45
# @File    : service.py
# @Software: Basebit
# @Description:
import re
import jieba
import jieba.posseg as psg

import services.paragraph2sentence.config as conf


class Paragraph2SentenceBase:

    def extract(self, block):
        """
        默认只以句号分割
        :param block:
        :return:
        """
        return [block]

    # def rough_setences(self, paragraph):
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
    #
    # def word_cut(self, text):
    #     """
    #     默认利用jieba分词
    #     :return: [['有无', 'option'], ['手术史', 'n']]
    #     """
    #     block_cut = []
    #     if not text:
    #         return block_cut
    #
    #     for k, v in psg.cut(text, HMM=False):
    #         if k in conf.NOT_BROKEN_SENTENCE:
    #             # 由于度数的单位 ° 在userdict中没法识别出来，在这里单独处理
    #             v = 'n'
    #         block_cut.append([k, v])
    #
    #     return block_cut


# class SpecialWordBlockExtract(Paragraph2SentenceBase):
#     def __init__(self, words):
#         self.words = words
#
#     def extract(self, block):
#         """
#         特殊词组，需要临时改变jieba自定义词组
#         :param block:
#         :return:
#         """
#         # 临时添加分词规则
#         for word in self.words:
#             jieba.add_word(word[0], conf.DEFAULT_FREQUENCY, word[1])
#
#         block_cut = super(SpecialWordBlockExtract, self).word_cut(block)
#
#         # 删除临时分词规则，如果与原来的配置冲突，则需要复原
#         for word in self.words:
#             jieba.del_word(word[0])
#             if word[0] in conf.JIEBA_USER_WORDS:
#                 for w in conf.JIEBA_USER_DICTS:
#                     if w[0] == word[0]:
#                         jieba.add_word(*w)
#                         break
#
#         return block_cut
