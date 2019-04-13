#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import time
import sqlite3
import datetime
import traceback
from time import ctime, sleep

import settings
from logger_utils import AppLogger

if settings.PYTHON_VERSION == '2':
    import pyttsx
    reload(sys)
    sys.setdefaultencoding('utf-8')
else:
    import imp
    imp.reload(sys)
    import pyttsx3

Alogger = AppLogger()._getHandler()

########Determine whether the table exists ###########
def whether_table_exists(table_name):
    '''
    查看接下来要操作的table是否存在, 不存在就创建
    @return: no
    '''

    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        table_list = cursor.execute('select name from sqlite_master where type="table"')
        table_list = [table[0] for table in table_list]
        if table_name not in table_list:
            cursor.execute(settings.TABLE_INFO[table_name])
        if table_name == 'user':
            user_list = cursor.execute('select * from user')
            user_list = [user[1] for user in user_list]
            if 'admin' not in user_list:
                cursor.execute('insert into user values(null, "admin", "admin@qq.com", "123123", "/static/img/img/a8.jpg")')
        elif table_name == 'background':
            background_list = cursor.execute('select * from background where style="loginbackground"')
            background_list = [background[0] for background in background_list]
            if not background_list:
                cursor.execute('insert into background values("loginbackground", "/static/img/background/a.jpg")')
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())

################ user login ##########################
def user_login(user_name, user_passwd):
    '''
    用户登陆验证
    @return: 0 : success
             other: fail
    '''
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('user')
        user_list = cursor.execute('select * from user')
        user_list = [{"name":user[1], "passwd":user[3]} for user in user_list]
        print(user_list)
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
    except Exception as e:
        Alogger.error(traceback.format_exc())

def change_passwd_for_user(username, password, oldpasswd):
    '''
    修改用户的密码
    @param: username: admin
            password: 123456
    '''
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('user')
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
    except Exception as e:
        Alogger.error(traceback.format_exc())

def get_user_image_url_from_db(username):
    '''
    获得用户的头像
    @param: username: like admin
    '''
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('user')
        user_list = cursor.execute('select * from user where name="%s"' % username)
        user_list = [{"id":user[0], "name":user[1], "mail":user[2], "image_url":user[4]} for user in user_list]
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
    if user_list and 'image_url' in user_list[0] and user_list[0]['image_url']:
        return user_list[0]['image_url']
    else:
        return '/static/img/img/bg.jpg'

################ background operation ######################
def change_background(img_src):
    '''
    更换背景图
    @param: img_src: /static/img/background/a.jpg
    '''
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('background')
        background_list = cursor.execute('select * from background')
        cursor.execute('update background set imgsrc="%s" where style="loginbackground"' % img_src)
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
    return '0'

def insert_background_into_db(img_src):
    '''
    添加背景图
    @param: img_src: /static/img/background/a.jpg
    '''
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('background')
        background_list = cursor.execute('select * from background')
        cursor.execute('insert into background values("loginbackground", "%s")' % img_src)
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
    return '0'

def get_background_from_db():
    '''
    从数据库中读取背景图
    @param: img_src: /static/img/background/a.jpg
    '''
    background_list = []
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('background')
        background_list = cursor.execute('select * from background')
        background_list = [background[1] for background in background_list]
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
    return background_list

################ user operation ######################
def insert_user_into_db(user_info):
    '''
    添加用户到数据库
    @return: 0 : success
             other : fail 
    '''
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        #判断用户是否存在
        whether_table_exists('user')
        user_list = cursor.execute('select * from user')
        user_list = [user[1] for user in user_list]
        if user_info['user_name'] in user_list:
            return '该用户已经存在！'
        
        cursor.execute('insert into user values(null, "%s", "%s", "%s", "%s")' % (user_info["user_name"], user_info["user_mail"], user_info["new_password"], '/static/img/img/a6.jpg'))
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
    return '0'

