#!/usr/bin/python
import hashlib
import os
import json
import time

def get_file_dir(file_name):
    fn_end=file_name.split('.')
    if file_name.endswith(fn_end[-1]):
        BASE_DIR='%s/%s/%s' %(os.getcwd(),fn_end[-1],file_name)

    return BASE_DIR


def json_write(file_dir,data):
    with open(file_dir,'w') as fd:
        fd.write(json.dumps(data))

def json_load(file_dir):
    with open(file_dir,'r') as fl:
        dic_j=json.load(fl)
    return dic_j

def write_bill_log(user,bill):
    file_name=user+'_bill.log'
    file_dir=get_file_dir(file_name)
    with open(file_dir,'a') as fb:
        bill='[%s] %s \n' % (time.ctime(),bill)
        fb.write(bill)

def write_shop_log(user,shop):
    file_name=user+'_shop.log'
    file_dir=get_file_dir(file_name)
    with open(file_dir,'a') as fb:
        shop='[%s] %s \n' % (time.ctime(),shop)
        fb.write(shop)


def encrypt(password):
    hash_pass=hashlib.md5(b'awm')
    hash_pass.update(password.encode('utf-8'))
    password=hash_pass.hexdigest()
    return password
