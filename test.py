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
                # 'paragraph': '外耳道异常分泌物：无 有(左 右 性质'
                'paragraph': '外耳道异常分泌物：无 有(左 右 性质'
                # 'paragraph': '耳漏：正常 左（血 脑脊液 脑组织） 右（血 脑脊液 脑组织）'
            }
    })
    main(
        args=[extract_obj],
        begin_handle=paragraph2sentence_handle
    )
