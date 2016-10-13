#!/bin/python
#coding=utf-8
'''
    输入用户倒排索引，输出两个用户在某一维度上的权重乘积。
    INPUT:  用户倒排索引
            格式: resblock_seg, user_x:weight_x,user_y:weight_y,...
    OUTPUT: user_x, user_y, 权重乘积
            其中user_x > user_y
    AUTHOR: songxin@lianjia.com
    DATE:   2016-07-12 15:57:11
'''

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def run(input_stream):
    '''
        输入用户倒排索引，输出两个用户在某一维度上的权重乘积。
    '''
    user_set = set()
    for line in open('user_pref_vector.txt', 'r'):
        vec = line.strip().split('\t')
        if len(vec) < 3:
            continue
        user_id = vec[0]
        user_set.add(user_id)

    for line in input_stream:
        vec = line.strip().split('\t')
        resblock_seg = vec[0]
        user_list = vec[1].split(',')
        for idx_x in range(0, len(user_list) - 1):
            user_x, weight_x = user_list[idx_x].split(':')
            if user_x not in user_set:
                continue
            for idx_y in range(idx_x+1, len(user_list)):
                user_y, weight_y = user_list[idx_y].split(':')
                if user_y not in user_set:
                    continue

                weight = float(weight_x) * float(weight_y)
                if user_x > user_y:
                    output_str = '{user_x}\t{user_y}\t{weight}'.format(
                        user_x=user_x,
                        user_y=user_y,
                        weight=weight)
                else:
                    output_str = '{user_x}\t{user_y}\t{weight}'.format(
                        user_x=user_y,
                        user_y=user_x,
                        weight=weight)

                print output_str

if __name__ == '__main__':
    run(sys.stdin)
