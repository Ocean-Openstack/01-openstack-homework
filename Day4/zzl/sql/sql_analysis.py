#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os

#part2:格式化入口
def sql_all_analysis(sql):
    '''
    sql解析的总控
    :param sql: 用户输入的字符串
    :return: 返回字典格式sql结果
    '''
    analysis_func={                 #按照优雅的方式分开增删改查
        'insert':insert_analysis,
        'delect':delect_analysis,
        'update':update_analysis,
        'select':select_analysis,
    }
    sql_lis=sql.split(' ')
    func=sql_lis[0]
    res=''
    if func in analysis_func:
        res=analysis_func[func](sql_lis)
    else:
        print("process won't support sql，please input again ")
    return res

def insert_analysis(sql_lis):
    '''
    sql 语句insert的解析
    :param sql_lis: 按照空格切割的列表
    :return:返回字典格式的sql
    '''
    sql_dic={
        'func':insert, #函数名
        'insert':[],   #inset项
        'into':[],     #表名
        'values':[],   #values值
    }
    return handle_analysis(sql_lis,sql_dic)

def delect_analysis(sql_lis):
    '''
    sql 语句delect的解析
    :param sql_lis:按照空格切割的列表
    :return:返回字典格式的sql
    '''
    sql_dic={
        'func':delect, #函数名
        'delect':[],   #delecte项
        'from':[],     #表名
        'where':[],    #过滤条件
    }
    return handle_analysis(sql_lis,sql_dic)

def update_analysis(sql_lis):
    '''
    sql语句update的解析
    :param sql_lis: 按照空格切割的列表
    :return: 返回字典格式的sql
    '''
    sql_dic={
        'func':update,#函数名
        'update':[],  #update选项
        'set':[],     #修改的值
        'where':[],   #过滤条件
    }
    return handle_analysis(sql_lis,sql_dic)

def select_analysis(sql_lis):
    '''
    sql 语句select的解析
    :param sql_lis: 按照空格切割的列表格式sql
    :return: 返回字典格式的sql
    '''
    sql_dic={
        'func':select, #函数名
        'select':[], #查询条件
        'from':[],   #表
        'where':[],  #过滤条件
        'limit':[],  #限制条件
    }
    return handle_analysis(sql_lis,sql_dic)

def handle_analysis(sql_lis,sql_dic):
    '''
    把字典中填充进去血与肉
    :param sql_lis: 按照空格分割的列表sql
    :param sql_dic: 字典的骨头架子
    :return: 返回字典的sql格式化结果，骨肉相连
    '''
    for item in sql_lis:
        if item in sql_dic:
            key=item
            continue
        if item not in sql_dic:
            value=item
        sql_dic[key].append(value)
    if sql_dic.get('where'):
        sql_dic['where']=where_analysis(sql_dic.get('where'))
    return sql_dic

def where_analysis(where_lis):
    '''
    :param where_lis: 它是where这样的list：['id', '>', '3', 'or', 'age', '<', '20']
    :return: 返回where这样的列表:[['id', '>', '3'], 'or', ['age', '<', '20']]
    '''
    res=[]
    key=['and','or','not']
    str=''
    for i in where_lis:
        if len(i) == 0:continue
        if i in key:
            if len(str) != 0:
                str=three_analysis(str)
                res.append(str)
            res.append(i)
            str=''
        else:
           str+=i
    else:
        str=three_analysis(str)
        res.append(str)
    # print('end %s' % res)
    return res

def three_analysis(extend_str):
    '''
    将每一个小的表达式条件加入到列表里面
    :param extend_str:id>3
    :return: ['id', '>', '3']
    '''
    # print("three_analysis is %s" % extend_str)
    key=['>','=','<']
    res=[]
    char=''
    opt=''
    tag=False
    for i in extend_str:
        if i in key: #拼接key里面的>
            tag=True
            if len(char) !=0:
                res.append(char)
                char=''
            opt+=i #opt=‘<’
        if not tag:
            char+=i #拼接id
        if tag and i not in key:
            tag=False
            res.append(opt)
            opt=''
            char+=i # 运算符之后的
    else:
        res.append(char)
    if len(res) == 1:
        res=res[0].split('like')
        res.insert(1,'like')
    # print('end is %s' % res)
    return res

