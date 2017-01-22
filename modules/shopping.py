#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import os
import sys

from conf import settings
from conf import sys_code
from conf import templates
from modules import creditcard
from database import init_db
from modules import manage
from modules import users


def show_goods():
    """
    显示商品信息
    :return:无
    """
    for k in init_db._shopping_list:
        print("{} {}".format(k, init_db._shopping_list[k]["typename"]))
        for i in range(len(init_db._shopping_list[k]["product"])):
            print("\t{} {} {}".format(init_db._shopping_list[k]["product"][i]["no"],\
                                 init_db._shopping_list[k]["product"][i]["name"],\
                                 init_db._shopping_list[k]["product"][i]["price"]))


user_cart = list()
def shopping_cart():
    """
    购物
    :return:用户名
    """
    count = 0
    user_flag = False
    exit_flag = False
    while count < settings.ERROR_MAX_COUNT and not exit_flag:
        if user_flag and not exit_flag:
            while not exit_flag:
                choice = input("请选择商品编码：")
                if choice == 'q':
                    print("购物车信息".center(56, '-'))
                    for i in range(len(user_cart)):
                        print("{} {} {}".format(user_cart[i]["no"],
                                                user_cart[i]["name"],
                                                user_cart[i]["price"]))
                    print("end".center(60, "-"))
                    exit_flag = True

                for k in init_db._shopping_list:
                    for i in range(len(init_db._shopping_list[k]["product"])):
                        if choice not in init_db._shopping_list[k]["product"][i]["no"]:
                            continue
                        else:
                            num = int(choice[1:]) - 1
                            user_cart.append(init_db._shopping_list[k]["product"][num])
                            print("\t\033[0;32m%s\033[0m 已添加到购物车" % init_db._shopping_list[k]["product"][i]["name"])
        else:
            username = input("Enter username : ")
            password = input("Enter password : ")
            status = users.login(username, password)
            if status == sys_code.SUCCESS:
                user_flag = True
            elif status == sys_code.USER_PASS_ERROR:
                count += 1

    #锁定用户
    if not user_flag and count >= settings.ERROR_MAX_COUNT:
        manage.user_lock(username)
        print("\t\033[0;31m%s is locked. Please contact administrator.\033[0m" % username)


def checkout():
    """
    结账
    :param username: 用户名
    :return:无
    """
    count = 0
    card_flag = False
    while count < settings.ERROR_MAX_COUNT and not card_flag:
        card_id = input("Enter card id : ")
        password = input("Enter password : ")
        status = creditcard.login(card_id, password)
        if status == sys_code.CARD_PASS_ERROR:
            count += 1
        if status == sys_code.SUCCESS:
            card_flag = True
            amount = 0
            for i in range(len(user_cart)):
                amount += user_cart[i]["price"]

            res = creditcard.consume(card_id, amount)

            #写购物记录
            if res:
                users.write_shopping_record(card_id, user_cart)

    if not card_flag and count >= settings.ERROR_MAX_COUNT:
        creditcard.card_frozen(card_id)


shopping_mart_dic = {
    "1":show_goods,
    "2":shopping_cart,
    "3":checkout,
}


def shopping_main():

    while True:
        print(templates.shopping_mart)
        choice = input("Enter: ")
        if choice == "4":
            break
        shopping_mart_dic[choice]()