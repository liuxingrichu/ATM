#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
系统代码表
"""
SUCCESS = 200                  # 成功
USER_LOCKED = 201              # 用户被锁定
CARD_FROZEN = 202              # 信用卡冻结
CARD_FROZEN_OTHER = 203        # 对方信用卡冻结
USER_NOT_EXISTS = 10000        # 用户名不存在
CARD_NOT_EXISTS = 10001        # 信用卡不存在
BALANCE_NOT_ENOUGH = 10002    # 信用卡余额不足
CARD_PASS_ERROR = 10003        # 信用卡密码错误
USER_PASS_ERROR = 10004        # 用户密码错误