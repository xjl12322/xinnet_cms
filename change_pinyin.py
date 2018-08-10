#! /usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = "X"
__date__ = "2017/11/6 20:09"
import re

from pypinyin import lazy_pinyin


def pinyin_change(keyword):
    if keyword:

        string = str(keyword.strip())
        if string:
            if string[0].isdigit():
                return "qt"
            if string[0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
                test = string[0].lower()
                return test
            c = re.search(u"[\u4e00-\u9fa5]+", string)
            if c:
                test = "".join(lazy_pinyin(string))[0]
                return test

            else:
                return "qt"

    else:
        pass


if __name__ == "__main__":
    for string in ["", " ", "你好", "re", "CD", ".dfe", ";e"]:
        # for string in ["1明天", "q明天", "aa11","33dd"]:
        aa = pinyin_change(string)
        print(aa)
