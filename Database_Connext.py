#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"
import pymysql
import redis
from DBUtils.PooledDB import PooledDB

from setings import *


# pool = PooledDB(pymysql,10,host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWD,db=MYSQL_DBNAME,port=MYSQL_PORT,charset='utf8',cursorclass=pymysql.cursors.DictCursor) #5为连接池里的最少连接数
#
# conn = pool.connection()  #以后每次需要数据库连接就是用connection（）函数获取连接就好了
# cur=conn.cursor()
# sql = "select tagname,tagimage from phome_enewstags"
# r=cur.execute(sql)
# ee=cur.fetchall()
# print(ee)
# cur.close()
# conn.close()


def connect_mysql():
    try:
        pool = PooledDB(pymysql, 10, host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DBNAME,
                        port=MYSQL_PORT, charset='utf8', cursorclass=pymysql.cursors.DictCursor)  # 5为连接池里的最少连接数
        conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
        return conn
    except Exception as e:
        print("mysql连接失败")
        print(e)


def connect_redis():
    try:
        POOL = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)
        p = redis.Redis(connection_pool=POOL)
        return p
    except Exception as e:
        print("redis连接失败")
        print(e)
