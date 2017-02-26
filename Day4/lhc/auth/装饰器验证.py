#!/usr/bin/env python
#coding=utf-8


def auth_login(file,auth_type):
    def func(func):
        def wapper(*args,**kwargs):
            if auth_type == 'file':
                name=input('please input name:').strip()
                passwd = input('please input passwd:').strip()
                with open(file) as fn:
                    for i in fn:
                        if name in i and passwd in i:
                            print('login successful!')
                            func(*args,**kwargs)
                            break
                        else:
                            print('用户名或密码错误')
            elif auth_type=='ladp':
                print('The user use ladp login, login successful')
                res = func(*args,**kwargs)
                return res
        return wapper
    return func

@auth_login('db.txt',auth_type='file')
def foo():
    print('welecom to home')
foo()