#part3根据用户输入，运行相应的操作

def sql_action(sql_dic):
    '''
    执行sql的总控接口
    :param sql_dic:承接上面的sql解析内容
    :return:返回sql增删改查的执行结果
    '''
    return sql_dic.get('func')(sql_dic)

def insert(sql_dic):
    '''
    插入内容：插入信息
    :param sql_dic: 承接解析后的字典
    :return: 返回插入成功的信息
    '''
    db,table=sql_dic.get('into')[0].split('.')
    with open('%s/%s' %(db,table),'ab+') as fh:
        offs = -100  #设置偏移量
        while True:
            fh.seek(offs,2)#表示文件指针：从文件末尾(2)开始向前100个字符(-100)
            lines = fh.readlines()#读取文件指针范围内所有行
            if len(lines)>2: #判断是否最后至少有两行，这样保证了最后一行是完整的
                last = lines[-1] #取最后一行
                break
            offs *= 2#如果off为100时得到的readlines只有一行内容，那么不能保证最后一行是完整的
                     #所以off翻倍重新运行，直到readlines不止一行
        last=last.decode(encoding='utf-8')
        last_id=int(last.split(',')[0])
        id_num=last_id+1
        record=sql_dic.get('values')[0].split(',')
        record.insert(0,str(id_num))
        record_str=','.join(record)+'\n'
        fh.write(bytes(record_str,encoding='utf-8'))
        fh.flush()
        return 'insert success'

def delect(sql_dic):
    db,table=sql_dic.get('from')[0].split('.')
    bak_file=table+'_bak'
    with open("%s/%s" %(db,table),'r',encoding='utf-8') as r_file,\
            open('%s/%s' %(db,bak_file),'w',encoding='utf-8') as w_file:
        del_count=0
        for line in r_file:
            title="id,name,age,phone,dept,enroll_date"
            dic=dict(zip(title.split(','),line.split(',')))
            filter_res=thinking_action(dic,sql_dic.get('where'))
            if not filter_res:
                w_file.write(line)
            else:
                del_count+=1
        w_file.flush()
    os.remove("%s/%s" % (db, table))
    os.rename("%s/%s" %(db,bak_file),"%s/%s" %(db,table))
    return [[del_count],['delete successful']]

def update(sql_dic):
    db,table=sql_dic.get('update')[0].split('.')
    set=sql_dic.get('set')[0].split(',')
    set_l=[]
    for i in set:
        set_l.append(i.split('='))
    bak_file=table+'_bak'
    with open("%s/%s" %(db,table),'r',encoding='utf-8') as r_file,\
            open('%s/%s' %(db,bak_file),'w',encoding='utf-8') as w_file:
        update_count=0
        for line in r_file:
            title="id,name,age,phone,dept,enroll_date"
            dic=dict(zip(title.split(','),line.split(',')))
            filter_res=thinking_action(dic,sql_dic.get('where'))
            if filter_res:
                for i in set_l:
                    k=i[0]
                    v=i[-1].strip("'")
                    print('k v %s %s' %(k,v))
                    dic[k]=v
                print('change dic is %s ' %dic)
                line=[]
                for i in title.split(','):
                    line.append(dic[i])
                update_count+=1
                line=','.join(line)
            w_file.write(line)

        w_file.flush()
    os.remove("%s/%s" % (db, table))
    os.rename("%s/%s" %(db,bak_file),"%s/%s" %(db,table))
    return [[update_count],['update successful']]

