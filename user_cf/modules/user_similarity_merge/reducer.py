#!/bin/python
#coding=utf-8
'''
    输入两个用户在某些维度上的权重乘积，汇总之
    INPUT: userid_x \t userid_y \t weight_sum
    OUTPUT: userid_x \t userid_y \t 汇总权重
    AUTHOR: songxin@lianjia.com
    DATE :  2016-07-12 16:37:38
'''
import sys
import math
from collections import defaultdict

def run(input_stream):
    '''
        输入两个用户在某些维度上的权重乘积，汇总之
    '''
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
            output_str = '{user_x}\t{user_y}\t{weight_sum}'.format(
                user_x=last_user_x,
                user_y=last_user_y,
                weight_sum=weight_sum)
            print output_str

            last_user_x = user_x
            last_user_y = user_y
            weight_sum = weight

    output_str = '{user_x}\t{user_y}\t{weight_sum}'.format(
        user_x=last_user_x,
        user_y=last_user_y,
        weight_sum=weight_sum)
    print output_str

if __name__ == '__main__':
    run(sys.stdin)
