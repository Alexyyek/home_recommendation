#!/bin/python
#coding=utf-8
'''
    输入top N最接近用户，输出推荐结果
    INPUT： userid \t userid_x:score_x,userid_y:score_y,...
    OUTPUT: userid \t resblock_seg_1:score_1,resblock_seg_1:score_2,...
    AUTHOR: songxin@lianjia.com
    DATE  : 2016-07-12 17:32:10
'''

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from collections import defaultdict

def run(input_stream, recommendation_no):
    '''
        输入top N最接近用户，输出推荐结果
    '''
    user_touring_set = defaultdict(set)
    for line in open('user_touring.txt', 'r'):
        vec = line.strip().split('\t')
        if len(vec) < 2:
            continue
        userid = vec[0]
        for _resblock_seg in vec[1].strip().split(','):
            user_touring_set[userid].add(_resblock_seg)

    user_pref_vec = dict()
    for line in open('user_pref_vector.txt', 'r'):
        vec = line.strip().split('\t')
        if len(vec) < 3:
            continue
        userid = vec[0]

        user_pref_vec[userid] = dict()
        for _resblock_info in vec[2].strip().split(','):
            _resblock_id, _weight, _ = _resblock_info.rsplit(':', 2)
            user_pref_vec[userid][_resblock_id] = float(_weight)

    for line in input_stream:
        vec = line.strip().split('\t')
        userid = vec[0]
        similar_user_list = vec[1].split(',')

        recommendation = defaultdict(float)
        rec_denom = defaultdict(float)

        for similar_user in similar_user_list:
            vec = similar_user.split(':')
            similar_userid = vec[0]
            similar_score = float(vec[1])

            if similar_userid not in user_pref_vec:
                continue

            for pref in user_pref_vec[similar_userid]:
                if pref not in user_touring_set[userid]:
                    recommendation[pref] += similar_score * user_pref_vec[similar_userid][pref]
                    rec_denom[pref] += similar_score

        recommendation = {key:value/rec_denom[key] for key, value in recommendation.iteritems()}
        recommendation = sorted(recommendation.iteritems(), key=lambda x: x[1], reverse=True)
        recommendation = [':'.join([key, str(value)]) for key, value in recommendation]
        output_str = '{userid}\t{recommendation}'.format(
            userid=userid,
            recommendation=','.join(recommendation[0:recommendation_no]))
        print output_str

if __name__ == '__main__':
    RECOMMENDATION_NO = int(sys.argv[1])
    run(sys.stdin, RECOMMENDATION_NO)
