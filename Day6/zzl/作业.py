#_*_coding:utf-8_*_
#!/usr/bin/env python

import os
import functools
def init(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        g=func(*args,**kwargs)
        next(g)
        return g
    return wrapper

def get_file(abs_path,target):
    '生产一个个文件：绝对路径'
    g=os.walk(abs_path)
    for top_dir,current_dir,files in g:
        for file in files:
            abs_file_path=r'%s\%s' %(top_dir,file)
            target.send(abs_file_path)
@init
def opener(target):
    '打开文件，获取句柄'
    while True:
        abs_file_path=yield
        with open(abs_file_path) as f:
            target.send((f,abs_file_path))
@init
def get_lines(target):
    '读取文件每一行的内容'
    while True:
        f,abs_file_path=yield
        for line in f:
            target.send((line,abs_file_path))
@init
def grep(pattern,target):
    '过滤行，得到你要的东西'
    while True:
        line,abs_file_path=yield
        if pattern in line:
            target.send(abs_file_path)
@init
def printer():
    while True:
        abs_file_path=yield
        print(abs_file_path)

file_name=get_file(r'D:\t1',opener(get_lines(grep('python',printer()))))





