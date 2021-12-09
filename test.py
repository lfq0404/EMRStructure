#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/3 15:51
# @File    : test.py
# @Software: Basebit
# @Description:
from utils.structures import ExtractStructure, ParagraphStructure
from main import main
from services.resource2raw.main import handle as resource2raw_handle
from services.raw2paragraph.main import handle as raw2paragraph_handle
from services.paragraph2sentence.main import handle as paragraph2sentence_handle
from services.sentence2segment.main import handle as sentence2segment_handle
from services.segment_structure.main import handle as segment_structure_handle

if __name__ == '__main__':
    extract_obj = ExtractStructure(
        file_name='西医_内科.txt',
        file_path='/Users/jeremy.li/Basebit/Projects/AutoTemplate/pdf2text/bookTextsManual',
        raw_text='123',
    )
    extract_obj.paragraphs = ParagraphStructure(**{
        'test':
            {
                'sort': 1,
                # 'paragraph': 'Laseque征：左(一 十)；右(一 十)'
                'paragraph': '桡骨膜反射：右( )；左( )；'
            }
    })
    main(
        args=[extract_obj],
        begin_handle=paragraph2sentence_handle
    )
