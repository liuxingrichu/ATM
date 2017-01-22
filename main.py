#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import sys_code
from conf import templates
from modules import creditcard
from modules import manage
from modules import shopping
from modules import users


if __name__ == '__main__':
    while True:
        print(templates.first_menu)
        choice = input("Enter number : ")
        if choice == "1":
            shopping.shopping_main()
        elif choice == "2":
            username = input("username :")
            password = input("password :")
            res = users.login(username, password)
            if res == sys_code.SUCCESS:
                users.user_main(username)
        elif choice == "3":
            card_id = input("Enter card id : ")
            password = input("Enter password : ")
            status = creditcard.login(card_id, password)
            if status == sys_code.SUCCESS:
                creditcard.card_main(card_id)
        elif choice == "4":
            username = input("username :")
            password = input("password :")
            res = manage.login(username, password)
            if res == sys_code.SUCCESS:
                manage.manage_main()
        elif choice == "5":
            print("\t欢迎下次光顾")
            break