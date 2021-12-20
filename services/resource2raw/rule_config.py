#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/3 12:11
# @File    : rule_config.py
# @Software: Basebit
# @Description:
import services.resource2raw.service as servive

RESOURCE_TYPE = {
    'html': servive.Html2Raw(),
}
