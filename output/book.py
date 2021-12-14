#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/10 12:05
# @File    : book.py.py
# @Software: Basebit
# @Description:

import json
import re

from main import *

check_map = {('Babinski征：阴 阳', 'Babinski征：右(- +) 左(- +)'): '0 1', ('Brudzinski征：无 有', 'Brudzinski征：阳性；阴性'): '1',
             ('Chaddock征：阴 阳', 'Chaddock征：右(- +) 左(- +)'): '0 1', ('Gordon征：阴 阳', 'Gordon征：右(- +) 左(- +)'): '0 1',
             ('Kernig征：无 有', 'Kernig征：右(- +) 左(- +)'): '0 1', ('Murphy征：阴性 阳性', 'Murphy征：阴性 阳性 其他'): '0',
             ('Oppenheim征：右(- +) 左(- +)', 'Oppenheim征：阴 阳'): '0 1',
             ('上肢：正常 肿胀 淤斑 畸形 肌萎缩', '上肢：正常 肿胀 淤斑 畸形 肌萎缩 骨质显露'): '1', ('下肢：正常 肿胀 淤斑 畸形', '下肢：正常 肿胀 淤斑 畸形 窦道'): '1',
             ('乳房：正常 异常', '乳房：正常对称 异常'): '0', ('乳突压痛：无 有', '乳突压痛：无 有(左 右)'): '1',
             ('体位：自动 被动 端坐呼吸 角弓反张', '体位：自动体位 被动体位', '体位：自动体位 半卧位', '体位：自主 被动 强迫'): '0',
             ('体型：无力型 正力型 超力型 步态：正常 不正常', '体型：无力型 正力型 超力型'): '1',
             ('压痛：无 有', '压痛：左 右 无 反常活动', '压痛(无 颈 胸 腰 骶 尾)'): '0 2', ('反跳痛：无 有', '反跳痛：无 有 液'): '0',
             ('发育：正常 不良 超常', '发育(好 中 差)', '发育：正常 不良', '发育： 正常 不良 超常'): '0 1',
             ('听力：正常 减弱(左 右) 丧失(左 右)', '听力：正常 减退(左 右) 耳鸣(左 右) 丧失(左 右)'): '1',
             ('听力障碍：无 有', '听力障碍：无 有(左 右)', '听力障碍： 无 有(左 右)', '听力障碍：无 右(左 右)'): '1',
             ('听诊：肠鸣音：{input1}次/分{input2}亢进{input3}减弱{input4}消失', '听诊：心率{input1}次/分{input2}心律：整齐{input3}不齐'): '1',
             ('周围血管征：无异常血管征 有', '周围血管征：无 有'): '1', ('周围血管征及其他：无 枪击音 Duroziez双重杂音 毛细血管搏动征 奇脉 交替脉 水冲脉 脉搏短绌 其他：',
                                                    '周围血管征及其他：无 有 枪击音 Duroziez双重杂音 毛细血管搏动征 奇脉 交替脉 水冲脉 脉搏短绌'): '0',
             ('呼吸：正常 反常 急促 困难 端正 喘鸣', '呼吸：规则 失调 停止', '呼吸：通畅 鼾声 不通畅(分泌物 舌后坠) 酒味 酮味 尿臭 肝臭'): '0 1 2',
             ('呼吸音：正常 异常', '呼吸音：清晰 粗糙 干啰音 湿啰音'): '1', ('嗅觉：正常 异常', '嗅觉：正常 迟钝 消失'): '1', (
                 '四肢：正常 异常 关节红肿 关节强直 杵状指(趾) Osler结节 Janeways结 肌肉萎缩', '四肢：正常 异常', '四肢：正常 异常 畸形',
                 '四肢：正常 异常 关节红肿 关节强直 杵状指(趾) Osler结 Janeway结 肌肉萎缩'): '0', ('外伤：无 有 外伤情况及时间', '外伤：无 有 外伤情况及时间：'): '0',
             ('外伤史：无 有', '外伤史(无 有)'): '0', ('外耳道异常分泌物：无 有', '外耳道异常分泌物：无 左（性质） 右（性质）'): '1',
             ('头发分布：正常 异常 其他：', '头发分布：正常 异常', '头发分布：正常 异常 描述'): '0',
             ('巩膜黄染：无 有', '巩膜黄染：无、轻、中、重', '巩膜黄染：无 轻 中 重'): '2', ('心包摩擦音：无 有', '心包摩擦音：无 有 其他：'): '1',
             ('心尖搏动：正常 抬举性 负性搏动', '心尖搏动：正常 异常'): '0', ('心尖搏动位置：正常 移位(距左锁骨中线 内 cm 外 cm)', '心尖搏动位置：正常 移位'): '0',
             ('心律：整齐 不齐', '心律：齐 、不齐', '心律：齐 不齐', '心律：整齐 不齐 绝对不齐'): '3',
             ('心率{input1}次/分', '心率：{input1}次/分', '心率:{input1}次/分'): '1',
             ('心脏相对浊音界：正常 缩小 扩大(向左 向右)', '心脏相对浊音界：正常 缩小 扩大(左 右)'): '0', ('心音：正常 异常 P A2', '心音：正常 异常'): '1',
             ('手术：无 有 手术名称及时间', '手术：无 有 名称及时间', '手术：无 有 名称及时间：'): '0', ('手术外伤史：无 有 手术或外伤名称及时间', '手术外伤史：无 有'): '0',
             ('指鼻试验：右(正常 正常 摇摆 不准 过度 )； 左(正常 摇摆 不准 过度)', '指鼻试验：阴 阳'): '0',
             ('杂音：无 有', '杂音：无 有(部位) 时期 性质 强度 传导 影响因素)', '杂音：无 有(部位) 传导 时期 性质 强度 影响因素)'): '1', (
                 '步态：剪刀步态 偏瘫步态 跨越步态 其他：', '步态：正常 不正常', '步态：剪刀步态 偏瘫步态 跨越步态',
                 '步态：正常 画圈样(右 左) 跨阈样(右 左) 剪刀样 慌张样 醉汉样 鸭步'): '0 3', (
                 '气管：正中 偏移(左/右)', '气管：居中 偏移(向左 向右)', '气管：居中、偏移(左、右)', '气管：居中 偏移(向左；向右)', '气管：正中 偏移(左 mm 右 mm)',
                 '气管：居中 偏移(左 右)', '气管：正中 偏移(向左 向右)'): '1 4', ('水肿：无 有', '水肿：无 有(分布)'): '1',
             ('浅表淋巴结肿大：无 有', '浅表淋巴结肿大：无 有 描述'): '1', ('甲状腺：正常 结节 肿大', '甲状腺：正常 异常'): '0',
             ('畸形：无 有 其他：', '畸形：无 有'): '0', ('皮下出血：无 有', '皮下出血：无 有(瘀点或出血点、紫癜、瘀斑、血肿)'): '1',
             ('皮疹：无 有', '皮疹：无 有(分布)'): '1', (
                 '皮肤粘膜：正常 苍白 潮红 发绀 黄疸 色素沉着 皮疹 皮下出血 水肿 其他：', '皮肤粘膜：正常 苍白 黄染 皮疹', '皮肤粘膜：色泽：正常 苍白 潮红 发绀 黄染 色素沉着',
                 '皮肤粘膜：红润 温暖 苍白 厥冷', '皮肤粘膜：正常 苍白 黄染 皮疹 出血点 色素沉着 其他：', '皮肤粘膜：红润 苍白 温暖 冷厥 发绀 冷汗 失水 水肿 皮疹 淤斑'): '0', (
                 '皮肤粘膜色泽：正常 苍白 潮红 发绀 黄染 色素沉着 其他', '皮肤粘膜色泽：正常 苍白 潮红 发绀 黄染 色素沉着 其他：', '皮肤粘膜色泽：正常 潮红 发绀 黄染 色素沉着 色素减退',
                 '皮肤粘膜色泽：正常 潮红 苍白 发绀 黄染 色素沉着 色素减退'): '3', ('直接光反射：灵敏 减弱 消失', '直接光反射：正常(左 右) 迟钝(左 右) 消失(左 右)'): '0',
             ('眼球位置：同向斜视 分离性斜视 外展(左 右)', '眼球位置：正常 异常'): '0 1', ('眼球运动：正常 异常', '眼球运动：不能 正常'): '0',
             ('眼球震颤：水平 垂直 旋转 无', '眼球震颤：无 有'): '0', (
                 '瞳孔：等大等圆 不等 左', '瞳孔：等大等圆 不等(左 mm 右 mm)', '瞳孔：等大等圆 不等（左 mm 右 mm）', '瞳孔：等大等圆、不等(左 mm 右 mm)',
                 '瞳孔：等圆等大 不等（左 mm 右 mm）', '瞳孔：等大等圆、不等(左 cm 右 cm)'): '1', (
                 '神志：清楚 嗜睡 模糊 昏睡 浅 昏迷 中度 昏迷 深昏迷 谵妄', '神志：清醒 淡漠 模糊', '神志：清楚 嗜睡 模糊 昏睡 浅昏迷 中度 昏迷 深昏迷 谵妄',
                 '神志：清楚 嗜睡 模糊 昏睡 浅昏迷 中度昏迷 深昏迷 谵妄'): '0', ('移动性浊音：阴性 阳性', '移动性浊音：无 有'): '0',
             ('结膜：正常 左（出血 水肿） 右（出血 水肿）', '结膜：正常 充血 水肿 出血'): '1',
             ('肌张力：正常 增高 减弱', '肌张力：正常(右 左) 减低(右 左) 折刀样增高(右 左) 铅管样增高(右 左) 齿轮样增高(右 左)'): '1',
             ('肌肉萎缩：无 有 部位', '肌肉萎缩：无 有(部位))'): '0', ('肝浊音界：存在 缩小 消失', '肝浊音界：正常 异常'): '0',
             ('肝脏：未触及 触及', '肝脏：未触及 触及(肋下 cm 剑突下 cm 质地 表面 边缘 压痛)'): '1',
             ('肠鸣音：正常 亢进 减弱 消失', '肠鸣音{input1}次/分', '肠鸣音：无 有', '肠鸣音：正常 亢进 减弱'): '0',
             ('肺叩诊：正常清音 过清音 实音 浊音', '肺叩诊：正常清音 异常'): '0', ('肿块：无 有 部位', '肿块：无 有'): '0', (
                 '胸廓：正常 桶状胸 膨隆 凹陷(左心前区 右心前区)', '胸廓：对称、畸形', '胸廓：正常 畸形', '胸廓：正常 异常', '胸廓：对称 畸形',
                 '胸廓：正常 桶状 胸 膨隆 凹陷(左心前区 右心前区)'): '0', ('胸膜摩擦感：无 有', '胸膜摩擦感：无 有(左 右)'): '1', (
                 '脊柱：正常 异常 畸形 压痛', '脊柱：正常 畸形 肿胀 瘘道', '脊柱：正常 畸形 肿胀 瘘道 压痛(第 椎体)', '脊柱：正常 异常',
                 '脊柱：正常 畸形 肿胀 瘘道 压痛(无 有 第 椎体)', '脊柱：正常 异常 畸形', '脊柱：正常 异常：畸形( 凸)压痛(部位)'): '2',
             ('腹部外形：正常 膨隆 舟状腹 蛙腹', '腹部外形：正常 膨隆 凹陷'): '0', ('腹部视诊：正常 膨隆 凹陷', '腹部视诊：平坦 膨隆 舟状腹 蛙腹'): '1',
             ('药物过敏史：无 有 不祥 过敏药品名称：', '药物过敏史：无 不详 有 过敏药物名称及过敏情况', '药物过敏史：无 有(药物名称)', '药物过敏史：无 有 不详 过敏药物名称'): '1',
             ('营养：良好 中等 不良 恶病质', '营养：良好 中等 不良 差', '营养：良好 中等 不 良 差', '营养：好 中 差', '营养(好 中 差)'): '0 3',
             ('血管杂音：无 有 部位', '血管杂音：无 有'): '0', ('表情：自如 痛苦 淡漠', '表情：自如 其他'): '0',
             ('视力：正常 异常', '视力：正常 减退(左 右) 失明(左 右)'): '1',
             ('角膜：正常 浑浊(左 右)', '角膜：正常 浑浊(左 右) 溃疡(左 右)', '角膜：正常 混浊(左 右) 溃疡(左 右)'): '1',
             ('角膜反射：正常 迟钝(左 右) 消失(左 右)', '角膜反射：灵敏 减弱 消失'): '0',
             ('跟膝胫试验：阴 阳', '跟膝胫试验：右(正常 正常 摇摆 不准)； 左(正常 摇摆 不准)'): '1',
             ('输血史：无 有', '输血史：无 有 输血时间', '输血史：无 有 输血时间：', '输血史：无 有 输血时间 输血反应'): '3',
             ('附加心音：无 有(奔马律 ；开瓣音；第三心音 ；第四心音)', '附加心音：无 有(奔马律；开瓣音；第三心音；第四心音)', '附加心音：无 有(奔马律 开瓣音 第三心音 第四心音)'): '2',
             ('面容：急性 慢性 贫血', '面容：正常 痛苦 慢性病容', '面容：无病容 急性面容 慢性面容', '面容：无病容 急性病容 慢性病容 贫血面容'): '3',
             ('预防接种史：无 不详 有 预防接种药品', '预防接种史：无 有 不详', '预防接种史：无 有 不祥 预防接种疫苗：', '预防接种史：无 不详 有 预防接种疫苗'): '0',
             ('颈部血管杂音：无 有', '颈部血管杂音：无 有(左 右)'): '1', ('颈静脉：正常 充盈 怒张', '颈静脉：不显露 充盈 怒张'): '0',
             ('颈项强直：无 有', '颈项强直：无 有(下颌距胸骨 横指)'): '1', ('高血压(无 有)', '高血压：无 有'): '1',
             ('鼻唇沟：对称 浅(左 右)', '鼻唇沟：对称 变浅(左 右)'): '1'}


