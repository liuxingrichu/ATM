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


def login(card_id, password):
    """
    信用卡登录
    :param username: 信用卡账户
    :param password: 密码
    :return:
        成功  True
        失败  False
    """
    _db_file = os.path.join(settings.DATABASE["dbpath"], "creditcard.db")
    with open(_db_file, 'r', encoding="utf-8") as f:
        f.seek(0)
        _card_dict = json.loads(f.read())
    tmp_password = common.encrypt(password)
    if card_id not in _card_dict:
        print("\t\033[0;31m卡号不存在！\033[0m")
        return sys_code.CARD_NOT_EXISTS
    else:
        if tmp_password == _card_dict[card_id]["password"]:
            print("\t\033[0;32mWelcome %s\033[0m" % card_id)
            return sys_code.SUCCESS
        else:
            print("\t\033[0;31m密码错误！\033[0m")
            return sys_code.CARD_PASS_ERROR


def write_card_record(card_id, type, amount):
    """
    写信用卡消费信息
    :param card_id: 卡号
    :param type: 类型
    :param amount: 金额
    :return:无
    """
    _filename = os.path.join(settings.REPORT_PATH, "creditcard.db")
    data_list = [str(datetime.now()), str(card_id), type, str(amount)]
    with open(_filename, "a+", encoding="utf-8") as f:
        f.write("\n")
        f.write(" ".join(data_list))
        f.flush()


def consume(card_id, amount):
    """
    信用卡消费
    :param card_id: 卡号
    :param amount: 金额
    :return:
    """
    _db_file = os.path.join(settings.DATABASE["dbpath"], "creditcard.db")
    with open(_db_file, 'r', encoding="utf-8") as f:
        _card_dict = json.loads(f.read())

    if _card_dict[card_id]["frozenstatus"] == 1:
        print("\t\033[0;31m%s is frozen. Please contact administrator.\033[0m" % card_id)
        return False
    else:
       if _card_dict[card_id]["credit_balance"] >= amount + amount*settings.TRANSACTION_TYPE["consume"]["interest"]:
           _card_dict[card_id]["credit_balance"] = _card_dict[card_id]["credit_balance"] - amount - \
                                                   amount*settings.TRANSACTION_TYPE["consume"]["interest"]

           _db_file = os.path.join(settings.DATABASE["dbpath"], "creditcard.db")
           with open(_db_file, 'w', encoding="utf-8") as f:
               f.seek(0)
               f.write(json.dumps(_card_dict))
               f.flush()

           #写信用卡消费信息
           write_card_record(card_id,"consume", amount)
           print("\t欢迎下次光临购物商城.")
           return True
       else:
           print("\t\033[0;31m信用卡余额不足！\033[0m")
           return False


def card_frozen(card_id):
    """
    冻结信用卡
    :param card_id: 卡号
    :return:无
    """
    _db_file = os.path.join(settings.DATABASE["dbpath"], "creditcard.db")
    with open(_db_file, 'r+', encoding="utf-8") as f:
        _card_dict = json.loads(f.read())
        _card_dict[card_id]["frozenstatus"] = 1
        f.seek(0)
        f.write(json.dumps(_card_dict))
    print("\t\033[0;31m%s is frozen. Please contact administrator.\033[0m" % card_id)


def withdraw(card_id, amount):
    """
    提现
    :param card_id: 卡号
    :param amount: 金额
    :return:状态码
    """
    _db_file = os.path.join(settings.DATABASE["dbpath"], "creditcard.db")
    with open(_db_file, 'r', encoding="utf-8") as f:
        _card_dict = json.loads(f.read())

    if _card_dict[card_id]["frozenstatus"] == 1:
        print("\t\033[0;31m%s is frozen. Please contact administrator.\033[0m" % card_id)
        return sys_code.CARD_FROZEN
    else:
        if _card_dict[card_id]["credit_balance"] >= amount + amount*settings.TRANSACTION_TYPE["withdraw"]["interest"]:
            _card_dict[card_id]["credit_balance"] = _card_dict[card_id]["credit_balance"] - amount - \
                                                   amount*settings.TRANSACTION_TYPE["withdraw"]["interest"]

            _db_file = os.path.join(settings.DATABASE["dbpath"], "creditcard.db")
            with open(_db_file, 'w', encoding="utf-8") as f:
               f.seek(0)
               f.write(json.dumps(_card_dict))
               f.flush()
            return sys_code.SUCCESS
        else:
            return sys_code.BALANCE_NOT_ENOUGH

