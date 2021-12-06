#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/6 14:43
# @File    : config.py
# @Software: Basebit
# @Description:


from utils.structures import CfgStructure
import services.sentence2segment.service as service

_ENUM_DISEASES = ['高血压', '脑梗塞', '糖尿病', '哮喘病', '心脏病']

# TODO：公共规则的提取。可能在不同阶段的配置中，在多个子节点有相同的配置，可以提到父节点中
root_node = CfgStructure(
    replace_cfg=[
        {
            # 将多个空格改为一个
            'patt': ' +',
            'repl': ' '
        },
    ],
    classify_cfg=[
        #  腹部视诊：正常 膨隆 凹陷 其他
        ['(.+[:：])(.+其他.*)', service.SingleChoiceWithOthers()],
        #  发育 ：正常 不良 超常
        ['(.+[:：])(.+)', service.SingleChoice()],

    ]
)