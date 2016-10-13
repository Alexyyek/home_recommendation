#coding=utf-8

import sys
import copy

def matrixMultiplicationReducer(top_Num, separator='\t'):

    #read resblock cocurrence matrix from RAM

    resblock_cocurrent_matrix = dict()

    for line in open('house_cosine','r'):

        resblock_dict = dict()
        resblock_alpha, resblock_lst = line.strip().split(separator, 1)
        resblock_lst = resblock_lst.split(separator)

        for resblock in resblock_lst:
            resblock_id, resblock_name, room_cnt, build_area, similarity = resblock.split(':')
            key = '{resblock_id}:{resblock_name}:{room_cnt}:{build_area}'.format(
                    resblock_id = resblock_id,
                    resblock_name = resblock_name,
                    room_cnt = room_cnt,
                    build_area = build_area)
            resblock_dict[key] = similarity

        resblock_cocurrent_matrix[resblock_alpha] = copy.deepcopy(resblock_dict)

    # read user house vector
    for line in sys.stdin:

        phone_dict = dict()
        phone, resblock_lst = line.strip().split(separator, 1)
        resblock_lst = resblock_lst.split(separator)

        for resblock in resblock_lst:
            resblock_id, resblock_name, room_cnt, build_area, score = resblock.strip().split(':')
            key = '{resblock_id}:{resblock_name}:{room_cnt}:{build_area}'.format(
                    resblock_id = resblock_id,
                    resblock_name = resblock_name,
                    room_cnt = room_cnt,
                    build_area = build_area)
            phone_dict[key] = score

        resblock_rank_dict = dict()
        for resblock_key, resblock_val_dict in resblock_cocurrent_matrix.iteritems():
            r_keys = set(resblock_val_dict.keys())
            u_keys = set(phone_dict.keys())
            intersection = r_keys.intersection(u_keys)
            if len(intersection) >  0:
                weight = 0.0
                for idx in intersection:
                    weight += float(phone_dict[idx]) * float(resblock_val_dict[idx])
                resblock_rank_dict[resblock_key] = weight
        recommendation = sorted(resblock_rank_dict.iteritems(), key=lambda x: x[1], reverse=True)
        recommendation = [':'.join([key, str(value)]) for key, value in recommendation]
        output_str = '{phone}\t{recommendation}'.format( 
                       phone=phone,
                       recommendation='\t'.join(recommendation[0:top_Num]))
        print output_str

if __name__ == "__main__":
    top_Num = int(sys.argv[1])
    matrixMultiplicationReducer(top_Num)
