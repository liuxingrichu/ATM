#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import settings
from modules import common

# 初始化数据表
_shopping_list = {
    "1": {"typename": "食品生鲜", "product": (
        {"no": "0001", "name": "进口牛奶 欧德堡(Oldenburger)1L*12", "price": 95},
        {"no": "0002", "name": "乐虎氨基酸维生素功能饮料250ML*24罐", "price": 120},
        {"no": "0003", "name": "意大利进口 Ferrero Rocher费列罗巧克力(盒)", "price": 205},
        {"no": "0004", "name": "品湖韵阳澄湖大闸蟹礼券1388型 8只", "price": 458},
        {"no": "0005", "name": "三胖蛋 正宗内蒙原味大瓜子218g*6桶/礼", "price": 168},
        {"no": "0006", "name": "臻味山珍礼盒 吉年纳福1600g干菌山珍大礼包", "price": 256}
    )},
    "2": {"typename": "数码产品", "product": (
        {"no": "1001", "name": "佳能（Canon） EOS 6D 单反机身（不含镜头） 家庭套餐", "price": 9326},
        {"no": "1002", "name": "360安全路由P1 3mm纤薄设计 大户型智能无线路由器", "price": 89},
        {"no": "1003", "name": "小米 4c 高配版 全网通 白色 移动联通电信", "price": 1499},
        {"no": "1004", "name": "华为（HUAWEI）荣耀手环zero 经典黑短", "price": 399},
        {"no": "1005", "name": "步步高（BBK）家教机S2 香槟金 32G ", "price": 3468},
        {"no": "1006", "name": "Apple MacBook Air 13.3英寸笔记本电脑", "price": 6988}
    )},
    "3": {"typename": "男装女装", "product": (
        {"no": "2001", "name": "伊莲娜2016新款连衣裙英伦格子针织连衣裙假两件裙加厚", "price": 163},
        {"no": "2002", "name": "Maxchic玛汐2016春时尚分割修身圆领修身长袖连衣裙", "price": 235},
        {"no": "2003", "name": "2015新冬款加厚加绒牛仔裤女保暖小脚裤大码弹力铅笔裤", "price": 169},
        {"no": "2004", "name": "秋冬新款青年男士休闲连帽羽绒服男韩版修身短款外套", "price": 319},
        {"no": "2005", "name": "AAPE秋冬季新款 时尚潮牌猿人头袖英文字母印花男士休闲", "price": 298},
        {"no": "2006", "name": "2015秋冬新款加绒保暖套头卫衣 15541707 BC17灰花灰", "price": 159}
    )}
}


_user_list = {
    "test": {"password": "12345", "name": "Tom", "mobile": "13511111111", "islocked": 0, "role": "user"},
    "super": {"password": "12345", "name": "Admin", "mobile": "15257157418", "islocked": 0, "role": "admin"},
}

_creditcard_list = {
    "1001012345": {"password": "12345", "credit_balance": settings.CREDIT_TOTAL, "frozenstatus": 0},
    "1001010002": {"password": "12345", "credit_balance": settings.CREDIT_TOTAL, "frozenstatus": 0},
}

def init_db_users():
    """
    初始化用户信息
    :return:无
    """
    _db_file = os.path.join(settings.DATABASE["dbpath"], "users.db")
    with open(_db_file, "w", encoding="utf-8") as f:
        for k in _user_list:
            tmp_password = _user_list[k]["password"]
            encrypt_password = common.encrypt(tmp_password)
            _user_list[k]["password"] = encrypt_password
        f.write(json.dumps(_user_list))

def init_db_creditcard():
    _db_file = os.path.join(settings.DATABASE["dbpath"], "creditcard.db")
    with open(_db_file, "w", encoding="utf-8") as f:
        for k in _creditcard_list:
            tmp_password = _creditcard_list[k]["password"]
            encrypt_password = common.encrypt(tmp_password)
            _creditcard_list[k]["password"] = encrypt_password
        f.write(json.dumps(_creditcard_list))

if __name__ == '__main__':
    _db_file = os.path.join(settings.DATABASE["dbpath"], "users.db")
    if not os.path.exists(_db_file):
        init_db_users()
    else:
        print("users.db is exist!")

    _db_file = os.path.join(settings.DATABASE["dbpath"], "creditcard.db")
    if not os.path.exists(_db_file):
        init_db_creditcard()
    else:
        print("creditcard.db is exist!")
