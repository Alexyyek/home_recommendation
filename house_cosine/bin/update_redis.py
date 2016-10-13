#!/bin/python
#coding=utf-8

import os
import sys
import time
import redis
import logging
from collections import defaultdict
sys.path.append("../conf")
import conf

reload(sys)
sys.setdefaultencoding('utf-8')

class UpdateRedisCreator:

    def __init__(self, config):
        self.date_str = time.strftime('%Y%m%d', time.localtime(time.time()))
        # data
        self.resb_dict = defaultdict(list)
        # config
        self.cnt = config['cnt']
        self.title= config['title']
        self.expire = config['expire']
        self.db_idc = config['db_idc']
        self.db_aws = config['db_aws']
        self.db_test = config['db_test']
        self.host_idc = config['host_idc']
        self.host_aws = config['host_aws']
        self.host_test = config['host_test']
        self.port_idc = config['port_idc']
        self.port_aws = config['port_aws']
        self.port_test = config['port_test']
        self.matrix_path = config['matrix_path']
        # log
        log_dir = config['log_dir']
        logging.basicConfig(level = logging.INFO, \
        datefmf = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',\
        filename = log_dir + "/%s.updateRedis.log" %self.date_str, \
        filemode = 'w')
        self._pre_process()

    def _pre_process(self):
        logging.info("Start Data Pre Processing")
        self._check_data(self.matrix_path)
        self._get_features()
        logging.info("Feature Size: %s", str(len(self.resb_dict)))
        logging.info("Feature Loading is Done")

    def _check_data(self, fname):
        if not os.path.isfile(fname):
            logging.error("File Not Found : %s" %(os.path.abspath(fname)))
            exit(-1)
        else:
            logging.info("File %s been found" %(os.path.abspath(fname)))

    def _get_features(self):
        with open(self.matrix_path, mode='r') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip().split('\t')
            self.resb_dict[line[0]].append([line[1], line[2]])
        return

    def run_sgl(self):

        #connect redis
        rds_idc = redis.Redis(host=self.host_idc, port=self.port_idc, db=self.db_idc)
        rds_aws = redis.Redis(host=self.host_aws, port=self.port_aws, db=self.db_aws)

        for line in sys.stdin:
            line = line.strip()
            resblock_alpha, resblock_beta, score = line.split('\t')
            score = float(score)
            rds_idc.zadd(resblock_alpha, resblock_beta, score)
            rds_aws.zadd(resblock_alpha, resblock_beta, score)
            rds_idc.expire(resblock_alpha,10)
            rds_aws.expire(resblock_alpha,10)

    def run_mul(self, host, port, db, expire):

        cnt = 0
        count = self.cnt

        #connect redis
        rds = redis.Redis(host=host, port=port, db=db)
        pipe = rds.pipeline()

        for resblock, sims in self.resb_dict.iteritems():
            resblock_alpha = self.title + resblock
            if pipe.exists(resblock):
                pipe.delete(resblock)
            for sim in sims:
                resblock_beta = sim[0]
                score = float(sim[1])
                pipe.zadd(resblock_alpha, resblock_beta, score)
                pipe.expire(resblock_alpha, self.expire)
                if cnt == count:
                    pipe.execute()
                    logging.info("%s has been updated" %cnt)
                    cnt = 0
                else:
                    cnt += 1
        pipe.execute()

    def run(self):
        self.run_mul(self.host_idc, self.port_idc, self.db_idc, self.expire)
        logging.info("Update idc is Done")
        self.run_mul(self.host_aws, self.port_aws, self.db_aws, self.expire)
        logging.info("Update aws is Done")


if __name__ == "__main__":
    config = {}
    config['cnt'] = conf.CNT
    config['title'] = conf.TITLE
    config['expire'] = conf.EXPIRE
    config['db_idc'] = conf.DB_IDC
    config['db_aws'] = conf.DB_AWS
    config['db_test'] = conf.DB_TEST
    config['host_idc'] = conf.HOST_IDC
    config['host_aws'] = conf.HOST_AWS
    config['host_test'] = conf.HOST_TEST
    config['port_idc'] = conf.PORT_IDC
    config['port_aws'] = conf.PORT_AWS
    config['port_test'] = conf.PORT_TEST
    config['log_dir'] = conf.LOG_DIR
    config['matrix_path'] = conf.MATRIX_PATH
    start = time.time()
    creator = UpdateRedisCreator(config)
    creator.run()
    end = time.time()
    logging.info('run time cost %d seconds' %(end-start))
