#!/bin/python
#coding=utf-8

'''
    INPUT: 特定格式的的用户行为记录。
           格式：userid \t timestamp \t house_pkid \t behavior_type
           其中，若behavior_type为用户线上行为(pc/mobile/ershoufang/resblock中的一种),则userid为用户ucid;
           若behavior_type为用户线下行为(touring/contract中的一种),则userid为用户电话号码
    OUTPUT: 标准化的用户行为记录。
            格式: userid \t timestamp \t house_info \t behavior_type
    AUTHOR: songxin@lianjia.com
    DATE ： 20160711
'''


import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def run(input_stream):
    '''
        输入特定格式的用户行为记录，输出标准化的用户行为记录
    '''
    house_info = dict()
    user_phone = dict()

    for line in open('house_detail.txt', 'r'):
        vec = line.strip().split('\t')
        house_pkid = vec[0]
        build_area = vec[2]
        room_cnt = vec[3]
        resblock_id = vec[8]
        resblock_name = vec[9]
        house_info[house_pkid] = ':'.join([resblock_id, resblock_name, room_cnt])

    for line in open('ucid_mobile.txt', 'r'):
        vec = line.strip().split('\t')
        if len(vec) == 2 and vec[1] != 'NULL':
            user_phone[vec[0]] = vec[1]

    for line in input_stream:
        vec = line.strip().split('\t')
        if len(vec) < 4:
            continue

        user_id = vec[0]
        timestamp = vec[1]
        house_pkid = vec[2]
        behavior_type = vec[3]

        if behavior_type == 'pc' or behavior_type == 'mobile' \
            or behavior_type == 'ershoufang' or behavior_type == 'resblock':
            if user_id in user_phone:
                user_id = user_phone[user_id]
            else:
                continue

        if house_pkid.startswith('BJ'):
            house_pkid = '1010' + house_pkid[4:]
        if house_pkid not in house_info:
            continue

        output_str = '{user_id}\t{timestamp}\t{house_info}\t{behavior_type}'.format(
            user_id=user_id,
            timestamp=timestamp,
            house_info=house_info[house_pkid],
            behavior_type=behavior_type)
        print output_str

if __name__ == '__main__':
    run(sys.stdin)
