#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import os
import sys

from conf import settings
from conf import sys_code
from conf import templates
from modules import common


def create_user(user_info):
    """
    创建用户
    :param user_info: 用户信息
    :return:无
    {"book": {"password": "12345", "name": "Lucy", "mobile": "13511111112", "islocked": 0, "role": "user"}}
    """
    _db_file = os.path.join(settings.DATABASE["dbpath"], "users.db")
    with open(_db_file, 'r', encoding="utf-8") as f:
        _users_dict = json.loads(f.read())
    tmp_dict = json.loads(user_info)
    _users_dict.update(tmp_dict)
    with open(_db_file, 'w', encoding="utf-8") as f:
        f.write(json.dumps(_users_dict))


def user_lock(username):
    """
    锁定用户
    :param username: 用户名
    :return:无
    """
    _db_file = os.path.join(settings.DATABASE["dbpath"], "users.db")
    with open(_db_file, 'r+', encoding="utf-8") as f:
        _users_dict = json.loads(f.read())
        _users_dict[username]["islocked"] = 1
        f.seek(0)
        f.write(json.dumps(_users_dict))
        f.flush()


def login(username, password):
    """
    管理员登录
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
        if tmp_password == _users_dict[username]["password"] \
                and _users_dict[username]["role"] == "admin":
            print("\t\033[0;32mWelcome %s\033[0m" % username)
            return sys_code.SUCCESS
        else:
            print("\t\033[0;31m密码错误！\033[0m")
            return sys_code.USER_PASS_ERROR


def manage_main():
    while True:
        print(templates.manager_login)
        choice = input("Enter number : ")
        if choice == "1":
            info = input("username info : ").strip()
            create_user(info)
            print("\t\033[0;32mcreate user success\033[0m")
        elif choice == "2":
            username = input("Enter username : ")
            user_lock(username)
            print("\t\033[0;32mlock user success\033[0m")
        elif choice == "3":
            break