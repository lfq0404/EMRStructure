#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/2 22:24
# @File    : funcs.py
# @Software: Basebit
# @Description: 全局公共方法

import regex
import re
from bs4 import BeautifulSoup

from html.parser import HTMLParser


class HtmlParse(HTMLParser):
    """
    将HTML转为纯文本
    """

    def __init__(self, file_path):
        HTMLParser.__init__(self)
        self.__text = []
        self.file_path = file_path

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = re.sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')
        elif tag == 'div':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()

    def html2text(self):
        """
        将HTML转为纯文本
        :return:
        """
        with open(self.file_path, 'r') as f:
            text = f.read()

        try:
            # 利用HTMLParser提取网页纯文本
            self.feed(text)
            self.close()
            text = self.text()
        except:
            # 利用bs提取
            text = self.beautifulsoup_extract(text)

        # # 特殊替换
        # for i in conf.HTML2TEXT_REPLACE:
        #     text = re.sub(i['patt'], i['repl'], text)

        return text

    @staticmethod
    def beautifulsoup_extract(text):
        """
        利用BeautifulSoup提取网页纯文本
        :param text:
        :return:
        """
        soup = BeautifulSoup(text, features="html.parser")
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip()
                  for line in lines
                  for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join("".join(chunk.split()) for chunk in chunks if chunk)

        return text


def replace_and_classify_base(obj, root_node, attr_name: str):
    """
    绝大部分层的统一逻辑
    先统一替换
    再分类
    :param obj:
    :param root_node:
    :param attr_name:
    :return:
    """
    node = root_node
    classify = None
    while node:
        # 先进行统一的替换
        for patt, repl in node.replace_cfg:
            obj.__setattr__(attr_name, regex.sub(patt, repl, obj.__getattribute__(attr_name)))
        # 根据规则分类
        for patt, classify_ in node.classify_cfg:
            match = regex.match(patt, obj.__getattribute__(attr_name))
            if match:
                if callable(classify_):
                    classify = classify_
                    node = None
                    break
                else:
                    node = classify_
    if not classify:
        raise ValueError('raw2paragraph的配置没有兼容：{}'.format(obj.__getattribute__(attr_name)))

    return classify().extract(obj)
