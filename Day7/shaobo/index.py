#!/usr/bin/python
from operate import *

def index(username):
    msg='''
    尊敬的用户： %s，欢迎来到您的个人主页
    1.查询
    2.提现
    3.转账
    4.还款
    5.购物
    6.流水'''
    oper_dic={
        'q':'break',
        '1':inquire,
        '2':withdraw,
        '3':transfer,
        '4':repayment,
        '5':shop,
        '6':bill
    }

    if username == 'admin':
        oper_dic['7']=manage
        msg=msg+'\n    7.账户管理'

    while True:
        print(msg % username)
        print('\t所有页面均可选择"q"退出\n')
        sel=input('Please input your select: ')
        print('\n')
        if sel not in oper_dic:
            print('Please input the right select')
            continue
        elif sel=='q':
            break

        oper_dic[sel](username)

