#!/usr/bin/env python
import sys
import time

def tail(file_name,key):
    with open(file_name) as f:
        f.seek(0,2) #zui hou yi hang
        while True:
            line=f.readline()
            if key in line:
                sys.stdout.write(line)
            time.sleep(1)

tail('test.txt','awm')
