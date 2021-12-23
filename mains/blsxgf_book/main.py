#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/16 11:25
# @File    : main.py
# @Software: Basebit
# @Description: 病历书写规范  最新版 13726225.pdf --> text，的结构化入口

import os

from mains.constant import *
from utils.funcs import update_html, raw_obj_call_handles, check_html_with_args
from utils.structures import ExtractStructure


def main(args, begin_handle):
    """
    入口函数
    :return:
    """
    level = HANDLES.index(begin_handle)
    args = raw_obj_call_handles(args, HANDLES[level:])

    check_html_with_args(args)
    return args


if __name__ == '__main__':
    # # 针对句子调试
    # extract_obj = ExtractStructure(
    #     file_name='西医_内科.txt',
    #     file_path='/Users/jeremy.li/Basebit/Projects/AutoTemplate/pdf2text/bookTextsManual',
    #     raw_text='123',
    # )
    # extract_obj.paragraphs = {
    #     'test':
    #         {
    #             'sort': 1,
    #             # 'paragraph': 'Laseque征：左(一 十)；右(一 十)'
    #             'paragraph': 'BarreⅡ试验：左(- +)；右(- +)'
    #         }
    # }
    # main(
    #     args=[extract_obj],
    #     begin_handle=paragraph2sentence_handle
    # )

    base_path = '/Users/jeremy.li/Basebit/Projects/AutoTemplate/pdf2text/bookTextsManual'
    g = os.walk(base_path)
    result = []
    for path, _, file_list in g:
        for ind, file in enumerate(file_list):
            if 'txt' not in file:
                continue
            print('开始处理：{}'.format('{}/{}'.format(base_path, file)))
            with open('{}/{}'.format(base_path, file), 'r') as f:
                raw_text = f.read()
            if not raw_text:
                continue
            extract_obj = ExtractStructure(
                file_name=file,
                file_path=base_path,
                raw_text=raw_text,
            )
            extract_obj.paragraphs = {
                '未分类': {'sort': 1, 'paragraph': raw_text}
            }
            main(
                args=[extract_obj],
                begin_handle=paragraph2sentence_handle
            )
