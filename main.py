#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/2 22:11
# @File    : main.py
# @Software: Basebit
# @Description:
import json
import os

import pandas as pd
import regex

from dao.data2excel import data2excel
from services.resource2raw.main import handle as resource2raw_handle
from services.raw2paragraph.main import handle as raw2paragraph_handle
from services.paragraph2sentence.main import handle as paragraph2sentence_handle
from services.sentence2segment.main import handle as sentence2segment_handle
from services.segment_structure.main import handle as segment_structure_handle
from utils.structures import ExtractStructure

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

    return args

    # display = ''
    # segments = []
    # for arg in args:
    #     d = ''
    #     type_ = None
    #     for type_, infos in arg.paragraphs.items():
    #         for segment in infos['segments_show']:
    #             d += segment['display'] + '。'
    #             segments.append(segment['segment'])
    #     if not type_:
    #         continue
    #     display += '<b>{}</b>：{}\r\n'.format(type_, d)
    #
    # with open('rjPhysicalDemo/template_base.json', 'r') as f:
    #     raw_json = json.loads(f.read())
    #
    # with open('rjPhysicalDemo/template.json', 'w') as f:
    #     raw_json['medical_history']['display'] = display + raw_json['medical_history']['display']
    #     raw_json['medical_history']['segments'].extend(segments)
    #
    #     f.write('demo({})'.format(json.dumps(raw_json, ensure_ascii=False)))
    # print(arg.file_name)
    # print('请检查')


if __name__ == '__main__':
    # extract_obj = ExtractStructure(
    #     file_path='西医_内科.txt',
    #     file_path='/Users/jeremy.li/Basebit/Projects/AutoTemplate/pdf2text/bookTextsManual',
    #     raw_text='123',
    # )
    # extract_obj.paragraphs = {
    #     'test': {'sort': 1, 'paragraph': '吸烟史：无 有 平均_支/日，时间_年 ，戒烟：否 是 时间'}
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
