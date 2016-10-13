#!/bin/python
#coding=utf-8
'''
    建立resblock_seg到userid的倒排索引。
    INPUT:  resblock_seg_name \t phone \t weight
    OUTPUT: resblock_seg_name \t phone1:weight1,phone2:weight2,...
    AUTHOR: songxin@lianjia.com
    DATE:   2016-07-12 15:53:01
'''
import sys

def run(input_stream):
    '''
        建立resblock_seg到userid的倒排索引。
    '''
    last_resblock_seg = ''
    user_set = set()
    for line in input_stream:
        vec = line.strip().split('\t')
        resblock_seg = vec[0]
        phone = vec[1]
        weight = vec[2]

        if last_resblock_seg == '':
            last_resblock_seg = resblock_seg
            user_set.add(":".join([phone, weight]))
        elif last_resblock_seg == resblock_seg:
            user_set.add(":".join([phone, weight]))
        else:
            output_str = '{resblock_seg}\t{user_set}'.format(
                resblock_seg=last_resblock_seg,
                user_set=','.join(user_set))
            print output_str

            last_resblock_seg = resblock_seg
            user_set.clear()
            user_set.add(":".join([phone, weight]))

    output_str = '{resblock_seg}\t{user_set}'.format(
        resblock_seg=last_resblock_seg,
        user_set=','.join(user_set))
    print output_str

if __name__ == '__main__':
    run(sys.stdin)