def record():
    """
    将原始文本解析后存入Excel
    :return:
    """
    base_path = '/Users/jeremy.li/Basebit/Projects/AutoTemplate/pdf2text/bookTextsManual'
    g = os.walk(base_path)
    for path, _, file_list in g:
        for ind, file in enumerate(file_list):
            if 'txt' not in file:
                continue
            print('开始处理：{}'.format('{}/{}'.format(base_path, file)))
            with open('{}/{}'.format(base_path, file), 'r') as f:
                raw_text = f.read()
            if not raw_text:
                continue
            extract_obj = ExtractStructure(
                file_name=file,
                file_path=base_path,
                raw_text=raw_text,
            )
            extract_obj.paragraphs = {
                '未分类': {'sort': 1, 'paragraph': raw_text}
            }
            result = main(
                args=[extract_obj],
                begin_handle=paragraph2sentence_handle
            )

            # 数据入库逻辑
            file_names = []
            displays = []
            segments = []
            texts = []

            # insert args
            # print(args)
            for arg in result:
                for infos in arg.paragraphs.values():
                    for segment in infos['segments_show']:
                        file_names.append(arg.file_name)
                        displays.append(segment['display'])
                        texts.append(segment['text'])
                        segments.append(json.dumps(segment['segment'], ensure_ascii=False))
            data2excel(pd.DataFrame({
                'file_name': file_names,
                'display': displays,
                'segment': segments,
                'text': texts,
            }), 'book_result.xlsx', 'base')


