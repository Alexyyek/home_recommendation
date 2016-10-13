#coding=utf-8
#!/bin/python

import sys

def run():

    showing_dict = dict()
    user_set = set()
    current_phone = ""
    phone = ""
    for line in open('user_preference','r'):
        phone, details = line.strip().split('\t', 1)
        resblock_id, resblock_name, room_cnt, build_area, info = details.split('\t', 4)
        value = '{resblock_id}\t{resblock_name}\t{room_cnt}\t{build_area}'.format(
                                   resblock_id = resblock_id,
                                   resblock_name = resblock_name,
                                   room_cnt = room_cnt,
                                   build_area = build_area)
        if current_phone == phone:
            user_set.add(value)
        else:
            if current_phone:
                showing_dict[phone] = user_set
            current_phone = phone
            user_set.clear()
            user_set.add(value)
    if current_phone == phone:
        showing_dict[phone] = user_set

    # filter resblock user has record
    for line in sys.stdin:
        words = line.strip().split('\t')
        if len(words) < 2 : continue
        phone, resblock_lst = line.strip().split('\t', 1)
        resblock_lst = resblock_lst.split('\t')
        for resblock in resblock_lst:
            resblock_id, resblock_name, room_cnt, build_area, score = resblock.strip().split(':')
            resblock_key = '{resblock_id}\t{resblock_name}\t{room_cnt}\t{build_area}'.format(
                                       resblock_id = resblock_id,
                                       resblock_name = resblock_name,
                                       room_cnt = room_cnt,
                                       build_area = build_area)

            if showing_dict.has_key(phone):
                details_set = showing_dict[phone]
                if resblock_key not in details_set:
                    print '{phone}\t{resblock_key}\t{score}'.format(
                            phone = phone,
                            resblock_key = resblock_key,
                            score = score)
                else:
                    continue

if __name__ == "__main__":
    run()
