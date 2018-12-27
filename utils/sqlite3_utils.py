#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import sqlite3
import datetime
import traceback
from time import ctime,sleep
if sys.version.split(" ")[0].split(".")[0] == '2':
    import pyttsx
    reload(sys)
    sys.setdefaultencoding('utf-8')
else:
    import imp
    imp.reload(sys)
    import pyttsx3

db_file = os.path.join(os.path.dirname(__file__), 'data.db')
currpath = os.path.join(os.getcwd(), os.path.dirname(__file__))
data_file = os.path.join(currpath[:currpath.rfind('utils')], 'data\\db\\data.db')
week = {0 : '星期日', 1 : '星期一', 2 : '星期二', 3 : '星期三', 4 : '星期四', 5 : '星期五', 6 : '星期六'}
#if os.path.isfile(user_file):
#    os.remove(user_file)

################ user login ##########################
def user_login(user_name, user_passwd):
    '''
    用户登陆验证
    @return: 0 : success
             other: fail
    '''
    conn = sqlite3.connect(data_file)
    cursor = conn.cursor()
    user_list = cursor.execute('select * from user')
    user_list = [{"name":user[1], "passwd":user[3]} for user in user_list]
    cursor.close()
    conn.commit()
    conn.close()
    for user in user_list:
        if user_name == user['name']:
            if user_passwd == user['passwd']:
                return '0'
            else:
                return '用户密码错误！'
    return '用户不存在！'
    
def change_passwd_for_user(username, password, oldpasswd):
    '''
    修改用户的密码
    @param: username: admin
            password: 123456
    '''
    conn = sqlite3.connect(data_file)
    cursor = conn.cursor()
    user_list = cursor.execute('select * from user')
    user_list = [{"name":user[1], "passwd":user[3]} for user in user_list]
    for user in user_list:
        if username == user['name']:
            if oldpasswd == user['passwd']:
                cursor.execute('update user set password="%s" where name="%s"' % (password, username))
                cursor.close()
                conn.commit()
                conn.close()
                return '0' 
            else:
                return '旧密码填写错误！'
    return '用户不存在！'
   
    
    
################ user operation ######################
def insert_user_into_db(user_info):
    '''
    添加用户到数据库
    @return: 0 : success
             other : fail 
    '''
    conn = sqlite3.connect(data_file)
    cursor = conn.cursor()
    table_list = cursor.execute('select name from sqlite_master where type="table"')
    table_list = [table[0] for table in table_list]
    if "user" not in table_list:
        cursor.execute('create table user(id integer primary key autoincrement, name varchar(20), mail varchar(50), password varchar(20))')
    #判断用户是否存在
    user_list = cursor.execute('select * from user')
    user_list = [user[1] for user in user_list]
    if user_info['user_name'] in user_list:
        return '该用户已经存在！'
    
    cursor.execute('insert into user values(null, "%s", "%s", "%s")' % (user_info["user_name"], user_info["user_mail"], user_info["new_password"]))
    cursor.close()
    conn.commit()
    conn.close()
    return '0'
    
def get_user_info_from_db():
    '''
    从数据库读取用户信息
    @return: user_list : 用户细信息列表
    '''
    conn = sqlite3.connect(data_file)
    cursor = conn.cursor()
    table_list = cursor.execute('select name from sqlite_master where type="table"')
    table_list = [table[0] for table in table_list]
    if "user" not in table_list:
        cursor.execute('create table user(id integer primary key autoincrement, name varchar(20), mail varchar(50), password varchar(20))')
    user_list = cursor.execute('select * from user')    
    user_list = [{"id":user[0], "name":user[1], "mail":user[2]} for user in user_list]
    cursor.close()
    conn.commit()
    conn.close()
    return user_list
    
def del_user_from_db(user_list):
    '''
    从数据库删除用户
    @return: 0 : success 
    '''
    user_id_list = [str(user['id']) for user in user_list]
    user_id =  ','.join(user_id_list)
    conn = sqlite3.connect(data_file)
    cursor = conn.cursor()
    cursor.execute('delete from user where id in (%s)' % user_id)
    cursor.close()
    conn.commit()
    conn.close()
    return '0'

