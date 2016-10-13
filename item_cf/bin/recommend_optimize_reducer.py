#coding=utf-8
#!/bin/python

import sys
import math
import numpy
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

def read_input(seperator='\t'):

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

    # load resblock price interval
    user_figure_dict = dict()

    for line in open('user_figure','r'):
        line = line.strip()
        phone, room_cnt, left_margin, right_margin = line.split(seperator)
        key = '{phone}\t{room_cnt}'.format(
                phone = phone,
                room_cnt = room_cnt)
        user_figure_dict[key] = '{left_margin}\t{right_margin}'.format(
                                  left_margin = left_margin,
                                  right_margin = right_margin)

    # filter recommend resblock that price not fit
    for line in sys.stdin:
        line = line.strip()
        phone, resblock_id, resblock_name, room_cnt, build_area, score = line.split('\t')
        resblock_price = get_resblock_price(resblock_id, room_cnt, resblock_price_dict)
        key = '{phone}\t{room_cnt}'.format(
                phone = phone,
                room_cnt = room_cnt)

        if key in user_figure_dict:
            left_margin, right_margin = user_figure_dict[key].split(seperator)
            left_margin = float(left_margin)
            right_margin = float(right_margin)
            if resblock_price > left_margin and resblock_price < right_margin:
                print line
        else:
            print line


def get_resblock_price(resblock_id, room_cnt, resblock_price_dict):

    key = '{resblock_id}\t{room_cnt}'.format(
            resblock_id = resblock_id,
            room_cnt= room_cnt)
    if key in resblock_price_dict:
        return resblock_price_dict[key]
    elif resblock_id in resblock_price_dict:
        return resblock_price_dict[resblock_id]
    else:
        return None

if __name__ == "__main__":
    read_input()
