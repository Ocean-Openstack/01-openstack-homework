#!/usr/bin/env python



def auth(pass_file,auth_type):
    def deco(func):
        def wrapper(*args,**kwargs):
            if auth_type=='file':
                name=input('Please input your username: ')
                passwd=input('Please input your password: ')
                with open(pass_file) as f:
                    for line in f:
                        if name in line and passwd in line:
                            res=func(*args,**kwargs)
                            return res
#            elif auth_type=='ldap':
#                print('ldap auth success')
#                res=func(*args,**kwargs)
#                return res
        return wrapper
    return deco



@auth('db.txt',auth_type='file')
def foo():
    print('This is foo')

foo()