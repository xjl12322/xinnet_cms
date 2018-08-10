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
from replace_news_zt_m import Replce_News_mi
from replace_news_zt_mip import Replce_News_mip
from setings import *


class Replce_News(object):
    def __init__(self):
        self.es = es_interface.Es_Interface()
        self.conn = connect_mysql()
        self.cursor = self.conn.cursor()
        self.max_n = self.max_num()
        self.content = open(r"news_template/news_zt.html", "r", encoding="utf-8").read()
        # self.sql_get_update_id = "select tagid from phome_enewstags where tagname=%s;"
        # self.sql = "select tagname,tagimage,tagintro from phome_enewstags where tagid=%s"
        self.flag = True
        self.replece_mi = Replce_News_mi()
        self.replece_mip = Replce_News_mip()
        # def summay_slice(self,summay):
        #     now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # if summay == "":
        #     return summay
        # else:
        #     if len(summay) > 180:
        #         summay = summay.strip()
        #         summay = summay[0:180]+"....."
        #         return "["+now_time+"]"+"&nbsp;简介:&nbsp;"+summay
        #     else:
        #         return "["+now_time+"]"+"&nbsp;简介:&nbsp;"+summay.strip()

    def max_num(self):
        self.cursor.execute('select max(tagid) as max from phome_enewstags')
        num = self.cursor.fetchone()
        if num["max"] is None:
            return 1
        else:
            return num["max"]

    def news_zt(self, last_get_mysql_id, keyword, description, tagimage):

        try:
            if not os.path.exists(generate_template_path):
                os.makedirs(generate_template_path)
            if not os.path.exists(generate_template_path + os.sep + "css"):
                shutil.copytree(os.getcwd() + os.sep + "news_template/css", generate_template_path + os.sep + "css")

            if not os.path.exists(generate_template_path + os.sep + "images"):
                shutil.copytree(os.getcwd() + os.sep + "news_template/images",
                                generate_template_path + os.sep + "images")

            if not os.path.exists(generate_template_path + os.sep + "js"):
                shutil.copytree(os.getcwd() + os.sep + "news_template/js", generate_template_path + os.sep + "js")
        except Exception as e:
            print(e, "创建文件异常")

        if keywrods_get_channel == "mysql":
            for id in range(1, self.max_n + 1):
                # for id in range(1,49):
                result_value = self.cursor.execute(self.sql, (id))
                if result_value != 0:
                    result = self.cursor.fetchone()
                    self.replece_news_zt(result, id)
                else:
                    continue

        if keywrods_get_channel == "redis":
            if description == None:
                description = ""
            if tagimage == None:
                tagimage = ""

            self.replece_news_zt(last_get_mysql_id, keyword, description, tagimage)
            self.replece_mi.replece_news_zt_mi(last_get_mysql_id, keyword, description, tagimage)
            self.replece_mip.replece_news_zt(last_get_mysql_id, keyword, description, tagimage)

    def replece_news_zt(self, last_get_mysql_id, keyword, description, tagimage):

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
            html = re.sub("\[!--mipurl--\]", "http://mip.xinnet.com/mip/tags/{}.html".format(last_get_mysql_id), html)

        except Exception as e:
            print("错误信息  ", e)

        # es = es_interface.Es_Interface()
        random_get_news_result_list = self.es.random_get_news()
        for index, list_node in enumerate(random_get_news_result_list, 1):
            # print(index, list_node['newsTitle'])
            # print(index, list_node['newsUrl'])
            html = re.sub("\[--randomurl--{}\]".format(index), list_node['newsUrl'], html)
            html = re.sub("\[--randomtitle--{}\]".format(index), list_node['newsTitle'], html)

        random_get_keyword_result_list = self.es.ramdom_get_keyword()

        for index2, list_node2 in enumerate(random_get_keyword_result_list, 1):
            html = re.sub("\[--randomkeyword--{}\]".format(index2), list_node2['tagName'], html)
            # self.cursor.execute(self.sql_get_update_id, (list_node2['tagName'],))
            # tagname_id = self.cursor.fetchone()
            html = re.sub("\[--randomkeywordurl--{}\]".format(index2),
                          "http://www.xinnet.com/xinzhi/tags/{}.html".format(list_node2['tagId']), html)

        reference_keyword_get_news_list = self.es.reference_keyword_get_news(tagname, tagintros)
        flag = True
        for index3, list_node3 in enumerate(reference_keyword_get_news_list, 1):
            if list_node3['newsPic']:
                new_pic = list_node3['newsPic']
            else:
                new_pic = 'http://www.xinnet.com/xinzhi/images/notimg.gif'
            divs = '<div class = "ZtDivs_div2">' \
                   '<div class = "ZtDivs2_head clearBoth">' \
                   '<a href="{}"><h2 class = "ZtDivs_h2">{}</h2></a>' \
                   '<p>{}</p>' \
                   '</div>' \
                   '<div class = "ZtDivs2_txt">' \
                   '<p>{}</p>' \
                   '<div><img src="{}" alt = ""></div>' \
                   '</div>' \
                   '</div>'.format(list_node3['newsUrl'],
                                   list_node3['newsTitle'] if len(list_node3['newsTitle']) < 35 else list_node3[
                                                                                                         'newsTitle'][
                                                                                                     0:30] + "....",
                                   str(list_node3['newsTime'][0:10]).strip(),
                                   list_node3['newsSmallText'] if len(list_node3['newsSmallText']) < 215 elselist_node3[
                                                                                                                 'newsSmallText'][
                                                                                                             0:215] + ".....",
                                   new_pic)

            html = re.sub("<!--\[--newstitleurl--{}\]-->".format(index3), divs, html)
            self.flag = False

        like_keyword_list = self.es.like_keyword(tagname, tagintros)
        for index4, list_node4 in enumerate(like_keyword_list, 1):
            html = re.sub("<!--\[--relevanturl--{}\]-->".format(index4),
                          '<li><a href="' + "http://www.xinnet.com/xinzhi/tags/{}.html".format(
                              list_node4['tagId']) + '" target="_blank">' + list_node4["tagName"] + '</a></li>', html)

        mobanjianzhan = "http://www.xinnet.com/xinzhi/tags/{}.html".format(last_get_mysql_id)
        html = re.sub("\[--mobanjianzhan--\]", mobanjianzhan, html)

        with open(generate_template_path + os.sep + '{}'.format(last_get_mysql_id) + ".html", 'w',
                  encoding="utf-8") as f:
            f.write(html)
        try:
            os.chmod(generate_template_path + os.sep + '{}'.format(last_get_mysql_id) + ".html",
                     stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)
        except Exception as e:
            print("文件授权失败")
            pass



            # return num["max"]
            # html_text = open(r"news_template/news_zt.html","rb",encoding="utf-8")
            # print(str(html_text).encode("utf-8"))
            # print(html_text)
            # html = etree.HTML(str(html_text).encode("utf-8"))
            # print(html)


if __name__ == "__main__":
    r = Replce_News()
    r.news_zt()