def analysis():
    """
    对书本的segments进行分析，去重合并
    :return:
    """
    finish_df = pd.DataFrame(columns=['display', 'segment', 'text', 'department'])
    check_df = pd.DataFrame(columns=['file_name', 'display', 'segment', 'text'])
    df = pd.read_excel('{}/output/book_result.xlsx'.format(cons.BASE_PATH), sheet_name='base')

    # 根据key排序
    df.sort_values('display', inplace=True)
    first_data = df.iloc[0]
    display, segment, department, is_same = first_data.display, first_data.segment, [first_data.file_name], True

    for _, line in df.iterrows():
        display_ = line.display
        segment_ = line.segment
        department_ = line.file_name
        if display_ != display:
            # 新的segment
            if is_same:
                line['department'] = json.dumps(department, ensure_ascii=False)
                finish_df = finish_df.append(line[['display', 'segment', 'text', 'department']], ignore_index=True)
            else:
                check_df = check_df.append(df.loc[df['display'] == display],
                                           ['file_name', 'display', 'segment', 'text'])
            display, segment, department, is_same = display_, segment_, [department_], True

        else:
            department.append(department_)
            # 与其他同名segment比较
            if segment_ != segment:
                is_same = False

    # TODO：在同个file中新增sheet
    data2excel(finish_df, 'finish_book_result.xlsx', '标准', is_append=False)
    data2excel(check_df, 'check_book_result.xlsx', '待确认', is_append=False)


