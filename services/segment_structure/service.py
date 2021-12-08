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
import services.segment_structure.config as conf


# ---------- 不同类型segment的结构  ---------------


class SegmentStructure:
    KEY_DISPLAY = 'display'
    KEY_SEGMENT = 'segment'

    def __init__(self, text):
        before_punctuation, text, after_punctuation = re.findall(
            '^([{punctuation}]*)(.+?)([{punctuation}]*)$'.format(punctuation=cons.BROKEN_PUNC), text)[0]
        self.before_punctuation = before_punctuation
        self.after_punctuation = after_punctuation
        self.text = text

    def show(self):
        """
        输出结果
        :return: {'display': xxx, 'segment': {}}
        """
        raise ValueError('SegmentStructure.show必须重写')

    def _get_text_addition(self, placeholder='', label='自定义文本', pre_fix='', post_fix=''):
        """
        获取自定义文本的addition
        :param label:
        :param placeholder:
        :return:
        """
        return {
            "label": label,
            "type": "TEXT",
            "value": "",
            "freetextPrefix": pre_fix,
            "freetextPostfix": post_fix,
            "placeholder": placeholder
        }

    def _get_input_option(self, color, value, before_display='', after_display='', placeholder='', label="其他"):
        """
        本选项允许用户自定义输入
        :param color:
        :param value:
        :return:
        """
        return {
            "label": label,
            "display": before_display + "{自定义文本}" + after_display,
            "props": {"color": color},
            "value": str(value),
            "addition": [self._get_text_addition(placeholder)]
        }

    def _get_radio_option(self, label, display, ind):
        """
        获取单选的选项
        :param label:
        :param display:
        :param ind:
        :return:
        """
        return {
            "label": label,
            "display": display,
            "props": {
                "color": "green" if ind == 0 else 'red'
            },
            "value": str(ind),
            "addition": None
        }

    def _get_label_name(self, raw_label):
        """
        获取label名，主要是为了剔除所有的符号，只保留中英文
        :param raw_label:
        :return:
        """
        return ''.join([i for i in regex.split('[{} ]'.format(cons.PUNCTUATION), raw_label) if i])

    def _del_option_splits(self, text):
        """
        删除文本中的选项连接符
        :param text:
        :return:
        """
        return regex.sub('[{}]'.format(''.join(cons.OPTION_SPLITS)), '', text)


class SingleChoiceStructure(SegmentStructure):
    """
    单选的segment
    腹部视诊：正常 膨隆 凹陷
    """
    display_format = '{}{}'

    def __init__(self, text, begin_ind=0, only_option=False):
        super().__init__(text)
        display, options = regex.findall('(.+?[:：])(.+)', self.text)[0]
        self.display = display
        self.begin_ind = begin_ind
        self.only_option = only_option  # 是否在display中只展示选项
        self.label = re.sub('[:：]', '', display)
        self.options = [i for i in re.findall(r'[^{} ]+'.format(cons.BROKEN_PUNC), options)]  # 标点符号 + 空格

    def show(self):
        return {
            self.KEY_DISPLAY: '{}{{{}}}{}'.format(self.before_punctuation, self.label, self.after_punctuation),
            self.KEY_SEGMENT: self.segment,
        }

    @property
    def segment(self):
        options = []
        ind = self.begin_ind
        for option in self.options:
            options.append({
                'label': option,
                'display': option if self.only_option else self.display_format.format(self.display, option),
                'value': str(ind),
                'props': {
                    'color': 'green' if ind == 0 else 'red',
                },
                'addition': None
            })
            ind += 1
        segment = {
            "label": self.label,
            "type": "RADIO",
            "value": [str(self.begin_ind)],
            "options": options
        }
        return segment


class BracketsSingleChoiceStructure(SingleChoiceStructure):
    """
    括号单选
    """
    display_format = '{}({})'

    def __init__(self, text, begin_ind=0, only_option=False):
        super(SingleChoiceStructure, self).__init__(text)
        # '振动觉', '正常 减退 消失'
        self.label, options = regex.findall('(.+?)[\(（](.+)[\)）]', self.text)[0]
        self.begin_ind = begin_ind
        self.only_option = only_option
        self.display = self.label
        self.options = [i for i in re.findall(r'[^{} ]+'.format(cons.BROKEN_PUNC), options)]  # 标点符号 + 空格


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
        self.addtion_texts = [i for i in self.options if i in s2s_cons.SINGLE_CHOICE_WITH_ADDITION_TEXTS]
        self.options = [i for i in self.options if i not in s2s_cons.SINGLE_CHOICE_WITH_ADDITION_TEXTS]

    @property
    def segment(self):
        segment = super().segment
        # 默认是最后一个选项才有补充说明
        # 拼接结果为：'毒品接触史 ：有（{毒品名称}，{时间}，{给药方式}）'
        segment['options'][-1]['display'] += '（{}）'.format('，'.join(['{{{}}}'.format(i) for i in self.addtion_texts]))
        segment['options'][-1]['addition'] = [self._get_text_addition(label=i, placeholder=i) for i in
                                              self.addtion_texts]

        return segment


