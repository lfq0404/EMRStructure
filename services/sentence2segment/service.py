#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/6 14:43
# @File    : service.py
# @Software: Basebit
# @Description:

from services.segment_structure.service import SingleChoiceWithOthersStructure, SingleChoiceStructure, \
    SingleChoiceWithAdditionStructure


class SingleChoiceWithOthers:
    """
    腹部视诊：正常 膨隆 凹陷 其他
    单选+自定义选项
    """

    def extract(self, sentence):
        print('“{}” 归类为：单选+自定义选项'.format(sentence))
        return [SingleChoiceWithOthersStructure(sentence)]


class SingleChoice:
    """
    腹部视诊：正常 膨隆 凹陷
    单选
    """

    def extract(self, sentence):
        print('“{}” 归类为：单选'.format(sentence))
        return [SingleChoiceStructure(sentence)]


class SingleChoiceWithAddition:
    """
    预防接种史：无 不详 有 预防接种疫苗
    单选 + 补充说明
    """

    def extract(self, sentence):
        print('“{}” 归类为：单选 + 补充说明'.format(sentence))
        return [SingleChoiceWithAdditionStructure(sentence)]
