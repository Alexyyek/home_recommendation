#coding=utf-8
#!/bin/python

import sys
import math
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

def read_input(seperator='\t'):

    #load spider data
    spider_set = set()
    for line in open('spider','r'):
        line = line.strip()
        spider_set.add(line)

    current_phone = ""
    phone = ""
    resblock_set = set()

    for line in sys.stdin:
        line = line.strip()
        phone, resblock_id, resblock_name, room_cnt, build_area, build_year, score, timestamp = line.split(seperator)
        if phone in spider_set:
            continue
        resblock_info = '{resblock_id}:{resblock_name}:{room_cnt}:{build_area}:{score}:{timestamp}'.format(
                          resblock_id = resblock_id,
                          resblock_name = resblock_name,
                          room_cnt = room_cnt,
                          build_area = build_area,
                          score = score,
                          timestamp = timestamp)
        if current_phone == phone:
            resblock_set.add(resblock_info)
        else:
            if current_phone:
                print '{phone}\t{resblocks}'.format(phone=current_phone,resblocks='\t'.join(resblock_set))
            current_phone = phone
            resblock_set.clear()
            resblock_set.add(resblock_info)

if __name__ == "__main__":
    read_input()
