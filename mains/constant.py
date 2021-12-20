#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/16 11:24
# @File    : constant.py
# @Software: Basebit
# @Description:

from services.resource2raw.main import handle as resource2raw_handle
from services.raw2paragraph.main import handle as raw2paragraph_handle
from services.paragraph2sentence.main import handle as paragraph2sentence_handle
from services.sentence2segment.main import handle as sentence2segment_handle
from services.segment_structure.main import handle as segment_structure_handle

# 整个层级流程配置，一般不能随意调换
HANDLES = [
    resource2raw_handle,
    raw2paragraph_handle,
    paragraph2sentence_handle,
    sentence2segment_handle,
    segment_structure_handle,
]
