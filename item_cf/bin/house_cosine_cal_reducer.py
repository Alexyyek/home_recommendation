#coding=utf-8
#!/bin/python

import sys
import math

def house_cosine_cal(separator='\t'):

    resblock_denominator_dict = dict()
    for line in open('house_user_vector','r'):
        line = line.strip()
        resblock_info, details = line.split(separator, 1)
        user_details = details.split(separator)
        sum = 0.0
        for user in user_details:
            phone, score = user.split(':')
            sum += float(score) * float(score)
        sum = math.sqrt(sum)
        resblock_denominator_dict[resblock_info] = sum

    current_resblock_alpha = ""
    current_resblock_beta = ""
    resblock_alpha = ""
    resblock_beta = ""
    numerator_sum = 0.0

    #parser the input we got from mapper
    for line in sys.stdin:
        line = line.strip()
        resblock_alpha, resblock_beta, numerator = line.split(separator)
        if current_resblock_alpha == resblock_alpha and current_resblock_beta == resblock_beta:
            numerator_sum += float(numerator)
        else:
            if current_resblock_alpha!='' and current_resblock_beta!='':
                if resblock_denominator_dict.has_key(current_resblock_alpha) and resblock_denominator_dict.has_key(current_resblock_beta):
                    similarity = numerator_sum / (resblock_denominator_dict[current_resblock_alpha] * resblock_denominator_dict[current_resblock_beta])
                    if similarity > 0.001:
                        print '{current_resblock_alpha}\t{current_resblock_beta}\t{similarity}'.format(
                                current_resblock_alpha = current_resblock_alpha,
                                current_resblock_beta = current_resblock_beta,
                                similarity = similarity)
            current_resblock_alpha = resblock_alpha
            current_resblock_beta = resblock_beta
            numerator_sum = 0.0

if __name__ == "__main__":
    house_cosine_cal()
