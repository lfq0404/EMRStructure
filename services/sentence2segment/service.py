#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/6 14:43
# @File    : service.py
# @Software: Basebit
# @Description:
import regex

import services.segment_structure.service as struc
import utils.constant as util_cons


class SingleChoiceWithOthers:
    """
    腹部视诊：正常 膨隆 凹陷 其他
    单选+自定义选项
    """

    def extract(self, sentence):
        # todo：字体颜色封装
        print('“{}” 归类为：\033[32m单选+自定义选项\033[0m'.format(sentence))
        return [struc.SingleChoiceWithOthersStructure(sentence)]


class SingleChoice:
    """
    腹部视诊：正常 膨隆 凹陷
    单选
    """

    def extract(self, sentence):
        print('“{}” 归类为：\033[32m冒号单选\033[0m'.format(sentence))
        return [struc.SingleChoiceStructure(sentence)]


class BracketsSingleChoice:
    """
    精神病(无 有)
    括号单选单选
    """

    def extract(self, sentence):
        print('“{}” 归类为：\033[32m括号单选\033[0m'.format(sentence))
        return [struc.BracketsSingleChoiceStructure(sentence)]


class Smoke:
    """
    吸烟史：无 有 平均_支/日，时间_年 ，戒烟：否 是 时间
    特殊处理
    """

    def extract(self, sentence):
        print('“{}” 归类为：\033[32m吸烟史-特殊处理\033[0m'.format(sentence))
        return [struc.SmokeStructure(sentence)]


class Drink:
    """
    饮酒史：无 有 平均_克(两)/日 ，时间 __年 ，戒酒 ：否 是 时间
    特殊处理
    """

    def extract(self, sentence):
        print('“{}” 归类为：\033[32m饮酒史-特殊处理\033[0m'.format(sentence))
        return [struc.DrinkStructure(sentence)]


class SingleChoiceWithExtendText:
    """
    瞳孔：等大等圆 不等(左_ mm 右__mm)
    """

    def extract(self, sentence):
        print('“{}” 归类为：\033[32m单选-输入扩展说明\033[0m'.format(sentence))
        return [struc.SingleChoiceWithExtendTextStructure(sentence)]


class SingleChoiceWithSingleChoice:
    """
    气管：正中 偏移 (左/右)
    """

    def extract(self, sentence):
        print('“{}” 归类为：\033[32m单选后再接单选\033[0m'.format(sentence))
        return [struc.SingleChoiceWithSingleChoiceStructure(sentence)]

class LRChoiceWithSingleChoice:
    """
    Laseque征：左(- +)；右(- +)
    """

    def extract(self, sentence):
        print('“{}” 归类为：\033[32m单选后再接单选\033[0m'.format(sentence))
        return [struc.LRChoiceWithSingleChoiceStructure(sentence)]


class YesNoWithSingleChoice:
    """
    有无下肢水肿(轻/中/重)
    """

    def extract(self, sentence):
        print('“{}” 归类为：\033[32m是否选择后再接单选\033[0m'.format(sentence))
        return [struc.YesNoWithSingleChoiceStructure(sentence)]


class YesNoWithBeforeSingleChoice:
    """
    左/右下肢有无静脉曲张
    """

    def extract(self, sentence):
        print('“{}” 归类为：\033[32m是否选择后再接前部单选\033[0m'.format(sentence))
        return [struc.YesNoWithBeforeSingleChoiceStructure(sentence)]


class YesNoChoice:
    """
    有无末梢发绀
    """

    def extract(self, sentence):
        print('“{}” 归类为：\033[32m是否选择\033[0m'.format(sentence))
        return [struc.YesNoChoiceStructure(sentence)]


class SingleChoiceWithAddition:
    """
    预防接种史：无 不详 有 预防接种疫苗
    单选 + 补充说明
    """

    def extract(self, sentence):
        print('“{}” 归类为：\033[32m单选 + 补充说明\033[0m'.format(sentence))
        return [struc.SingleChoiceWithAdditionStructure(sentence)]


class TextInput:
    """
    T   ℃
    自定义输入
    """

    def extract(self, sentence):
        print('“{}” 归类为：\033[32m自定义输入\033[0m'.format(sentence))
        return [struc.TextInputStructure(sentence)]


class MultipleChoiceWithOthers:
    """
    有无心脑血管疾病、代谢性疾病、肝、肾等慢性疾病史
    多选 + 输入补充
    """

    def extract(self, sentence):
        print('“{}” 归类为：\033[32m多选 + 输入补充\033[0m'.format(sentence))
        return [struc.MultipleChoiceWithOthersStructure(sentence)]
