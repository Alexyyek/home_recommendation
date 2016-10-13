#!/bin/python
#coding=utf-8

RUN_PATH = '/home/work/yangyekang/resblock/resblock_recommend/house_cosine/'
DAT_PATH = RUN_PATH + 'data/'

MATRIX_PATH = DAT_PATH + 'house_cosine'
LOG_DIR = RUN_PATH + 'logs'

TITLE = 'SimilarityMatrixV2:'

EXPIRE = 2592000
HOST_IDC = 'm11036.zeus.redis.ljnode.com'
HOST_AWS = 'm11036.ares.redis.ljnode.com'
HOST_TEST = '172.30.0.20'
PORT_IDC = 11036
PORT_AWS = 11036
PORT_TEST = 6379
DB_IDC = 0
DB_AWS = 0
DB_TEST = 2
CNT = 10000
