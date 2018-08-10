#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"

import json
import requests

import replace_news_zt
from Database_Connext import connect_mysql
from md5_use import getsecret
from setings import *


class Es_Interface(object):
    def random_get_news(self):
        try:
            sign, innerApp, ts = getsecret()
            random_get_news_interface = server + '/rest/cms/randomGetNews?sign={}&innerApp={}&ts={}'.format(sign,
                                                                                                            innerApp,
                                                                                                            ts)

            response_result = requests.post(url=random_get_news_interface)
            content = json.loads(response_result.text)

            return content["list"]
        except Exception as e:
            print("random_get_news  异常", e)

    def add_keyword(self):
        replace_new = replace_news_zt.Replce_News()
        max_num = replace_new.max_num()
        conn = connect_mysql()
        cursor = conn.cursor()
        sql = "select tagname,tagintro,tagimage from phome_enewstags WHERE tagid=%s"
        for id in range(1, max_num + 1):
            result_value = cursor.execute(sql, (id,))
            if result_value != 0:
                print("查询成功")
                result = cursor.fetchone()
                sign, innerApp, ts = getsecret()
                add_keyword_interface = server + '/rest/cms/addOrUpdateTag?sign={}&innerApp={}&ts={}'.format(sign,
                                                                                                             innerApp,
                                                                                                             ts)
                response_findtag = requests.post(url=add_keyword_interface, json={
                    "tagId": int(id),
                    "tagName": result["tagname"],
                    "tagDesc": result["tagintro"],

                })
                content = json.loads(response_findtag.text)
                print(content["result"])
                if content["result"] == "True":
                    print("插入es关键字成功")
                    # es.add_keyword(id, result["tagname"], result["tagintro"], result["tagimage"])
            else:
                continue

    def add_keyword_dan(self, tagid, tagname, tagintro):

        try:
            sign, innerApp, ts = getsecret()
            add_keyword_interface = server + '/rest/cms/addOrUpdateTag?sign={}&innerApp={}&ts={}'.format(sign, innerApp,
                                                                                                         ts)
            response_findtag = requests.post(url=add_keyword_interface, json={
                "tagId": tagid,
                "tagName": tagname,
                "tagDesc": tagintro

            })
            print(response_findtag.text, "dddd")
            content = json.loads(response_findtag.text)

            print(content["result"], type(content["result"]))
            if content["result"] == True:
                print("插入es关键字成功")
            else:
                print("插入es关键字失败")
                # es.add_keyword(id, result["tagname"], result["tagintro"], result["tagimage"])
        except Exception as e:
            print("random_get_news_dan  异常", e)

    def ramdom_get_keyword(self):
        try:
            sign, innerApp, ts = getsecret()
            random_get_keyword_interface = server + '/rest/cms/randomGetTag?sign={}&innerApp={}&ts={}'.format(sign,
                                                                                                              innerApp,
                                                                                                              ts)
            response_result = requests.post(url=random_get_keyword_interface)
            content = json.loads(response_result.text)
            # print(content["list"])
            return content["list"]
        except Exception as e:
            print("ramdom_get_keyword  异常", e)

    def tramdom_get_keyword(self):
        try:
            sign, innerApp, ts = getsecret()
            trandom_get_keyword_interface = server + '/rest/cms/getNewestNews?sign={}&innerApp={}&ts={}'.format(sign,
                                                                                                                innerApp,
                                                                                                                ts)
            response_result = requests.post(url=trandom_get_keyword_interface)
            content = json.loads(response_result.text)
            # print(content["list"])
            return content["list"]
        except Exception as e:
            print("ramdom_get_keyword  异常", e)

    def reference_keyword_get_news(self, tagname="", tagintro=""):

        try:
            sign, innerApp, ts = getsecret()
            reference_keyword_get_news_interface = server + '/rest/cms/searchNews?sign={}&innerApp={}&ts={}'.format(
                sign, innerApp, ts)
            response_result = requests.post(url=reference_keyword_get_news_interface,
                                            json={"tagName": tagname, "tagDesc": tagintro})
            content = json.loads(response_result.text)
            # print(content["list"])
            return content["list"]
        except Exception as e:
            print("reference_keyword_get_news  异常", e)

    def like_keyword(self, tagname, tagintro):
        try:
            sign, innerApp, ts = getsecret()
            like_keyword_interface = server + '/rest/cms/searchTag?sign={}&innerApp={}&ts={}'.format(sign, innerApp, ts)
            response_result = requests.post(url=like_keyword_interface, json={"tagName": tagname, "tagDesc": tagintro})
            content = json.loads(response_result.text)
            # print(content["list"])
            return content["list"]
        except Exception as e:
            print("like_keyword  异常", e)


if __name__ == "__main__":
    # 下面为测试es接口
    es = Es_Interface()

    # es.add_keyword()
    ll = es.tramdom_get_keyword()
    print(ll)
    # for index3, list_node3 in enumerate(ll, 1):
    #     print(list_node3['newsUrl'])
