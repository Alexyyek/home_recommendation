#coding=utf-8
#!/bin/python

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def read_input(seperator='\t'):

    # load user preference details

    for line in sys.stdin:
        line = line.strip()
        phone, details = line.split(seperator, 1)
        resblock_details = details.split(seperator)
        for resblock_alpha in resblock_details:
            resblock_id_alpha, resblock_name_alpha, room_cnt_alpha, build_area_alpha, score_alpha = resblock_alpha.split(':')
            resblock_alpha = '{resblock_id_alpha}:{resblock_name_alpha}:{room_cnt_alpha}:{build_area_alpha}'.format(
                               resblock_id_alpha = resblock_id_alpha,
                               resblock_name_alpha = resblock_name_alpha,
                               room_cnt_alpha = room_cnt_alpha,
                               build_area_alpha = build_area_alpha)
            for resblock_beta in resblock_details:
                resblock_id_beta, resblock_name_beta, room_cnt_beta, build_area_beta, score_beta = resblock_beta.split(':')
                resblock_beta = '{resblock_id_beta}:{resblock_name_beta}:{room_cnt_beta}:{build_area_beta}'.format(
                                  resblock_id_beta = resblock_id_beta,
                                  resblock_name_beta = resblock_name_beta,
                                   room_cnt_beta = room_cnt_beta,
                                   build_area_beta = build_area_beta)
                if resblock_id_alpha != resblock_id_beta:
                    weight = float(score_alpha) * float(score_beta)
                    print '{resblock_alpha}\t{resblock_beta}\t{weight}'.format(
                            resblock_alpha = resblock_alpha,
                            resblock_beta = resblock_beta,
                            weight = weight)

if __name__ == "__main__":
    read_input()
