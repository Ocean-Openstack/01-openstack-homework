#!/usr/bin/env python
#-*-coding:utf-8-*-
def user_info():
    file = open('user_info')
    data=file.readlines()
    list_info=[]
    for i in data:
        lis=[i.strip()]
        for s in lis:
            result = [ele.strip() for ele in s.split(",")]
            dict_info={}
            for x in result:
                res = [ele.strip() for ele in x.split(':')]
                dict_info.update(dict([res]))
            list_info.append(dict_info)
    return list_info

user_list=user_info()

def help():
    print(user_list)

current_user={'username':None,'login':False}
def auth(auth_type='file'):
    def auth_deco(func):
        def wrapper(*args,**kwargs):
            if auth_type == 'file':
                if current_user['username'] and current_user['login']:
                    res=func(*args,**kwargs)
                    return res
                username=input('用户名: ').strip()
                passwd=input('密码: ').strip()

                for index,user_dic in enumerate(user_list):
                    if username == user_dic['name'] and passwd == user_dic['passwd']:
                        current_user['username']=username
                        current_user['login']=True
                        res=func(*args,**kwargs)
                        return res
                        break
                else:
                    print('用户名或者密码错误,重新登录')
            elif auth_type == 'ldap':
                print('我是ldap')
                res=func(*args,**kwargs)
                return res
        return wrapper
    return auth_deco

@auth(auth_type='ldap')
def index():
    print('欢迎来到主页面')

@auth(auth_type='file')
def home():
    print('到家了')

index()

print(user_list)
home()