#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/3 15:51
# @File    : test.py
# @Software: Basebit
# @Description:
from main import *

if __name__ == '__main__':
    extract_obj = ExtractStructure(
        file_name='西医_内科.txt',
        file_path='/Users/jeremy.li/Basebit/Projects/AutoTemplate/pdf2text/bookTextsManual',
        raw_text='123',
    )
    extract_obj.paragraphs = {
        'test':
            {
                'sort': 1,
                # 'paragraph': 'Laseque征：左(一 十)；右(一 十)'
                'paragraph': '吸烟史：无 有 平均_支/日，时间_年 ，戒烟：否 是 时间'
            }
    }
    main(
        args=[extract_obj],
        begin_handle=paragraph2sentence_handle
    )
