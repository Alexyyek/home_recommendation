#!/bin/python
#coding=utf-8

import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

def run(input):
    for line in input:
        vec = line.strip().split('\t')
        if len(vec) < 22:
            continue
        timestamp = vec[0]
        user_id = vec[4]
        detail_id = vec[21]

        channel_id = vec[15]
        if channel_id == '2':
            evt_type = 'ershoufang'
        elif channel_id == '13':
            evt_type = 'chengjiao'
        else:
            continue

        detail_id_type = vec[20]
        if user_id != '\N' and detail_id_type == '1':
            output_str = '{user_id}\t{timestamp}\t{house_pkid}\tpc\t{evt_type}'.format(
                          user_id = user_id,
                          timestamp = timestamp,
                          house_pkid = detail_id,
                          evt_type = evt_type)
            print output_str

if __name__ == '__main__':
    run(sys.stdin)
