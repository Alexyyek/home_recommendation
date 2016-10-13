#!/bin/python
#coding=utf-8
from __future__ import print_function

import sys
import json
import re

reload(sys)
sys.setdefaultencoding('utf-8')

def run(input):
    pc_pattern = re.compile('^https?://[a-z]{1,5}\.lianjia\.com/((?:ershoufang)|(?:chengjiao))/([A-Z0-9]{4,12})\.html')
    mweb_pattern = re.compile('^https?://m\.lianjia\.com/[a-z]{1,5}/((?:ershoufang)|(?:chengjiao))/([A-Z0-9]{4,12})\.html')
    mobile_pattern = re.compile('^http://app\.api\.lianjia\.com/house/((?:ershoufang)|(?:chengjiao))/detailV[23]\?.*house_code=([A-Z0-9]{4,12})')
    patterns = [('pc', pc_pattern), ('mweb', mweb_pattern), ('mobile', mobile_pattern)]

    for line in input:
        vec = line.strip().split('\001')
        if len(vec) < 25:
            continue
        timestamp = vec[0][0:19].replace('T', ' ')
        uuid = vec[9]
        ucid = vec[10]
        request_url = vec[15]

        if ucid == '' or ucid == '-':
            continue

        for source_type, pattern in patterns:
            match = pattern.search(request_url)
            if match:
                evt_type = match.groups()[0]
                house_pkid = match.groups()[1]
                print(ucid, timestamp, house_pkid, source_type, evt_type, sep='\t')
                break

if __name__ == '__main__':
    run(sys.stdin)
