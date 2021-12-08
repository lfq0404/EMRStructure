#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/3 09:14
# @File    : config.py
# @Software: Basebit
# @Description:

from zhon.hanzi import punctuation as zh_punc
import re
import jieba
import jieba.posseg as psg

import services.paragraph2sentence.service as service
from utils.structures import CfgStructure

_ENUM_DISEASES = ['高血压', '脑梗塞', '糖尿病', '哮喘病', '心脏病']

root_node = CfgStructure(
    replace_cfg=[
        {
            # 补全右括号
            'patt': '(.*)(\()([^\)]*)$',
            'repl': r'\1\2\3)'
        },
        {
            # 补全右括号
            'patt': '(.*)(（)([^\)]*)$',
            'repl': r'\1\2\3）'
        },

    ],
    classify_cfg=[
        # ['/有阳性家族史', service.SpecialWordBlockExtract([('有阳性家族史', 'n')])],
        # ['体质一般', service.SpecialWordBlockExtract([('一般', 'option')])],
        # ['有无咽部红肿', service.SpecialWordBlockExtract([('咽部红肿', 'n')])],
        # ['关节无红肿畸形', service.SpecialWordBlockExtract([('红肿畸形', 'n')])],
        # ['输入压痛明显', service.SpecialWordBlockExtract([('压痛明显', 'n')])],
        ['', service.Paragraph2SentenceBase()],
    ]
)

AG_DEL = 'del'  # 需要被删除的词性
AG_OPTION = 'option'  # 作为选项的词，与jiebadict的option一致
AG_TEXT = 'text'  # 作为自定义文本的词，与jiebadict的option一致
AG_MERGE_OPTION = 'mergge_option'  # 需要合并的option
AG_DISPLAY = 'display'  # 直接用于展示的内容
SPLIT_TEXT = '$'  # option之间的分隔符，找一个冷门的字符串。注：只能是一个字符
UNKNOW = 'unknow'  # 不知道怎么写，预填的值
OPTION_FORMAT = '{{{}}}'.format(AG_OPTION)

# segment的各种key
KEY_LABEL = 'label'
KEY_TYPE = 'type'
KEY_VALUE = 'value'
KEY_OPTIONS = 'options'
KEY_DISPLAY = 'display'
KEY_PROPS = 'props'
KEY_COLOR = 'color'
KEY_ADDITION = 'addition'
KEY_FREETEXTPOSTFIX = 'freetextPostfix'  # 在text框后面显示的内容
KEY_FREETEXTPREFIX = 'freetextPrefix'  # 在text框前面显示的内容
KEY_PLACEHOLDER = 'placeholder'
KEY_VALIDATION = 'validation'
KEY_REGEX = 'regex'
KEY_MESSAGE = 'message'

# segment的各种value
VALUE_TYPE_TEXT = 'TEXT'
VALUE_TYPE_RADIO = 'RADIO'
VALUE_TYPE_CHECKBOX = 'CHECKBOX'
VALUE_CUSTOM_TEXT = '自定义文本'

# 默认的词频，设置的比较高，尽量让自定义的词组识别出来
DEFAULT_FREQUENCY = 99999999999999

# 扩展选项。当option设定为该值时，需要扩展为TEXT，让用户填写
EXTENSION_OPTIONS = 'EXTENSION_OPTIONS'

