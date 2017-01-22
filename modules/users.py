#!/usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import datetime
import json
import os
import sys

from conf import settings
from conf import sys_code
from conf import templates
from modules import common


def auth(func):
    """
    通过手机号认证用户
    :param func: 用户登录函数
    :return:无
    """
    def inner(*args, **kwargs):
        res = func(*args, **kwargs)
        if res == sys_code.SUCCESS:
            phone = input("Enter your phone number: ")
            while len(phone) != 11:
                print("\t\033[0;31mYour phone number is wrong!\033[0m")
                phone = input("Enter your phone number: ")
            code = common.identifying_code()
            print("\tYour identify code : %s" %  code)
            _code = input("Enter your identify code : ")
            while _code != code:
                print("\t\033[0;31mYour identify code is wrong!\033[0m")
                _code = input("Enter your identify code : ")
                if _code == code:
                    break
        return res
    return inner


@auth
def login(username, password):
    """
    用户登录
    :param username: 用户名
    :param password: 密码
    :return:状态码
    """
    _db_file = os.path.join(settings.DATABASE["dbpath"], "users.db")
    with open(_db_file, 'r', encoding="utf-8") as f:
        _users_dict = json.loads(f.read())
    tmp_password = common.encrypt(password)
    if username not in _users_dict:
        print("\t\033[0;31m用户不存在！\033[0m")
        return sys_code.USER_NOT_EXISTS
    else:
        if tmp_password == _users_dict[username]["password"]:
            if _users_dict[username]["islocked"] == 1:
                print("\t\033[0;31m%s is locked. Please contact administrator.\033[0m" % username)
                return sys_code.USER_LOCKED
            else:
                print("\t\033[0;32mWelcome %s\033[0m" % username)
                return sys_code.SUCCESS
        else:
            print("\t\033[0;31m密码错误！\033[0m")
            return sys_code.USER_PASS_ERROR


def write_shopping_record(card_id, user_cart):
    """
    写购物记录
    :param card_id: 卡号
    :param user_cart: 购物信息
    :return:无
    """
    _filename = os.path.join(settings.REPORT_PATH, "shopping.db")
    with open(_filename, "a+", encoding="utf-8") as f:
        f.write("\n")
        f.write(str(datetime.now()))
        f.write("   ")
        f.write(card_id)
        f.write("\n")
        for i in range(len(user_cart)):
            f.write(json.dumps(user_cart[i]))
            f.write("\n")
        f.flush()


def user_main(username):
    """
    用户系统
    :param username: 用户名
    :return:无
    """
    while True:
        print(templates.user_login)
        choice = input("Enter number : ")
        if choice == "1":
            _db_file = os.path.join(settings.DATABASE["dbpath"], "users.db")
            with open(_db_file, 'r', encoding="utf-8") as f:
                _users_dict = json.loads(f.read())
            if _users_dict[username]["islocked"]:
                _islocked = "是"
            else:
                _islocked = "否"

            print(templates.user_info.format(name=_users_dict[username]["name"],
                                             mobile=_users_dict[username]["mobile"],
                                             islocked=_islocked))
        elif choice == "2":
            _filename = os.path.join(settings.REPORT_PATH, "shopping.db")
            print("用户历史购物单".center(55, "*"))
            with open(_filename, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.startswith("{"):
                        if line.strip():
                            print(line)
                    else:
                        line_dict = json.loads(line)
                        print("{} {} {}".format(line_dict["no"], line_dict["name"], line_dict["price"]))
            print("end".center(60, "*"))
        elif choice == "3":
            break