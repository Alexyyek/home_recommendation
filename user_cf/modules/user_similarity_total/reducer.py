#!/bin/python
#coding=utf-8
'''
    输入两个用户在某些维度上的权重乘积，汇总之，然后输出两个用户的余弦相似性
    INPUT: userid_x \t userid_y \t weight_sum
    OUTPUT: userid_x \t userid_y \t 余弦相似分数
    AUTHOR: songxin@lianjia.com
    DATE :  2016-07-12 16:37:38
'''
import sys
import math
from collections import defaultdict

def run(input_stream):
    '''
        输入两个用户在某些维度上的权重乘积，汇总之，然后输出两个用户的余弦相似性
    '''
    user_pref_norm = defaultdict(float)
    for line in open('user_pref_vector.txt', 'r'):
        vec = line.strip().split('\t')
        if len(vec) < 3:
            continue
        user_id = vec[0]
        resblock_no = vec[1]
        vec_norm = 0.0
        for _resblock_seg_info in vec[2].strip().split(','):
            _, _resblock_seg_weight, _ = _resblock_seg_info.strip().rsplit(':', 2)
            _resblock_seg_weight = float(_resblock_seg_weight)
            vec_norm += _resblock_seg_weight * _resblock_seg_weight
        user_pref_norm[user_id] = math.sqrt(vec_norm)

    last_user_x = ""
    last_user_y = ""
    weight_sum = 0.0
    for line in input_stream:
        vec = line.strip().split('\t')
        user_x = vec[0]
        user_y = vec[1]
        weight = float(vec[2])

        if last_user_x == "" or last_user_y == "":
            last_user_x = user_x
            last_user_y = user_y
            weight_sum = weight
        elif last_user_x == user_x and last_user_y == user_y:
            weight_sum += weight
        else:
            similar_score = weight_sum / (user_pref_norm[last_user_x] * user_pref_norm[last_user_y])
            output_str = '{user_x}\t{user_y}\t{similar_score}'.format(
                user_x=last_user_x,
                user_y=last_user_y,
                similar_score=similar_score)
            print output_str

            last_user_x = user_x
            last_user_y = user_y
            weight_sum = weight

    similar_score = weight_sum / (user_pref_norm[last_user_x] * user_pref_norm[last_user_y])
    output_str = '{user_x}\t{user_y}\t{similar_score}'.format(
        user_x=last_user_x,
        user_y=last_user_y,
        similar_score=similar_score)
    print output_str

if __name__ == '__main__':
    run(sys.stdin)
