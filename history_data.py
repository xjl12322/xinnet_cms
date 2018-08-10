#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"
import json
import requests
import time

import pymysql
from DBUtils.PooledDB import PooledDB

from  setings import *


# MYSQL_HOST = '119.10.116.237'
# MYSQL_DBNAME = 'ecms72'
# MYSQL_PORT = 3306
# MYSQL_USER = 'py'
# MYSQL_PASSWD = 'py'
# int_data = "2017-1-15"

# data =int(time.mktime(datetime.datetime.strptime(int_data,"%Y-%m-%d").timetuple()))
# print(data)
# change_data = time.localtime(data)
# time_str = time.strftime('%Y-%m-%d %H:%M:%S', change_data)
# print(time_str)
def connect_mysql():
    try:
        pool = PooledDB(pymysql, 10, host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DBNAME,
                        port=MYSQL_PORT, charset='utf8', cursorclass=pymysql.cursors.DictCursor)  # 5为连接池里的最少连接数
        conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
        return conn
    except Exception as e:
        print("mysql连接失败")
        print(e)


# 'http://127.0.0.1:8081/rest/cms/addNews
#
# {
#     "newsId": 118,
#     "classId": 61,
#     "newsTitle": "文章测试1",
#     "newsText": "这是一篇测试文章的正文。",
#     "newsUrl": "http://www.xinnet.com/xinzhi/61/101.html",
#     "newsPic": "http://www.xinnet.com/aaa.jpg",
#     "newsSmallText": "这是一篇测试文章的简介。",
#     "newsTags": "测试,文章",
#     "newsTime": "2018-03-12 00:00:00"
# }'


def add_news():
    conn = connect_mysql()
    cursor = conn.cursor()
    # sql = "SELECT rr.id,rr.classid,rr.titleurl,rr.title,rr.titlepic,rr.newstime,rr.smalltext,yy.infotags,yy.newstext FROM phome_ecms_xinnews as rr JOIN phome_ecms_xinnews_data_1 as yy ON rr.id=yy.id JOIN phome_ecms_xinnews_index as cc ON yy.id=cc.id WHERE cc.checked=0;"
    sql = "SELECT rr.id,rr.classid,rr.titleurl,rr.title,rr.titlepic,rr.newstime,rr.smalltext,yy.infotags,yy.newstext FROM phome_ecms_xinnews rr,phome_ecms_xinnews_data_1 yy where rr.id=yy.id;"

    result_value = cursor.execute(sql)
    print(result_value)
    if result_value != 0:
        print("查询成功")

        result = cursor.fetchall()
        # print(result)
        for result_node in result:
            add_news_interface = 'http://tagapi.xinnet.com/rest/cms/addOrUpdateNews'
            change_data = time.localtime(result_node["newstime"])

            time_str = time.strftime('%Y-%m-%d %H:%M:%S', change_data)
            response_findtag = requests.post(url=add_news_interface, json=
            {
                "newsId": result_node["id"],
                "classId": result_node["classid"],
                "newsTitle": result_node["title"],
                "newsText": result_node["newstext"],
                "newsUrl": result_node["titleurl"],
                "newsPic": result_node["titlepic"] if result_node["titlepic"] else "",
                "newsSmallText": result_node["smalltext"],
                "newsTags": result_node["infotags"],
                "newsTime": str(time_str)
            })

            content = json.loads(response_findtag.text)

            if content["result"] == True:
                print("插入es新闻成功")

            else:
                print("插入es新闻失败")
    print("处理完毕")


add_news()
