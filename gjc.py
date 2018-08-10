#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 10
REDIS_PASSWORD = "xinnet123"
import redis

print('\u91cd\u5e86\u5c0f\u7231\u79d1\u6280\u6709\u9650\u516c\u53f8')


class TxtRedis(object):
    '''读取txt域名文件并且储存到redis list里'''

    def __init__(self):
        try:
            self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)
        except Exception as e:
            print(e)

    # def read_whois(self):
    #     for path,dirs,files in os.walk("whois"):
    #         return files
    def get_txt_up_redis(self):
        flag = True
        num = 0
        # f = codecs.open("gjc.txt", "rb",encoding="utf-8")
        #
        #
        # for x in f:
        #     print(x)
        # result_num = self.r.rpush("cms_tags", x)
        # print(result_num)
        with open('gjc.txt', mode='r', encoding='utf-8') as f:
            for lines in f:
                x = lines.strip()
                result_num = self.r.rpush("cms_tags", x)
                print(result_num)





                # cc = TxtRedis()
                # cc.get_txt_up_redis()
