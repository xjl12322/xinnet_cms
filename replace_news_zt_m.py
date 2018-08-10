#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"
import datetime
import os
import re
import shutil
import stat

import es_interface
from Database_Connext import connect_mysql
from setings import *


class Replce_News_mi(object):
    def __init__(self):
        self.es = es_interface.Es_Interface()
        self.conn = connect_mysql()
        self.cursor = self.conn.cursor()
        self.max_n = self.max_num()
        self.content = open(r"news_template_m/mob_zt.html", "r", encoding="utf-8").read()
        # self.sql_get_update_id = "select tagid from phome_enewstags where tagname=%s;"
        # self.sql = "select tagname,tagimage,tagintro from phome_enewstags where tagid=%s"
        self.flag = True

    def max_num(self):
        self.cursor.execute('select max(tagid) as max from phome_enewstags')
        num = self.cursor.fetchone()
        if num["max"] is None:
            return 1
        else:
            return num["max"]

    def replece_news_zt_mi(self, last_get_mysql_id, keyword, description, tagimage):
        try:
            if not os.path.exists(generate_template_path_m):
                os.makedirs(generate_template_path_m)
            if not os.path.exists(generate_template_path_m + os.sep + "css"):
                shutil.copytree(os.getcwd() + os.sep + "news_template_m/css", generate_template_path_m + os.sep + "css")
            if not os.path.exists(generate_template_path_m + os.sep + "images"):
                shutil.copytree(os.getcwd() + os.sep + "news_template_m/images",
                                generate_template_path_m + os.sep + "images")
            if not os.path.exists(generate_template_path_m + os.sep + "js"):
                shutil.copytree(os.getcwd() + os.sep + "news_template_m/js", generate_template_path_m + os.sep + "js")
        except Exception as e:
            print(e, "创建文件异常")

        tagname = keyword
        tagimage = tagimage
        tagintros = description

        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        tagintros = "[" + str(now_time) + "]" + "&nbsp;&nbsp;简介:&nbsp;&nbsp;" + tagintros

        html = self.content

        try:

            html = re.sub("\[--tagname--\]", tagname, html)
            html = re.sub("\[--tagimage--\]", tagimage, html)
            html = re.sub("\[--tagintro--\]", tagintros, html)
            html = re.sub("\[--pcurl--\]", "http://www.xinnet.com/xinzhi/tags/{}.html".format(last_get_mysql_id), html)
            html = re.sub("\[--mipurl--\]", "http://mip.xinnet.com/mip/tags/{}.html".format(last_get_mysql_id), html)
        except Exception as e:
            print("错误信息  ", e)

        treference_keyword_get_news_list = self.es.tramdom_get_keyword()
        for index0, list_node0 in enumerate(treference_keyword_get_news_list, 1):
            new_url0 = re.sub("http://www.xinnet.com/xinzhi", "http://m.xinnet.com/mweb", list_node0['newsUrl'])
            html = re.sub("\[--trandomurl--{}\]".format(index0), new_url0, html)
            html = re.sub("\[--trandomtitle--{}\]".format(index0), list_node0['newsTitle'], html)
            html = re.sub("\[--trandomtime--{}\]".format(index0), str(list_node0['newsTime'][0:10]).strip(), html)

        random_get_news_result_list = self.es.random_get_news()
        for index, list_node in enumerate(random_get_news_result_list, 1):
            new_url = re.sub("http://www.xinnet.com/xinzhi", "http://m.xinnet.com/mweb", list_node['newsUrl'])
            html = re.sub("\[--randomurl--{}\]".format(index), new_url, html)
            html = re.sub("\[--randomtitle--{}\]".format(index), list_node['newsTitle'], html)
            html = re.sub("\[--randomtime--{}\]".format(index), str(list_node['newsTime'][0:10]).strip(), html)

        random_get_keyword_result_list = self.es.ramdom_get_keyword()
        for index2, list_node2 in enumerate(random_get_keyword_result_list, 1):
            html = re.sub("<!--\[--trelevanturl--{}\]-->".format(index2),
                          'http://m.xinnet.com/mweb/tags/{}.html'.format(list_node2["tagId"]), html)
            html = re.sub("<!--\[--trelevantkeyword--{}\]-->".format(index2), list_node2["tagName"], html)

        reference_keyword_get_news_list = self.es.reference_keyword_get_news(tagname, tagintros)
        flag = True
        for index3, list_node3 in enumerate(reference_keyword_get_news_list, 1):
            new_url3 = re.sub("http://www.xinnet.com/xinzhi", "http://m.xinnet.com/mweb", list_node3['newsUrl'])
            if list_node3['newsPic']:
                new_pic = re.sub("http://www.xinnet.com/xinzhi", "http://m.xinnet.com/mweb", list_node3['newsPic'])
            else:
                new_pic = 'http://m.xinnet.com/mweb/images/notimg.gif'
            divs = '<div class = "newps_div clearfix">' \
                   '<div class = "newps_dl"><a href="{}"><img src="{}" alt = "域名解析，域名如何解析？"></a>' \
                   '</div>' \
                   '<div class = "newps_dr">' \
                   '<p class = "newpsd_p0"><a href="{}">{}</a></p>' \
                   '<p class = "newpsd_p1">{}</p>' \
                   '</div>' \
                   '</div>'.format(new_url3, new_pic, new_url3,
                                   list_node3['newsTitle'] if len(list_node3['newsTitle']) < 15 else list_node3[
                                                                                                         'newsTitle'][
                                                                                                     0:13] + "...",
                                   list_node3['newsSmallText'] if len(list_node3['newsSmallText']) < 49 else list_node3[
                                                                                                                 'newsSmallText'][
                                                                                                             0:45] + "....")

            html = re.sub("<!--\[--newstitleurl--{}\]-->".format(index3), divs, html)

        like_keyword_list = self.es.like_keyword(tagname, tagintros)
        for index4, list_node4 in enumerate(like_keyword_list, 1):
            # if len(list_node4["tagName"])>4
            html = re.sub("<!--\[--relevanturl--{}\]-->".format(index4),
                          'http://m.xinnet.com/mweb/tags/{}.html'.format(list_node4["tagId"]), html)

            html = re.sub("<!--\[--relevantkeyword--{}\]-->".format(index4), list_node4["tagName"], html)

        html = re.sub(
            '<p><a href="<!--\[--relevanturl--\d+\]-->"><!--\[--relevantkeyword--\d+\]--></a><a href="<!--\[--relevanturl--\d+\]-->"><!--\[--relevantkeyword--\d+\]--></a><a href="<!--\[--relevanturl--\d+\]-->"><!--\[--relevantkeyword--\d+\]--></a><a href="<!--\[--relevanturl--\d+\]-->"><!--\[--relevantkeyword--\d+\]--></a></p>',
            "", html, re.S)
        html = re.sub(
            '<p><a href="<!--\[--trelevanturl--\d+\]-->"><!--\[--trelevantkeyword--\d+\]--></a><a href="<!--\[--trelevanturl--\d+\]-->"><!--\[--trelevantkeyword--\d+\]--></a><a href="<!--\[--trelevanturl--\d+\]-->"><!--\[--trelevantkeyword--\d+\]--></a><a href="<!--\[--trelevanturl--\d+\]-->"><!--\[--trelevantkeyword--\d+\]--></a></p>',
            "", html, re.S)
        mobanjianzhan = "http://m.xinnet.com/mweb/tags/{}.html".format(last_get_mysql_id)
        html = re.sub("\[--mobanjianzhan--\]", mobanjianzhan, html)

        with open(generate_template_path_m + os.sep + '{}'.format(last_get_mysql_id) + ".html", 'w',
                  encoding="utf-8") as f:
            f.write(html)
        try:
            os.chmod(generate_template_path_m + os.sep + '{}'.format(last_get_mysql_id) + ".html",
                     stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)
        except Exception as e:
            print("文件授权失败")
            pass