def select(sql_dic):
    '''
    查询sql的执行接口
    :param sql_dic: 承接格式化好的sql语句
    查询的原则：第一处理的是from
                第二处理的是where
                第三处理的是limit
                第四处理的是select
    :return: 返回查询的结果
    '''
    db,table=sql_dic.get('from')[0].split('.')
    f = open("%s/%s" %(db,table),'r',encoding='utf-8')
    where_res=where_action(f,sql_dic.get('where'))
    f.close()
    limit_res=limit_action(where_res,sql_dic.get('limit'))
    search_res=search_action(limit_res,sql_dic.get('select'))
    for i in search_res[-1]:
        print(i)
    # return search_res

def where_action(f,where_lis):
    '''
    对用户输出的where条件进行操作
    :param f: 打开文件的句柄
    :param where_lis: 格式化好的where字句
    :return: 返回符合条件的结果
    '''
    res=[]
    title="id,name,age,phone,dept,enroll_date"
    if len(where_lis) !=0:
        for line in f:
            dic=dict(zip(title.split(','),line.split(',')))
            thinking_res=thinking_action(dic,where_lis)
            if thinking_res:
                res.append(line.split(','))
    else:
        res=f.readlines()
    return res

def thinking_action(dic,where_lis):
    '''
    :param dic: 格式化好的语句字典
    :param where_lis: 列表
    #dic与exp做bool运算
    :return:返回符合条件的结果
    '''
    res=[]
    # print('==\033[45;1m%s\033[0m==\033[48;1m%s\033[0m' %(dic,where_l))
    for exp in where_lis:
        if type(exp) is list:
            exp_k,opt,exp_v=exp
            if exp[1] == '=':
                opt='%s=' %exp[1]
            if dic[exp_k].isdigit():
                dic_v=int(dic[exp_k])
                exp_v=int(exp_v)
            else:
                dic_v="'%s'" %dic[exp_k]
            if opt != 'like':
                exp=str(eval("%s%s%s" %(dic_v,opt,exp_v)))
            else:
                if exp_v in dic_v:
                    exp='True'
                else:
                    exp='False'
        res.append(exp)
    res=eval(' '.join(res))
    return res

def limit_action(where_res,limit_l):
    '''
    对用户输入的limit条件进行操作
    :param where_res: 承接上面查询到的结果
    :param limit_l: 用户输入的limit条件
    :return: 返回符合limit条件的内容
    '''
    res=[]
    if len(limit_l) !=0:
        index=int(limit_l[0])
        print(res)
        res=where_res[0:index]
    else:
        res=where_res
    return res

def search_action(limit_res,select_l):
    '''
    对用户输入的select进行操作
    :param limit_res:承接上面的limit结果
    :param select_l:用户输入的select后的语句
    :return:符合条件的列
    '''
    res=[]
    fileds_l=[]
    title="id,name,age,phone,dept,enroll_date"
    if select_l[0] == '*':
        res=limit_res
        fileds_l=title.split(',')
    else:
        for record in limit_res:
            dic=dict(zip(title.split(','),record))
            # print("dic is %s " %dic)
            fileds_l=select_l[0].split(',')
            r_l=[]
            for i in fileds_l:
                r_l.append(dic[i].strip())
            res.append(r_l)
    return [fileds_l,res]

def help():
    msg = '''
                       =_= 欢迎查询my db =_=
    本系统支持基本SQL语句查询，数据库为db，用户表名为user，最好使用列出的SQL语句操作，其他的有可能还不支持哦
    例：
    查询： select * from db.user where name like zzl and id < 3
           select name,age from db.user where id > 3 and id < 6
    增加:  insert into db.user values tom,1000,17738386838,teache,2011-11-10
    修改:  update db.user set age=18 where name like ylqh
           update db.user set dept=ceo where name like ylqh
    删除:  delect from db.user where id = 6
    退出: exit
    帮助: help
        '''
    print(msg)

if __name__ == '__main__':
    help()
    while True:
#part1：用户输入
        sql=input("请输入sql》").strip()
        if sql == 'exit':break
        if sql == 'help':
            help()
            continue
        if len(sql) == 0:continue
#part2：格式化用户输入
        sql_dic=sql_all_analysis(sql)
        # print('sql_dic is %s' % sql_dic)
        if len(sql) == 0:continue
        res=sql_action(sql_dic)
