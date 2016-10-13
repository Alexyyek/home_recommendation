#!/bin/python

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from collections import defaultdict

def run(input_stream, resblock_bedroom_price_file, user_vector_clean_file):
    resblock_price = dict()
    for line in open(resblock_bedroom_price_file, 'r'):
        vec = line.strip().split('\t')
        if len(vec) < 4:
            continue
        resblock_id, resblock_name, room_cnt, price = vec
        resblock_seg = ':'.join(vec[0:3])
        resblock_price[resblock_seg] = float(price)

    room_cnt_pref = dict()
    resblock_price_pref = dict()
    for line in open(user_vector_clean_file, 'r'):
        vec = line.strip().split('\t')
        if len(vec) < 3:
            continue
        user_id, _, pref_set = vec
        room_cnt_pref[user_id] = defaultdict(float)
        resblock_price_pref[user_id] = defaultdict(float)
        for pref in pref_set.split(','):
            resblock_id, resblock_name, room, weight, timestamp = pref.split(':')
            if room.find('#') != -1:
                room_cnt = room[0:room.find('#')]
            else:
                room_cnt = room
            room_cnt_pref[user_id][room_cnt] += float(weight)
            resblock_seg = ':'.join([resblock_id, resblock_name, room_cnt])
            if resblock_seg in resblock_price:
                resblock_price_pref[user_id][room_cnt] += float(weight) * resblock_price[resblock_seg]
        resblock_price_pref[user_id] = {key:value/room_cnt_pref[user_id][key] for key, value in resblock_price_pref[user_id].iteritems()}
        weight_sum = sum(room_cnt_pref[user_id].itervalues())
        room_cnt_pref[user_id] = {key:value/weight_sum for key, value in room_cnt_pref[user_id].iteritems()}

    for line in input_stream:
        vec = line.strip().split('\t')
        if len(vec) < 2:
            continue
        user_id = vec[0]
        recommendations = vec[1]
        recommendation_result = defaultdict(float)
        for recommendation in recommendations.split(','):
            resblock_id, resblock_name, room, weight = recommendation.split(':')
            if room.find('#') != -1:
                room_cnt = room[0:room.find('#')]
            else:
                room_cnt = room
            resblock_seg = ':'.join([resblock_id, resblock_name, room_cnt])
            if room_cnt in room_cnt_pref[user_id] and \
                room_cnt_pref[user_id][room_cnt] > 0.2 and \
                (resblock_seg not in resblock_price or room_cnt not in resblock_price_pref[user_id] or \
                resblock_price_pref[user_id][room_cnt] * 0.7 <= resblock_price[resblock_seg] <= resblock_price_pref[user_id][room_cnt] * 1.3):
                recommendation_result[resblock_seg] += float(weight)
        recommendation_result = sorted(recommendation_result.iteritems(), key=lambda x: x[1], reverse=True)
        output_str = '{user_id}\t{recommendation_str}'.format(
            user_id=user_id,
            recommendation_str=','.join([':'.join([key, str(value)]) for key, value in recommendation_result]))
        print output_str

if __name__ == '__main__':
    RESBLOCK_BEDROOM_PRICE = sys.argv[1]
    USER_VECTOR_CLEAN = sys.argv[2]
    run(sys.stdin, RESBLOCK_BEDROOM_PRICE, USER_VECTOR_CLEAN)
