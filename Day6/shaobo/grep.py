#!/usr/bin/python

#  实现功能在一个目录下找到带有”python“字样的文件
#例：grep -rl 'python' /root

import os
import functools



def base(func):
    '''
       实现功能的装饰器
    '''

    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        res=func(*args,**kwargs)
        next(res)
        return res
    return wrapper

def get_file(abs_path,target):
    '生产一个个文件：绝对路径'
    g=os.walk(abs_path)
    for top_dir,_,files in g:
        for file in files:
            abs_file_path=top_dir+'/'+file
            target.send(abs_file_path)
@base
def opener(target):
    '打开文件，获取句柄'
    while True:
        abs_file_path=yield
        with open(abs_file_path) as f:
            target.send((f,abs_file_path))


@base
def get_lines(target):
    '读取文件每一行的内容'
    while True:
        f,abs_file_path=yield
        for line in f:
            target.send((line,abs_file_path))

@base
def grep(pattern,target):
    '过滤行，得到想要的'
    while True:
        line,abs_file_path=yield
        if pattern in line:
            target.send(abs_file_path)
@base
def printer():
    while True:
        abs_file_path=yield
        print(abs_file_path)

def main():
    get_file(r'/root/test',opener(get_lines(grep('python',printer()))))

if __name__ == '__main__':
    main()



