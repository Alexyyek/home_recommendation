#!/bin/python
#coding=utf-8
'''
    输入半个相似性矩阵，输出整个相似性矩阵
    INPUT:  userid_x \t userid_y \t 相似性分数
    OUTPUT: userid_x \t userid_y \t 相似性分数
            userid_y \t userid_x \t 相似性分数
    AUTHOR: songxin@lianjia.com
    DATE:   20160711
'''

import sys

def run(input_stream):
    '''
        输入半个相似性矩阵，输出整个相似性矩阵
    '''
    for line in input_stream:
        vec = line.strip().split('\t')
        user_x = vec[0]
        user_y = vec[1]
        similarity_score = vec[2]

        output_str = '{user_x}\t{user_y}\t{similarity_score}'.format(
            user_x=user_x,
            user_y=user_y,
            similarity_score=similarity_score)
        print output_str

        output_str = '{user_x}\t{user_y}\t{similarity_score}'.format(
            user_x=user_y,
            user_y=user_x,
            similarity_score=similarity_score)
        print output_str

if __name__ == '__main__':
    run(sys.stdin)
