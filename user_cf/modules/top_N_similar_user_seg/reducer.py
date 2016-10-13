#!/bin/python
#coding=utf-8
'''
    输入用户相似性矩阵，输出每一个用户的top N最相似用户。
    INPUT:  userid_x \t  userid_y \t 相似性分数
            已经按照userid_x和userid_y排好序
    OUTPUT: userid_x \t userid_y:相似性分数,userid_z:相似性分数...
    AUTHOR: songxin@lianjia.com
    DATE:   20160711
'''

import sys
import heapq

class SimilarUser(object):
    '''
        相似用户类
        Attribute:
            userid: 用户id
            similar_score: 相似分数
    '''
    def __init__(self, userid, similar_score):
        self.userid = userid
        self.similar_score = similar_score

    def __cmp__(self, other):
        return cmp(self.similar_score, other.similar_score)

    def __str__(self):
        return ':'.join([self.userid, str(self.similar_score)])

def run(input_stream, similar_user_number):
    '''
        计算用户top N最相似用户
    '''
    last_userid = ""
    similar_user_list = []

    for line in input_stream:
        vec = line.strip().split('\t')
        userid = vec[0]

        similar_user_id = vec[1]
        similar_score = float(vec[2])
        similar_user = SimilarUser(similar_user_id, similar_score)

        if last_userid == "":
            last_userid = userid
            heapq.heappush(similar_user_list, similar_user)
        elif last_userid == userid:
            if len(similar_user_list) < similar_user_number:
                heapq.heappush(similar_user_list, similar_user)
            else:
                farthest_user = similar_user_list[0]
                if farthest_user < similar_user:
                    heapq.heappushpop(similar_user_list, similar_user)
        else:
            similar_user_list.sort(reverse=True)
            for _similar_user in similar_user_list:
                output_str = '{user_x}\t{user_y}\t{score}'.format(
                    user_x=last_userid,
                    user_y=_similar_user.userid,
                    score=_similar_user.similar_score)
                print output_str

            last_userid = userid
            similar_user_list = []
            heapq.heappush(similar_user_list, similar_user)

    similar_user_list.sort(reverse=True)
    for _similar_user in similar_user_list:
        output_str = '{user_x}\t{user_y}\t{score}'.format(
            user_x=last_userid,
            user_y=_similar_user.userid,
            score=_similar_user.similar_score)
        print output_str

if __name__ == '__main__':
    SIMILAR_USER_NUMBER = int(sys.argv[1])
    run(sys.stdin, SIMILAR_USER_NUMBER)