# jieba自定义词组
JIEBA_USER_DICTS = [
    ['手术史', DEFAULT_FREQUENCY, 'n'],
    ['家族性', DEFAULT_FREQUENCY, 'n'],
    ['疾病史', DEFAULT_FREQUENCY, 'n'],
    ['减充血剂', DEFAULT_FREQUENCY, 'n'],
    ['侧下', DEFAULT_FREQUENCY, 'n'],
    ['°', DEFAULT_FREQUENCY, 'n'],
    ['kg/m2', DEFAULT_FREQUENCY, 'n'],
    ['冶游史', DEFAULT_FREQUENCY, 'n'],
    ['治游史', DEFAULT_FREQUENCY, 'n'],
    ['婚', DEFAULT_FREQUENCY, 'n'],
    ['额部', DEFAULT_FREQUENCY, 'n'],
    ['枕部', DEFAULT_FREQUENCY, 'n'],
    ['次/分', DEFAULT_FREQUENCY, 'n'],
    ['C5/6', DEFAULT_FREQUENCY, 'n'],
    ['±', DEFAULT_FREQUENCY, 'n'],
    ['Ⅰ', DEFAULT_FREQUENCY, 'n'],
    ['Ⅱ', DEFAULT_FREQUENCY, 'n'],
    ['Ⅲ', DEFAULT_FREQUENCY, 'n'],
    ['无法暴露', DEFAULT_FREQUENCY, 'n'],
    ['Hoffmann’s', DEFAULT_FREQUENCY, 'n'],
    ['hoffman征', DEFAULT_FREQUENCY, 'n'],
    ['未婚未育', DEFAULT_FREQUENCY, 'n'],
    ['已婚未育', DEFAULT_FREQUENCY, 'n'],
    ['已婚已育', DEFAULT_FREQUENCY, 'n'],
    ['清创缝合', DEFAULT_FREQUENCY, 'n'],
    ['育有', DEFAULT_FREQUENCY, 'n'],
    ['吸凹征', DEFAULT_FREQUENCY, 'n'],
    ['呼吸节律', DEFAULT_FREQUENCY, 'n'],
    ['发绀', DEFAULT_FREQUENCY, 'n'],
    ['曾在', DEFAULT_FREQUENCY, 'n'],
    ['或', DEFAULT_FREQUENCY // 10, 'n'],
    ['阳性家族史', DEFAULT_FREQUENCY, 'n'],
    ['反跳痛', DEFAULT_FREQUENCY, 'n'],
    ['足靴区', DEFAULT_FREQUENCY, 'n'],
    ['踝周', DEFAULT_FREQUENCY, 'n'],
    ['导管评估', DEFAULT_FREQUENCY, 'n'],
    ['导管情况', DEFAULT_FREQUENCY, 'n'],
    ['内置', DEFAULT_FREQUENCY, 'n'],
    ['外露', DEFAULT_FREQUENCY, 'n'],
    ['紫暗', DEFAULT_FREQUENCY, 'n'],
    ['冲管', DEFAULT_FREQUENCY, 'n'],
    ['冷', DEFAULT_FREQUENCY, 'n'],
    ['叩', DEFAULT_FREQUENCY, 'n'],
    ['松', DEFAULT_FREQUENCY, 'n'],
    ['2%利多卡因5ml', DEFAULT_FREQUENCY, 'n'],
    ['4%阿替卡因1.7ml', DEFAULT_FREQUENCY, 'n'],
    ['远中龈切/去骨/分牙', DEFAULT_FREQUENCY, 'n'],
    ['有瘀斑', DEFAULT_FREQUENCY, 'n'],
    ['下肢', DEFAULT_FREQUENCY, 'n'],
    ['锌基封', DEFAULT_FREQUENCY, 'n'],
    ['暂封', DEFAULT_FREQUENCY, 'n'],
    ['后突', DEFAULT_FREQUENCY, 'n'],
    ['长期生活于', DEFAULT_FREQUENCY, 'n'],
    ['瘀血证', DEFAULT_FREQUENCY, 'n'],
    ['寒湿证', DEFAULT_FREQUENCY, 'n'],
    ['肾虚证', DEFAULT_FREQUENCY, 'n'],
    ['左下肢足靴区', DEFAULT_FREQUENCY, 'n'],
    ['内侧', DEFAULT_FREQUENCY, 'n'],
    ['外侧', DEFAULT_FREQUENCY, 'n'],
    ['侧方应力试验', DEFAULT_FREQUENCY, 'n'],
    ['气滞血瘀证', DEFAULT_FREQUENCY, 'n'],
    ['肝肾亏虚证', DEFAULT_FREQUENCY, 'n'],
    ['感受外寒证', DEFAULT_FREQUENCY, 'n'],
    ['湿热中阻证', DEFAULT_FREQUENCY, 'n'],
    ['寒湿犯腰证', DEFAULT_FREQUENCY, 'n'],
    ['湿热犯腰证', DEFAULT_FREQUENCY, 'n'],
    ['左寸口细脉', DEFAULT_FREQUENCY, 'n'],
    ['右寸口细脉', DEFAULT_FREQUENCY, 'n'],
    ['S1-12', DEFAULT_FREQUENCY, 'n'],
    ['Fc棉捻', DEFAULT_FREQUENCY, 'n'],
    ['氢氧化钙糊剂', DEFAULT_FREQUENCY, 'n'],
    ['C/D', DEFAULT_FREQUENCY, 'n'],
    ['右：', DEFAULT_FREQUENCY, 'n'],
    ['左：', DEFAULT_FREQUENCY, 'n'],
    ['右眼结膜充血', DEFAULT_FREQUENCY, 'n'],
    ['左眼结膜充血', DEFAULT_FREQUENCY, 'n'],
    ['T', DEFAULT_FREQUENCY, 'n'],
    ['导管是否完整', DEFAULT_FREQUENCY, 'n'],
    ['阻生', DEFAULT_FREQUENCY, 'n'],
    ['废用', DEFAULT_FREQUENCY, 'n'],

    ['穿刺点及周围皮肤情况', DEFAULT_FREQUENCY * 10, 'n'],
    ['港体及导管处皮肤情况', DEFAULT_FREQUENCY * 10, 'n'],
    ['未冲管', DEFAULT_FREQUENCY * 10, 'n'],
    ['及时间', DEFAULT_FREQUENCY * 10, 'n'],
    ['发生时间', DEFAULT_FREQUENCY * 10, 'n'],
    ['双附件', DEFAULT_FREQUENCY * 10, 'n'],
    ['已告知', DEFAULT_FREQUENCY * 10, 'n'],
    ['未引出', DEFAULT_FREQUENCY * 10, 'n'],
    ['程度', DEFAULT_FREQUENCY * 10, 'n'],
    ['无殊', DEFAULT_FREQUENCY * 10, 'n'],
    ['无渣饮食', DEFAULT_FREQUENCY * 10, 'n'],
    ['如有', DEFAULT_FREQUENCY * 10, 'n'],
    ['可考虑', DEFAULT_FREQUENCY * 10, 'n'],
    ['未来潮', DEFAULT_FREQUENCY * 10, 'n'],
    ['时间：', DEFAULT_FREQUENCY * 10, 'n'],
    ['维护情况', DEFAULT_FREQUENCY * 10, 'n'],
    ['异常情况', DEFAULT_FREQUENCY * 10, 'n'],
    ['一般可', DEFAULT_FREQUENCY * 10, 'n'],
    ['皮肤情况', DEFAULT_FREQUENCY * 10, 'n'],
    ['拔管情况', DEFAULT_FREQUENCY * 10, 'n'],
    ['无明显症状按时复诊', DEFAULT_FREQUENCY * 10, 'n'],
    ['侧', DEFAULT_FREQUENCY * 10, 'n'],
    ['明显红肿', DEFAULT_FREQUENCY * 10, 'n'],
    ['氯双', DEFAULT_FREQUENCY * 10, 'n'],
    ['肩峰下缘', DEFAULT_FREQUENCY * 10, 'n'],

    ['时间', DEFAULT_FREQUENCY // 10, 'text'],
    ['[0]', DEFAULT_FREQUENCY, 'text'],
    ['输入', DEFAULT_FREQUENCY, 'text'],
    ['请输入', DEFAULT_FREQUENCY, 'text'],
    ['编辑', DEFAULT_FREQUENCY, 'text'],
    ['情况', DEFAULT_FREQUENCY, 'text'],
    ['/文字描述', DEFAULT_FREQUENCY, 'text'],

    # 在这添加了option，需要在OPTION_MAP中添加对应的解析
    ['有无', DEFAULT_FREQUENCY, 'option'],
    ['无', DEFAULT_FREQUENCY // 10, 'option'],
    ['是否', DEFAULT_FREQUENCY, 'option'],
    ['左右双', DEFAULT_FREQUENCY, 'option'],
    ['左右', DEFAULT_FREQUENCY, 'option'],
    ['右', DEFAULT_FREQUENCY, 'option'],
    ['左', DEFAULT_FREQUENCY, 'option'],
    ['双', DEFAULT_FREQUENCY, 'option'],
    ['(+)', DEFAULT_FREQUENCY, 'option'],
    ['（+）', DEFAULT_FREQUENCY, 'option'],
    ['(-)', DEFAULT_FREQUENCY, 'option'],
    ['（-）', DEFAULT_FREQUENCY, 'option'],
    ['正常', DEFAULT_FREQUENCY, 'option'],
    ['薄', DEFAULT_FREQUENCY, 'option'],
    ['厚', DEFAULT_FREQUENCY, 'option'],
    ['阴性', DEFAULT_FREQUENCY, 'option'],
    ['阳性', DEFAULT_FREQUENCY, 'option'],
    ['已', DEFAULT_FREQUENCY, 'option'],
    ['（+-）', DEFAULT_FREQUENCY, 'option'],
    ['局部', DEFAULT_FREQUENCY, 'option'],
    ['齐', DEFAULT_FREQUENCY, 'option'],
    ['不齐', DEFAULT_FREQUENCY * 10, 'option'],
    ['升高', DEFAULT_FREQUENCY, 'option'],
    ['未及', DEFAULT_FREQUENCY, 'option'],
    ['阳阴性', DEFAULT_FREQUENCY, 'option'],
    ['淡红', DEFAULT_FREQUENCY, 'option'],
    ['白腻', DEFAULT_FREQUENCY, 'option'],
    ['脉滑', DEFAULT_FREQUENCY, 'option'],
    ['可', DEFAULT_FREQUENCY, 'option'],
    ['弦细', DEFAULT_FREQUENCY, 'option'],
    ['粗', DEFAULT_FREQUENCY, 'option'],
    ['两', DEFAULT_FREQUENCY, 'option'],
    ['中上', DEFAULT_FREQUENCY, 'option'],
    ['平软', DEFAULT_FREQUENCY, 'option'],
    ['平', DEFAULT_FREQUENCY // 10, 'option'],
    ['紫绀', DEFAULT_FREQUENCY, 'option'],
    ['潮红', DEFAULT_FREQUENCY, 'option'],
    ['软', DEFAULT_FREQUENCY, 'option'],
    ['切题', DEFAULT_FREQUENCY, 'option'],
    ['桶状', DEFAULT_FREQUENCY, 'option'],
    ['膨隆', DEFAULT_FREQUENCY, 'option'],
    ['轻度', DEFAULT_FREQUENCY, 'option'],
    ['脓性粘性水样血性干酪样', DEFAULT_FREQUENCY, 'option'],
    ['息肉样乳头状桑葚状菜花样', DEFAULT_FREQUENCY, 'option'],
    ['清', DEFAULT_FREQUENCY, 'option'],
    ['颈项部', DEFAULT_FREQUENCY, 'option'],
    ['广泛性', DEFAULT_FREQUENCY, 'option'],
    ['光泽', DEFAULT_FREQUENCY, 'option'],
    ['好', DEFAULT_FREQUENCY, 'option'],
    ['平伏', DEFAULT_FREQUENCY, 'option'],
    ['反光可见', DEFAULT_FREQUENCY, 'option'],
    ['有关节', DEFAULT_FREQUENCY, 'option'],
    ['原籍', DEFAULT_FREQUENCY, 'option'],
    ['骶棘', DEFAULT_FREQUENCY, 'option'],
    ['条索样', DEFAULT_FREQUENCY, 'option'],
    ['肱二头肌、肱三头肌', DEFAULT_FREQUENCY, 'option'],
    ['合作', DEFAULT_FREQUENCY, 'option'],
    ['-/±/+', DEFAULT_FREQUENCY, 'option'],
    ['黄红状', DEFAULT_FREQUENCY, 'option'],
    ['++/+++', DEFAULT_FREQUENCY, 'option'],
    ['下', DEFAULT_FREQUENCY, 'option'],
    ['双侧上', DEFAULT_FREQUENCY, 'option'],
    ['多', DEFAULT_FREQUENCY // 10, 'option'],
    ['红肿', DEFAULT_FREQUENCY // 10, 'option'],
    ['+/-', DEFAULT_FREQUENCY, 'option'],
    ['减轻', DEFAULT_FREQUENCY, 'option'],
    ['不能', DEFAULT_FREQUENCY, 'option'],
    ['减弱', DEFAULT_FREQUENCY, 'option'],
    ['明显', DEFAULT_FREQUENCY // 10, 'option'],
]
# 自定义词组存在的词
JIEBA_USER_WORDS = [i[0] for i in JIEBA_USER_DICTS]
# 词性为指定的text，且需要在display中保留的词
RETAIN_TEXTS = ['时间']

# option对应的解析规则
# 1、阴性放前面
# 2、sign标识。
#   0：表示阴阳
#   1：表示枚举，颜色全为orange
#   2：全是阳性，颜色均为red
OPTION_MAP = {
    '有无': [['无', '有'], 0, VALUE_TYPE_RADIO],
    '是否': [['否', '是'], 0, VALUE_TYPE_RADIO],
    '左右双': [['左', '右', '双'], 1, VALUE_TYPE_RADIO],
    '双': [['左', '右', '双'], 1, VALUE_TYPE_RADIO],
    '两': [['左', '右', '两'], 1, VALUE_TYPE_RADIO],
    '左右': [['左', '右'], 1, VALUE_TYPE_RADIO],
    '右': [['左', '右'], 1, VALUE_TYPE_RADIO],
    '左': [['左', '右'], 1, VALUE_TYPE_RADIO],
    '无': [['无', '有'], 0, VALUE_TYPE_RADIO],
    '(+)': [['(-)', '(+)'], 0, VALUE_TYPE_RADIO],
    '(-)': [['(-)', '(+)'], 0, VALUE_TYPE_RADIO],
    '（+）': [['（-）', '（+）'], 0, VALUE_TYPE_RADIO],
    '（-）': [['（-）', '（+）'], 0, VALUE_TYPE_RADIO],
    '（+-）': [['（-）', '（+）'], 0, VALUE_TYPE_RADIO],
    '正常': [['正常', '不正常'], 0, VALUE_TYPE_RADIO],
    '薄': [['正常', '薄', '厚'], 0, VALUE_TYPE_RADIO],
    '厚': [['正常', '薄', '厚'], 0, VALUE_TYPE_RADIO],
    '阴性': [['阴性', '阳性'], 0, VALUE_TYPE_RADIO],
    '阳性': [['阴性', '阳性'], 0, VALUE_TYPE_RADIO],
    '已': [['已', '未'], 0, VALUE_TYPE_RADIO],
    '局部': [['局部'], 1, VALUE_TYPE_RADIO],
    '齐': [['齐', '不齐'], 0, VALUE_TYPE_RADIO],
    '不齐': [['齐', '不齐'], 0, VALUE_TYPE_RADIO],
    '升高': [['正常', '升高', '降低'], 0, VALUE_TYPE_RADIO],
    '未及': [['未及', '可及'], 0, VALUE_TYPE_RADIO],
    '阳阴性': [['阴性', '阳性'], 0, VALUE_TYPE_RADIO],
    '淡红': [['淡红', '无淡红'], 0, VALUE_TYPE_RADIO],
    '白腻': [['无白腻', '白腻'], 0, VALUE_TYPE_RADIO],
    '脉滑': [['脉无滑', '脉滑'], 0, VALUE_TYPE_RADIO],
    '可': [['可', '不可'], 0, VALUE_TYPE_RADIO],
    '清': [['清', '不清'], 0, VALUE_TYPE_RADIO],
    '弦细': [['弦细', '粗'], 0, VALUE_TYPE_RADIO],
    '粗': [['弦细', '粗'], 0, VALUE_TYPE_RADIO],
    '中上': [['右上', '中上', '左上', '右下', '中下', '左下'], 1, VALUE_TYPE_RADIO],
    '平软': [['平软', '僵硬'], 0, VALUE_TYPE_RADIO],
    '平': [['平', '不平'], 0, VALUE_TYPE_RADIO],
    '紫绀': [['紫绀'], 0, VALUE_TYPE_RADIO],
    '潮红': [['潮红'], 0, VALUE_TYPE_RADIO],
    '软': [['软', '硬'], 0, VALUE_TYPE_RADIO],
    '切题': [['切题', '不切题'], 0, VALUE_TYPE_RADIO],
    '桶状': [['桶状'], 1, VALUE_TYPE_RADIO],
    '轻度': [['轻度', '中度', '重度'], 2, VALUE_TYPE_RADIO],
    '一般': [['一般'], 1, VALUE_TYPE_RADIO],
    '脓性粘性水样血性干酪样': [['脓性', '粘性', '水样', '血性', '干酪样'], 2, VALUE_TYPE_RADIO],
    '息肉样乳头状桑葚状菜花样': [['息肉样', '乳头状', '桑葚状', '菜花样'], 2, VALUE_TYPE_RADIO],
    '颈项部': [['颈项部'], 1, VALUE_TYPE_RADIO],
    '广泛性': [['广泛性'], 1, VALUE_TYPE_RADIO],
    '光泽': [['光泽'], 0, VALUE_TYPE_RADIO],
    '好': [['好', '不好'], 0, VALUE_TYPE_RADIO],
    '平伏': [['平伏'], 0, VALUE_TYPE_RADIO],
    '反光可见': [['反光可见', '反光不可见'], 0, VALUE_TYPE_RADIO],
    '有关节': [['无关节', '有关节'], 0, VALUE_TYPE_RADIO],
    '原籍': [['原籍', EXTENSION_OPTIONS], 0, VALUE_TYPE_RADIO],
    '骶棘': [['骶棘', EXTENSION_OPTIONS], 1, VALUE_TYPE_RADIO],
    '条索样': [['条索样', EXTENSION_OPTIONS], 1, VALUE_TYPE_RADIO],
    '肱二头肌、肱三头肌': [['肱二头肌、肱三头肌', '肱二头肌', '肱三头肌'], 1, VALUE_TYPE_RADIO],
    '合作': [['合作', '不配合'], 0, VALUE_TYPE_RADIO],
    '平稳': [['平稳', '急促'], 0, VALUE_TYPE_RADIO],
    '红润': [['红润', '苍白', '发绀'], 0, VALUE_TYPE_RADIO],
    '有力': [['有力', '低钝', '遥远'], 0, VALUE_TYPE_RADIO],
    '-/±/+': [['-', '±', '+'], 0, VALUE_TYPE_RADIO],
    '++/+++': [['-', '+', '++', '+++'], 0, VALUE_TYPE_RADIO],
    '黄红状': [['黄红状'], 0, VALUE_TYPE_RADIO],
    '下': [['下', '上'], 1, VALUE_TYPE_RADIO],
    '多': [['少', '多'], 0, VALUE_TYPE_RADIO],
    '双侧上': [['双侧上', '双侧下', '左侧下', '左侧上', '右侧下', '右侧上'], 1, VALUE_TYPE_RADIO],
    '红肿': [['正常', '红肿'], 0, VALUE_TYPE_RADIO],
    '透明': [['透明', '云翳', '斑翳'], 0, VALUE_TYPE_RADIO],
    '圆': [['圆', '欠圆'], 0, VALUE_TYPE_RADIO],
    '+/-': [['-', '+'], 0, VALUE_TYPE_RADIO],
    'n': [['n', 'n+1', 'n+2', 'n-1'], 0, VALUE_TYPE_RADIO],
    '红': [['红', '暗紫', '有瘀斑'], 0, VALUE_TYPE_RADIO],
    '龋': [['正常', '龋', '缺损'], 0, VALUE_TYPE_RADIO],
    '紧张': [['正常', '紧张'], 0, VALUE_TYPE_RADIO],
    '减轻': [['减轻', '加重'], 0, VALUE_TYPE_RADIO],
    '可以': [['可以', '不能'], 0, VALUE_TYPE_RADIO],
    '不能': [['可以', '不能'], 0, VALUE_TYPE_RADIO],
    '阻生': [['阻生', '废用'], 0, VALUE_TYPE_RADIO],
    '明显': [['不明显', '明显'], 0, VALUE_TYPE_RADIO],
    '减弱': [['正常', '减弱', '增强'], 0, VALUE_TYPE_RADIO],
}

# 全为阳性的选项
POSITIVE_OPTIONS = {'寒湿证', '肾虚证', '瘀血证'}

# 针对OPTION_MAP拆解的词，作用在display中会有特殊的展示
SPECIAL_OPTION_DISPLAY = {
    '是': '',  # 一般来讲，“是”会省略。是可见 --> 可见
    '否': '不',
}

# 选项的分割线。以下相隔的文本视为选项
OPTION_SPLITS = ['/', '或']

# 不断句的标点符号
NOT_BROKEN_SENTENCE = ['°', ' ', '(', ')', '（', '）', '+', '-', '’', '：', ':'] + OPTION_SPLITS

# 读取自定义的词组
for word in JIEBA_USER_DICTS:
    jieba.add_word(*word)
# 为了不拆分userword中的特殊字符。eg：中括号等
psg.re_han_internal = re.compile('([^°]+)', re.U)
jieba.re_userdict = re.compile('^(.+?)(\u0040\u0040[0-9]+)?(\u0040\u0040[a-z]+)?$', re.U)