def get_user_info_from_db():
    '''
    从数据库读取用户信息
    @return: user_list : 用户细信息列表
    '''
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('user')
        user_list = cursor.execute('select * from user')
        user_list = [{"id":user[0], "name":user[1], "mail":user[2], "image": user[4]} for user in user_list]
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
    return user_list

def del_user_from_db(user_list):
    '''
    从数据库删除用户
    @return: 0 : success 
    '''
    try:
        user_id_list = [str(user['id']) for user in user_list]
        user_id =  ','.join(user_id_list)
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('background')
        cursor.execute('delete from user where id in (%s)' % user_id)
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
    return '0'

################ cpu and mem info operation ######################
def insert_cup_info_into_db(cpu_info):
    '''
    添加CPU和内存信息到数据库
    @return: 0 : success
             other : fail
    '''
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('cpu')
        cpu_list = cursor.execute('select * from cpu')
        cpu_list = [{"time":cpu[0], "cpu_percent":cpu[1], "mem_percent":cpu[2]} for cpu in cpu_list]
        if len(cpu_list) > 60:
            cursor.execute('delete from cpu where time="%s"' % cpu_list[0]['time'])
        
        cursor.execute('insert into cpu values("%s", "%s", "%s")' % (cpu_info["time"], cpu_info["cpu_percent"], cpu_info["mem_percent"]))
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
    return '0'

def get_cup_info_from_db():
    '''
    从数据库中读取CPU和内存信息
    @return: 0 : success
             other : fail
    '''
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('cpu')
        cpu_info = cursor.execute('select * from cpu')
        cpu_info = [{"time":cpu[0], "cpu_percent":cpu[1], "mem_percent":cpu[2]} for cpu in cpu_info]    
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
    return cpu_info

################ alarm info operation ##############################
def insert_alarm_into_db(alarm_info):
    '''
    添加报警信息到数据库
    @return: 0 : success
             other : fail 
    '''
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('alarm')
        cursor.execute('insert into alarm values(null, "%s", "%s", "%s")' % (alarm_info["time"], alarm_info["level"], alarm_info["message"]))
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
    return '0'

def get_alarm_info_from_db():
    '''
    从数据库中读取报警信息
    @return: 0 : success
             other : fail
    '''
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('alarm')
        alarm_info = cursor.execute('select * from alarm')
        alarm_info = [{"id":alarm[0], "time":alarm[1], "level":alarm[2], "message":alarm[3]} for alarm in alarm_info]
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
    return alarm_info[::-1]

def del_alert_from_db(alarm_list):
    '''
    从数据库删除报警信息
    @return: 0 : success    
    '''
    try:
        alarm_id_list = [str(alarm['id']) for alarm in alarm_list]
        alarm_id =  ','.join(alarm_id_list)
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('alarm')
        cursor.execute('delete from alarm where id in (%s)' % alarm_id)
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
    return '0'

#################################  label wall #################################
def insert_label_into_db(label_title, label_content):
    '''
    添加标签到数据库
    @return: 0 : success
             other : fail 
    '''
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('label')
        label_time  = datetime.datetime.now().strftime("%Y{y}%m{m}%d{d} %H:%M:%S").format(y='年', m='月', d='日') + '(%s)' % settings.WEEK_INFO[datetime.datetime.now().weekday()]
        cursor.execute('insert into label values(null, "%s", "%s", "%s")' % (label_time, label_title, label_content))
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
    return '0'

def get_label_info_from_db():
    '''
    从数据库中读取标签信息
    @return: 0 : success
             other : fail
    '''
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('label')
        label_info = cursor.execute('select * from label')
        label_info = [{"id":label[0], "time":label[1], "title":label[2], "content":label[3]} for label in label_info]

        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
    return label_info

def del_label_from_db(label_id):
    '''
    从数据库删除标签墙
    @return: 0 : success    
    '''
    print(label_id)
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('label')
        cursor.execute('delete from label where id in (%s)' % label_id)
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
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
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('event')
        cursor.execute('insert into event values(null, "%s", "%s", "%s")' % (event_start, event_end, event_title))
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
    return '0'

