#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import json
import redis
import base64
import sqlite3
import datetime
import traceback
import subprocess
from PIL import Image
from datetime import timedelta
from flask_session import Session
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify

currpath = os.path.join(os.getcwd(), os.path.dirname(__file__))
if not currpath in sys.path:
    sys.path.append(currpath)

utilspath = os.path.join(currpath, 'utils')
if not utilspath in sys.path:
    sys.path.append(utilspath)

import settings
import mail_utils
import zadmin_utils
import system_utils
import sqlite3_utils
from menu_utils import admin_menu, admin_menu2
from logger_utils import AppLogger
from zadmin_utils import CN12306

Alogger = AppLogger()._getHandler()

app = Flask(__name__)
app.debug = True
app.secret_key = 'please-generate-a-random-secret_key'

app.config['SESSION_TYPE']           = 'filesystem'  
app.config['SESSION_FILE_DIR']       = settings.SESSION_PATH  # session类型为redis
app.config['SESSION_FILE_THRESHOLD'] = 500  # 存储session的个数如果大于这个值时，就要开始进行删除了
app.config['SESSION_FILE_MODE']      = 384  # 文件权限类型
app.permanent_session_lifetime = timedelta(minutes=30)

app.config['SESSION_PERMANENT']      = False  # 如果设置为True，则关闭浏览器session就失效。
app.config['SESSION_USE_SIGNER']     = False  # 是否对发送到浏览器上session的cookie值进行加密
app.config['SESSION_KEY_PREFIX']     = 'session:'  # 保存到session中的值的前缀

Session(app)

@app.route('/')
def index():
    username = session.get('username')
    if not username:
        login_url = url_for('login')
        return redirect(login_url)      #重定向为登录页面

    image_url = sqlite3_utils.get_user_image_url_from_db(username)
    settings.USER_INFO['image_url'] = image_url
    song_list = zadmin_utils.get_song_list()
    return render_template('index.html', admin_menu=admin_menu, username=username, song_list=song_list['data'], image_url=image_url)

@app.route('/get_home', methods=['GET', 'POST'])
def get_home():
    if request.method == 'GET':
        return render_template('404.html')

