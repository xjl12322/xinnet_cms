#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"

import csv

import redis

from setings import *


class CsvRedis(object):
    '''读取csv文件并且储存到redis list里'''

    def __init__(self):
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)
        self.reader = csv.reader(open('domain_list.csv', 'r', encoding="utf-8"))
        self.whole = self.r.lrange(import_keyword_redis_listname, 0, -1)
        self.result_nums = 0

    def get_csv_up_redis(self):
        print("loading.................")
        for item in self.reader:
            item = "".join(item)
            if item not in self.whole:
                try:
                    result_num = self.r.rpush(import_keyword_redis_listname, item)
                    self.result_nums = result_num
                except Exception as e:
                    print(e)
                    print("插入{}失败".format())
            else:
                print("{}已存在列表中".format(item))
        if int(self.r.llen(import_keyword_redis_listname)) == int(self.result_nums):
            print("插入redis完成")
            # else:

            # print("csv插入redis不完整")


        # class TxtRedis(object):
        #     '''读取txt文件并且储存到redis list里'''
        #     def __init__(self):
        #         self.r = redis.Redis(REDIS_HOST, REDIS_PORT, REDIS_DB)
        #         # self.r = redis.StrictRedis(host="10.2.24.8", port=17480, password="J9O543637e5SYaymJge", db=0)
        #         self.reader = open('./www_domain_name.txt', 'r')
        #         self.item = self.reader.readlines()
        #         self.whole= self.r.lrange("my_url_list", 0, -1)
        #         self.p = self.r.pipeline()
        #         self.result_nums = 0
        # self.q = queue.Queue()
        # def get_txt_up_redis(self):
        #     print("loading.................")
        #     for x in self.item:
        #         item = x.strip()
        #         self.q.put(item)
        #
        # def aa(self):
        #     while True:
        #         if self.q.get() not in self.whole:
        #             try:
        #                 result_num = self.r.rpush("my_url_list", self.q.get())
        #                 self.result_nums = result_num
        #             except Exception as e:
        #                 print(e)
        #                 print("插入{}失败".format(self.q.get()))
        #             else:
        #                 print("{}已存在列表中".format(self.q.get()))
        #         if int(self.r.llen("my_url_list")) == int(self.result_nums):
        #             print("插入redis完成")

        #     if item not in self.whole:
        #         try:
        #             result_num = self.r.rpush("my_url_list", item)
        #             self.result_nums = result_num
        #         except Exception as e:
        #             print(e)
        #             print("插入{}失败".format())
        #     else:
        #         print("{}已存在列表中".format(item))
        # if int(self.r.llen("my_url_list")) == int(self.result_nums):
        #     print("插入redis完成")

        # def get_txt_up_redis(self):
        #     for x in self.item:
        #         item = x.strip()
        #         if item not in self.whole:
        #             try:
        #                 self.p.rpush("my_url_list", item)
        #             except Exception as e:
        #                 print(e)
        #                 print("插入{}失败".format())
        #         else:
        #             print(item,"已存在")
        #             pass
        #
        #     print("正在插入。。。。可能时间较长")
        #     self.p.execute()
        #     # if summer[0] == len(self.item):
        #     print("插入完成")
        #     return
        # print("插入完成")

        # if int(self.r.llen("my_url_list")) == int(self.result_nums):
        #     print("插入redis完成")


if __name__ == "__main__":
    # code = input("请输入文件格式1为csv，2为txt")
    # if code == "1":
    #     csv_redis = CsvRedis()
    #     csv_redis.get_csv_up_redis()
    # elif code == "2":

    # txt_redis = TxtRedis()
    # txt_redis.get_txt_up_redis()
    keyman_input = CsvRedis()
    keyman_input.get_csv_up_redis()


class Get_Redis(object):
    def __init__(self):
        self.POOL = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0)
        self.p = redis.Redis(connection_pool=self.POOL)

    def get_domain(self):
        '''从redis里读取列表里的domain'''
        url = self.p.brpop("my_url_list")
        url = str(url[1], encoding="utf-8")
        # print(url)
        return url

        # if __name__ == "__main__":
        #     get_redis = Get_Redis()
        #     get_redis.get_domain()


        # def test():
        #     reader = csv.reader(open('test.csv', 'r'))
        #     lists = []
        #     for item in reader:
        #         item = "".join(item)
        #         lists.append(item)
        #     return lists
