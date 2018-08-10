#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"

import csv

import pymysql
import redis

import_keyword_redis_listname = "cms_tags"
tags_table_name = "phome_enewstags"

# MYSQL_HOST = '119.10.116.237'
# MYSQL_DBNAME = 'ecms72'
# MYSQL_PORT = 3306
# MYSQL_USER = 'py'
# MYSQL_PASSWD = 'py'
# REDIS_HOST = "119.10.116.235"
# REDIS_PORT = 7344
# REDIS_DB = 10
# REDIS_PASSWORD = "xinnetpassword"


MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'ecms72test'
MYSQL_PORT = 3306
MYSQL_USER = 'py'
MYSQL_PASSWD = 'py'
#
#
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = ""


def connect_mysql():
    try:
        conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DBNAME, port=MYSQL_PORT,
                               charset='utf8', cursorclass=pymysql.cursors.DictCursor)  # 5为连接池里的最少连接数
        # conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
        con = conn.cursor()
        return con
    except Exception as e:
        print("mysql连接失败")
        print(e)


class CsvRedis(object):
    def __init__(self):
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)
        self.reader = csv.reader(open('domain_list.csv', 'r', encoding="utf-8"))
        self.whole = self.r.lrange(import_keyword_redis_listname, 0, -1)
        self.result_nums = 0
        self.cursor = connect_mysql()

    def get_csv_up_redis(self):
        num = self.cursor.execute("select tagname from " + tags_table_name)
        if num:
            result = self.cursor.fetchall()
            for x in result:
                result_value = x["tagname"]
                print(result_value)
                try:
                    result_num = self.r.rpush(import_keyword_redis_listname, result_value)
                    print("插入成功第{}条tag".format(result_num))
                except Exception as e:
                    print(e)
                    print("插入{}失败".format(result_value))
        else:
            print("读取失败")


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
