#coding=utf-8
#!/bin/python

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def read_input(seperator='\t'):

    for line in sys.stdin:
        line = line.strip()
        resblock_alpha, resblock_beta, similarity = line.split(seperator)
        print '{resblock_alpha}\t{resblock_beta}\t{similarity}'.format(
                resblock_alpha = resblock_alpha,
                resblock_beta = resblock_beta,
                similarity = similarity)

if __name__ == "__main__":
    read_input()
