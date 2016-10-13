#coding=utf-8
#!/bin/python

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def read_input(seperator='\t'):

    for line in sys.stdin:
        line = line.strip()
        resblock_alpha, resblock_beta, similarity = line.split(seperator)
        resblock_id_alpha, resblock_name_alpha, room_cnt_alpha, build_area_alpha = resblock_alpha.split(':')
        resblock_alpha = '{resblock_id_alpha}:{room_cnt_alpha}:{build_area_alpha}'.format(
                           resblock_id_alpha = resblock_id_alpha,
                           room_cnt_alpha = room_cnt_alpha,
                           build_area_alpha = build_area_alpha)
        resblock_id_beta, resblock_name_beta, room_cnt_beta, build_area_beta = resblock_beta.split(':')
        resblock_beta = '{resblock_id_beta}:{room_cnt_beta}:{build_area_beta}'.format(
                          resblock_id_beta = resblock_id_beta,
                          room_cnt_beta = room_cnt_beta,
                          build_area_beta = build_area_beta)
        print '{resblock_alpha}\t{resblock_beta}\t{similarity}'.format(
                resblock_alpha = resblock_alpha,
                resblock_beta = resblock_beta,
                similarity = similarity)

if __name__ == "__main__":
    read_input()
