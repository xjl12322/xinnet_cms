#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"

import json

import requests

#
#
# url_findnews = "http://119.10.116.247:8081/rest/cms/findNews"
# response_findnews = requests.post(url=url_findnews,json={"newsId": 101,"classId": 61})
# print(response_findnews.status_code)
# content = json.loads(response_findnews.text)
# print(content)


# url_searchnews = 'http://119.10.116.247:8081/rest/cms/searchNews'
# response_searchnews = requests.post(url=url_searchnews,json={"tagName": "测试","tagDesc": "测试文章"})
# content = json.loads(response_searchnews.text)
# print(content)



# url_findtag = 'http://119.10.116.247:8081/rest/cms/findTag'
# response_findtag = requests.post(url=url_findtag,json={"tagId": 5004})
# content = json.loads(response_findtag.text)
# print(content)


# from elasticsearch import Elasticsearch
#
#
# es = Elasticsearch([{"host":"119.10.116.247","port":8081}])
# # body = {"query":{"match_all":{}}}
# res = result = es.get(index="my_index",doc_type="test_type",id=1)
# print(res)

url_random_get_news = 'http://tagapi.xinnet.com/rest/cms/randomGetNews'
response_findtag = requests.post(url=url_random_get_news)
content = json.loads(response_findtag.text)
print(content)
