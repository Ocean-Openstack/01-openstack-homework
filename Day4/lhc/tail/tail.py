#!/usr/bin/env python

def tail(file,key):
    with open(file, 'r') as f:
        f.seek(0, 2)
        while True:
            last_pos = f.tell()
            line = f.readline()
            if key in line:
                print (line)

tail('error.txt','127.0.0.1')
