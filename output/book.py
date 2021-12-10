#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/10 12:05
# @File    : book.py.py
# @Software: Basebit
# @Description:

from main import *


def record(result):
    # 数据入库逻辑
    file_names = []
    displays = []
    segments = []

    # insert args
    # print(args)
    for arg in result:
        for infos in arg.paragraphs.values():
            for segment in infos['segments_show']:
                file_names.append(arg.file_name)
                displays.append(segment['display'])
                segments.append(segment['segment'])
    data2excel(pd.DataFrame({
        'file_name': file_names,
        'display': displays,
        'segment': segments,
    }), 'book_result.xlsx', 'base')


if __name__ == '__main__':
    base_path = '/Users/jeremy.li/Basebit/Projects/AutoTemplate/pdf2text/bookTextsManual'
    g = os.walk(base_path)
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
            result = main(
                args=[extract_obj],
                begin_handle=paragraph2sentence_handle
            )
            record(result)