@app.route('/get_profile', methods=['GET', 'POST'])
def get_profile():
    if request.method == 'GET':
        return render_template('profile.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        picture_list = os.listdir(settings.BACKGROUND_PICTURE_PATH)
        if settings.PYTHON_VERSION == '2':               #判断python的版本
            picture_info = ["/static/img/background/%s" % pic.decode("gbk") for pic in picture_list]
        else:
            picture_info = ["/static/img/background/%s" % pic for pic in picture_list]
        background = sqlite3_utils.get_background_from_db()

        if not background:
            sqlite3_utils.insert_background_into_db("/static/img/background/a.jpg")
            background = ["/static/img/background/a.jpg"]
        return render_template('login.html', picture_info=picture_info, background=background)
        
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_passwd = request.form.get('user_passwd')
        retcode = sqlite3_utils.user_login(user_name, user_passwd)
        if retcode == "0":
            session['username'] = user_name
            settings.USER_INFO['user_name'] = user_name
        return retcode

@app.route('/change_background', methods=['GET', 'POST'])
def change_background():
    if request.method == 'POST':
        img_src = request.form.get('img_src')
        retcode = sqlite3_utils.change_background(img_src)
        return retcode

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return '0'

@app.route('/user_manager', methods=['GET', 'POST'])
def user_manager():
    if request.method == 'GET':
        return render_template('user_manager.html')

    if request.method == 'POST':
        user_list = sqlite3_utils.get_user_info_from_db()
        return jsonify(user_list)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('add_user.html')
    
    if request.method == 'POST':
        user_info = {}
        user_info['user_name'] = 'user_name' in request.form and request.form.get('user_name') or None
        user_info['user_mail'] = 'user_mail' in request.form and request.form.get('user_mail') or None
        user_info['new_password'] = 'new_password' in request.form and request.form.get('new_password') or None
        retcode = sqlite3_utils.insert_user_into_db(user_info)
        return retcode

@app.route('/del_user', methods=['POST'])
def del_user():
    user_list = []
    user_list = request.form.get('user_list')
    user_list = json.loads(user_list)
    for user in user_list:
        if user['name'] == 'admin':
            return '1'
        if user['name'] == session.get('username'):
            return '2'
    retcode = sqlite3_utils.del_user_from_db(user_list)
    return retcode

@app.route('/modify_password', methods=['GET', 'POST'])
def modify_password():
    if request.method == 'GET':
        current_user = session.get('username')
        return render_template('modify_password.html', current_user=current_user)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        oldpasswd = request.form.get('oldpasswd')
        retcode = sqlite3_utils.change_passwd_for_user(username, password, oldpasswd)
        return retcode

@app.route('/view_log', methods=['GET', 'POST'])
def view_log():
    if request.method == 'GET':
        return render_template('view_log.html')
        
    if request.method == 'POST':
        alarm_info = sqlite3_utils.get_alarm_info_from_db()
        return jsonify(alarm_info)

@app.route('/del_alarm', methods=['GET', 'POST'])
def del_alarm():
    alarm_list = []
    alarm_list = request.form.get('alarm_list')
    alarm_list = json.loads(alarm_list)
    retcode = sqlite3_utils.del_alert_from_db(alarm_list)
    return retcode

@app.route('/disk_usage', methods=['GET', 'POST'])
def disk_usage():
    if request.method == 'GET':
        disk_info = zadmin_utils.get_disk_info()
        return render_template('disk_usage.html', disk_info=disk_info)

@app.route('/cpu_usage', methods=['GET', 'POST'])
def cpu_usage():
    if request.method == 'GET':
        return render_template('cpu_usage.html')

@app.route('/get_cpu_info_post', methods=['GET', 'POST'])
def get_cpu_info_post():
    if request.method == 'POST':
        cpu_info = sqlite3_utils.get_cup_info_from_db()
        return jsonify(cpu_info)

@app.route('/china_map', methods=['GET', 'POST'])
def china_map():
    if request.method == 'GET':
        return render_template('china_map.html')

@app.route('/show_audio', methods=['GET', 'POST'])
def show_audio():
    if request.method == 'GET':
        song_list = zadmin_utils.get_song_list()
        return render_template('show_audio.html', song_list=song_list['data'])

@app.route('/show_video', methods=['GET', 'POST'])
def show_video():
    if request.method == 'GET':
        return render_template('show_video.html')

@app.route('/show_voice', methods=['GET'])
def show_voice():
    if request.method == 'GET':
        return render_template('show_voice.html')

@app.route('/read_content', methods=['POST'])
def read_content():
    if request.method == 'POST':
        content = request.form.get('read_content')
        retcode = zadmin_utils.read_content(content)
        return retcode

@app.route('/get_music_lrc', methods=['GET', 'POST'])
def get_music_lrc():
    if request.method == 'POST':
        song_name = request.form.get('song_name')
        lrc_content = zadmin_utils.analysis_lrc(song_name)
        return jsonify(lrc_content)

@app.route('/label_wall', methods=['GET', 'POST'])
def label_wall():
    if request.method == 'GET':
        label_list = sqlite3_utils.get_label_info_from_db()
        return render_template('label_wall.html', label_list=label_list)

@app.route('/add_label', methods=['GET', 'POST'])
def add_label():
    if request.method == 'POST':
        label_name = request.form.get('label_name')
        label_content = request.form.get('label_content')
        retcode = sqlite3_utils.insert_label_into_db(label_name, label_content)
        return retcode

@app.route('/del_label', methods=['POST'])
def del_label():
    label_id = request.form.get('label_id')
    retcode = sqlite3_utils.del_label_from_db(label_id)
    return retcode

@app.route('/receive_mail', methods=['GET'])
def receive_mail():
    #mail_info = mail_utils.get_mail()
    mail_info = [{'mail_from':'张三', 'mail_to':'李四','mail_subject':'这个月的报表', 'mail_date':'2019-4-15 14:56:00'}, 
                 {'mail_from':'王五', 'mail_to':'李四','mail_subject':'今天天气', 'mail_date':'2019-4-15 14:57:00'}]
    return render_template('receive_mail.html', mail_info=mail_info)

@app.route('/write_mail', methods=['GET'])
def write_mail():
    return render_template('write_mail.html')

@app.route('/send_mail', methods=['GET'])
def send_mail():
    return render_template('send_mail.html')

@app.route('/mail_detail', methods=['GET'])
def mail_detail():
    return render_template('mail_detail.html')

@app.route('/get_calendar', methods=['GET'])
def get_calendar():
    event_list = sqlite3_utils.get_calendar_event_info_from_db()
    return render_template('get_calendar.html', event_list=event_list)

@app.route('/check_session', methods=['POST'])
def check_session():
    Alogger.error("this session is %s" % session.get('username'))
    if not session.get('username'):
        return '1'
    else:
        return '0'

@app.route('/lock_screen', methods=['GET'])
def lock_screen():
    user_name = settings.USER_INFO['user_name']
    image_url = settings.USER_INFO['image_url']
    if (not user_name) or (not image_url):
        login_url = url_for('login')
        return redirect(login_url)              #重定向为登录页面
    return render_template('lock_screen.html', user_name=user_name, image_url=image_url)

@app.route('/check_message', methods=['POST'])
def check_message():
    new_meaasge_count = 0
    info_list = []
    current_user = session.get('username')
    user_list = sqlite3_utils.get_user_info_from_db()
    for user in user_list:
        if user['name'] == current_user:
            continue
        info = {}
        message_count = sqlite3_utils.check_message_from_db(current_user, user['name'])
        info['message_from'] = user['name']
        info['message_count'] = message_count
        info_list.append(info)
        new_meaasge_count += message_count
    Alogger.error(info_list)
    return jsonify(new_meaasge_count)

@app.route('/add_event', methods=['POST'])
def add_event():
    event_title = request.form.get('event_title')
    start = request.form.get('start')
    end = request.form.get('end')
    retcode = sqlite3_utils.insert_calendar_event_into_db(event_title, start, end)
    return retcode

@app.route('/del_event', methods=['POST'])
def del_event():
    event_title = request.form.get('event_title')
    retcode = sqlite3_utils.del_calendar_from_db(event_title)
    return retcode

@app.route('/system_info', methods=['GET'])
def system_info():
    system_info = system_utils.get_system_info()
    return render_template('system_info.html', system_info=system_info)

@app.route('/get_picture', methods=['GET'])
def get_picture():
    info = []
    path = currpath + "static\\img\\image\\"
    picture_list = os.listdir(path)
    if settings.PYTHON_VERSION == '2':               #python2
        picture_info = [pic.decode("gbk") for pic in picture_list]
    else:
        picture_info = [pic for pic in picture_list]
    return render_template('get_picture.html', picture_info=picture_info)

@app.route('/picture_content', methods=['GET'])
def picture_content():
    picture_name = request.args.get('picture_name')
    path = settings.PICTURE_PATH
    picture_info = {}
    picture_list = os.listdir(settings.PICTURE_PATH)
    for pic in picture_list:
        if settings.PYTHON_VERSION == '2':               #python2
            if pic.decode('gbk') == picture_name:
                size = 0
                pic_list = os.listdir(path + pic)
                image_list = []
                for p in pic_list:
                    str = "/static/img/image/%s/%s" % (pic, p)
                    image_list.append(str.decode('gbk'))
                    img = Image.open(path + pic + "\\" + p)
                    size = img.size
                picture_info['list'] = image_list
                picture_info['size'] = size[0]/110
                picture_info['title'] = pic.decode('gbk')

        else:
            if pic == picture_name:
                size = 0
                pic_list = os.listdir(path + pic)
                image_list = []
                for p in pic_list:
                    str = "/static/img/image/%s/%s" % (pic, p)
                    image_list.append(str)
                    img = Image.open(path + pic + "\\" + p)
                    size = img.size
                picture_info['list'] = image_list
                picture_info['size'] = round(size[0]/110)
                picture_info['title'] = pic
    return render_template('picture_content.html', picture_info=picture_info)

@app.route('/get_article', methods=['GET', 'POST'])
def get_article():
    if request.method == 'GET':
        return render_template('get_article.html')
        
    if request.method == 'POST':
        article_list = zadmin_utils.article_main()
        return jsonify(article_list)

@app.route('/get_train_ticket', methods=['GET', 'POST'])
def get_train_ticket():
    if request.method == 'GET':
        return render_template('get_train_ticket.html')

    if request.method == 'POST':
        train_ticket_info = zadmin_utils.get_train_ticket('', '', '')
        return jsonify(train_ticket_info)  

@app.route('/train_ticket_content', methods=['GET'])
def train_ticket_content():
    if request.method == 'GET':
        from_station = request.args.get('from_station')
        to_station = request.args.get('to_station')
        train_time = request.args.get('train_time')
        train_ticket_info = zadmin_utils.get_train_ticket(from_station, to_station, train_time)
        return render_template('train_ticket_content.html', train_ticket_info=train_ticket_info)

@app.route('/refresh_code', methods=['GET', 'POST'])
def refresh_code():
    from cn import CN
    CN.get_auth_code()
    return jsonify("0")

@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    if request.method == 'GET':
        username = '---'
        import cn
        if cn.CN == None:
            CN1 = CN12306()
            cn.change_cn(CN1)
            CN1.get_init()
            CN1.get_newpasscode()
            CN1.get_auth_code()
        if session.get('username'):
            username = session.get('username')
        return render_template('book_ticket.html', username=json.dumps(username))

    if request.method == 'POST':
        from cn import CN
        try:
            account_number = request.form.get('account_number')
            user_passwd = request.form.get('user_passwd')
            auth_code = request.form.get('auth_code')

            CN.codes = ""
            for code in auth_code.split():
                CN.codes += settings.LOCATE[code]

            result = CN.auth_auth_code()
            if result['result_code'] == "4":
                CN.login(account_number, user_passwd)
                CN.userLogin()
                CN.getjs()
                CN.post_uamtk()
                result = CN.post_uamauthclient()
                CN.get_userLogin()
                CN.get_leftTicket()
                CN.get_GetJS()
                CN.get_qufzjql()
                return jsonify(result)
            else:
                return jsonify(result)
        except Exception as e:
            Alogger.error(traceback.format_exc())

@app.route('/buy_ticket', methods=['GET', 'POST'])
def buy_ticket():
    if request.method == 'POST':
        from cn import CN
        try:
            from_station = request.form.get('from_station')
            to_station = request.form.get('to_station')
            train_time = request.form.get('train_time')
            seattype = request.form.get('seattype')
            CN.sta_code(from_station, to_station, train_time, seattype)
            flag = CN.get_queryZ()
            # if flag:
                # CN.post_submitOrderRequest()
                # CN.post_initDc()
                # CN.post_getPassengerDTOs()
                # CN.post_checkOrderInfo()
                # CN.post_getQueueCount()
                # CN.post_confirmSingleForQueue()
            # else:
                # return jsonify("1")
        except Exception as e:
            Alogger.error(traceback.format_exc())
            
        return jsonify("0")

@app.route('/exit_login', methods=['GET', 'POST'])
def exit_login():
    if request.method == 'POST':
       import cn
       cn.change_cn(None)
    return jsonify("0")

@app.route('/editor_article', methods=['GET', 'POST'])
def editor_article():
    if request.method == 'POST':
        return jsonify("0")

    if request.method == 'GET':
        return render_template('editor_article.html')

@app.route('/show_directory', methods=['GET', 'POST'])
def show_directory():
    if request.method == 'POST':
        targetpath = request.form.get('path')
        children = []
        show_file = True
        try:
            pathlist = os.listdir(targetpath)
            pathdir = []
            for i in range(len(pathlist)):
                pathlist[i] = pathlist[i]
            pathlist.sort()
            for path in pathlist:
                if path.find('.') == 0:
                    continue
                if not show_file:
                    subpath = os.path.join(targetpath, path)
                    if os.path.isdir(subpath):
                        pathdir.append(subpath)
                        children.append({"name": path, "path": subpath, "isParent":"true"})
                else:
                    subpath = os.path.join(targetpath, path)
                    pathdir.append(subpath)
                    if os.path.isdir(subpath):
                        if subpath.find("internal_op") < 0:
                            children.append({"name": path, "path": subpath, "isParent":"true"})
                    else:
                        children.append({"name": path, "path": subpath, "isParent":"false"})
            if len(pathdir) > 20000:
                return {"name": "too many dir", "dirnums": len(pathdir)}
        except Exception as e:
            Alogger.error(traceback.format_exc())
        return jsonify(children)

    if request.method == 'GET':
        return render_template('show_directory.html')

@app.route('/base64_transition', methods=['GET', 'POST'])
def base64_transition():
    if request.method == 'POST':
        path = os.path.join(settings.EXE_PATH, 'base64_transition.exe')
        os.system(path)
        return jsonify('0')

@app.route('/chat_other', methods=['GET', 'POST'])
def chat_other():
    if request.method == 'GET':
        user_list = sqlite3_utils.get_user_info_from_db()
        for user in user_list:
            if user['name'] == session.get('username'):
                user_list.remove(user)
        login_user = session.get('username')
        if user_list:
            chat_user_name = user_list[0]['name']
        else:
            chat_user_name = ''
        return render_template('chat_other.html', user_list=user_list, login_user=login_user, chat_user_name=chat_user_name)

@app.route('/receive_message', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'POST':
        message_to = request.form.get('to')
        chat_info = sqlite3_utils.get_chat_info_from_db(session.get('username'), message_to, session.get('username'))
        Alogger.error(chat_info)
        Alogger.error(len(chat_info))
        return jsonify(chat_info)

@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        message_from = session.get('username')
        message_to = request.form.get('to')
        message_info = request.form.get('message')
        message_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_flag = '0'
        retcode = sqlite3_utils.insert_chat_info_into_db(message_from, message_to, message_info, message_time, message_flag)
        return '0'

@app.route('/delete_message', methods=['GET', 'POST'])
def delete_message():
    if request.method == 'POST':
        message_from = session.get('username')
        message_to = request.form.get('to')
        current_user = session.get('username')
        Alogger.error(message_from, message_to, current_user)
        retcode = sqlite3_utils.del_chat_info_from_db(message_from, message_to, current_user)
        return '0'

@app.route('/image_cropper', methods=['GET', 'POST'])
def image_cropper():
    if request.method == 'GET':
        return render_template('image_cropper.html')

    if request.method == 'POST':
        file = request.files['file']
        Alogger.error(file)
        file_name = file.filename
        Alogger.error(os.path.join(settings.HEAD_PORTRAIT_PATH, file_name))
        file.save(os.path.join(settings.HEAD_PORTRAIT_PATH, file_name))
        return jsonify('0')

@app.route('/system_tool', methods=['GET', 'POST'])
def system_tool():
    if request.method == 'GET':
        return render_template('system_tool.html')
