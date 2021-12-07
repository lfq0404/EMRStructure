#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/6 14:43
# @File    : config.py
# @Software: Basebit
# @Description:


from utils.structures import CfgStructure
import services.sentence2segment.service as service
import services.sentence2segment.constant as cons

_ENUM_DISEASES = ['高血压', '脑梗塞', '糖尿病', '哮喘病', '心脏病']

# TODO：公共规则的提取。可能在不同阶段的配置中，在多个子节点有相同的配置，可以提到父节点中

single_choice_with_addition_node = CfgStructure(
    replace_cfg=[

    ],
    classify_cfg=[
        # 吸烟史：无 有 平均_支/日，时间_年 ，戒烟：否 是 时间
        ['吸烟史.+', service.Smoke()],
        # 饮酒史：无 有 平均_克(两)/日 ，时间 __年 ，戒酒 ：否 是 时间
        ['饮酒史.+', service.Drink()],
        # 瞳孔：等大等圆 不等(左_ mm 右__mm)
        ['[左右]\s+mm\s+[左右]\s+mm', service.SingleChoiceWithExtendText()],
        # 心尖搏动位置：正常 移位(距左锁骨中线 内_ cm 外_ cm)
        ['[内外]\s+cm\s+[内外]\s+cm', service.SingleChoiceWithExtendText()],
        # 肝脏：未触及 触及 肋下 cm 剑突下 cm 质地 表面 边缘 压痛
        ['肋下.*剑突.*', service.SingleChoiceWithExtendText()],
        # 脊柱：正常 畸形 肿胀 瘘道 压痛(第 椎体)
        ['第.+椎体', service.SingleChoiceWithExtendText()],
        # 气管：正中 偏移(左/右)
        ['\(.*左.+右\)', service.SingleChoiceWithSingleChoice()],
        # 预防接种史：无 不详 有 预防接种疫苗
        # 该类型的兜底方法
        ['', service.SingleChoiceWithAddition()],
    ]
)
input_node = CfgStructure(
    replace_cfg=[
        {
            'patt': '左 cm 右 cm',
            'repl': '左输入cm，右输入cm'
        },
        {
            # 将所有空格视为输入
            'patt': '\s+',
            'repl': '输入'
        },

    ],
    classify_cfg=[
        ['', service.TextInput()],
    ]
)
single_choice_node = CfgStructure(
    replace_cfg=[],
    classify_cfg=[
        # 吸烟史：无 有 平均_支/日，时间_年 ，戒烟：否 是 时间
        ['吸烟史.+', service.Smoke()],
        # 饮酒史：无 有 平均_克(两)/日 ，时间 __年 ，戒酒 ：否 是 时间
        ['饮酒史.+', service.Drink()],
        # 肢体长度：左 cm 右 cm
        ['[左右].*?cm.*[左右].*cm', input_node],
        # 发育 ：正常 不良 超常
        # 该类型的兜底方法
        ['', service.SingleChoice()],
    ]
)

yes_no_enum_node = CfgStructure(
    replace_cfg=[
        {
            'patt': '放、化疗',
            'repl': '放化疗'
        },
        {
            'patt': '抗结核治疗史$',
            'repl': '抗结核等治疗史'
        },

    ],
    classify_cfg=[
        ['等', service.MultipleChoiceWithOthers()],
    ]
)

root_node = CfgStructure(
    replace_cfg=[
        {
            # 将下划线改为空格
            'patt': '_',
            'repl': ' '
        },
        {
            # 肝脏：未触及 触及 肋下 cm 剑突下 cm 质地 表面 边缘 压痛 --> “肋下”前加括号
            'patt': '(?<=(触及))(\s*)(?=肋下)',
            'repl': '('
        },
        {
            # 肝脏：未触及 触及 肋下 cm 剑突下 cm 质地 表面 边缘 压痛 --> 结尾加括号
            'patt': '(?<=(触及).*肋下.+)()$',
            'repl': ')'
        },
        {
            # 将多个空格改为一个
            'patt': ' +',
            'repl': ' '
        },
        {
            # 去掉冒号前的空格
            'patt': '(\s+)(?=[:：])',
            'repl': ''
        },
        # 去除这些字前面的空格
        {
            'patt': '(\s+)(?=[常\(（])',
            'repl': ''
        },

    ],

    classify_cfg=[
        #  单选 + 自定义选项
        ['(.+[:：])(.+({}).*)'.format('|'.join(cons.SINGLE_CHOICE_WITH_OTHERS_TEXTS)),
         service.SingleChoiceWithOthers()],
        # 单选 + 补充说明：针对“有”
        ['(.+[:：])(.+有.+({}).*)'.format('|'.join(cons.SINGLE_CHOICE_WITH_ADDITION_TEXTS)),
         single_choice_with_addition_node],
        # 单选 + 补充说明：偏移 (左/右)
        ['(.+[:：])(.+[\(\（].+[\)\）]\s*)', single_choice_with_addition_node],
        #  单选类型
        ['(.+[:：])(.+)', single_choice_node],
        #  有无+枚举类型
        ['^有无.*', yes_no_enum_node],
        #  自定义输入类型
        ['^(.+\s+)(.+)$', input_node],

    ]
)
