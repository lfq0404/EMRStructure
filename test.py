#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/17 11:11
# @File    : test.py
# @Software: Basebit
# @Description:
import re

from anytree import Node, RenderTree, findall_by_attr, findall, find_by_attr, find

con = ['TOP', [['IP', [['VP', [['VP', [['VV', ['出生']]]], ['CC', ['并']],
                               ['VP', [['VV', ['生长']], ['PP', [['P', ['于']], ['NP', [['NN', ['原籍']]]]]]]]]],
                       ['PU', ['，']], ['VP', [['VV', ['否认']], ['NP', [
        ['IP', [['NP', [['NN', ['疫']], ['NN', ['水']]]], ['VP', [['VV', ['接触']]]]]], ['NP', [['NN', ['史']]]]]]]],
                       ['PU', ['，']],
                       ['VP', [['VV', ['否认']], ['NP', [['IP', [['VP', [['NN', ['吸烟']]]]]], ['NP', [['NN', ['史']]]]]]]],
                       ['PU', ['，']], ['IP', [['NP', [['IP', [['VP', [['VV', ['饮酒']]]]]], ['NP', [['NN', ['史']]]]]],
                                              ['QP', [['QP', [['QP', [['CD', ['20']]]], ['CD', ['余']]]],
                                                      ['CLP', [['M', ['年']]]]]], ['NP', [['AD', ['每日']]]], ['NP', [
            ['QP', [['CD', ['半']], ['CLP', [['M', ['斤']]]]]], ['NP', [['NN', ['黄酒']]]]]]]], ['PU', ['，']], ['VP', [
        ['VV', ['否认']],
        ['NP', [['IP', [['NP', [['NN', ['性病']]]], ['VP', [['NN', ['冶']], ['NN', ['游']]]]]], ['NP', [['NN', ['史']]]]]]]],
                       ['PU', ['。']]]]]]


def extract_con(con, parent: Node = None):
    if not parent:
        parent = Node(con.pop(0))

    node = None
    while con:
        con_ = con.pop(0)
        if type(con_) is list:
            # 证明还有子节点
            # 此时一定有node
            extract_con(con_, node or parent)
        elif type(con_) is str:
            if not con:
                # 如果该con最后一个仍然是str，则表示是叶子结点，将str附在父节点中
                parent.text = con_
            else:
                node = Node(con_, parent=parent)
    return parent


def contact_node_text(node):
    """
    拼接该node的所有子node的文本
    :return:
    """
    text = ''
    for n in findall(node, filter_=lambda x: hasattr(x, 'text')):
        text += n.text

    return text


def get_sentences(con_tree):
    """
    根据语法树，获取独立的语句
    :param con_tree:
    :return:
    """
    sentences = []

    for node in con_tree.children:
        sentence = contact_node_text(node)
        segment_key = ''

        # 将最外层NP对应的文本作为segment_key
        # 此处以NP为准，是统计的规律，后续可能会调整
        # tag含义：https://hanlp.hankcs.com/docs/annotations/constituency/ctb.html
        node_ = findall(node, filter_=lambda node: 'NP' in node.name)
        if node_:
            segment_key = contact_node_text(node_[0])

        sentences.append({
            'segment_key': segment_key,
            'sentence': sentence
        })

    return sentences


if __name__ == '__main__':
    import hanlp

    semantic_parser = hanlp.load('SEMEVAL16_NEWS_BIAFFINE_ZH')
    sent = [('蜡烛', 'NN'), ('两', 'CD'), ('头', 'NN'), ('烧', 'VV')]
    print(semantic_parser(sent))