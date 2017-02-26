#!/usr/bin/env python
import os


dic1 = {'name': 0, 'age': 1, 'phone': 2, 'carrer': 3, 'time': 4}
def select(cmd):
    # select * from t1
    table=cmd[-1]
    column=cmd[1]
    with open(table, 'r') as f1:
        if column == '*':
            print(f1.read())
        else:
            if column in dic1:
                ind = dic1[column]
                for line in f1:
                    li = line.split(',')
                    print(li[ind])

def insert(cmd):
    table=cmd[-1]
    info=cmd[1]
    with open(table,'a') as f2:
        f2.writelines(info+'\n')


def delete(cmd):
    name = cmd[1]
    table = cmd[-1]

    with open(table, 'r') as old_fn, open('new_file', 'w') as new_fn:
        for line in old_fn:
            if name in line:
                continue
            new_fn.write(line)
    bak=table+'.bak'
    file_path = 'D:/untitled/sql/' + bak
    file_exists = os.path.exists(file_path)
    if file_exists:
        os.remove(file_path)
    os.rename(table,bak)
    os.rename('new_file', table)

def update(cmd):
    col = cmd[1]
    table = cmd[-1]
    old_col = cmd[2]
    new_col = cmd[4]

    with open(table, 'r') as old_fn, open('new_file','w') as new_fn:
        for line in old_fn:
            if old_col in line:
                l = line.split(',')
                ind=dic1[col]
                l[ind] = new_col
                new_line = ','.join(l)
                new_fn.write(new_line)
                continue
            new_fn.write(line)

    bak = table + '.bak'
    file_path = 'D:/untitled/sql/' + bak
    file_exists = os.path.exists(file_path)
    if file_exists:
        os.remove(file_path)
    os.rename(table, bak)
    os.rename('new_file', table)

def main():
    msg='''
        1.select: usage-> 'select column from tname'
        2.delete: usage-> 'delete name from tname'
        3.insert: usage-> 'insert name,age,phone,carrer,time to tname'
        4.update: usage-> 'update column old to new from tname'
    '''
    print(msg)
    while True:
        res=input('Mysql> ')
        cmd1 = res.split()
        dic = {
            'select':select,
            'delete':delete,
            'insert':insert,
            'update':update
        }

        if cmd1[0] in dic:
            dic[cmd1[0]](cmd1)
        else:
            print('Please input the right CMD! ')


if __name__ == '__main__':
    main()


