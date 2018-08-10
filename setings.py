#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"

keywrods_get_channel = "redis"
# keywrods_get_channel = "mysql"  #redis或mysql

# 线上87
# # es
# server = 'http://tagapi.xinnet.com'
# #mysql
# MYSQL_HOST = '10.2.2.103'
# MYSQL_DBNAME = 'ecms72'
# MYSQL_PORT = 3306
# MYSQL_USER = 'xinnetcmsuser'
# MYSQL_PASSWD = 'yumCSWqpjQVsZyPC'
# #redis
# REDIS_HOST = "127.0.0.1"
# REDIS_PORT = 6379
# REDIS_DB = 10
# REDIS_PASSWORD = "xinnet123"

##################################################

# 247 and local
# es
server = 'http://tagapi.xinnet.com'
# mysql
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'ecms72test'
MYSQL_PORT = 3306
MYSQL_USER = 'py'
MYSQL_PASSWD = 'py'
# redis
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 10
REDIS_PASSWORD = ""

import_keyword_redis_listname = "cms_tags"
tags_table_name = "phome_enewstags"
# pc_path
generate_template_path = "E:/php/ecms72/xol/xinzhi/tags"
# generate_template_path = "/usr/local/nginx/html/ecms72/xol/xinzhi/tags"

# move_path
generate_template_path_m = "E:/php/ecms72/xol/xinzhi/tags2"
# generate_template_path_m = "/usr/local/nginx/html/ecms72/xol/mweb/tags"

# mip_path
generate_template_path_mip = "E:/php/ecms72/xol/xinzhi/tags3"
# generate_template_path_mip = "/usr/local/nginx/html/ecms72/xol/mip/tags"
