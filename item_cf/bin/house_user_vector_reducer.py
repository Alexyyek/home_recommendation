#coding=utf-8
#!/bin/python

import sys
import math

def house_user_vector(separator='\t'):

    alpha = 0.0063
    current_resblock_info = ""
    resblock_info = ""
    user_dict = dict()

    for line in sys.stdin:
        line = line.strip()
        resblock_id, resblock_name, room_cnt, build_area, build_year, phone, score = line.split(separator)
        resblock_info = '{resblock_id}:{resblock_name}:{room_cnt}:{build_area}'.format(
                          resblock_id = resblock_id,
                          resblock_name = resblock_name,
                          room_cnt = room_cnt,
                          build_area = build_area)
        #parser the input we got from mapper
        if current_resblock_info == resblock_info:
            if not user_dict.has_key(current_resblock_info):
                user_dict[phone] = score
            else:
                continue
        else:
            if current_resblock_info:
                outpt_set = set()
                for key, val in user_dict.iteritems():
                    outpt_set.add('{key}:{val}'.format(
                                    key = key,
                                    val = val))
                print '{current_resblock_info}\t{customers}'.format(current_resblock_info=current_resblock_info, customers='\t'.join(outpt_set))
            current_resblock_info = resblock_info
            user_dict.clear()
            user_dict[phone] = score

if __name__ == "__main__":
    house_user_vector()
