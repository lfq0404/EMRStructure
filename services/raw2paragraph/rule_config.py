#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/3 09:14
# @File    : rule_config.py
# @Software: Basebit
# @Description:

from zhon.hanzi import punctuation as zh_punc

from utils.structures import CfgStructure
import services.raw2paragraph.service as service

_ENUM_DISEASES = ['高血压', '脑梗塞', '糖尿病', '哮喘病', '心脏病']

# TODO：公共规则的提取。可能在不同阶段的配置中，在多个子节点有相同的配置，可以提到父节点中
root_node = CfgStructure(
    replace_cfg=[
        {
            'patt': '\n{',
            'repl': '{'
        },
    ],
    classify_cfg=[
        ['', service.ColonCut()]
    ]
)

# 暂时不需要抓取的段落
NOT_EXTRACT_PARAGRAPHS = '(现病史|主诉)'

PRESENT_NAME = '现病史'
PHYSICAL_NAME = '查体'
PAST_NAME = '既往史'
FAMILY_NAME = '家族史'
ALLERGY_NAME = '药物过敏史'
PERSONAL_NAME = '个人史'
MARRIAGEBIRTH_NAME = '婚育史'
MENSTRUAL_NAME = '月经史'
CUSTOM_NAME = '其他'

# 已知的分类，不在该map中的，统一放在custom中
KNOWN_CATEGORY_MAP = {
    PHYSICAL_NAME: 'PHYSICAL',
    PAST_NAME: 'PAST',
    FAMILY_NAME: 'FAMILY',
    ALLERGY_NAME: 'ALLERGY',
    PERSONAL_NAME: 'PERSONAL',
    MARRIAGEBIRTH_NAME: 'MARRIAGEBIRTH',
    MENSTRUAL_NAME: 'MENSTRUATION',
    PRESENT_NAME: 'PRESENT',
}
