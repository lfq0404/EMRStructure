#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/3 18:06
# @File    : structures.py
# @Software: Basebit
# @Description:
import re

import regex
from anytree import NodeMixin

import utils.constant as cons


class CfgStructure:
    """
    配置的结构体
    """

    def __init__(self, replace_cfg, classify_cfg):
        self.replace_cfg = replace_cfg
        self.classify_cfg = classify_cfg


class ExtractStructure:
    """
    解析的结构体
    TODO：提供print打印
    """

    def __init__(self, file_name, file_path, raw_text):
        self.file_name = file_name
        self.file_path = file_path
        self.raw_text = raw_text

class RJExtractStructure:
    """
    解析的结构体
    TODO：提供print打印
    """

    def __init__(self, diagnosis):
        self.diagnosis = diagnosis