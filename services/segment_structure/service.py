#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/6 17:04
# @File    : service.py
# @Software: Basebit
# @Description:
import re
import regex

import utils.constant as cons
import services.sentence2segment.constant as s2s_cons


# ---------- 不同类型segment的结构  ---------------


class SegmentStructure:
    KEY_DISPLAY = 'display'
    KEY_SEGMENT = 'segment'

    def __init__(self, text):
        before_punctuation, text, after_punctuation = re.findall(
            '^([{punctuation}]*)(.+?)([{punctuation}]*)$'.format(punctuation=cons.PUNCTUATION), text)[0]
        self.before_punctuation = before_punctuation
        self.after_punctuation = after_punctuation
        self.text = text

    def show(self):
        """
        输出结果
        :return: {'display': xxx, 'segment': {}}
        """
        raise ValueError('SegmentStructure.show必须重写')

    def _get_input_option(self, color, value, before_display='', after_display='', placeholder='', label="其他"):
        """
        获取用户输入的选项结构
        :param color:
        :param value:
        :return:
        """
        return {
            "label": label,
            "display": before_display + "{自定义文本}" + after_display,
            "props": {"color": color},
            "value": str(value),
            "addition": [{
                "label": "自定义文本",
                "type": "TEXT",
                "value": "",
                "freetextPrefix": "",
                "freetextPostfix": "",
                "placeholder": placeholder}]
        }


class TextSegmentStructure(SegmentStructure):
    """
    纯文本类型的segment
    """

    def show(self):
        return {
            self.KEY_DISPLAY: self.text,
            self.KEY_SEGMENT: {}
        }


class SingleChoiceStructure(SegmentStructure):
    """
    单选的segment
    腹部视诊：正常 膨隆 凹陷
    """

    def __init__(self, text):
        super().__init__(text)
        display, options = regex.findall('(.+[:：])(.+)', self.text)[0]
        self.display = display
        self.label = re.sub('[:：]', '', display)
        self.options = [i for i in re.findall(r'[^{} ]+'.format(cons.PUNCTUATION), options)]  # 标点符号 + 空格

    def show(self):
        return {
            self.KEY_DISPLAY: '{}{{{}}}{}'.format(self.before_punctuation, self.label, self.after_punctuation),
            self.KEY_SEGMENT: self.segment,
        }

    @property
    def segment(self):
        options = []
        for ind, option in enumerate(self.options):
            options.append({
                'label': option,
                'display': '{}{}'.format(self.display, option),
                'value': str(ind),
                'props': {
                    'color': 'green' if ind == 0 else 'red',
                },
                'addition': None
            })
        segment = {
            "label": self.label,
            "type": "RADIO",
            "value": ["0"],
            "options": options
        }
        return segment


class SingleChoiceWithOthersStructure(SingleChoiceStructure):
    """
    单选+补充的segment
    腹部视诊：正常 膨隆 凹陷 其他
    """

    def __init__(self, text):
        super().__init__(text)
        self.options = [i for i in self.options if i not in s2s_cons.SINGLE_CHOICE_WITH_OTHERS_TEXTS]

    @property
    def segment(self):
        segment = super().segment
        options = segment['options']
        count = len(options)
        segment['options'].append(
            self._get_input_option('red', count + 1, before_display=self.display)
        )

        return segment


class SingleChoiceWithAdditionStructure(SingleChoiceStructure):
    """
    预防接种史：无 不详 有 预防接种疫苗
    单选 + 补充说明
    """

    def __init__(self, text):
        super().__init__(text)
        self.addtion_text = [i for i in self.options if i in s2s_cons.SINGLE_CHOICE_WITH_ADDITION_TEXTS][0]
        self.options = [i for i in self.options if i not in s2s_cons.SINGLE_CHOICE_WITH_ADDITION_TEXTS]

    @property
    def segment(self):
        segment = super().segment
        # 默认是最后一个选项才有补充说明
        segment['options'][-1]['display'] += '（{{{}}}）'.format(self.addtion_text)
        segment['options'][-1]['addition'] = [self._get_input_option('red', 0, label='预防接种疫苗', placeholder='预防接种疫苗')]

        return segment


class MultipleChoiceWithOthersStructure(SegmentStructure):
    """
    多选+补充的segment
    乙肝、卡介苗、脊灰糖丸、百白破、麻疹、流脑、乙脑，其他：
    """