class SmokeStructure(SingleChoiceStructure):
    """
    吸烟史，特殊处理
    """

    def __init__(self, text):
        # 继承单选
        super().__init__(text)
        self.options = ['无']

    def show(self):
        return {
            self.KEY_DISPLAY: '{}{{{}}}{}'.format(self.before_punctuation, self.label, self.after_punctuation),
            self.KEY_SEGMENT: self.segment,
        }

    @property
    def segment(self):
        segment = super().segment
        segment['options'].append({
            "label": "有",
            "display": "平均{频率}支/日，时间{吸烟时长}年，戒烟：{戒烟}",
            "props": {
                "color": "red"
            },
            "addition": [
                self._get_text_addition(label='频率'),
                self._get_text_addition(label='吸烟时长'),
                SingleChoiceWithAdditionStructure('戒烟：否 是 时间').segment,
            ],
            "value": "1"
        })
        return segment


class DrinkStructure(SingleChoiceStructure):
    """
    饮酒史，特殊处理
    """

    def __init__(self, text):
        # 继承单选
        super().__init__(text)
        self.options = ['无']

    def show(self):
        return {
            self.KEY_DISPLAY: '{}{{{}}}{}'.format(self.before_punctuation, self.label, self.after_punctuation),
            self.KEY_SEGMENT: self.segment,
        }

    @property
    def segment(self):
        segment = super().segment
        segment['options'].append({
            "label": "有",
            "display": "平均{频率}{单位}/日，时间{饮酒时长}年，戒酒：{戒酒}",
            "props": {
                "color": "red"
            },
            "addition": [
                self._get_text_addition(label='频率'),
                SingleChoiceStructure('单位：克 两', begin_ind=1, only_option=True).segment,
                self._get_text_addition(label='饮酒时长'),
                SingleChoiceWithAdditionStructure('戒酒：否 是 时间').segment,
            ],
            "value": "1"
        })
        return segment


class TextInputStructure(SegmentStructure):
    """
    自定义输入

    T   ℃
    """

    def __init__(self, text):
        super().__init__(text)
        self.label = re.sub('[{}输入]'.format(cons.PUNCTUATION), '', self.text)
        n = 0
        self.add_labels = []
        while '输入' in self.text:
            n += 1
            add_label = 'input{}'.format(n)
            self.text = re.sub('输入', '{{{}}}'.format(add_label), self.text, 1)
            self.add_labels.append(add_label)

        self.display = self.text

    def show(self):
        return {
            self.KEY_DISPLAY: '{}{{{}}}{}'.format(self.before_punctuation, self.label, self.after_punctuation),
            self.KEY_SEGMENT: self.segment,
        }

    @property
    def segment(self):
        if len(self.add_labels) == 1:
            # 如果输入框只有一个，则走普通的逻辑
            pre_fix, post_fix = self.text.split('{input1}')
            return self._get_text_addition(label=self.label, pre_fix=pre_fix, post_fix=post_fix)
        else:
            # 目前在一个segment中不支持多个一级输入框，暂时使用radio来过渡下
            return {
                'label': self.label,
                'type': 'RADIO',
                'value': ['0'],
                'options': [
                    {
                        "label": "",
                        "display": self.display,
                        "props": {
                            "color": "orange"
                        },
                        "addition": [self._get_text_addition(label=i) for i in self.add_labels],
                        "value": "0"
                    }
                ]
            }


