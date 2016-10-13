#!/bin/python
#coding=utf-8
'''
    输入两个用户在某一维度上的权重乘积，汇总之
    INPUT: userid_x \t userid_y \t weight
    OUTPUT: userid_x \t userid_y \t weight_sum
    ATTENTION: 由于上游mapper的数据已经进行了切分，
               因此输出并非为两个用户在所有维度上的乘积的和
    AUTHOR: songxin@lianjia.com
    DATE:   2016-07-12 16:34:20
'''
import sys

def run(input_stream):
    '''
        输入两个用户在某一维度上的权重乘积，汇总之
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
            similar_score = weight_sum
            output_str = '{user_x}\t{user_y}\t{similar_score}'.format(
                user_x=last_user_x,
                user_y=last_user_y,
                similar_score=similar_score)
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
