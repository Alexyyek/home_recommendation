#coding=utf-8
#!/bin/python

import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

def read_input(param_dict, seperator='\t'):

    # load house basic info
    # house_pkid, resblock_id, resblock_name, room_cnt, parlor_cnt, build_area, build_year

    house_dict = dict()
    for line in open('dim_merge_house_day', 'r'):
        line = line.strip()
        house_pkid, resblock_id, details = line.split(seperator, 2)
        house_pkid, details = line.split(seperator, 1)
        house_pkid = house_pkid[4:]
        if resblock_id == 'NULL': continue
        if not house_dict.has_key(house_pkid):
            house_dict[house_pkid] = details
        else:
            continue

    # load online & offline details
    # with time dacay factor been considered
    # since 2014

    for line in sys.stdin:
        try:
            line = line.strip()
            if len(line.split('\t')) == 4:
                user_id, timestamp, house_pkid, type = line.split(seperator)
            elif len(line.split('\t')) == 5:
                user_id, timestamp, house_pkid, type, source = line.split(seperator)
            user_id, timestamp, house_pkid, type = line.split(seperator)
            score = 0

            # weight different user behavior
            if type == 'pc' or type == 'mobile':
                score = param_dict["online_browse_weight"]
                type = 'online'
            elif type == 'ershoufang_fav':
                score = param_dict["online_fav_weight"]
                type = 'online'
            elif type == 'touring':
                score = param_dict["offline_touring_weight"]
                type = 'offline'
            elif type == 'contract':
                score = param_dict["offline_contract_weight"]
                type = 'offline'
            else:
                continue

            # transform house code to link
            house_pkid = house_pkid[4:]

            if house_dict.has_key(house_pkid):
                resblock_id, resblock_name, room_cnt, parlor_cnt, build_area, build_year, details = house_dict[house_pkid].split(seperator, 6)
                outpt_str = '{user_id}\t{resblock_id}\t{resblock_name}\t{room_cnt}\t{build_area}\t{build_year}\t{score}\t{timestamp}\t{type}'.format(
                              user_id = user_id,
                              resblock_id = resblock_id,
                              resblock_name = resblock_name,
                              room_cnt = room_cnt,
                              build_area = build_area,
                              build_year = build_year,
                              score = score,
                              timestamp = timestamp,
                              type = type)
                print outpt_str
        except Exception, e:
            continue

if __name__ == "__main__":
    online_browse_weight = int(sys.argv[1])
    online_fav_weight = int(sys.argv[2])
    offline_touring_weight = int(sys.argv[3])
    offline_contract_weight = int(sys.argv[4])

    param_dict = dict()
    param_dict["online_browse_weight"] = online_browse_weight
    param_dict["online_fav_weight"] = online_fav_weight
    param_dict["offline_touring_weight"] = offline_touring_weight
    param_dict["offline_contract_weight"] = offline_contract_weight

    read_input(param_dict)
