#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/2 22:24
# @File    : funcs.py
# @Software: Basebit
# @Description: 全局公共方法

import json
import regex
import re
from bs4 import BeautifulSoup

from html.parser import HTMLParser

from utils.structures import CfgStructure
import utils.constant as cons


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


def replace_and_classify_base(text, node, step):
    """
    绝大部分层的统一逻辑
    先统一替换
    再分类
    :param text:
    :param node:
    :param step: 
    :return:
    """
    print('{}预处理的文本：{}'.format(step, text))
    classify = None
    while node:
        # 先进行统一的替换
        for cfg in node.replace_cfg:
            patt = cfg['patt']
            repl = cfg['repl']
            need_sub = regex.search(patt, text)
            if need_sub:
                text = regex.sub(patt, repl, text)
                print('{}根据规则 “{}” ，将文本修改为：{}'.format(step, patt, text))

        # 根据规则分类
        for patt, classify_ in node.classify_cfg:
            match = regex.search(patt, text)
            if match:
                print('满足条件：{}'.format(patt))
                if hasattr(classify_, 'extract'):
                    classify = classify_
                    node = None
                elif isinstance(node, CfgStructure):
                    node = classify_
                else:
                    raise ValueError('{}的配置错误：{}'.format(step, node))
                break
        else:
            raise ValueError('{}的配置没有兼容：{}'.format(step, text))

    return classify, text


def update_html(display, segments):
    """
    修改HTML，用于看效果
    :param display:
    :param segments:
    :return:
    """
    with open('{}/rjPhysicalDemo/template_base.json'.format(cons.BASE_PATH), 'r') as f:
        raw_json = json.loads(f.read())

    with open('{}/rjPhysicalDemo/template.json'.format(cons.BASE_PATH), 'w') as f:
        raw_json['medical_history']['display'] = display + raw_json['medical_history']['display']
        raw_json['medical_history']['segments'].extend(segments)

        f.write('demo({})'.format(json.dumps(raw_json, ensure_ascii=False)))


def raw_obj_call_handles(args, handles):
    """
    将原始的obj，调用所有的流程
    :return:
    """
    for handle in handles:
        new_args = []
        for arg in args:
            _new = handle(arg)
            if type(_new) is list:
                new_args.extend(_new)
            else:
                new_args.append(_new)
        args = new_args.copy()

    return args
