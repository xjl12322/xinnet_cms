#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"

import logging


class Log(object):
    def __init__(self):
        self.logging_path = "rzi.txt"
        self.logger = logging.getLogger()  # 创建logger对象
        self.logger.setLevel(logging.DEBUG)  # 设置logger对象的级别 DEBUG以上
        self.fileHandler = logging.FileHandler(
            self.logging_path)  # 生成一个Handler（logger）。logging支持许多Handler，例如FileHandler, SocketHandler, SMTPHandler等，  我由于要写文件就使用了FileHandler
        self.fileHandler.setLevel(logging.DEBUG)  # 设置logger文件对象fileHandler对象的级别 debug以上
