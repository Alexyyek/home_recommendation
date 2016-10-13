#coding=utf-8
#!/bin/python

import sys
import math
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

def read_input(alpha, ratio, seperator='\t'):

    # load user preference details

    current_phone = ""
    phone = ""
    resblock_set = set()

    for line in sys.stdin:
        line = line.strip()
        phone, details = line.split(seperator, 1)
        phone, resblock_id, resblock_name, room_cnt, build_area, build_year, score, timestamp = line.split(seperator)
        if current_phone == phone:
            resblock_set.add(details)
        else:
            if current_phone:
                sum = 0
                for resblock in resblock_set:
                    resblock_id, resblock_name, room_cnt, build_area, build_year, score, timestamp = resblock.split(seperator)
                    sum += float(score)
                threshold = sum * ratio
                for resblock in resblock_set:
                    resblock_id, resblock_name, room_cnt, build_area, build_year, score, timestamp = resblock.split(seperator)
                    if float(score) > threshold:
                        #time decay
                        #score = time_decay(alpha, timestamp) * float(score)
                        print '{current_phone}\t{resblock_id}\t{resblock_name}\t{room_cnt}\t{build_area}\t{build_year}\t{score}\t{timestamp}'.format(
                                current_phone = current_phone,
                                resblock_id = resblock_id,
                                resblock_name = resblock_name,
                                room_cnt = room_cnt,
                                build_area = build_area,
                                build_year = build_year,
                                score = score,
                                timestamp = timestamp)
            current_phone = phone
            resblock_set.clear()
            resblock_set.add(details)

def time_decay(alpha, timestamp):
    now= datetime.datetime.now()
    time_distance = (now - timestamp).days
    res = math.exp(-alpha * time_distance)
    return res

if __name__ == "__main__":
    alpha = float(sys.argv[1])
    ratio = float(sys.argv[2])
    read_input(alpha, ratio)