################ cpu and mem info operation ######################
def insert_cup_info_into_db(cpu_info):
    '''
    添加CPU和内存信息到数据库
    @return: 0 : success
             other : fail
    '''
    conn = sqlite3.connect(data_file)
    cursor = conn.cursor()
    table_list = cursor.execute('select name from sqlite_master where type="table"')
    table_list = [table[0] for table in table_list]
    if "cpu" not in table_list:
        cursor.execute('create table cpu(time varchar(20), cpu integer, mem integer)')
        
    cpu_list = cursor.execute('select * from cpu')
    cpu_list = [{"time":cpu[0], "cpu_percent":cpu[1], "mem_percent":cpu[2]} for cpu in cpu_list]
    if len(cpu_list) > 20:
        cursor.execute('delete from cpu where time="%s"' % cpu_list[0]['time'])
    
    cursor.execute('insert into cpu values("%s", "%s", "%s")' % (cpu_info["time"], cpu_info["cpu_percent"], cpu_info["mem_percent"]))
    cursor.close()
    conn.commit()
    conn.close()
    return '0'

def get_cup_info_from_db():
    '''
    从数据库中读取CPU和内存信息
    @return: 0 : success
             other : fail
    '''
    conn = sqlite3.connect(data_file)
    cursor = conn.cursor()
    table_list = cursor.execute('select name from sqlite_master where type="table"')
    table_list = [table[0] for table in table_list]
    if "cpu" not in table_list:
        cursor.execute('create table cpu(time varchar(20), cpu integer, mem integer)')
        return []
    cpu_info = cursor.execute('select * from cpu')
    cpu_info = [{"time":cpu[0], "cpu_percent":cpu[1], "mem_percent":cpu[2]} for cpu in cpu_info]    
    cursor.close()
    conn.commit()
    conn.close()
    return cpu_info

################ alarm info operation ##############################
def insert_alarm_into_db(alarm_info):
    '''
    添加报警信息到数据库
    @return: 0 : success
             other : fail 
    '''
    conn = sqlite3.connect(data_file)
    cursor = conn.cursor()
    table_list = cursor.execute('select name from sqlite_master where type="table"')
    table_list = [table[0] for table in table_list]
    if "alarm" not in table_list:
        cursor.execute('create table alarm(id integer primary key autoincrement, time varchar(20), level varchar(10), message varchar(50))')
   
    cursor.execute('insert into alarm values(null, "%s", "%s", "%s")' % (alarm_info["time"], alarm_info["level"], alarm_info["message"]))
    cursor.close()
    conn.commit()
    conn.close()
    return '0'
    
def get_alarm_info_from_db():
    '''
    从数据库中读取报警信息
    @return: 0 : success
             other : fail
    '''
    conn = sqlite3.connect(data_file)
    cursor = conn.cursor()
    table_list = cursor.execute('select name from sqlite_master where type="table"')
    table_list = [table[0] for table in table_list]
    if "alarm" not in table_list:
        cursor.execute('create table alarm(id integer primary key autoincrement, time varchar(20), level varchar(10), message varchar(50))')
        return []
    alarm_info = cursor.execute('select * from alarm')
    alarm_info = [{"id":alarm[0], "time":alarm[1], "level":alarm[2], "message":alarm[3]} for alarm in alarm_info]    
    cursor.close()
    conn.commit()
    conn.close()
    return alarm_info
    
def del_alert_from_db(alarm_list):
    '''
    从数据库删除报警信息
    @return: 0 : success    
    '''
    alarm_id_list = [str(alarm['id']) for alarm in alarm_list]
    alarm_id =  ','.join(alarm_id_list)
    conn = sqlite3.connect(data_file)
    cursor = conn.cursor()
    cursor.execute('delete from alarm where id in (%s)' % alarm_id)
    cursor.close()
    conn.commit()
    conn.close()
    return '0'
    
