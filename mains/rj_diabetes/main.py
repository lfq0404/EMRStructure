#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/16 11:46
# @File    : main.py
# @Software: Basebit
# @Description:
import pandas as pd
from mains.constant import *
from utils.funcs import raw_obj_call_handles
from utils.structures import RJExtractStructure
from utils.constant import BASE_PATH


def main(args, begin_handle):
    level = HANDLES.index(begin_handle)
    args = raw_obj_call_handles(args, HANDLES[level:])


if __name__ == '__main__':
    file_path = '{}/mains/rj_diabetes/sh_rj_nfma.xlsx'.format(BASE_PATH)
    df = pd.read_excel(file_path)
    df.fillna('', inplace=True)

    for ind, line in df.iterrows():
        if ind < 5:
            continue
        extract_obj = RJExtractStructure(
            diagnosis=line.诊断,
        )
        extract_obj.paragraphs = {
            '个人史': {'sort': 1, 'paragraph': line.个人史},
            '既往史': {'sort': 2, 'paragraph': line.既往史},
            '家族史': {'sort': 3, 'paragraph': line.家族史},
            '接种史': {'sort': 4, 'paragraph': line.接种史},
            '月经生育史': {'sort': 5, 'paragraph': line.月经生育史},
            '婚姻史': {'sort': 6, 'paragraph': line.婚姻史},
            # '体格检查': {'sort': 7, 'paragraph': line.体格检查},
            # '专科检查': {'sort': 8, 'paragraph': line.专科检查},
            '辅助检查': {'sort': 9, 'paragraph': line.辅助检查},
            '系统回顾': {'sort': 10, 'paragraph': line.系统回顾},
        }
        main(
            args=[extract_obj],
            begin_handle=paragraph2sentence_handle,
        )
