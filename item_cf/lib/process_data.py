#!/bin/bash
#coding=utf-8
'''
    输入原始推荐结果，合并其中相同小区的推荐结果，输出
    INPUT:  phone \t resblock_id \t resblock_name_dict \t room_cnt \t build_area \t score
    OUTPUT: \t phone \t resblock_id \t resblock_name_dict \t X居室或Y居室 \t
    AUTHOR: yangyekang@lianjia.com
    DATE  : 2016-08-30 23:29:08
'''
import sys
from collections import defaultdict

def main(input_stream):

    '''
        输入原始推荐结果，合并其中相同小区的推荐结果，输出
    '''

    current_phone = ""
    phone = ""
    resblock_name_dict = dict()
    resblock_room_cnt = defaultdict(list)
    resblock_score = dict()

    for line in input_stream:
        line = line.strip()
        if len(line.split('\t')) < 6:
            continue
        phone, resblock_id, resblock_name, room_cnt, build_area, score = line.split('\t')
        if current_phone == phone:
            if resblock_id in resblock_name_dict:
                resblock_room_cnt[resblock_id].append(room_cnt+'居室')
                resblock_score[resblock_id] = str(max(float(resblock_score[resblock_id]), float(score)))
            else:
                resblock_name_dict[resblock_id] = resblock_name
                resblock_room_cnt[resblock_id].append(room_cnt+'居室')
                resblock_score[resblock_id] = score
        else:
            if current_phone:
                for resblock_id in resblock_name_dict:
                    resblock_room_cnt[resblock_id] = set(resblock_room_cnt[resblock_id])
                    resblock_room_cnt[resblock_id] = list(resblock_room_cnt[resblock_id])
                    resblock_room_cnt[resblock_id].sort()
                    print '\t'.join([current_phone, resblock_id, \
                        resblock_name_dict[resblock_id], '或'.join(  \
                        resblock_room_cnt[resblock_id]), resblock_score[resblock_id]])
            current_phone = phone
            resblock_name_dict.clear()
            resblock_room_cnt.clear()
            resblock_score.clear()
            resblock_name_dict[resblock_id] = resblock_name
            resblock_room_cnt[resblock_id].append(room_cnt+'居室')
            resblock_score[resblock_id] = score
    if current_phone == phone:
        for resblock_id in resblock_name_dict:
            resblock_room_cnt[resblock_id] = set(resblock_room_cnt[resblock_id])
            resblock_room_cnt[resblock_id] = list(resblock_room_cnt[resblock_id])
            resblock_room_cnt[resblock_id].sort()
            print '\t'.join([current_phone, resblock_id, \
                resblock_name_dict[resblock_id], '或'.join(  \
                resblock_room_cnt[resblock_id]), resblock_score[resblock_id]])

if __name__ == '__main__':
    main(sys.stdin)
