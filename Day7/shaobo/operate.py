#!/usr/bin/python
from base import *

def inquire(user):
    file_dir=get_file_dir('user.db')
    atm_db=json_load(file_dir)
    user_balance=atm_db[user]['balance']
    print('尊敬的用户您当前余额为：[%s]'% user_balance)
    return file_dir,atm_db,user_balance



def withdraw(user):
    file_dir,atm_db,user_balance=inquire(user)
    aom=input('请输入您要提现的金额: ')
    user_balance=user_balance-int(aom)
    atm_db[user]['balance']=user_balance
    json_write(file_dir,atm_db)
    print('您当前余额为：[%s]'% user_balance)

    bills='用户[%s]提现[%s]' %(user,aom)
    write_bill_log(user,bills)


def repayment(user):
    file_dir,atm_db,user_balance=inquire(user)
    aom=input('请输入您还款的金额: ')
    user_balance=user_balance+int(aom)
    atm_db[user]['balance']=user_balance
    json_write(file_dir,atm_db)
    print('您当前余额为：[%s]'% user_balance)

    bills='用户[%s]还款[%s]' %(user,aom)
    write_bill_log(user,bills)

def transfer(user):
    file_dir,atm_db,user_balance=inquire(user)
    t_user=input('请输入您要转账的用户: ')
    aom=input('请输入您转账的金额: ')
    t_user_balance=atm_db[t_user]['balance']
    user_balance=user_balance-int(aom)
    t_user_balance=t_user_balance+int(aom)
    atm_db[user]['balance']=user_balance
    atm_db[t_user]['balance']=t_user_balance
    json_write(file_dir,atm_db)
    print('转账成功！您当前余额为: [%s]' % user_balance)

    bills='用户[%s]给用户[%s]转账[%s]' %(user,t_user,aom)
    write_bill_log(user,bills)

def bill(user):
    file_name=user+'_bill.log'
    file_dir=get_file_dir(file_name)
    with open(file_dir,'r') as f:
        print(f.read())


def shop(user):
    msg='''
        1.购买商品
        2.查看清单
    '''
    print(msg)
    sel=input('请输入你的选择: ')
    if sel=='1':
        file_dir,atm_db,user_balance=inquire(user)
        shop_file=get_file_dir('shop.db')
        shop_dic=json_load(shop_file)
        print('商品清单：%s' % shop_dic)
        comm=input('请输入你要购买的商品: ')
        comm_aom=shop_dic[comm]

        user_balance=user_balance-int(comm_aom)
        atm_db[user]['balance']=user_balance
        json_write(file_dir,atm_db)

        shops='用户[%s]花费[%s]购买了商品[%s] ' %(user,comm_aom,comm)
        write_shop_log(user,shops)
    elif sel=='2':
        file_name=user+'_shop.log'
        file_dir=get_file_dir(file_name)
        with open(file_dir,'r') as f:
            print(f.read())


def manage(user):
    msg='''
    1.添加账户
    2.额度查询
    3.冻结账户
    '''
    print(msg)
    sel=input('请输入你的选择： ')
    if sel=='1':
        file_dir,user_dic,_b_=inquire(user)
        username=input('请输入账户名：')
        password=input('请输入密码：')
        password=encrypt(password)
        s_dic={}
        s_dic['password']=password
        s_dic['balance']=15000
        s_dic['isfuzz']=0
        user_dic[username]=s_dic
        json_write(file_dir,user_dic)
    elif sel=='2':
        username=input('请输入你要查询的用户：')
        file_dir,_,user_balance=inquire(username)
        print('[%s]的额度是[%s]'%(username,user_balance))
    elif sel=='3':
        username=input('请输入你要冻结的用户名: ')
        file_dir,user_dic,_=inquire(username)
        user_dic[username]['isfuzz']=1
        json_write(file_dir,user_dic)

