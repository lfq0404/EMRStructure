#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/3 15:51
# @File    : test.py
# @Software: Basebit
# @Description:


class A:
    def __init__(self):
        self.a = 123

    def func(self):
        pass


a = A()
print(a)
print(vars(a))