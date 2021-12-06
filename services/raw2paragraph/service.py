#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/3 11:25
# @File    : service.py
# @Software: Basebit
# @Description:
import regex

import services.raw2paragraph.config as conf
from utils.structures import ParagraphStructure


class ColonCut:
    # 经常会匹配错的文本，需要删除
    # 某些文本满足“只要后面不是跟着 .*[:：] ，就继续匹配”的规则，但实际是不需要的，删除
    error_match_texts = [
        '/输入',
        '/$',
        '^/',
        '(?<=^.*[:：])(/)',  # 删除紧跟着type_name的 / 。eg：'既往史：/(与本疾病相关既往史)' --> '既往史：(与本疾病相关既往史)'
        '处理 辅助检查.+emr_reference.+',
        '辅助检查',
        '检验：\s*[无]?\s*$',
    ]

    def extract(self, extract_obj):
        """
        类似于瑞金的模板，不同的段落以“文本+：”的形式分割
        :param extract_obj:
        :return:
        """
        paragraphs = {}
        # 末尾加回车，是为了保证能匹配到最后一行
        # 只要后面不是跟着 .*[:：] ，就继续匹配
        paragraphs_tmp = regex.findall('(.*?[:：][\s\S]*?)\n(?=[\u4e00-\u9fa5]+[:：])', extract_obj.raw_text + '\n')

        for ind, paragraph in enumerate(paragraphs_tmp):
            # 由于有较为灵活的断言，不能用自带的re模块
            for patt in self.error_match_texts:
                paragraph = regex.sub(patt, '', paragraph)

            # 只获取需要的文本块
            temp = regex.findall('^([\u4e00-\u9fa5]+)[:：]?([\s\S]*)', paragraph)
            if temp and not regex.search('(SPAN>|emr_reference)', temp[0][1]) and not regex.search(
                    conf.NOT_EXTRACT_PARAGRAPHS, temp[0][0]):
                temp = temp[0]
                paragraphs[(ind, temp[0])] = temp[1]

        # 如果某些未知的分类夹杂在已知分类中，需要与上一个分类合并
        # ----
        # 个人史：
        # 流行病学史：xxx
        # 婚育史：
        # ---
        # 则需要把“流行病学史”放在“个人史”后
        last_known_sign = False
        del_keys = []
        need_merge_keys = []

        for key in sorted([i for i in paragraphs.keys()], key=lambda x: x[0], reverse=True):
            _, category_name = key
            if category_name in conf.KNOWN_CATEGORY_MAP:
                last_known_sign = True
            if last_known_sign and category_name not in conf.KNOWN_CATEGORY_MAP:
                # 记录待合并的key
                need_merge_keys.append(key)
            if last_known_sign and category_name in conf.KNOWN_CATEGORY_MAP and need_merge_keys:
                # 分类合并
                for need_merge_key in need_merge_keys:
                    paragraphs[key] += '\n{}：{}'.format(need_merge_key[1], paragraphs[need_merge_key])
                del_keys.extend(need_merge_keys)
                need_merge_keys = []

        paragraphs = {k[1]: {
            'sort': k[0],
            'paragraph': v
        } for k, v in paragraphs.items() if k not in del_keys}
        extract_obj.paragraphs = ParagraphStructure(**paragraphs)
        # paragraphs = sorted([[k[0], k[1], v] for k, v in paragraphs.items()], key=lambda x: x[0])
        #
        # paragraphs = [i[1:] for i in paragraphs]
        # extract_obj.paragraphs = paragraphs

        print('段落解析完成：{}'.format(extract_obj.file_name))
        return extract_obj
