#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/17 18:38
# @File    : test.py
# @Software: Basebit
# @Description:
from service import *


def demo(paragraph):
    doc = HanLP(paragraph)
    doc.pretty_print()


if __name__ == '__main__':
    paragraph = '一般健康状况：一般。疾病史：否认高血压、冠心病等慢性病史。手术外伤史：因“胃息肉”行开腹手术治疗（具体不详）'
    demo(paragraph)
