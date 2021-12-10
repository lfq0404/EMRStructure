#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/10 10:45
# @File    : data2excel.py
# @Software: Basebit
# @Description:
import os

import pandas as pd


def data2excel(data, file_path, sheet_name, is_append=True):
    """
    将数据写入Excel中
    :param data: 需要新写入的数据
    :param file_path:
    :param sheet_name:
    :param is_append:
    :return:
    """
    if is_append:
        if os.path.exists(file_path):
            old_data = pd.read_excel(file_path, sheet_name=sheet_name)  # 读取原数据文件和表
            # 拼接新老数据
            data = pd.concat([old_data, data])

    data.to_excel(file_path, sheet_name=sheet_name, startrow=0, index=False, header=True)


if __name__ == '__main__':
    data = pd.DataFrame({
        '水果': ['苹果1', '梨1', '草莓1'],
        '数量': [3, 2, 5],
        '价格': [10, 5.5, 8],
    })
    data2excel(data, 'test.xlsx', '测试')
