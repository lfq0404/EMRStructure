#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/6 14:43
# @File    : service.py
# @Software: Basebit
# @Description:

from services.segment_structure.service import SingleChoiceWithOthersStructure, SingleChoiceStructure


class SingleChoiceWithOthers:
    """
    腹部视诊：正常 膨隆 凹陷 其他
    单选+补充
    """

    def extract(self, sentence):
        return [SingleChoiceWithOthersStructure(sentence)]


class SingleChoice:
    """
    腹部视诊：正常 膨隆 凹陷
    单选
    """

    def extract(self, sentence):
        return [SingleChoiceStructure(sentence)]
