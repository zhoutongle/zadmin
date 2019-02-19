#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import json
import sqlite3
import traceback
import subprocess
from PIL import Image
from datetime import timedelta
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify

currpath = os.path.join(os.getcwd(), os.path.dirname(__file__))
if not currpath in sys.path:
    sys.path.append(currpath)

utilspath = os.path.join(currpath, 'utils')
if not utilspath in sys.path:
    sys.path.append(utilspath)

MONITOR_PATH = currpath + "\\utils\\monitor_reporter.py"
python_version = sys.version.split(" ")[0].split(".")[0]

import mail_utils
import zadmin_utils
import system_utils
import sqlite3_utils
from menu_utils import admin_menu, admin_menu2
from logger_utils import AppLogger
from zadmin_utils import CN12306

locate = {
    '1':'44,44,',
    '2':'114,44,',
    '3':'185,44,',
    '4':'254,44,',
    '5':'44,124,',
    '6':'114,124,',
    '7':'185,124,',
    '8':'254,124,',
}

Alogger = AppLogger()._getHandler()
    
app = Flask(__name__)

@app.route('/')
def index():
    from cn import USER_NAME
    username = USER_NAME
    song_list = zadmin_utils.get_song_list()
    return render_template('index.html', admin_menu=admin_menu, admin_menu2=admin_menu2, username=username, song_list=song_list['data'])

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
        info = []
        path = currpath + "static\\img\\background\\"
        picture_list = os.listdir(path)
        if python_version == "2":               #python2
            picture_info = ["/static/img/background/%s" % pic.decode("gbk") for pic in picture_list]   
        else:
            picture_info = ["/static/img/background/%s" % pic for pic in picture_list]
        background = sqlite3_utils.get_background_from_db()

        if not background: 
            sqlite3_utils.insert_background_into_db("/static/img/background/a.jpg")
            background = "/static/img/background/a.jpg"
        return render_template('login.html', picture_info=picture_info, background=background)
        
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_passwd = request.form.get('user_passwd')
        retcode = sqlite3_utils.user_login(user_name, user_passwd)
        if retcode == "0": 
            import cn
            cn.change_name(user_name)
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
        session.clear
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
    retcode = sqlite3_utils.del_user_from_db(user_list)
    return retcode
        
@app.route('/modify_password', methods=['GET', 'POST'])
def modify_password():
    if request.method == 'GET':
        from cn import USER_NAME
        current_user = USER_NAME
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
    mail_info = mail_utils.get_mail()
    return render_template('receive_mail.html', mail_info=mail_info)
    
@app.route('/get_calendar', methods=['GET'])
def get_calendar():
    event_list = sqlite3_utils.get_calendar_event_info_from_db()
    return render_template('get_calendar.html', event_list=event_list)
    
@app.route('/check_session', methods=['POST'])
def check_session():
    #if not session.get('name'):
    #    return 'session wxpired'
    #else:
    #    return 0
    return 0

@app.route('/add_event', methods=['POST'])
def add_event():
    event_title = request.form.get('event_title')
    #print(event_title)
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
    #print(system_info)
    return render_template('system_info.html', system_info=system_info)

@app.route('/get_picture', methods=['GET'])
def get_picture():
    info = []
    path = currpath + "static\\img\\image1\\"
    picture_list = os.listdir(path)
    if python_version == "2":               #python2
        picture_info = [pic.decode("gbk") for pic in picture_list]
    else:
        picture_info = [pic for pic in picture_list]
    return render_template('get_picture.html', picture_info=picture_info)
    
@app.route('/picture_content', methods=['GET'])
def picture_content():
    picture_name = request.args.get('picture_name')

    picture_info = {}
    path = currpath + "static\\img\\image1\\"
    picture_list = os.listdir(path)
    for pic in picture_list:
        if python_version == "2":               #python2
            if pic.decode('gbk') == picture_name:
                size = 0
                pic_list = os.listdir(path + pic)
                image_list = []
                for p in pic_list:
                    str = "/static/img/image1/%s/%s" % (pic, p)
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
                    str = "/static/img/image1/%s/%s" % (pic, p)
                    image_list.append(str)
                    img = Image.open(path + pic + "\\" + p)
                    size = img.size
                picture_info['list'] = image_list
                picture_info['size'] = round(size[0]/110)
                picture_info['title'] = pic
    print(picture_info)
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
        if cn.CN.user_name:
            username = cn.CN.user_name
        return render_template('book_ticket.html', username=json.dumps(username))
        
    if request.method == 'POST':
        from cn import CN
        try:
            account_number = request.form.get('account_number')
            user_passwd = request.form.get('user_passwd')
            auth_code = request.form.get('auth_code')

            CN.codes = ""
            for code in auth_code.split():
                CN.codes += locate[code]

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
            print(traceback.format_exc())
            
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
            print(traceback.format_exc())
            
        return jsonify("0")

@app.route('/exit_login', methods=['GET', 'POST'])
def exit_login():
    if request.method == 'POST':
       import cn
       cn.change_cn(None)
    return jsonify("0")  
#######################################################################
'''
    #原有的菜单
'''
@app.route('/graph_echarts', methods=['GET'])
def graph_echarts():
    return render_template('default_menu/graph_echarts.html')
    
@app.route('/graph_flot', methods=['GET'])
def graph_flot():
    return render_template('default_menu/graph_flot.html')
    

#######################################################################

if __name__ == '__main__':
    try:
        #ret = subprocess.Popen('python3 %s >> /dev/null 2>&1' % MONITOR_PATH)
        app.run(debug=True)
    except Exception as e:
        print("----------- %s" % traceback.format_exc())
    