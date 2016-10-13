#!/bin/python
#coding=utf-8
'''
    输入用户行为向量，为每个用户建立倒排索引
    INPUT： phone \t 感兴趣的resblock_seg数量 \t 用户行为向量
    OUTPUT: resblock_seg_name \t phone \t 权重
    AUTHOR: songxin@lianjia.com
    DATE:   2016-07-12 15:46:43
'''

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def run(input_stream):
    '''
        输入用户行为向量，建立倒排索引
    '''
    for line in input_stream:
        vec = line.strip().split('\t')
        if len(vec) < 3:
            continue
        phone = vec[0]
        resblock_seg_no = vec[1]
        resblock_segs = vec[2].split(',')
        for resblock_seg in resblock_segs:
            resblock_seg_name, weight, _ = resblock_seg.rsplit(':', 2)
            output_str = '{resblock_seg_name}\t{phone}\t{weight}'.format(
                resblock_seg_name=resblock_seg_name,
                phone=phone,
                weight=weight)
            print output_str

if __name__ == '__main__':
    run(sys.stdin)
