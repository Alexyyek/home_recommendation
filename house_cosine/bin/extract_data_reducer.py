#coding=utf-8
#!/bin/python

import sys
import math
import datetime

def extract_data_reducer(param_dict, separator='\t'):
    alpha = param_dict["alpha"]

    current_ucid = ""
    ucid = ""
    resblock_type_dict = dict()
    current_detail_dict = dict()

    for line in sys.stdin:
        line = line.strip()
        ucid, details = line.split(separator, 1)
        resblock_id, resblock_name, room_cnt, build_area, build_year, score, timestamp, type = details.split(separator)
        score = float(score)
        timestamp = time_format(timestamp)
        build_area = float(build_area)
        build_area_type = room_cnt_interval(room_cnt, build_area, param_dict)
        if build_area_type == "null" : continue
        resblock_key = '{resblock_id}\t{room_cnt}\t{build_area_type}\t{resblock_name}\t{build_year}'.format(
                               resblock_id = resblock_id,
                               room_cnt = room_cnt,
                               build_area_type = build_area_type,
                               resblock_name = resblock_name,
                               build_year = build_year)
        #parser the input we got from mapper
        if current_ucid == ucid:
            if resblock_key not in current_detail_dict:
                current_detail_dict[resblock_key] = timestamp
                resblock_type_dict[resblock_key] = dict()
            if current_detail_dict[resblock_key] < timestamp:
                current_detail_dict[resblock_key] = timestamp
            if type not in resblock_type_dict[resblock_key]:
                resblock_type_dict[resblock_key][type] = score
            else:
                resblock_type_dict[resblock_key][type] += score
        else:
            if current_ucid:
                print_str(param_dict, current_ucid, current_detail_dict, resblock_type_dict)
            current_ucid = ucid
            resblock_type_dict.clear()
            current_detail_dict.clear()
            current_detail_dict[resblock_key] = timestamp
            resblock_type_dict[resblock_key] = dict()
            resblock_type_dict[resblock_key][type] = score
    if current_ucid == ucid:
        print_str(param_dict, current_ucid, current_detail_dict, resblock_type_dict)


def print_str(param_dict, current_ucid, current_detail_dict, resblock_type_dict):
    for resblock_key, timestamp in current_detail_dict.iteritems():
        type_dict = resblock_type_dict[resblock_key]
        score = get_score(type_dict, param_dict)
        #score = round(time_decay(alpha, timestamp) * float(score), 3)
        resblock_id, room_cnt, build_area_type, resblock_name, build_year = resblock_key.strip().split('\t')
        output_str = '{resblock_id}\t{resblock_name}\t{room_cnt}\t{build_area_type}\t{build_year}\t{score}\t{timestamp}'.format(
                      resblock_id = resblock_id,
                      resblock_name = resblock_name,
                      room_cnt = room_cnt,
                      build_area_type = build_area_type,
                      build_year = build_year,
                      score = score,
                      timestamp = timestamp)
        print '{current_ucid}\t{output_str}'.format(
                current_ucid = current_ucid,
                output_str = output_str)


def time_decay(alpha, timestamp):
    now = datetime.datetime.now()
    time_distance = (now - timestamp).days
    res = math.exp(-alpha * time_distance)
    return res


def time_format(timestamp):
    if len(timestamp) > 8:
        timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    else:
        timestamp = datetime.datetime.strptime(timestamp, "%Y%m%d")
    return timestamp


def get_score(type_dict, param_dict):

    ##线上权重总和不能高于线下权重总和的阈值倍数
    ##同时拥有线上与线下行为，权重翻倍

    score = 0
    online_score = 0
    offline_score = 0

    online_code = param_dict["online_code"]
    offline_code = param_dict["offline_code"]
    online_offline_threshold = param_dict["online_offline_threshold"]

    if type_dict.has_key(online_code):
        online_score = float(type_dict[online_code])
    if type_dict.has_key(offline_code):
        offline_score = float(type_dict[offline_code])
    if offline_score > 0 and (online_score / offline_score) > online_offline_threshold:
        online_score = offline_score * online_offline_threshold
    if online_score > 0 and offline_score > 0:
        score = (online_score + offline_score) * 2
    else:
        score = online_score + offline_score
    return score


def room_cnt_interval(room_cnt, build_area, param_dict):
    interval = ""
    room_cnt = int(room_cnt)

    one_room_interval_dict = param_dict["one_room_interval"]
    two_room_interval_dict = param_dict["two_room_interval"]
    three_room_interval_dict = param_dict["three_room_interval"]

    if room_cnt == 1:
        if build_area >= one_room_interval_dict["lower"] and build_area <= one_room_interval_dict["mid"]:
            interval = "30-50"
        elif build_area > one_room_interval_dict["mid"] and build_area <= one_room_interval_dict["higher"]:
            interval = "50-80"
        else:
            interval = "null"
    elif room_cnt == 2:
        if build_area >= two_room_interval_dict["lower"] and build_area <= two_room_interval_dict["mid"]:
            interval = "50-80"
        elif build_area > two_room_interval_dict["mid"] and build_area <= two_room_interval_dict["higher"]:
            interval = "80-130"
        else:
            interval = "null"
    elif room_cnt == 3:
        if build_area >= three_room_interval_dict["lower"] and build_area <= three_room_interval_dict["mid-low"]:
            interval = "75-90"
        elif build_area > three_room_interval_dict["mid-low"] and build_area <= three_room_interval_dict["mid-high"]:
            interval = "90-140"
        elif build_area > three_room_interval_dict["mid-high"] and build_area <= three_room_interval_dict["higher"]:
            interval = "140-300"
        else:
            interval = "null"
    else:
        interval = "null"

    return interval


if __name__ == "__main__":
    alpha = float(sys.argv[1])
    online_code = sys.argv[2]
    offline_code = sys.argv[3]
    online_offline_threshold = float(sys.argv[4])
    one_room_interval = sys.argv[5].strip().split(',')
    two_room_interval = sys.argv[6].strip().split(',')
    three_room_interval = sys.argv[7].strip().split(',')

    one_room_interval_dict = dict()
    one_room_interval_dict["lower"] = float(one_room_interval[0])
    one_room_interval_dict["mid"] = float(one_room_interval[1])
    one_room_interval_dict["higher"] = float(one_room_interval[2])

    two_room_interval_dict = dict()
    two_room_interval_dict["lower"] = float(two_room_interval[0])
    two_room_interval_dict["mid"] = float(two_room_interval[1])
    two_room_interval_dict["higher"] = float(two_room_interval[2])

    three_room_interval_dict = dict()
    three_room_interval_dict["lower"] = float(three_room_interval[0])
    three_room_interval_dict["mid-low"] = float(three_room_interval[1])
    three_room_interval_dict["mid-high"] = float(three_room_interval[2])
    three_room_interval_dict["higher"] = float(three_room_interval[3])

    param_dict = dict()
    param_dict["alpha"] = alpha
    param_dict["online_code"] = online_code
    param_dict["offline_code"] = offline_code
    param_dict["online_offline_threshold"] = online_offline_threshold
    param_dict["one_room_interval"] = one_room_interval_dict
    param_dict["two_room_interval"] = two_room_interval_dict
    param_dict["three_room_interval"] = three_room_interval_dict

    extract_data_reducer(param_dict)
