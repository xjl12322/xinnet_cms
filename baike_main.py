#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/13 20:49"
from urllib.parse import quote

import re
import requests
from lxml import etree

import es_interface
from Database_Connext import connect_mysql, connect_redis
from change_pinyin import pinyin_change
from replace_news_zt import Replce_News
from setings import *


class BaiduBaike(object):
    def __init__(self):
        self.conn = connect_mysql()
        self.cursor = self.conn.cursor()
        self.p = connect_redis()
        self.error = "https://baike.baidu.com/error.html"
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
        self.replce_news = Replce_News()
        self.sql_get_update_id = "select tagid from phome_enewstags where tagname=%s;"
        self.sql_update = "update phome_enewstags set tagimage=%s,tagintro=%s where tagname=%s;"
        self.es = es_interface.Es_Interface()

    def get_keyman(self):
        '''从redis里读取列表里的domain'''
        try:
            keyman = self.p.blpop(import_keyword_redis_listname)
            if keyman[1] == "":
                print("redis列表为空")
                return ""
            else:
                keyman = str(keyman[1], encoding="utf-8")
                return keyman
        except Exception as e:
            print("redis异常{}".format(e))
            pass

    def requests_url(self, tags):
        # 发送请求
        param = tags
        params = quote(param)
        base_url = "https://baike.baidu.com/item/{}".format(params)
        print("发送 关键字：{} HTTP请求".format(tags))
        try:
            response = requests.get(url=base_url, headers=self.header, timeout=20)
            response.encoding = "utf-8"
            return response, param
        except Exception as e:
            print("请求失败！！错误信息：{}".format(e))
            return None, param

    def baidu_encyclopedia(self, tags):
        # 解析爬取字段值
        response, params = self.requests_url(tags)
        param = quote(params)
        if response:

            if response.url != self.error and response.status_code == 200:
                print("请求 {} 响应成功".format(params))
                try:
                    html = etree.HTML(response.text)
                except Exception as e:
                    print(e)
                    print("html解析失败！！错误信息：{}".format(e))
                keyword = param
                descriptions = html.xpath('string(//div[@class="lemma-summary"])').strip()
                if descriptions is not None:
                    description = re.sub("\[\d+\]", "", descriptions)
                    description = description
                else:
                    description = ""
                try:
                    tagimage = html.xpath('//div[@class="summary-pic"]/a/img/@src')[0].strip()
                except Exception as e:
                    tagimage = ""
                    print("关键字: {} 无简介图".format(tags))
                return params, description, tagimage

            else:
                print("百度百科无此关键字: {}  继续生成无关键字模板".format(tags))
                description, tagimage = "", ""
                if int(response.status_code) >= 400:
                    print("警告：ip可能被封！！！！！！！！！！" * 20)
                    params = "@@ip"
                    return params, description, tagimage
                return params, description, tagimage
        else:
            return params, "", ""

    def insert_database(self, keyword, description="", tagimage=""):
        sql = "insert ignore into phome_enewstags(tagname,num,isgood,cid,tagimage,tagintro,first) values(%s,%s,%s,%s,%s,%s,%s)"
        pinyin_result = pinyin_change(keyword)
        try:
            self.cursor.execute(sql, (keyword, 1, 0, 0, tagimage, description, pinyin_result))
            last_resualt = int(self.cursor.lastrowid)
            self.es.add_keyword_dan(last_resualt, keyword, description)
            self.replce_news.news_zt(last_resualt, keyword, description, tagimage)

        except Exception as e:
            print("mysql异常信息1{}".format(e))
            pass

    def update_database_tagimage_tagintro(self, keyword, tagintro, tagimage):
        sql_tagimage_update = "update phome_enewstags set tagimage=%s,tagintro=%s where tagname=%s;"
        num = self.cursor.execute(sql_tagimage_update, (tagimage, tagintro, keyword))

        if num == 0:
            print("无更新")
        else:
            print("更新成功")

    def update_database_tagintro(self, keyword, tagintro):
        sql_tagimage_update = "update phome_enewstags set tagintro=%s where tagname=%s;"
        num = self.cursor.execute(sql_tagimage_update, (tagintro, keyword))
        if num == 0:
            print("无更新")
        else:
            print("更新成功")

    def update_database_tagimage(self, keyword, tagimage):
        sql_tagimage_update = "update phome_enewstags set tagimage=%s where tagname=%s;"
        num = self.cursor.execute(sql_tagimage_update, (tagimage, keyword))
        if num == 0:
            print("无更新")
        else:
            print("更新成功")

    def is_empty(self, word):
        if word is None or word == '':
            return True
        else:
            return False

    def judgement_keyword(self, keyword):
        sql_keyword_exist = 'select tagid,tagintro,tagimage from phome_enewstags where tagname=%s;'
        self.cursor.execute(sql_keyword_exist, (keyword,))
        result = self.cursor.fetchone()

        tagid = None
        tagintro = None
        tagimage = None

        if result is not None:
            tagid = result["tagid"]
            tagintro = result["tagintro"]
            tagimage = result["tagimage"]

        keywords, tagintro_baidu, tagimage_baidu = self.baidu_encyclopedia(keyword)

        if tagid is None:
            print(tagid, "3333333")
            if keywords == "@@ip":
                pass
            else:
                self.insert_database(keywords, tagintro_baidu, tagimage_baidu)

        else:
            #
            if keywords == "@@ip":
                pass

            else:
                print("关键字：{} 已存在".format(keyword))
                if (self.is_empty(tagintro)) and (self.is_empty(tagimage)):
                    self.update_database_tagimage_tagintro(keyword, tagintro_baidu, tagimage_baidu)
                elif self.is_empty(tagintro):
                    self.update_database_tagintro(keyword, tagintro_baidu)
                elif self.is_empty(tagimage):
                    self.update_database_tagimage(keyword, tagimage_baidu)

            tagintro_new = tagintro
            if self.is_empty(tagintro_new):
                tagintro_new = tagintro_baidu

            tagimage_new = tagimage
            if self.is_empty(tagimage_new):
                tagimage_new = tagimage_baidu

            self.es.add_keyword_dan(tagid, keyword, tagintro_new)
            self.replce_news.news_zt(tagid, keyword, tagintro_new, tagimage_new)


if __name__ == "__main__":
    # 程序入口
    baike = BaiduBaike()

    if keywrods_get_channel == "redis":
        # 获取redis列表里关键字
        while True:
            print("开始监控redis列表")
            keyword_tag = baike.get_keyman()
            if keyword_tag is not None and keyword_tag != "":
                print("获取redis关键字为:{}".format(keyword_tag))
                baike.judgement_keyword(keyword_tag)


            else:
                continue

    if keywrods_get_channel == "mysql":
        replce_news = Replce_News()
        replce_news.news_zt()
