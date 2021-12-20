#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/6 09:45
# @File    : service.py
# @Software: Basebit
# @Description:
import copy
import re
import hanlp
from itertools import chain

import services.paragraph2sentence.config as conf
import services.paragraph2sentence.constant as cons
from anytree import Node, RenderTree, findall_by_attr, findall, find_by_attr, find

# 根据 https://github.com/hankcs/HanLP#%E6%80%A7%E8%83%BD ，zh-close-ernie是最新的
HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ERNIE_GRAM_ZH)
# 实体命名自定义，key与mtl模型相关，需要与模型联动调整
ner = HanLP['ner/msra']
ner.dict_whitelist = conf.NER_DICT_WHITELIST
ner.dict_tags = conf.NER_DICT_TAGS
# 词性自定义
pos = HanLP['pos/ctb']
pos.dict_tags = conf.POS_DICT_TAGS
# 分词
tok = HanLP['tok/fine']
tok.dict_force = conf.TOK_DICT_FORCE
tok.dict_combine = conf.TOK_DICT_COMBINE


class Paragraph2SentenceBase:

    def extract(self, paragraph):
        """
        将段落解析成语句
        :param paragraph:
        :return:
        """
        # paragraph = '一般健康状况:一般。疾病史:否认高血压、冠心病等慢性病史。手术外伤史:因“胃息肉”行开腹手术治疗（具体不详）。输血史:否认。传染病史:诉既往曾患“肝炎”（具体不详），诉已愈。'
        # paragraph = '出生并生长于原籍，否认疫水接触史，否认吸烟史，饮酒史20余年，每日半斤黄酒，否认性病冶游史。'
        # paragraph = '因右肺中叶恶性肿瘤病史，2019-03-25在上海胸科医院全身麻醉VATS，肺右中叶切除术，术后病理:右肺中叶外侧段肺泡上皮异型增生、癌变（原位癌，非粘液型），肿瘤肺间质内淋巴细胞浸润伴淋巴滤泡形成，右肺中叶支气管切端未见癌累及，送检5组淋巴结未见癌转移。'
        # TOK ：tokenization（词语切分）
        # POS ：Part-of-speech tagging（词性标注）
        # NER ：Named Entity Recognition（命名实体识别）
        # SRL ：Semantic Role Labeling （语义角色标注）
        # DEP ：Dependency Parsing（依存句法分析）
        # SDP ：Semantic Dependency Parsing（语义依存分析）
        # CON ：Constituency Parsing（短语成分分析）
        # LEM : Lemmatization（词干提取）
        # FEA ：Features of Universal Dependencies（词法语法特征）
        # AMR : Abstract Meaning Representation（抽象意义表示）
        # doc = HanLP(paragraph, tasks=['con', 'pos', 'ner'])
        print(paragraph)
        doc = HanLP(paragraph)
        doc.pretty_print()

        # 第一层永远是根节点，不用遍历
        # doc['con']是phrasetree.tree.Tree，该类型对子父节点的获取不太方便，转成list，重新构建数
        sentences = self.get_sentences(doc['con'].to_list()[1][0])

        print()
        for i in sentences:
            print(i)
        return sentences

    def get_sentences(self, con):
        """
        根据语法树，获取独立的语句
        :param con: HanLP解析出来的con数据
        :return:
        """
        sentences = []

        # 根据模型解析的依存关系，构建语法树
        con_tree = self._extract_con(con)

        segment_tree = self._get_segment_tree(con_tree)

        # 解析
        for node in segment_tree.children:
            # node：segment对应的语法树
            sentence = self._contact_node_text(node)
            segment_key = self._get_segment_key(node)

            sentences.append({
                'segment_key': segment_key,
                'sentence': sentence
            })

        return sentences

    def _get_segment_tree(self, con_tree):
        """
        根据NP节点断句，返回segment tree
        :param con_tree:
        :return:
        """
        segment_tree = Node('root')

        for node in con_tree.children:
            # print(RenderTree(node))
            # node为自动识别的sentence信息树
            np_nodes = findall(node, filter_=lambda x: x.name in ['NP'])
            descendants = set(chain(*map(lambda x: x.descendants, np_nodes)))
            # 获取分别最上层的NP节点 = NP节点 - NP节点的所有后代节点
            np_nodes = [i for i in np_nodes if i not in descendants]

            if np_nodes:
                for node_ in np_nodes:
                    # 基于NP节点向上搜索，保证一个segment中只有一个NP
                    # node_：本层
                    # pnode：上层
                    # 计算当前节点包括的NP节点数
                    np_count = len(findall(node_, filter_=lambda x: x.name == 'NP'))
                    pnode = node_.parent
                    # 往上查询一层进行判断，直到NP节点数与最开始不一致再停止
                    while len(findall(pnode, filter_=lambda x: x.name == 'NP')) == np_count:
                        node_ = pnode
                        if node_.is_root:
                            # 如果上升到根节点，则终止
                            break
                        pnode = node_.parent
                    # 如果node_为node的子节点，并且所有兄弟节点中不包括标点符号，则直接合并，并开始下一次循环
                    if node_ in node.children and 'PU' not in [i.name for i in node.children]:
                        segment_node = copy.deepcopy(node)
                        segment_node.parent = segment_tree
                        break
                    else:
                        segment_node = copy.deepcopy(node_)
                        segment_node.parent = segment_tree
                        # print('新添加：')
                        # print(RenderTree(segment_node))
            else:
                # 如果是标点符号等，则直接添加
                segment_node = copy.deepcopy(node)
                segment_node.parent = segment_tree
                # print('新添加：')
                # print(RenderTree(segment_node))

        return segment_tree

    def _contact_node_text(self, node):
        """
        拼接该node的所有子node的文本
        :return:
        """
        text = ''
        for n in findall(node, filter_=lambda x: hasattr(x, 'text')):
            text += n.text

        return text

    def _get_segment_key(self, node):
        """
        获取该node的segment_key，将第一个NP节点作为key
        tag含义：https://hanlp.hankcs.com/docs/annotations/constituency/ctb.html
        :param node:
        :return:
        """
        segment_key = ''
        node_ = findall(node, filter_=lambda node: 'NP' in node.name)
        if node_:
            segment_key = self._contact_node_text(node_[0])
            # 只取冒号前面的作为key
            segment_key = re.split('[：:]', segment_key)[0]

        return segment_key

    def _extract_con(self, con, parent: Node = None, root: Node = None):
        """
        将返回的con数据，转为树
        同时添加一些后处理规则
        一般	JJ ───►ADJP──┐
        健康	NN ──┐       ├►NP ───┐
        状况	NN ──┴►NP ───┘       │
        ： 	PU ──────────────────┼►IP
        一般	VA ───────────►ADVP──┘
        :param con: HanLP解析出来的con数据
        :param parent: 父节点
        :return: con_tree
        """
        # TODO：控制一个语句的最短长度，防止“右肺”这种短句出现
        if not root:
            root = Node(con.pop(0))
        if not parent:
            parent = root

        node = None
        count = len(con)
        for ind, con_ in enumerate(con):
            if type(con_) is list:
                # 后处理1：如果上个兄弟节点的词性为split，则强制从根节点开始
                if ind - 1 > 0 and con[ind - 1][0] == cons.TAG_SPLIT:
                    parent = root
                # elif con_[0] == cons.TAG_CONTACT and parent == root:
                elif con_[0] == cons.TAG_CONTACT:
                    # 后处理2：如果该节点的词性为contact and 被归在了根节点下，则继续跟在上一个子节点下
                    # print('0\n', RenderTree(root))
                    # print('1\n', RenderTree(parent))
                    parent = parent.children[-1] if parent.children else parent
                    if parent.descendants and parent.descendants[-1].name == cons.TAG_SPLIT:
                        # 如果parent有结束的标识，则从新开始
                        parent = root.children[-1]
                    # print('2\n', RenderTree(parent))
                    # print()
                # 证明还有子节点
                self._extract_con(con_, node or parent, root)
            elif type(con_) is str:
                if ind + 1 == count:
                    # 如果该con最后一个仍然是str，则表示是叶子结点，将str附在父节点中
                    # 将所有文字放在text中
                    parent.text = con_
                else:
                    node = Node(con_, parent=parent)
        return parent