#################################  label wall #################################
def insert_label_into_db(label_title, label_content):
    '''
    添加标签到数据库
    @return: 0 : success
             other : fail 
    '''
    try:
        conn = sqlite3.connect(data_file)
        cursor = conn.cursor()
        table_list = cursor.execute('select name from sqlite_master where type="table"')
        table_list = [table[0] for table in table_list]
        if "label" not in table_list:
            cursor.execute('create table label(id integer primary key autoincrement, time varchar(20), title varchar(30), content varchar(200))')
        
        label_time  = datetime.datetime.now().strftime("%Y{y}%m{m}%d{d} %H:%M:%S").format(y='年', m='月', d='日') + '(%s)' % week[datetime.datetime.now().weekday()]
        #label_time  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '(%s)' % week[datetime.datetime.now().weekday()]
        cursor.execute('insert into label values(null, "%s", "%s", "%s")' % (label_time, label_title, label_content))
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        print(traceback.format_exc())
    return '0'
    
def get_label_info_from_db():
    '''
    从数据库中读取标签信息
    @return: 0 : success
             other : fail
    '''
    conn = sqlite3.connect(data_file)
    cursor = conn.cursor()
    table_list = cursor.execute('select name from sqlite_master where type="table"')
    table_list = [table[0] for table in table_list]
    if "label" not in table_list:
        cursor.execute('create table label(id integer primary key autoincrement, time varchar(20), title varchar(30), content varchar(200))')
        return []
    label_info = cursor.execute('select * from label')
    label_info = [{"id":label[0], "time":label[1], "title":label[2], "content":label[3]} for label in label_info]
  
    cursor.close()
    conn.commit()
    conn.close()
    return label_info
    
def del_label_from_db(label_id):
    '''
    从数据库删除标签墙
    @return: 0 : success    
    '''
    print(label_id)
    try:
        conn = sqlite3.connect(data_file)
        cursor = conn.cursor()
        cursor.execute('delete from label where id in (%s)' % label_id)
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        print(traceback.format_exc())
    return '0'
    
#################################  calendar #################################
def insert_calendar_event_into_db(event_title, event_start, event_end):
    '''
    添加日历事件到数据库
    @return: 0 : success
             other : fail 
    '''
    print(event_title, event_start, event_end)
    try:
        conn = sqlite3.connect(data_file)
        cursor = conn.cursor()
        table_list = cursor.execute('select name from sqlite_master where type="table"')
        table_list = [table[0] for table in table_list]
        if "event" not in table_list:
            cursor.execute('create table event(id integer primary key autoincrement, start varchar(20), end varchar(20), title varchar(200))')
        
        cursor.execute('insert into event values(null, "%s", "%s", "%s")' % (event_start, event_end, event_title))
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        print(traceback.format_exc())
    return '0'
    
def get_calendar_event_info_from_db():
    '''
    从数据库中读取事件信息
    @return: 0 : success
             other : fail
    '''
    try:
        conn = sqlite3.connect(data_file)
        cursor = conn.cursor()
        table_list = cursor.execute('select name from sqlite_master where type="table"')
        table_list = [table[0] for table in table_list]
        if "event" not in table_list:
            cursor.execute('create table event(id integer primary key autoincrement, start varchar(20), end varchar(20), title varchar(200))')
            return []
        event_info = cursor.execute('select * from event')
        event_info = [{"start": str(event[1].replace("/", "-")), "end": str(event[2].replace("/", "-")), "title": str(event[3])} for event in event_info]
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        print(traceback.format_exc())
    return event_info
    
def del_calendar_from_db(event_title):
    '''
    从数据库删除标签墙
    @return: 0 : success    
    '''
    print(event_title)
    try:
        conn = sqlite3.connect(data_file)
        cursor = conn.cursor()
        cursor.execute('delete from event where title = "%s"' % event_title)
        cursor.close()
        conn.commit()
        conn.close()
    except Exceptiona as e:
        print(traceback.format_exc())
    return '0'