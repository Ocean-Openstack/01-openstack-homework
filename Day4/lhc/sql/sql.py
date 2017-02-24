#!/usr/bin/env python
#coding=utf-8

#############》》 select语句函数  《《##################
dict={'id':0,'name':1,'age':2,'phone':3,'bm':4,'time':5}
def select(cmd):
    '''
    :return:
    '''

    with open('old') as fn:
        if cmd[1] == '*':
            print (fn.read())
        else:
            if cmd[1] in dict:
                i_d=dict[cmd[1]]
                for line in fn:
                    I_D=line.split(',')
                    print(I_D[i_d])
#######################################################

#############》》 delete语句函数  《《##################

def delete(cmd):
    '''

    :return:
    '''
    import os
    old_fn=open('old','r')
    new_fn=open('new','w')
    for line in old_fn:
        Line=line.split(',')
        if cmd_l[-1] == Line[0]:
            continue
        new_fn.write(line)
    old_fn.close()
    new_fn.close()
    os.rename('old','.old.swp')
    os.rename('new','old')
#######################################################

#############》》 update语句函数  《《##################
def update(cmd_l):
    '''

    :return:
    '''
    import re
    import os
    old_fn=open('old','r')
    new_fn=open('new','w')
    for old_line in old_fn.readlines():
        Old_line=old_line.split(',')
        if cmd_l[-1] == Old_line[0]:
            gengxin=input('请输入要更新的内容：')
            new_fn.write(gengxin + '\n')
            continue
        new_fn.write(old_line)
    old_fn.close()
    new_fn.close()
    os.rename('old','.old.swp')
    os.rename('new','old')
#######################################################

#############》》 insert语句函数  《《##################
def insert():
    '''

    :return:
    '''
    import os
    old_fn=open('old','r')
    new_fn=open('new','w')
    charu=input('请插入信息：')
    for old_line in old_fn.readlines():
        if charu in old_line:
            print ('此数据已存在！')
            continue
        else:
            new_fn.write(old_line)
            continue
    new_fn.write('\n' + charu)
    old_fn.close()
    new_fn.close()
    os.rename('old','old.swp')
    os.rename('new','old')
#######################################################

cmd_dic={
    'select':select,
    'insert':insert,
    'update':update,
    'delete':delete,
}
while True:
    cmd = input('sql>:')
    if cmd == 'exit':break
    cmd_l=cmd.split()
    CMD=cmd_l[0]
    if CMD not in cmd_dic:
        print('Error')
    else:
        cmd_dic[CMD](cmd_l)




