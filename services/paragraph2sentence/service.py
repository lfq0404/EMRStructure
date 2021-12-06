#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/6 09:45
# @File    : service.py
# @Software: Basebit
# @Description:

import services.paragraph2sentence.config as conf


class Paragraph2SentenceBase:

    def extract(self, block):
        """
        默认只以句号分割
        :param block:
        :return:
        """
        return [block]
