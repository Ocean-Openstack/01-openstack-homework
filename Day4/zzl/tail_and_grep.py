#!/usr/bin/env python
#-*-coding:utf-8-*-

import time
def tail(file_path):
    f=open(file_path,'r')
    f.seek(0,2)
    while True:
        line=f.readline()
        if not line:
            time.sleep(0.1)
        else:
            yield line

g=tail('access.log')
for i in g:
    if "404" in i:
        print(i)