#!/usr/bin/env python
#coding=utf-8

import os
import functools
def init(func):
    @functools.wraps(func)
    def wapper(*args,**kwargs):
        '这是wrapper'
        g=func(*args,**kwargs)
        next(g)
        return g
    return wapper


def get_file(abs_path,target):
    '生产一个个的文件绝对路径'
    g=os.walk(abs_path)
    for topdir,cdir,files in g:
        for file in files:
            abs_file_path=r'%s\%s' %(topdir,file)
            target.send(abs_file_path)
@init
def opener(target):
    '打开文件获取句柄'
    while True:
        abs_file_path=yield
        with open(abs_file_path) as f:
            target.send((f,abs_file_path))
@init
def get_lines(target):
    '读取文件每一行'
    while True:
        f,abs_file_path=yield
        for line in f:
            target.send((line,abs_file_path))
@init
def grep(pattern,target):
    '过滤行得到想要的信息'
    while True:
        line,abs_file_path=yield
        if pattern in line:
            target.send((abs_file_path))
@init
def printer():
    while True:
        abs_file_path=yield
        print(abs_file_path)

file_name=get_file(r'E:\test',opener(get_lines(grep('python',printer()))))