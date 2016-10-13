#coding=utf-8
#!/bin/python

import sys
import math
import numpy
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

def read_input(param_dict, seperator='\t'):

    # load resblock price
    resblock_price_dict = dict()
    for line in open('resblock_price','r'):
        line = line.strip()
        words = line.split(seperator)
        if len(words) != 12 : continue
        city_code, city_name, district_code, district_name, bizcircle_code, \
        bizcircle_name, resblock_id, resblock_name, stat_date, room_cnt, \
        resblock_volume, resblock_trans_price = line.split(seperator)
        resblock_trans_price = float(resblock_trans_price)
        if room_cnt == '-1':
            resblock_price_dict[resblock_id] = resblock_trans_price
        elif room_cnt in ('1', '2', '3'):
            key = '{resblock_id}\t{room_cnt}'.format(
                    resblock_id = resblock_id,
                    room_cnt = room_cnt)
            resblock_price_dict[key] = resblock_trans_price


    # load user records
    for line in sys.stdin:

        resblock_room_dict = dict()
        resblock_time_dict = dict()
        resblock_cnt = 0

        line = line.strip()
        phone, resblock_lst = line.split(seperator, 1)
        resblock_lst = resblock_lst.split(seperator)
        for resblock in resblock_lst:
            resblock_id, resblock_name, room_cnt, build_area, score, timestamp = resblock.split(':')
            resblock_val = '{resblock_id}\t{resblock_name}\t{score}'.format(
                             resblock_id = resblock_id,
                             resblock_name = resblock_name,
                             score = score)
            if not resblock_room_dict.has_key(room_cnt):
                resblock_room_dict[room_cnt] = []
                resblock_time_dict[room_cnt] = False
            resblock_room_dict[room_cnt].append(resblock_val)
            resblock_time_dict[room_cnt] |= isRecent(param_dict, timestamp)
            resblock_cnt += 1

        #filter resblock record that room_cnt scale lower than threshold
        for room_cnt, resblock_lst in resblock_room_dict.iteritems():
            if not resblock_time_dict[room_cnt] and \
                len(resblock_lst) < (resblock_cnt * param_dict['ROOM_THRESHOLD']):
                continue
            else:
                resblock_margin = get_price_interval(room_cnt, resblock_lst, resblock_price_dict, param_dict)
                if resblock_margin:
                    print '{phone}\t{room_cnt}\t{resblock_margin}'.format(
                            phone = phone,
                            room_cnt = room_cnt,
                            resblock_margin = resblock_margin)


def isRecent(param_dict, timestamp):

    today = datetime.datetime.now()
    timestamp = datetime.datetime.strptime(timestamp, '%Y%m%d')
    if (today - timestamp).days <= param_dict['RECENT_DAYS']:
        return True
    else:
        return False

def get_one_record_interval(resblock_price, param_dict):

    one_record_margin = param_dict['ONE_RECORD_MARGIN']
    left_margin = resblock_price * (1 - one_record_margin)
    right_margin = resblock_price * (1 + one_record_margin)

    return '{left_margin}\t{right_margin}'.format(
             left_margin = left_margin,
             right_margin = right_margin)


#confidence interval
def get_confidence_interval(ratio, resblock_mean_lst):

    # cal mean & var
    length = len(resblock_mean_lst)
    array_alpha = numpy.array(resblock_mean_lst)
    sum_alpha = array_alpha.sum()
    array_beta = array_alpha * array_alpha
    sum_beta = array_beta.sum()
    mean = sum_alpha / length
    var = math.sqrt(sum_beta / length - mean ** 2)

    left_margin = mean - ratio * var
    right_margin = mean + ratio * var
    return '{left_margin}\t{right_margin}'.format(
             left_margin = left_margin,
             right_margin = right_margin)


def get_price_interval(room_cnt, resblock_lst, resblock_price_dict, param_dict):

    left_margin = 0
    right_margin = 0
    resblock_mean_lst = []
    threshold_ninty = param_dict['THRESHOLD_NINTY']

    for resblock in resblock_lst:
        resblock_id, resblock_name, score = resblock.split('\t')
        key = '{resblock_id}\t{room_cnt}'.format(
                resblock_id = resblock_id,
                room_cnt= room_cnt)
        if key in resblock_price_dict.keys():
            price = resblock_price_dict[key]
        elif resblock_id in resblock_price_dict.keys():
            price = resblock_price_dict[resblock_id]
        else:
            continue

        i = 0
        score = float(score)
        while(i < score):
            resblock_mean_lst.append(price)
            i += 1

    if len(resblock_mean_lst) == 0:
        return False
    elif len(set(resblock_mean_lst)) == 1:
        return get_one_record_interval(resblock_mean_lst[0], param_dict)
    else:
        return get_confidence_interval(threshold_ninty, resblock_mean_lst)


if __name__ == "__main__":
    ROOM_THRESHOLD = float(sys.argv[1])
    RECENT_DAYS = int(sys.argv[2])
    ONE_RECORD_MARGIN = float(sys.argv[3])
    THRESHOLD_NINTY = float(sys.argv[4])
    param_dict = dict()
    param_dict["ROOM_THRESHOLD"] = ROOM_THRESHOLD
    param_dict["RECENT_DAYS"] = RECENT_DAYS
    param_dict["ONE_RECORD_MARGIN"] = ONE_RECORD_MARGIN
    param_dict["THRESHOLD_NINTY"] = THRESHOLD_NINTY
    read_input(param_dict)