def check_result():
    """
    人工校验check_book_result.xlsx
    :return:
    """
    df = pd.read_excel('check_book_result.xlsx')
    finish_df = pd.DataFrame(columns=['display', 'segment', 'text', 'department'])
    check_df = pd.DataFrame(columns=['file_name', 'display', 'segment', 'text'])
    for display in df.display.unique():
        df_ = df.loc[df['display'] == display]
        texts = df_.text.unique()
        save_inds = check_map.get(tuple(texts))
        if not save_inds:
            for ind, text in enumerate(texts):
                print(ind, text)
            save_inds = input('请输入要保留的ind（多个ind用非数字分割）：')

        if save_inds:
            check_map[tuple(texts)] = save_inds
            # 如果有标准
            for save_ind in re.split('\D', save_inds):
                #  获取需要保存的segment对应的所有department
                save_df = df_.loc[df_['text'] == texts[int(save_ind)]]
                department = []
                for _, line in save_df.iterrows():
                    department.append(line.file_name)
                temp_df = save_df.iloc[0]
                temp_df['department'] = json.dumps(department, ensure_ascii=False)
                finish_df = finish_df.append(temp_df[['display', 'segment', 'text', 'department']])
        else:
            # 任然没有标准，还需要人工处理
            check_df = check_df.append(df_)

    print(check_map)
    data2excel(finish_df, 'finish_book_result.xlsx', '标准', is_append=True)
    data2excel(check_df, 'check_book_result.xlsx', '待确认', is_append=False)


def check_again_with_html():
    """
    在页面上检查是否正确
    :return:
    """
    df = pd.read_excel('finish_book_result.xlsx')
    for _, line in df.iterrows():
        display = line.display + '\n'
        segments = [json.loads(line.segment)]
        update_html(display, segments)
        print('检查')


if __name__ == '__main__':
    # record()
    # analysis()
    # check_result()
    check_again_with_html()
