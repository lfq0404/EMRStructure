#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/3 14:07
# @File    : service.py
# @Software: Basebit
# @Description:
import os
import re

from services.resource2raw.constant import RAW_TEMPLATES_PATH, EXTRACT_TEMPLATE_FILES
from utils.funcs import HtmlParse
from utils.structures import ExtractStructure


class Html2Raw:
    """
    HTML转原始文本
    todo：所有的service校验必须有extract
    """

    def extract(self):
        g = os.walk(RAW_TEMPLATES_PATH)
        result = []
        for path, _, file_list in g:
            for ind, file in enumerate(file_list):
                # file = '4280000-门诊推拿科-门诊病历(初诊)-腰肌筋膜炎-门诊病历(初诊).html'

                if self._is_continue(file):
                    continue

                file_path = '{}/{}'.format(path, file)
                print('开始处理<{}>：{}'.format(ind, file_path))

                result.append(ExtractStructure(
                    file_name=file,
                    file_path=file_path,
                    raw_text=HtmlParse(file_path).html2text()
                ))

        return result

    def _is_continue(self, file_name):
        """
        是否继续下一个文件（跳过该文件）
        :return:
        """
        # 如果文件不是以HTML结尾，则忽略
        if not re.findall('^\d.*html', file_name):
            return True

        # 如果文件不在此次范围内，则忽略
        if EXTRACT_TEMPLATE_FILES is not None and file_name not in EXTRACT_TEMPLATE_FILES:
            return True
