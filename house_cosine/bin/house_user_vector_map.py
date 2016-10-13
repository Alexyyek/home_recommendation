#coding=utf-8
#!/bin/python

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def read_input(seperator='\t'):

    # load user preference details

    for line in sys.stdin:
        line = line.strip()
        phone, resblock_id, resblock_name, room_cnt, build_area, build_year, score, timestamp = line.split(seperator)
        outpt_str = '{resblock_id}\t{resblock_name}\t{room_cnt}\t{build_area}\t{build_year}\t{phone}\t{score}'.format(
                      resblock_id = resblock_id,
                      resblock_name = resblock_name,
                      room_cnt = room_cnt,
                      build_area = build_area,
                      build_year = build_year,
                      phone = phone,
                      score = score)
        print outpt_str

if __name__ == "__main__":
    read_input()
