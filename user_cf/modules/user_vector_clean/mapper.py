#!/bin/python
#coding=utf-8

'''
    用户行为向量清洗，清洗掉每个用户权重占比不到一定百分比的行为.
    INPUT:  用户行为向量
            格式: userid \t 带看resblock_seg数量 \t 行为向量
    OUTPUT: 清洗过的用户行为向量
            格式: userid \t 带看resblock_seg数量 \t 行为向量
    AUTHOR: songxin@lianjia.com
    DATE:   2016-07-12 15:27:52
'''

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def run(input_stream, weight_lower_bound):
    '''
    用户行为向量清洗，清洗掉每个用户权重占比不到一定百分比的行为.
    '''
    spider = set()
    for line in open('spider.txt', 'r'):
        spider.add(line.strip())

    for line in input_stream:
        vec = line.strip().split('\t')
        if len(vec) < 3:
            continue

        user_id = vec[0]
        if user_id in spider:
            continue

        resblock_no = vec[1]
        resblock_segs = vec[2].strip().split(',')
        weight_sum = 0.0
        pref_vec = dict()
        visit_date = dict()
        for resblock_seg in resblock_segs:
            _resblock_seg_id, weight, timestamp = resblock_seg.rsplit(':', 2)
            weight_sum += float(weight)
            pref_vec[_resblock_seg_id] = float(weight)
            visit_date[_resblock_seg_id] = timestamp

        pref_vec = {key:value for key, value in pref_vec.iteritems() \
                              if float(value) >= weight_sum * weight_lower_bound}
        resblock_no = len(pref_vec)
        pref_vec_str = ','.join([':'.join([_resblock_seg, str(_weight), visit_date[_resblock_seg]])\
                                              for _resblock_seg, _weight in pref_vec.iteritems()])
        output_str = '{user_id}\t{resblock_no}\t{pref_vec_str}'.format(
            user_id=user_id,
            resblock_no=resblock_no,
            pref_vec_str=pref_vec_str)
        print output_str

if __name__ == '__main__':
    WEIGHT_LOWER_BOUND = float(sys.argv[1])
#    WEIGHT_LOWER_BOUND = 0.005
    run(sys.stdin, WEIGHT_LOWER_BOUND)
