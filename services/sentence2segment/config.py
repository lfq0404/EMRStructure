#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/6 14:43
# @File    : config.py
# @Software: Basebit
# @Description:


from utils.structures import CfgStructure
import services.sentence2segment.service as service
import services.sentence2segment.constant as cons
import utils.constant as util_cons

_ENUM_DISEASES = ['高血压', '脑梗塞', '糖尿病', '哮喘病', '心脏病']

# TODO：公共规则的提取。可能在不同阶段的配置中，在多个子节点有相同的配置，可以提到父节点中

single_choice_with_addition_node = CfgStructure(
    replace_cfg=[
        {
            'patt': '左 右 水平性 旋转性 垂直性 快相向左、右',
            'repl': '水平性 旋转性 垂直性 快相向左 快相向右'
        },
        {
            'patt': '左 右 心前区',
            'repl': '左心前区 右心前区'
        },

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
        ['(部位|性质)', service.SingleChoiceWithExtendText()],
        # 气管：正中 偏移(左/右)
        ['\(.*左.+右\)', service.SingleChoiceWithSingleChoice()],
        # 无 有(奔马律 开瓣音 第三心音 第四心音)
        ['\(.*(第三心音|瘀斑|心前区|脑组织)', service.SingleChoiceWithSingleChoice()],
        # 耳漏：无 左(血 脑脊液 脑组织) 右(血 脑脊液 脑组织)
        ['[左右][（\(].+[）\)].*[左右][（\(].+[）\)]', service.SingleChoiceWithSingleChoice()],
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
    replace_cfg=[

    ],
    classify_cfg=[
        # 吸烟史：无 有 平均_支/日，时间_年 ，戒烟：否 是 时间
        ['吸烟史.+', service.Smoke()],
        # 饮酒史：无 有 平均_克(两)/日 ，时间 __年 ，戒酒 ：否 是 时间
        ['饮酒史.+', service.Drink()],
        # 肢体长度：左 cm 右 cm
        ['[左右].*?cm.*[左右].*cm', input_node],
        # 肢体长度：左 cm 右 cm
        ['生育史', input_node],
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
        {
            'patt': '抗结核治疗史$',
            'repl': '抗结核等治疗史'
        },

    ],
    classify_cfg=[
        # 无穷枚举类型
        ['等', service.MultipleChoiceWithOthers()],
        # 有无xx，针对有存在选项的
        ['^有无.+[{}]'.format(''.join(util_cons.OPTION_SPLITS)), service.YesNoWithSingleChoice()],
        ['^有无.+', service.YesNoChoice()],
        ['[{}].*有无'.format(''.join(util_cons.OPTION_SPLITS)), service.YesNoWithBeforeSingleChoice()],
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
        {
            'patt': '\(有/无\)',
            'repl': '有无'
        },
        {
            'patt': '不等 左 mm 右 mm',
            'repl': '不等（左 mm 右 mm）'
        },
        {
            'patt': '无 有 不详；预防接种药品：',
            'repl': '无 不详 有 预防接种药品'
        },
        {
            'patt': '有\(左 右 性质',
            'repl': '左 右 性质'
        },
        {
            'patt': '无 有 不详 过敏食物/药物名称',
            'repl': '无 不详 有 过敏食物 药物名称'
        },
        {
            # 添加阴性
            'patt': '\(减退 消失 过敏\)',
            'repl': '(正常 减退 消失 过敏)'
        },
        {
            'patt': '有\(部位',
            'repl': '有(部位)'
        },
        {
            'patt': '次 /分',
            'repl': '次/分'
        },
        {
            # 保证第一个是阴性
            'patt': '\(有 无\)',
            'repl': '(无 有)'
        },
        {
            # 保证第一个是阴性：将“无”放在第一位
            'patt': '(\()(?=.+(无|正常))',
            'repl': r'\1\2 '
        },
        {
            # 同时存在两个无选项，删除第二个
            'patt': '(\((无|正常)[^(无|正常)]+?)( (无|正常))',
            'repl': r'\1'
        },
        {
            # 自身替换
            # 耳漏(正常 左 右 血 脑脊液 脑组织)
            # 耳漏：正常 左（血 脑脊液 脑组织） 右（血 脑脊液 脑组织）
            'patt': '(^.+?)[\(:：]?((无|正常) [左右]) ([左右]) (.+?)[\)]?$',
            'repl': r'\1：\2（\5） \4（\5）'
        },
        {
            # 将选项统一加上冒号
            'patt': '(听力障碍|肠鸣音|压痛及叩击痛|膀胱区膨隆) (?=(无|正常|是))',
            'repl': r'\1：'
        },
        {
            # 将这些词前面的空格换成逗号
            'patt': '([ ]+)(?=(结婚年龄|妊娠|足月产|流产|早产))',
            'repl': '，'
        },
        {
            'patt': '未 见',
            'repl': '未见'
        },
        {
            'patt': ' 表现为瘀点或出血点 、紫癜 、瘀斑 、血肿',
            'repl': '(瘀点或出血点、紫癜、瘀斑、血肿)'
        }
    ],

    classify_cfg=[
        #  单选 + 自定义选项
        ['(.+[:：])(.+({}).*)'.format('|'.join(cons.SINGLE_CHOICE_WITH_OTHERS_TEXTS)),
         service.SingleChoiceWithOthers()],
        # 单选 + 补充说明：针对“有”
        ['(.+[:：])(.+(有|可触及).+({}).*)'.format('|'.join(cons.SINGLE_CHOICE_WITH_ADDITION_TEXTS)),
         single_choice_with_addition_node],
        # 单选 + 补充说明：偏移 (左/右)
        ['(.+[:：])(.+[\(\（].+[\)\）]\s*)', single_choice_with_addition_node],
        #  自定义输入
        ['(次/分)', input_node],
        #  冒号单选类型
        ['(.+[:：])(.+)', single_choice_node],
        #  括号单选：经量(少 一般 多)
        ['.+\(.+\)', service.BracketsSingleChoice()],
        #  有无+枚举类型
        ['有无.*', yes_no_enum_node],
        #  自定义输入类型
        ['^(.+\s+)(.+)$', input_node],

    ]
)
