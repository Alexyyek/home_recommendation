#coding=utf-8
#!/bin/python

import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

def read_input(seperator='\t'):

    #load spider data
    spider_set = set()
    for line in open('spider','r'):
        line = line.strip()
        spider_set.add(line)

    # load user preference details

    for line in sys.stdin:
        line = line.strip()
        phone, resblock_id, resblock_name, room_cnt, build_area, build_year, score, timestamp = line.split(seperator)
        if phone in spider_set:
            continue
        else:
            print '{phone}\t{resblock_id}\t{resblock_name}\t{room_cnt}\t{build_area}\t{build_year}\t{score}\t{timestamp}'.format(
                    phone = phone,
                    resblock_id = resblock_id,
                    resblock_name = resblock_name,
                    room_cnt = room_cnt,
                    build_area = build_area,
                    build_year = build_year,
                    score = score,
                    timestamp = timestamp)

if __name__ == "__main__":
    read_input()