class SingleChoiceWithExtendTextStructure(SegmentStructure):
    """
    瞳孔：等大等圆 不等(左_ mm 右__mm)
    """
    replace_cfg = [
        {'patt': '左\s*mm', 'repl': '左{左}mm', 'label': '左'},
        {'patt': '右\s*mm', 'repl': '右{右}mm', 'label': '右'},
        {'patt': '内\s*cm', 'repl': '内{内}cm', 'label': '内'},
        {'patt': '外\s*cm', 'repl': '外{外}cm', 'label': '外'},
        {'patt': '肋下\s*cm', 'repl': '肋下{肋下}cm', 'label': '肋下'},
        {'patt': '剑突下\s*cm', 'repl': '剑突下{剑突下}cm', 'label': '剑突下'},
        {'patt': '质地', 'repl': '质地：{质地}', 'label': '质地'},
        {'patt': '表面', 'repl': '表面：{表面}', 'label': '表面'},
        {'patt': '边缘', 'repl': '边缘：{边缘}', 'label': '边缘'},
        {'patt': '压痛', 'repl': '压痛：{压痛}', 'label': '压痛'},
        {'patt': '第\s+椎体', 'repl': '第{椎体}椎体', 'label': '椎体'},
    ]

    def __init__(self, text):
        super().__init__(text)
        # '瞳孔：', '等大等圆 不等', '(左 mm 右 mm)'
        self.display, self.options, self.extend_text = re.findall('(.+[:：])\s*(.+)([\(（].+[\)）])', text)[0]

    def show(self):
        return SingleChoiceStructure(self.display + self.options).show()

    @property
    def segment(self):
        segment = SingleChoiceStructure(self.display + self.options).segment
        # 默认是最后一个选项才有补充说明
        addtions = []
        for cfg in self.replace_cfg:
            match = regex.search(cfg['patt'], self.extend_text)
            if match:
                addtions.append(cfg['label'])
                self.extend_text = regex.sub(cfg['patt'], cfg['repl'], self.extend_text)
        segment['options'][-1]['display'] += self.extend_text
        segment['options'][-1]['addition'] = [self._get_text_addition(label=i) for i in addtions]

        return segment


class SingleChoiceWithSingleChoiceStructure(SegmentStructure):
    """
    角膜：正常 混浊(左 右) 溃疡(左 右)
    """

    def __init__(self, text):
        super().__init__(text)
        # ['混浊(左 右)', '溃疡(左 右)']
        self.addition_options = re.findall('(?<=[\s:：])(\S+?[\(（].+?[\)）])', text)
        # 角膜：正常
        for i in self.addition_options:
            text = text.replace(i, '')
        # '角膜：', '正常'
        self.display, self.options = re.findall('(.+[:：])\s*(.+)', text)[0]
        # ['左', '右']
        # self.sub_options = [i for i in regex.split('[{} ]'.format(cons.PUNCTUATION), sub_options) if i]

    def show(self):
        return SingleChoiceStructure(self.display + self.options).show()

    @property
    def segment(self):
        segment = SingleChoiceStructure(self.display + self.options).segment
        last_value = int(segment['options'][-1]['value'])
        for addition_option in self.addition_options:
            last_value += 1
            temp = [i for i in regex.split('[{} ]'.format(cons.PUNCTUATION), addition_option) if i]
            label = temp[0]
            if conf.OPTIONS_MAP.get(''.join(temp[1:])):
                addition_label, sub_options = conf.OPTIONS_MAP[''.join(temp[1:])]
            else:
                addition_label = ''.join(temp[1:])
                sub_options = temp[1:]
            segment['options'].append({
                'label': label,
                'display': '{}{}({{{}}})'.format(self.display, label, addition_label),
                'value': str(last_value),
                'props': {
                    'color': 'red'
                },
                'addition': [SingleChoiceStructure(
                    '{}：{}'.format(addition_label, ' '.join(sub_options)), begin_ind=1, only_option=True).segment]
            })

        return segment


class YesNoChoiceStructure(SegmentStructure):
    """
    有无末梢发绀
    """

    def __init__(self, text):
        super().__init__(text)
        self.label = self._get_label_name(self.text.replace('有无', ''))

    def show(self):
        return {
            self.KEY_DISPLAY: '{}{{{}}}{}'.format(self.before_punctuation, self.label, self.after_punctuation),
            self.KEY_SEGMENT: self.segment,
        }

    @property
    def segment(self):
        return {
            "label": self.label,
            "type": "RADIO",
            "value": [
                "0"
            ],
            "options": [self._get_radio_option(*i) for i in [
                ['无', self.text.replace('有无', '无'), 0],
                ['有', self.text.replace('有无', '有'), 1],
            ]],

        }


class YesNoWithSingleChoiceStructure(YesNoChoiceStructure):
    """
    有无下肢水肿(轻/中/重)
    """

    def __init__(self, text):
        super().__init__(text)
        self.raw_text = self.text
        self.text = re.sub('\(.*\)', '', self.text)

    @property
    def segment(self):
        segment = super().segment
        # 去掉所有的选项分割符，与配置比较
        text_temp = self._del_option_splits(self.raw_text)
        options = []
        for option_text, opt in conf.OPTIONS_MAP.items():
            if option_text in text_temp:
                options = opt[1]
                break
        if not options:
            raise ValueError('YesNoWithSingleChoiceStructure的配置还不兼容：{}'.format(self.raw_text))

        # 将display：'有下肢水肿(轻/中/重)' --> '有下肢水肿({轻中重})'
        segment['options'][-1]['display'] += '（{{{}}}）'.format(opt[0])
        segment['options'][-1]['addition'] = [
            SingleChoiceStructure('{}:{}'.format(opt[0], ' '.join(options)), begin_ind=1,
                                  only_option=True).segment,
        ]
        return segment


