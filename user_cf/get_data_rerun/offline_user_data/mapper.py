#!/bin/python
#coding=utf-8

import sys
import json
from collections import defaultdict

reload(sys)
sys.setdefaultencoding('utf-8')

def run(input, BEGIN_DATE, CITY_ID):
    for line in input:
        vec = line.strip().split('\t')
        phone = vec[0].strip()
        user_detail = json.loads(vec[1])

        if 'tourings' in user_detail:
            for touring in user_detail['tourings']:
                if 'biz_type' in touring and touring['biz_type'] == 200200000001 \
                    and 'end_time' in touring and touring['end_time'] >= BEGIN_DATE \
                    and 'houses' in touring:
                    for house in touring['houses']:
                        if 'city_id' in house and house['city_id'] == CITY_ID \
                            and 'house_id' in house:
                            touring_output_str = '{phone}\t{touring_date}\t{house_pkid}\ttouring'.format(
                                                    phone = phone,
                                                    touring_date = touring['end_time'][0:8],
                                                    house_pkid = house['house_id'])
                            print touring_output_str

        if 'contracts' in user_detail:
            for house in user_detail['contracts']:
                if 'biz_type' in house and house['biz_type'] == 200200000001 \
                    and 'city_id' in house and house['city_id'] == CITY_ID \
                    and 'deal_time' in house and house['deal_time'] >= BEGIN_DATE \
                    and 'house_pkid' in house:
                    contract_output_str = '{phone}\t{deal_time}\t{house_pkid}\tcontract'.format(
                                            phone = phone,
                                            deal_time= house['deal_time'][0:8],
                                            house_pkid = house['house_pkid'])
                    print contract_output_str

if __name__ == '__main__':
    BEGIN_DATE = sys.argv[1]
    CITY_ID = int(sys.argv[2])
    run(sys.stdin, BEGIN_DATE, CITY_ID)
