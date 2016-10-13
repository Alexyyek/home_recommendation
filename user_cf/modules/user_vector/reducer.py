#!/bin/python
#coding=utf-8
'''
    INPUT: 标准化的用户行为记录。
           格式: userid \t timestamp \t house_info \t behavior_type
    OUTPUT: userid \t 用户带看resblock_seg数量 \t resblock_seg1名称:权重:最后行为时间,resblock_seg2名称:权重:最后行为时间,...
    AUTHOR: songxin@lianjia.com
    DATE: 2016-07-12 15:21:03
'''
import sys
from collections import defaultdict
from collections import Counter

reload(sys)
sys.setdefaultencoding('utf-8')

BEHAVIOR_WEIGHT = {'pc': 0.5,
                   'mobile': 0.5,
                   'ershoufang': 4.0,
                   'touring': 5.0,
                   'contract': 25.0}
ON_OFF_RATIO = 5.0
ONLINE_TOURING_HOUSE_RATIO = 5.0

def run(input_stream):
    '''
        输入标准化的用户行为，输出用户兴趣向量
    '''
    last_user_id = ''

    for line in input_stream:
        vec = line.strip().split('\t')

        if len(vec) < 4:
            continue
        user_id = vec[0]
        timestamp = vec[1][0:10].replace('-', '')
        resblock_seg = vec[2]
        behavior_type = vec[3]

        if last_user_id == '':
            last_user_id = user_id
            visit_date = defaultdict(str)
            visit_date[resblock_seg] = timestamp

            online_visit_houses = defaultdict(float)
            offline_visit_houses = defaultdict(float)
            online_visit_set = set()
            offline_visit_set = set()
            focus_set = set()

            if behavior_type == 'pc' or behavior_type == 'mobile':
                online_visit_set.add(resblock_seg)
                online_visit_houses[resblock_seg] += BEHAVIOR_WEIGHT[behavior_type]
            elif behavior_type == 'ershoufang':
                focus_set.add(resblock_seg)
                online_visit_houses[resblock_seg] += BEHAVIOR_WEIGHT[behavior_type]
            elif behavior_type == 'touring':
                offline_visit_set.add(resblock_seg)
                offline_visit_houses[resblock_seg] += BEHAVIOR_WEIGHT[behavior_type]
            elif behavior_type == 'contract':
                offline_visit_set.add(resblock_seg)
                offline_visit_houses[resblock_seg] += BEHAVIOR_WEIGHT[behavior_type]

        elif last_user_id == user_id:
            if behavior_type == 'pc' or behavior_type == 'mobile':
                online_visit_set.add(resblock_seg)
                online_visit_houses[resblock_seg] += BEHAVIOR_WEIGHT[behavior_type]
            elif behavior_type == 'ershoufang':
                focus_set.add(resblock_seg)
                online_visit_houses[resblock_seg] += BEHAVIOR_WEIGHT[behavior_type]
            elif behavior_type == 'touring':
                offline_visit_set.add(resblock_seg)
                offline_visit_houses[resblock_seg] += BEHAVIOR_WEIGHT[behavior_type]
            elif behavior_type == 'contract':
                offline_visit_set.add(resblock_seg)
                offline_visit_houses[resblock_seg] += BEHAVIOR_WEIGHT[behavior_type]

            if timestamp > visit_date[resblock_seg]:
                visit_date[resblock_seg] = timestamp
        else:
            intersection_set = online_visit_set.intersection(offline_visit_set)
            for _resblock_seg in intersection_set:
                online_visit_houses[_resblock_seg] *= ONLINE_TOURING_HOUSE_RATIO

            online_weight = sum(online_visit_houses.itervalues())
            offline_weight = sum(offline_visit_houses.itervalues())
            if offline_weight > 0.00000001 and online_weight > offline_weight * ON_OFF_RATIO:
                online_visit_houses = {key:value*ON_OFF_RATIO/(online_weight/offline_weight)  \
                                        for key, value in online_visit_houses.iteritems()}

            visit_houses = Counter(online_visit_houses)
            visit_houses.update(offline_visit_houses)

            visit_houses_str = ','.join([':'.join([_resblock_seg, str(_weight), visit_date[_resblock_seg]])\
                                                   for _resblock_seg, _weight in visit_houses.iteritems()])
            output_str = '{user_id}\t{resblock_seg_no}\t{visit_houses_str}'.format(
                user_id=last_user_id,
                resblock_seg_no=len(visit_houses),
                visit_houses_str=visit_houses_str)
            print output_str

            last_user_id = user_id
            visit_date = defaultdict(str)
            visit_date[resblock_seg] = timestamp

            online_visit_houses = defaultdict(float)
            offline_visit_houses = defaultdict(float)
            online_visit_set = set()
            offline_visit_set = set()
            focus_set = set()

            if behavior_type == 'pc' or behavior_type == 'mobile':
                online_visit_set.add(resblock_seg)
                online_visit_houses[resblock_seg] += BEHAVIOR_WEIGHT[behavior_type]
            elif behavior_type == 'ershoufang':
                focus_set.add(resblock_seg)
                online_visit_houses[resblock_seg] += BEHAVIOR_WEIGHT[behavior_type]
            elif behavior_type == 'touring':
                offline_visit_set.add(resblock_seg)
                offline_visit_houses[resblock_seg] += BEHAVIOR_WEIGHT[behavior_type]
            elif behavior_type == 'contract':
                offline_visit_set.add(resblock_seg)
                offline_visit_houses[resblock_seg] += BEHAVIOR_WEIGHT[behavior_type]

    intersection_set = online_visit_set.intersection(offline_visit_set)
    for _resblock_seg in intersection_set:
        online_visit_houses[_resblock_seg] *= ONLINE_TOURING_HOUSE_RATIO

    online_weight = sum(online_visit_houses.itervalues())
    offline_weight = sum(offline_visit_houses.itervalues())
    if offline_weight > 0.00000001 and online_weight > offline_weight * ON_OFF_RATIO:
        online_visit_houses = {key:value*ON_OFF_RATIO/(online_weight/offline_weight) \
                               for key, value in online_visit_houses.iteritems()}

    visit_houses = Counter(online_visit_houses)
    visit_houses.update(offline_visit_houses)
    visit_houses_str = ','.join([':'.join([_resblock_seg, str(_weight), visit_date[_resblock_seg]])\
                                           for _resblock_seg, _weight in visit_houses.iteritems()])
    output_str = '{user_id}\t{resblock_no}\t{visit_houses_str}'.format(
        user_id=last_user_id,
        resblock_no=len(visit_houses),
        visit_houses_str=visit_houses_str)
    print output_str

if __name__ == '__main__':
    run(sys.stdin)
