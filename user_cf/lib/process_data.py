#!/bin/bash
#coding=utf-8
'''
    输入原始推荐结果，合并其中相同小区的推荐结果，输出
    INPUT:  phone \t resblock_id:resblock_name:room_cnt:score,...
    OUTPUT: \t phone \t resblock_id \t resblock_name \t X居室或Y居室 \t
    AUTHOR: songxin@lianjia.com
    DATE  : 2016-07-12 17:43:13
'''
import sys
from collections import defaultdict

def main(input_stream):
    '''
        输入原始推荐结果，合并其中相同小区的推荐结果，输出
    '''
    for line in input_stream:
        vec = line.strip().split('\t')
        if len(vec) < 2:
            continue
        phone = vec[0]
        recommendations = vec[1].split(',')
        resblock_name = dict()
        resblock_room_cnt = defaultdict(list)
        resblock_score = dict()
        for recommendation in recommendations:
            resblock_id, name, room_cnt, score = recommendation.split(':')
            if resblock_id in resblock_name:
                resblock_room_cnt[resblock_id].append(room_cnt+'居室')
                resblock_score[resblock_id] = str(max(float(resblock_score[resblock_id]), float(score)))
            else:
                resblock_name[resblock_id] = name
                resblock_room_cnt[resblock_id].append(room_cnt+'居室')
                resblock_score[resblock_id] = score

        for resblock_id in resblock_name:
            resblock_room_cnt[resblock_id].sort()
            print '\t'.join(['', phone, resblock_id, resblock_name[resblock_id], \
                             '或'.join(resblock_room_cnt[resblock_id]), resblock_score[resblock_id], ''])

if __name__ == '__main__':
    main(sys.stdin)
