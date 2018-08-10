#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"

import datetime
import os
import re
import stat

import es_interface
from Database_Connext import connect_mysql
from setings import *


class Replce_News_mip(object):
    def __init__(self):
        self.es = es_interface.Es_Interface()
        self.conn = connect_mysql()
        self.cursor = self.conn.cursor()
        self.max_n = self.max_num()
        self.content = open(r"news_template_mip/new_zt_mip.html", "r", encoding="utf-8").read()
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

    def replece_news_zt(self, last_get_mysql_id, keyword, description, tagimage):

        try:

            if not os.path.exists(generate_template_path_mip):
                os.makedirs(generate_template_path_mip)
        except Exception as e:
            print(e, "创建文件异常")

        tagname = keyword
        tagimage = tagimage
        tagintros = description

        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        tagtime = "[" + str(now_time) + "]"
        now_time2 = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        curent_time = str(now_time2)

        html = self.content

        try:
            html = re.sub("\[--tagtime--\]", tagtime, html)
            html = re.sub("\[--tagname--\]", tagname, html)
            html = re.sub("\[--tagimage--\]", tagimage, html)
            html = re.sub("\[--tagintro--\]", tagintros, html)
            html = re.sub("\[--pcurl--\]", "http://www.xinnet.com/xinzhi/tags/{}.html".format(last_get_mysql_id), html)
            html = re.sub("\[--mipurl--\]", "http://mip.xinnet.com/mip/tags/{}.html".format(last_get_mysql_id), html)
            html = re.sub("\[--curent_time--\]", curent_time, html)
        except Exception as e:
            print("错误信息  ", e)

        random_get_news_result_list = self.es.random_get_news()
        for index, list_node in enumerate(random_get_news_result_list, 1):
            new_url = re.sub("http://www.xinnet.com/xinzhi", "http://mip.xinnet.com/mip", list_node['newsUrl'])
            html = re.sub("\[--randomurl--{}\]".format(index), new_url, html)
            html = re.sub("\[--randomtitle--{}\]".format(index), list_node['newsTitle'], html)
            html = re.sub("\[--randomtime--{}\]".format(index), str(list_node['newsTime'][0:10]).strip(), html)

        treference_keyword_get_news_list = self.es.tramdom_get_keyword()
        for index0, list_node0 in enumerate(treference_keyword_get_news_list, 1):
            new_url0 = re.sub("http://www.xinnet.com/xinzhi", "http://mip.xinnet.com/mip", list_node0['newsUrl'])
            html = re.sub("\[--trandomurl--{}\]".format(index0), new_url0, html)
            html = re.sub("\[--trandomtitle--{}\]".format(index0), list_node0['newsTitle'], html)
            html = re.sub("\[--trandomtime--{}\]".format(index0), str(list_node0['newsTime'][0:10]).strip(), html)

        reference_keyword_get_news_list = self.es.reference_keyword_get_news(tagname, tagintros)
        flag = True
        for index3, list_node3 in enumerate(reference_keyword_get_news_list, 1):
            if list_node3['newsPic']:
                new_pic = re.sub("http://www.xinnet.com/xinzhi", "http://mip.xinnet.com/mip", list_node3['newsPic'])
            else:
                new_pic = 'http://mip.xinnet.com/mip/images/notimg.gif'

            new_url3 = re.sub("http://www.xinnet.com/xinzhi", "http://mip.xinnet.com/mip", list_node3['newsUrl'])
            divs = '<div class = "ZtDivs_div2">' \
                   '<div class = "ZtDivs2_head clearBoth">' \
                   '<a href="{}"><h2 class = "ZtDivs_h2">{}</h2></a>' \
                   '<p>{}</p>' \
                   '</div>' \
                   '<div class = "ZtDivs2_txt">' \
                   '<p>{}</p>' \
                   '<div><img src="{}" alt = ""></div>' \
                   '</div>' \
                   '</div>'.format(new_url3,
                                   list_node3['newsTitle'] if len(list_node3['newsTitle']) < 35 else list_node3[
                                                                                                         'newsTitle'][
                                                                                                     0:30] + "....",
                                   str(list_node3['newsTime'][0:10]).strip(),
                                   list_node3['newsSmallText'] if len(list_node3['newsSmallText']) < 215 elselist_node3[
                                                                                                                 'newsSmallText'][
                                                                                                             0:215] + ".....",
                                   new_pic)

            divs2 = '''<div class="mipui-category-list-item">
            <div class="item-content">
<h4><a href="{0}" data-type="mip" data-title="{1}" title='{1}'>{1}</a></h4>
                        <p class="description">{2}</p>
                        <p>
                            <span>{3}</span>
                        </p>
                    </div>
                </div>'''.format(new_url3, list_node3['newsTitle'], list_node3['newsSmallText'],
                                 str(list_node3['newsTime'][0:10]).strip())

            html = re.sub("<!--\[--newstitleurl--{}\]-->".format(index3), divs2, html)

        like_keyword_list = self.es.like_keyword(tagname, tagintros)
        for index4, list_node4 in enumerate(like_keyword_list, 1):
            html = re.sub("<!--\[--relevanturl--{}\]-->".format(index4),
                          '<li class="m-b-sm"><a href="http://mip.xinnet.com/mip/tags/{1}.html" data-type="mip" data-title="{0}" title="{0}">{0}</a></li>'.format(
                              list_node4["tagName"], list_node4['tagId']), html)

        with open(generate_template_path_mip + os.sep + '{}'.format(last_get_mysql_id) + ".html", 'w',
                  encoding="utf-8") as f:
            f.write(html)
        try:
            os.chmod(generate_template_path_mip + os.sep + '{}'.format(last_get_mysql_id) + ".html",
                     stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)
        except Exception as e:
            print("文件授权失败")
            pass
