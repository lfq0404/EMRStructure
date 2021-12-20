def ner_dict():
    import hanlp
    from hanlp.components.mtl.tasks.ner.tag_ner import TaggingNamedEntityRecognition
    from hanlp.utils.io_util import get_resource

    HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ERNIE_GRAM_ZH)
    ner: TaggingNamedEntityRecognition = HanLP['ner/msra']
    ner.dict_whitelist = {'午饭后': 'TIME'}
    doc = HanLP('2021年测试高血压是138，时间是午饭后2点45，低血压是44', tasks='ner/msra')
    doc.pretty_print()
    print(doc['ner/msra'])

    ner.dict_tags = {('名字', '叫', '金华'): ('O', 'O', 'S-PERSON')}
    HanLP('他在浙江金华出生，他的名字叫金华。', tasks='ner/msra').pretty_print()
    print()


def pos_dict():
    #
    # -*- coding:utf-8 -*-
    # Author: hankcs
    # Date: 2020-12-15 22:26
    import hanlp
    from hanlp.components.mtl.multi_task_learning import MultiTaskLearning
    from hanlp.components.mtl.tasks.pos import TransformerTagging
    from hanlp.components.mtl.tasks.tok.tag_tok import TaggingTokenization

    # HanLP: MultiTaskLearning = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
    HanLP: MultiTaskLearning = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ERNIE_GRAM_ZH)

    # Demonstrates custom dict in part-of-speech tagging
    pos: TransformerTagging = HanLP['pos/ctb']
    pos.dict_tags = {'HanLP': 'state-of-the-art-tool'}
    print(f'自定义单个词性:')
    HanLP("HanLP为生产环境带来次世代最先进的多语种NLP技术。", tasks='pos/ctb').pretty_print()
    print(f'根据上下文自定义词性:')
    pos.dict_tags = {('的', '希望'): ('', '名词'), '希望': '动词'}
    HanLP("我的希望是希望张晚霞的背影被晚霞映红。", tasks='pos/ctb').pretty_print()
    HanLP("我的希望是希望张晚霞的背影被晚霞映红。").pretty_print()

    # 需要算法基础才能理解，初学者可参考 http://nlp.hankcs.com/book.php
    # See also https://hanlp.hankcs.com/docs/api/hanlp/components/taggers/transformer_tagger.html


def sim():
    # -*- coding:utf-8 -*-
    # Author: hankcs
    # Date: 2021-05-24 13:15
    # 文本语义相似性
    # sts包包含预训练的语义文本相似性 (STS) 模型。我们调查了有监督和无监督模型，我们认为无监督模型在这一刻仍然不成熟。无监督 STS 对 IR 有好处，但对 NLP 不好，尤其是在词汇重叠很少的句子上。

    import hanlp

    sim = hanlp.load(hanlp.pretrained.sts.STS_ELECTRA_BASE_ZH)
    print(sim([
        ['看图猜一电影名', '看图猜电影'],
        ['无线路由器怎么无线上网', '无线上网卡和无线路由器怎么用'],
        ['北京到上海的动车票', '上海到北京的动车票'],
        ['出生并生长于原籍', '出生生长于原籍', '出生并长期生长于原籍', '生于原籍 ，长期在河北保定生活，近年来在深圳工作'],
        ['否认嗜烟嗜酒', '无烟酒不良嗜好', '无饮酒嗜好'],
    ]))


def tok():
    # -*- coding:utf-8 -*-
    # Author: hankcs
    # Date: 2020-12-15 22:26
    import hanlp
    from hanlp.components.mtl.multi_task_learning import MultiTaskLearning
    from hanlp.components.mtl.tasks.pos import TransformerTagging
    from hanlp.components.mtl.tasks.tok.tag_tok import TaggingTokenization

    HanLP: MultiTaskLearning = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)

    # Demonstrates custom dict in tokenization
    tok: TaggingTokenization = HanLP['tok/fine']

    tok.dict_force = tok.dict_combine = None
    print(f'不挂词典:\n{HanLP("商品和服务项目")["tok/fine"]}')

    tok.dict_force = {'和服', '服务项目'}
    print(f'强制模式:\n{HanLP("商品和服务项目")["tok/fine"]}')  # 慎用，详见《自然语言处理入门》第二章

    tok.dict_force = {'和服务': ['和', '服务']}
    print(f'强制校正:\n{HanLP("正向匹配商品和服务、任何和服务必按上述切分")["tok/fine"]}')

    tok.dict_force = None
    tok.dict_combine = {'和服', '服务项目'}
    print(f'合并模式:\n{HanLP("商品和服务项目")["tok/fine"]}')

    # 需要算法基础才能理解，初学者可参考 http://nlp.hankcs.com/book.php
    # See also https://hanlp.hankcs.com/docs/api/hanlp/components/tokenizers/transformer.html


