#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/2 22:11
# @File    : main.py
# @Software: Basebit
# @Description:
import os

import regex

from services.resource2raw.main import handle as resource2raw_handle
from services.raw2paragraph.main import handle as raw2paragraph_handle
from services.paragraph2sentence.main import handle as paragraph2sentence_handle
from services.sentence2segment.main import handle as sentence2segment_handle
from services.segment_structure.main import handle as segment_structure_handle
from utils.structures import ExtractStructure, ParagraphStructure

# 整个层级流程配置，一般不能随意调换
HANDLES = [
    resource2raw_handle,
    raw2paragraph_handle,
    paragraph2sentence_handle,
    sentence2segment_handle,
    segment_structure_handle,
]


def main(args, begin_handle):
    """
    入口函数
    :return:
    """
    level = HANDLES.index(begin_handle)
    # input_ = input('即将从 {} 层开始执行，参数为：{}\n确认请输入y：'.format(level, args))
    input_ = 'y'
    if input_ != 'y':
        return

    # 数据处理逻辑
    handles = HANDLES[level:]
    for handle in handles:
        new_args = []
        for arg in args:
            _new = handle(arg)
            if type(_new) is list:
                new_args.extend(_new)
            else:
                new_args.append(_new)
        args = new_args.copy()

    # 数据入库逻辑
    # insert args
    print(args)


if __name__ == '__main__':
    extract_obj = ExtractStructure(
        file_name='西医_内科.txt',
        file_path='/Users/jeremy.li/Basebit/Projects/AutoTemplate/pdf2text/bookTextsManual',
        raw_text='123',
    )
    extract_obj.paragraphs = ParagraphStructure(**{
        'test': {'sort': 1, 'paragraph': '预防接种史：无 不详 有 预防接种疫苗。'}
    })
    main(
        args=[extract_obj],
        begin_handle=paragraph2sentence_handle
    )


    base_path = '/Users/jeremy.li/Basebit/Projects/AutoTemplate/pdf2text/bookTextsManual'
    g = os.walk(base_path)
    result = []
    for path, _, file_list in g:
        for ind, file in enumerate(file_list):
            with open('{}/{}'.format(base_path, file), 'r') as f:
                raw_text = f.read()
            extract_obj = ExtractStructure(
                file_name=file,
                file_path='/Users/jeremy.li/Basebit/Projects/AutoTemplate/pdf2text/bookTextsManual',
                raw_text=raw_text,
            )
            extract_obj.paragraphs = ParagraphStructure(**{
                '未分类': {'sort': 1, 'paragraph': raw_text}
            })
            main(
                args=[extract_obj],
                begin_handle=paragraph2sentence_handle
            )
