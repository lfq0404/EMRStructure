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
    paragraph = '未及胸膜摩擦音'
    demo(paragraph)
