#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys


# 程序文件主目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 添加环境变量
sys.path.append(BASE_DIR)

# 数据库信息
DATABASE = dict(engineer="file",
                dbpath=os.path.join(BASE_DIR, "database"),
                )

# 日志文件存放路径
REPORT_PATH = os.path.join(BASE_DIR, "report")
# 用户登录失败最大次数
ERROR_MAX_COUNT = 3
# 日息费率
EXPIRE_DAY_RATE = 0.0005
# 转账、提现手续费
FETCH_MONEY_RATE = 0.05
# 还款、消费手续费
COMMON_MONEY_RATE = 0
# 信用额度
CREDIT_TOTAL = 15000

#信用卡交易类型
TRANSACTION_TYPE = {
    'withdraw': {'action': 'minus', 'interest': FETCH_MONEY_RATE},
    'transfer': {'action': 'minus', 'interest': FETCH_MONEY_RATE},
    'repay':{'action': 'plus', 'interest': COMMON_MONEY_RATE},
    'consume': {'action': 'minus', 'interest': COMMON_MONEY_RATE}
}