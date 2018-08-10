#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/10/22 23:07"

import hashlib
import time


def mad5_url(urls):
    '''mad加密功能
    parmes：对每个文章url链接md5加密相同长度的指纹
    '''

    if isinstance(urls, str):  # py3里全是uncode字符集 也就是str，md5前判断 因为py3 unicode不能直接md5必须转换utf-8，相反py2则不用
        urls = urls.encode("utf-8")
    md5_url = hashlib.md5()
    md5_url.update(urls)
    md5_url.hexdigest()
    # print(md5_url.hexdigest())
    return md5_url.hexdigest()


def getsecret():
    innerApp = "pythontool"
    secret = "a6d903a2-dac5-4d9d-9e6b-e32caad1dafc"
    ts = str(int(time.time() * 1000))
    sign = "innerApp=" + innerApp + "&secret=" + secret + "&ts=" + ts
    singn = mad5_url(sign)
    return singn, innerApp, ts


def getsecret2(ts):
    innerApp = "cms"
    secret = "f7f0f6f6-a101-4290-9c8c-144d2b286b7b"
    sign = "innerApp=" + innerApp + "&secret=" + secret + "&ts=" + ts
    singn = mad5_url(sign)
    return singn, innerApp, ts


if __name__ == "__main__":
    ts = "111111"
    # print(ts.isdigit())
    a = mad5_url(ts)
    print(a)
    before = time.time()
    print(before)