def demo_pipeline():
    import hanlp

    # tokenizer = hanlp.load('LARGE_ALBERT_BASE')
    # tagger = hanlp.load('CTB9_POS_ALBERT_BASE')
    # syntactic_parser = hanlp.load('CTB7_BIAFFINE_DEP_ZH')
    # semantic_parser = hanlp.load('SEMEVAL16_TEXT_BIAFFINE_ZH')

    # pipeline = hanlp.pipeline() \
    #     .append(hanlp.utils.rules.split_sentence, output_key='sentences') \
    #     .append(tokenizer, output_key='tokens') \
    #     .append(tagger, output_key='part_of_speech_tags') \
    #     .append(syntactic_parser, input_key=('tokens', 'part_of_speech_tags'), output_key='syntactic_dependencies',
    #             conll=False) \
    #     .append(semantic_parser, input_key=('tokens', 'part_of_speech_tags'), output_key='semantic_dependencies',
    #             conll=False)
    # print(pipeline)

    text = '''HanLP是一系列模型与算法组成的自然语言处理工具包，目标是普及自然语言处理在生产环境中的应用。
    HanLP具备功能完善、性能高效、架构清晰、语料时新、可自定义的特点。
    内部算法经过工业界和学术界考验，配套书籍《自然语言处理入门》已经出版。
    '''

    # doc = pipeline(text)
    # print(doc)
    # By default the doc is json serializable, it holds true if your pipes output json serializable object too.
    # print(json.dumps(doc, ensure_ascii=False, indent=2))

    # You can save the config to disk for deploying or sharing.
    # pipeline.save('zh.json')
    # Then load it smoothly.
    deployed = hanlp.load('zh.json')
    print(deployed)
    doc = deployed(text)
    doc.pretty_print()
    print(doc)


def demo_dep():
    import hanlp

    syntactic_parser = hanlp.load(hanlp.pretrained.dep.CTB7_BIAFFINE_DEP_ZH)
    sent = [('蜡烛', 'NN'), ('两', 'CD'), ('头', 'NN'), ('烧', 'VV')]
    sent = [('出生', 'VV'), ('并', 'CC'), ('生长', 'VV'), ('于', 'P'), ('原籍', 'NN'), ('，', 'PU'), ('否认', 'VV'), ('疫', 'NN'),
            ('水', 'NN'), ('接触', 'VV'), ('史', 'NN'), ('，', 'PU'), ('否认', 'VV'), ('吸烟', 'NN'), ('史', 'NN'), ('，', 'PU'),
            ('饮酒', 'VV'), ('史', 'NN'), ('20', 'CD'), ('余', 'CD'), ('年', 'M'), ('，', 'PU'),
            ('每日', 'AD'), ('半', 'CD'), ('斤', 'M'), ('黄酒', 'NN'),
            ('，', 'PU'), ('否认', 'VV'), ('性病', 'NN'), ('冶', 'NN'), ('游', 'NN'), ('史', 'NN'),
            ('。', 'PU')]
    tree = syntactic_parser(sent)
    print(tree)
    print(tree.to_tree())


def demo_sdp():
    import hanlp

    semantic_parser = hanlp.load('SEMEVAL16_NEWS_BIAFFINE_ZH')
    sent = [('蜡烛', 'NN'), ('两', 'CD'), ('头', 'NN'), ('烧', 'VV')]
    print(semantic_parser(sent))


def demo_classifier():
    from hanlp.datasets.classification.sentiment import CHNSENTICORP_ERNIE_TEST

    import hanlp

    classifier = hanlp.load('CHNSENTICORP_BERT_BASE_ZH')
    print(classifier.predict('前台客房服务态度非常好！早餐很丰富，房价很干净。再接再厉！'))

    # predict a whole file in batch mode
    outputs = classifier.predict(classifier.transform.file_to_inputs(CHNSENTICORP_ERNIE_TEST), gold=True)
    print(outputs[:5])