def get_calendar_event_info_from_db():
    '''
    从数据库中读取事件信息
    @return: 0 : success
             other : fail
    '''
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('event')
        event_info = cursor.execute('select * from event')
        event_info = [{"start": str(event[1].replace("/", "-")), "end": str(event[2].replace("/", "-")), "title": str(event[3])} for event in event_info]
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
    return event_info

def del_calendar_from_db(event_title):
    '''
    从数据库删除标签墙
    @return: 0 : success
    '''
    print(event_title)
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('event')
        cursor.execute('delete from event where title = "%s"' % event_title)
        cursor.close()
        conn.commit()
        conn.close()
    except Exceptiona as e:
        Alogger.error(traceback.format_exc())
    return '0'

################################# chat #################################
def insert_chat_info_into_db(message_from, message_to, message_info, message_time, message_flag):
    '''
    添加聊天到数据库
    @return: 0 : success
             other : fail 
    '''
    print(message_from, message_to, message_info, message_time, message_flag)
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('chat')
        from_image = get_user_image_url_from_db(message_from)
        Alogger.error(from_image)
        cursor.execute('insert into chat values(null, "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (message_from, message_to, message_info, message_time, message_flag, message_from, from_image))
        cursor.execute('insert into chat values(null, "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (message_from, message_to, message_info, message_time, message_flag, message_to, from_image))
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
    return '0'

def get_chat_info_from_db(message_from, message_to, current_user):
    '''
    从数据库中读取聊天信息
    @return: 0 : success
             other : fail
    '''
    chat_info = []
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('chat')
        info = cursor.execute('select * from chat where message_from="%s" and message_to="%s" and current_user="%s"' % (message_from, message_to, current_user))
        info = [{"message_from": chat[1], "message_to": chat[2], "message_info": chat[3], "message_time": str(chat[4].replace("/", "-")), "message_flag": chat[5], "current_user": chat[6], "from_image": chat[7]} for chat in info]
        chat_info.extend(info)
        Alogger.error(chat_info)
        info = cursor.execute('select * from chat where message_from="%s" and message_to="%s" and current_user="%s"' % (message_to, message_from, current_user))
        info = [{"message_from": chat[1], "message_to": chat[2], "message_info": chat[3], "message_time": str(chat[4].replace("/", "-")), "message_flag": chat[5], "current_user": chat[6], "from_image": chat[7]} for chat in info]
        chat_info.extend(info)
        Alogger.error(chat_info)
        chat_info = sorted(chat_info, key=lambda d:int(time.mktime(time.strptime(d['message_time'], "%Y-%m-%d %H:%M:%S"))), reverse=False)
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
    return chat_info

def del_chat_info_from_db(message_from, message_to, current_user):
    '''
    从数据库删除标签墙
    @return: 0 : success
    '''
    print(message_from, message_to, current_user)
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('chat')
        cursor.execute('delete from chat where message_from = "%s" and message_to="%s" and current_user="%s"' % (message_from, message_to, current_user))
        cursor.execute('delete from chat where message_from = "%s" and message_to="%s" and current_user="%s"' % (message_to, message_from, current_user))
        cursor.close()
        conn.commit()
        conn.close()
    except Exceptiona as e:
        Alogger.error(traceback.format_exc())
    return '0'

################################# check_message #################################
def check_message_from_db(current_user, message_from):
    '''
    从数据库中读取聊天信息
    @return: 0 : success
             other : fail
    '''
    count = 0
    try:
        conn = sqlite3.connect(settings.DATA_PATH)
        cursor = conn.cursor()
        whether_table_exists('chat')
        sql = 'select * from chat where message_from="%s" and current_user="%s" and message_flag="0"' % (message_from, current_user)
        info = cursor.execute(sql)
        for i in info:
            count += 1
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        Alogger.error(traceback.format_exc())
    return count