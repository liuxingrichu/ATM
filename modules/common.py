#!/usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import datetime
import hashlib
import logging
import os
import random
import sys

from conf import settings


def identifying_code(lenth=6):
    """
    默认生成6位数字的随机验证码
    :return:返回验证码
    """
    _code = list()
    for i in range(lenth):
        _code.append(str(random.randrange(0, 9)))
    return "".join(_code)


def encrypt(string):
    """
    加密字符串
    :param string: 待加密字符串
    :return:返回加密字符串
    """
    ha = hashlib.md5(b"123abc")
    ha.update(string.encode("utf-8"))
    return ha.hexdigest()