def demo_cws():
    import hanlp

    tokenizer = hanlp.load(hanlp.pretrained.tok.LARGE_ALBERT_BASE)
    print(tokenizer('商品和服务'))
    print(tokenizer(['萨哈夫说，伊拉克将同联合国销毁伊拉克大规模杀伤性武器特别委员会继续保持合作。',
                     '上海华安工业（集团）公司董事长谭旭光和秘书张晚霞来到美国纽约现代艺术博物馆参观。',
                     'HanLP支援臺灣正體、香港繁體，具有新詞辨識能力的中文斷詞系統']))

    text = 'NLP统计模型没有加规则，聪明人知道自己加。英文、数字、自定义词典统统都是规则。'
    print(tokenizer(text))

    dic = {'自定义词典': 'custom_dict', '聪明人': 'smart'}

    def split_by_dic(text: str):
        # We use regular expression for the sake of simplicity.
        # However, you should use some trie trees for production
        import re
        p = re.compile('(' + '|'.join(dic.keys()) + ')')
        sents, offset, words = [], 0, []
        for m in p.finditer(text):
            if offset < m.start():
                sents.append(text[offset: m.start()])
                words.append((m.group(), dic[m.group()]))
                offset = m.end()
        if offset < len(text):
            sents.append(text[offset:])
            words.append((None, None))
        flat = []
        for pred, (word, tag) in zip(tokenizer(sents), words):
            flat.extend(pred)
            if word:
                flat.append((word, tag))
        return flat

    print(split_by_dic(text))


def demo_cws_trie():
    """
    文本替换
    :return:
    """
    from hanlp_trie.trie import Trie

    import hanlp

    tokenizer = hanlp.load('LARGE_ALBERT_BASE')
    text = 'NLP统计模型没有加规则，聪明人知道自己加。英文、数字、自定义词典统统都是规则。'
    print(tokenizer(text))

    trie = Trie()
    trie.update({'自定义词典': 'custom_dict', '聪明人': 'smart'})

    def split_sents(text: str, trie: Trie):
        words = trie.parse_longest(text)
        sents = []
        pre_start = 0
        offsets = []
        for start, end, value in words:
            if pre_start != start:
                sents.append(text[pre_start: start])
                offsets.append(pre_start)
            pre_start = end
        if pre_start != len(text):
            sents.append(text[pre_start:])
            offsets.append(pre_start)
        return sents, offsets, words

    print(split_sents(text, trie))

    def merge_parts(parts, offsets, words):
        items = [(i, p) for (i, p) in zip(offsets, parts)]
        items += [(start, [value]) for (start, end, value) in words]
        return [each for x in sorted(items) for each in x[1]]

    tokenizer = hanlp.pipeline() \
        .append(split_sents, output_key=('parts', 'offsets', 'words'), trie=trie) \
        .append(tokenizer, input_key='parts', output_key='tokens') \
        .append(merge_parts, input_key=('tokens', 'offsets', 'words'), output_key='merged')

    print(tokenizer(text))


def demo_pos():
    # -*- coding:utf-8 -*-
    # Author: hankcs
    # Date: 2019-12-28 21:25
    import hanlp
    from hanlp.pretrained.pos import CTB9_POS_ALBERT_BASE

    tagger = hanlp.load(CTB9_POS_ALBERT_BASE)
    print(tagger.predict(['我', '的', '希望', '是', '希望', '世界', '和平']))
    print(tagger.predict([['支持', '批处理', '地', '预测'], ['速度', '更', '快']]))


def demo_del_tasks():
    import hanlp
    from hanlp.components.mtl.multi_task_learning import MultiTaskLearning
    from hanlp_common.document import Document

    HanLP: MultiTaskLearning = hanlp.load(hanlp.pretrained.mtl.OPEN_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
    pos = HanLP['pos/ctb']
    pos.dict_tags = {'：': 'NN'}
    tasks = list(HanLP.tasks.keys())
    print(tasks)  # Pick what you need from what we have
    for task in tasks:
        if task not in ('tok', 'pos', 'con'):
            del HanLP[task]
    # You can save it as a new component
    # HanLP.save('path/to/new/component')
    # HanLP.load('path/to/new/component')
    print(HanLP.tasks.keys())
    doc: Document = HanLP(['一般健康状况:一般。疾病史:否认高血压、冠心病等慢性病史。手术外伤史:因“胃息肉”行开腹手术治疗（具体不详）。输血史:否认。传染病史:诉既往曾患“肝炎”（具体不详），诉已愈。'])
    print(doc)

    doc.pretty_print()


if __name__ == '__main__':
    tok()
    # demo_cws_trie()