class YesNoWithBeforeSingleChoiceStructure(YesNoChoiceStructure):
    """
    左/右下肢有无静脉曲张
    """

    def __init__(self, text):
        super().__init__(text)
        self.raw_text = self.text
        # 左右下肢有无静脉曲张
        self.text = self._del_option_splits(self.raw_text)
        # 下肢有无静脉曲张
        for repl in conf.OPTIONS_MAP:
            self.text = self.text.replace(repl, '')

    @property
    def segment(self):
        segment = super().segment
        # 去掉所有的选项分割符，与配置比较
        text_temp = self._del_option_splits(self.raw_text)
        options = []
        for option_text, opt in conf.OPTIONS_MAP.items():
            if option_text in text_temp:
                options = opt[1]
                break
        if not options:
            raise ValueError('YesNoWithSingleChoiceStructure的配置还不兼容：{}'.format(self.raw_text))

        segment['options'][-1]['display'] = '{{{}}}'.format(opt[0]) + segment['options'][-1]['display']
        segment['options'][-1]['addition'] = [
            SingleChoiceStructure('{}:{}'.format(opt[0], ' '.join(options)), begin_ind=1,
                                  only_option=True).segment,
        ]
        return segment


class MultipleChoiceStructure(SegmentStructure):
    """
    多选
    乙肝、卡介苗、脊灰糖丸、百白破、麻疹、流脑、乙脑
    """

    def __init__(self, text, begin_ind=1):
        super().__init__(text)
        self.str_options = text
        self.begin_ind = begin_ind
        self.label = regex.sub('[{}]'.format(cons.BROKEN_PUNC), '', self.str_options)
        # ['乙肝', '卡介苗', '脊灰糖丸', '百白破', '麻疹', '流脑', '乙脑']
        self.options = regex.split('[{}]'.format(cons.BROKEN_PUNC), self.text)

    def show(self):
        return {
            self.KEY_DISPLAY: '{}{{{}}}{}'.format(
                self.before_punctuation, self.label, self.after_punctuation),
            self.KEY_SEGMENT: self.segment,
        }

    @property
    def segment(self):
        options = []
        ind = self.begin_ind
        for option in self.options:
            options.append({
                'label': option,
                'display': option,
                'value': str(ind),
                'props': {
                    'color': 'green' if ind == 0 else 'red',
                },
                'addition': None
            })
            ind += 1
        segment = {
            "label": self.label,
            "type": "CHECKBOX",
            "value": [str(self.begin_ind)],
            "options": options
        }
        return segment


class MultipleChoiceWithOthersStructure(MultipleChoiceStructure):
    """
    有无心脑血管疾病、代谢性疾病、肝、肾等慢性疾病史
    """

    def __init__(self, text, begin_ind=1):
        before_punctuation, text, after_punctuation = re.findall(
            '^([{punctuation}]*)(.+?)([{punctuation}]*)$'.format(punctuation=cons.BROKEN_PUNC), text)[0]
        self.before_punctuation = before_punctuation
        self.after_punctuation = after_punctuation
        # '心脑血管疾病、代谢性疾病、肝、肾', '等慢性疾病史'
        self.str_options, self.desc = re.findall('有无(.*)(等.*)', text)[0]
        self.text = self.str_options
        self.begin_ind = begin_ind
        self.label = regex.sub('[{}]'.format(cons.BROKEN_PUNC), '', self.str_options)
        self.options = regex.split('[{}]'.format(cons.BROKEN_PUNC), self.text)

    @property
    def segment(self):
        segment = super().segment
        label = segment['label']
        value = int(segment['options'][-1]['value']) + 1
        segment['options'].append(self._get_input_option('red', value, before_display='其他：'))
        # 拼接“有无”的那层选项
        return {
            'label': '有无' + label,
            'type': 'RADIO',
            'value': ['0'],
            'options': [
                {
                    "label": "无",
                    "display": "无{}{}".format(self.str_options, self.desc),
                    "props": {
                        "color": "green"
                    },
                    "addition": None,
                    "value": "0"
                },
                {
                    "label": "有",
                    "display": "有{{{}}}".format(label),
                    "props": {
                        "color": "red"
                    },
                    "addition": [segment],
                    "value": "1"
                },

            ]
        }