def transfer(card_id_one, card_id_two, amount):
    """
    转账
    :param card_id_one: 卡号
    :param card_id_two: 对方卡号
    :param amount: 金额
    :return:状态码
    """
    _db_file = os.path.join(settings.DATABASE["dbpath"], "creditcard.db")
    with open(_db_file, 'r', encoding="utf-8") as f:
        _card_dict = json.loads(f.read())

    if _card_dict[card_id_one]["frozenstatus"] == 1:
        print("\t\033[0;31m%s is frozen. Please contact administrator.\033[0m" % card_id_one)
        return sys_code.CARD_FROZEN
    elif _card_dict[card_id_two]["frozenstatus"] == 1:
        print("\t\033[0;31m%s is frozen. Please contact administrator.\033[0m" % card_id_two)
        return sys_code.CARD_FROZEN_OTHER
    else:
        if _card_dict[card_id_one]["credit_balance"] >= amount + amount*settings.TRANSACTION_TYPE["transfer"]["interest"]:
            _card_dict[card_id_one]["credit_balance"] = _card_dict[card_id_one]["credit_balance"] - amount - \
                                                       amount*settings.TRANSACTION_TYPE["transfer"]["interest"]

            _card_dict[card_id_two]["credit_balance"] += amount

            _db_file = os.path.join(settings.DATABASE["dbpath"], "creditcard.db")
            with open(_db_file, 'w', encoding="utf-8") as f:
               f.seek(0)
               f.write(json.dumps(_card_dict))
               f.flush()
            return sys_code.SUCCESS
        else:
            return sys_code.BALANCE_NOT_ENOUGH


def repay(card_id, amount):
    """
    还款
    :param card_id: 卡号
    :param amount: 金额
    :return:状态码
    """
    _db_file = os.path.join(settings.DATABASE["dbpath"], "creditcard.db")
    with open(_db_file, 'r', encoding="utf-8") as f:
        _card_dict = json.loads(f.read())

    if _card_dict[card_id]["frozenstatus"]:
        print("\t\033[0;31m%s is frozen. Please contact administrator.\033[0m" % card_id)
        return sys_code.CARD_FROZEN
    else:
        _card_dict[card_id]["credit_balance"] = _card_dict[card_id]["credit_balance"] + amount - \
                                               amount*settings.TRANSACTION_TYPE["repay"]["interest"]

        _db_file = os.path.join(settings.DATABASE["dbpath"], "creditcard.db")
        with open(_db_file, 'w', encoding="utf-8") as f:
           f.seek(0)
           f.write(json.dumps(_card_dict))
           f.flush()
        return sys_code.SUCCESS


def card_main(card_id):
    """
    ATM对信用卡信息、提现、转账、还款、对账单操作
    :param card_id: 卡号
    :return:无
    """
    while True:
        print(templates.credit_card)
        choice = input("Enter number : ")
        if choice == "1":
            _db_file = os.path.join(settings.DATABASE["dbpath"], "creditcard.db")
            with open(_db_file, 'r', encoding="utf-8") as f:
                _card_dict = json.loads(f.read())
            if _card_dict[card_id]["frozenstatus"]:
                _status = "冻结"
            else:
                _status = "正常"
            print(templates.card_info.format(cardno=card_id, total=settings.CREDIT_TOTAL,
                                             balance=_card_dict[card_id]["credit_balance"],
                                             status=_status))
        elif choice == "2":
            amount = int(input("withdraw amount : ").strip())
            res = withdraw(card_id, amount)
            if res == sys_code.SUCCESS:
                write_card_record(card_id, "withdraw", amount)
                print("\t\033[0;32mwithdraw %s success\033[0m" % amount)
            elif res == sys_code.BALANCE_NOT_ENOUGH:
                print("\t\033[0;31m余额不足！\033[0m")
            else:
                print("\t\033[0;31m%s is frozen. Please contact administrator.\033[0m" % card_id)
        elif choice == "3":
            amount = int(input("transfer amount : ").strip())
            card_id_two = input("transfer card id :")
            res = transfer(card_id, card_id_two, amount)
            if sys_code.SUCCESS:
                type = "transfer" + " " + card_id_two
                write_card_record(card_id, type, amount)
                print("\t\033[0;32mtransfer from %s to %s : %s\033[0m" % (card_id, card_id_two, amount))
            elif res == sys_code.BALANCE_NOT_ENOUGH:
                print("\t\033[0;31m余额不足！\033[0m")
            elif res == sys_code.CARD_FROZEN:
                print("\t\033[0;31m%s is frozen. Please contact administrator.\033[0m" % card_id)
            elif res == sys_code.CARD_FROZEN_OTHER:
                print("\t\033[0;31m%s is frozen. Please contact your friend.\033[0m" % card_id_two)
        elif choice == "4":
            amount = int(input("repay amount : ").strip())
            res = repay(card_id, amount)
            if res == sys_code.SUCCESS:
                write_card_record(card_id, "repay", amount)
                print("\t\033[0;32m%s repay %s success\033[0m" % (card_id, amount))
            else:
                print("\t\033[0;31m%s is frozen. Please contact administrator.\033[0m" % card_id)
        elif choice == "5":
            _filename = os.path.join(settings.REPORT_PATH, "creditcard.db")
            print("信用卡账单信息".center(55, "*"))
            with open(_filename, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        print(line)
            print("end".center(60, "*"))
        elif choice == "6":
            break