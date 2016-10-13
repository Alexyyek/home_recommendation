#coding=utf-8
#!/bin/python

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def read_input(topN, seperator='\t'):

    # load house cosine details

    current_resblock = ""
    resblock_alpha = ""
    resblock_dict = dict()

    for line in sys.stdin:
        line = line.strip()
        resblock_alpha, resblock_beta, similarity = line.split(seperator)
        if current_resblock == resblock_alpha:
            resblock_dict[resblock_beta] = similarity
        else:
            if current_resblock:
                print get_resblock_top(topN, current_resblock, resblock_dict)
            current_resblock = resblock_alpha
            resblock_dict.clear()
            resblock_dict[resblock_beta] = similarity
    if current_resblock == resblock_alpha:
        print get_resblock_top(topN, resblock_alpha, resblock_dict)

def get_resblock_top(topN, current_resblock, resblock_dict):
    resblock_dict = sorted(resblock_dict.iteritems(), key=lambda x:x[1], reverse=True)
    resblock_dict = [':'.join([key, str(value)]) for key, value in resblock_dict]
    outpt_str = '{current_resblock}\t{resblock_dict}'.format(
                  current_resblock= current_resblock,
                  resblock_dict = '\t'.join(resblock_dict[0:topN]))
    return outpt_str

if __name__ == "__main__":
    topN = int(sys.argv[1])
    read_input(topN)
