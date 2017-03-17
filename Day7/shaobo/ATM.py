#!/usr/bin/python
from index import index
from base import encrypt
from base import json_load
from base import get_file_dir

username=input('请输入用户名：')
password=input('请输入密码： ')
def login(username,passwd):
    def auth(func):
        def wrapper(*args,**kwargs):
            file_path=get_file_dir('user.db')
            user_dic=json_load(file_path)
            if username in user_dic:
                password=encrypt(passwd)
                if password==user_dic[username]['password']:
                    print('登录成功')
                    res=func(*args,**kwargs)
                    return res
                else:
                    print('密码错误')
            else:
                print('账号错误')
        return wrapper
    return auth

@login(username=username,passwd=password)
def main():
    msg='''
    ----------------欢迎使用奇葩信用卡专用ATM机-----------------
    ########################################################
              **        ***************   ****        ****
             ****       ***************   ** **      ** **
            **  **            ***         ** **      ** **
           **    **           ***         **  **    **  **
          **********          ***         **  **    **  **
         ************         ***         **   **  **   **
        **          **        ***         **   **  **   **
       **            **       ***         **     **     **
      **              **      ***         **     **     **
    ########################################################

    '''
    print(msg)
    index(username)




if __name__ == '__main__':
    main()
