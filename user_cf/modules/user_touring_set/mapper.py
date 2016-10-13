#!/bin/python
#coding=utf-8
'''
    输入用户线下行为数据，输出其线下行为覆盖的resblock_seg
    INPUT:  用户线下行为数据
            格式：userid \t timestamp \t house_pkid \t behavior_type
            其中behavior_type为touring或contract
    OUTPUT: 用户线下行为resblock_seg集合
            格式: userid \t resblock_id:resblock_name:room_cnt,......
    AUTHOR: songxin@lianjia.com
    DATE  : 2016-07-12 17:58:06
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def run(input_stream):
    '''
        输入用户线下行为数据，输出其线下行为覆盖的resblock_seg
    '''
    house_info = dict()
    for line in open('house_detail.txt', 'r'):
        vec = line.strip().split('\t')
        house_pkid = vec[0]
        build_area = float(vec[2])
        room_cnt = vec[3]
        if room_cnt == '1':
            if build_area < 30:
                room_cnt = '#'.join([room_cnt, "小于30"])
            elif 50 > build_area >= 30:
                room_cnt = '#'.join([room_cnt, "30至50"])
            elif 80 >= build_area >= 50:
                room_cnt = '#'.join([room_cnt, "50至80"])
            else:
                room_cnt = '#'.join([room_cnt, "大于80"])
        elif room_cnt == '2':
            if build_area < 50:
                room_cnt = '#'.join([room_cnt, "小于50"])
            elif 80 > build_area >= 50:
                room_cnt = '#'.join([room_cnt, "50至80"])
            elif 130 > build_area >= 80:
                room_cnt = '#'.join([room_cnt, "80至130"])
            else:
                room_cnt = '#'.join([room_cnt, "大于130"])
        elif room_cnt == '3':
            if build_area < 75:
                room_cnt = '#'.join([room_cnt, "小于75"])
            elif 90 > build_area >= 75:
                room_cnt = '#'.join([room_cnt, "75至90"])
            elif 140 > build_area >= 90:
                room_cnt = '#'.join([room_cnt, "90至140"])
            elif 300 >= build_area >= 140:
                room_cnt = '#'.join([room_cnt, "140至300"])
            else:
                room_cnt = '#'.join([room_cnt, "大于300"])

        resblock_id = vec[8]
        resblock_name = vec[9]
        house_info[house_pkid] = ':'.join([resblock_id, resblock_name, room_cnt])

    last_user_id = ''
    for line in input_stream:
        vec = line.strip().split('\t')
        if len(vec) < 4:
            continue

        user_id = vec[0]
        house_pkid = vec[2]

        if house_pkid.startswith('BJ'):
            house_pkid = '1010' + house_pkid[4:]
        if house_pkid not in house_info:
            continue
        if last_user_id == '':
            last_user_id = user_id
            touring_set = set()
            touring_set.add(house_info[house_pkid])
        elif last_user_id == user_id:
            touring_set.add(house_info[house_pkid])
        else:
            output_str = '{user_id}\t{touring_set_str}'.format(
                user_id=last_user_id,
                touring_set_str=','.join(touring_set))
            print output_str

            last_user_id = user_id
            touring_set = set()
            touring_set.add(house_info[house_pkid])

    output_str = '{user_id}\t{touring_set_str}'.format(
        user_id=last_user_id,
        touring_set_str=','.join(touring_set))
    print output_str

if __name__ == '__main__':
    run(sys.stdin)
