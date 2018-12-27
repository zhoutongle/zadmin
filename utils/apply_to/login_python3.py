#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import getpass
import requests
from PIL import Image
from json import loads
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
disable_warnings(InsecureRequestWarning)

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
head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}
now_session = requests.Session()
now_session.verify = False
username = '1140082051@qq.com'
password = 'ztl19930809'

def login():
    print('-----------------验证码验证-----------------')
    resp1 = now_session.get(
        'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.8430851651301317',
        headers=head)
    with open('code.png','wb') as f:
        f.write(resp1.content)
    try:
        im = Image.open('code.png')
        # 展示验证码图片，会调用系统自带的图片浏览器打开图片，线程阻塞
        im.show()
        # 关闭，只是代码关闭，实际上图片浏览器没有关闭，但是终端已经可以进行交互了(结束阻塞)
        im.close()
    except:
        print ('请输入验证码')
        
    print('请输入验证码坐标代号, 以","分割[例如2,5]:')
    code  = input()
    write = code.split(',')
    codes = ''
    for i in write:
        codes += locate[i]
    data = {
        'answer'    : codes,
        'login_site': 'E',
        'rand'      : 'sjrand'
    }
    resp = now_session.post('https://kyfw.12306.cn/passport/captcha/captcha-check',headers=head,data=data)
    html = loads(resp.content.decode("utf-8"))
    if html['result_code'] == '4':
        print('验证码校验成功！')
        # 用户输入用户名，这里可以直接给定字符串
        #username = input('Please input your userName:')
        # 用户输入密码，这里也可以直接给定
        # pwd = raw_input('Please input your password:')
        # 输入的内容不显示，但是会接收，一般用于密码隐藏
        #password = getpass.getpass('Please input your password:')
        print('-----------------登录中-----------------')
        login_url = 'https://kyfw.12306.cn/passport/web/login'
        user = {
            'username': username,
            'password': password,
            'appid'   : 'otn'
        }
        resp2 = now_session.post(login_url,headers=head,data=user)
        html = loads(resp2.content.decode("utf-8"))
        print(html)
        if html['result_code'] == 0:
            print('登陆成功！')
            yzdata = {
                'appid':'otn'
            }
            tk_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
            resp3 = now_session.post(tk_url,data=yzdata,headers=head)
            print('-----------------第一次验证-----------------')
            print(resp3.text)
            login_message = resp3.json()['newapptk']
            print('loginMessage=',login_message)
            yz2data = {
                'tk':login_message
            }
            client_url = 'https://kyfw.12306.cn/otn/uamauthclient'
            resp4 = now_session.post(client_url,data=yz2data,headers=head)
            print('-----------------第二次验证-----------------')
            print(resp4.text)
        else:
            print('登陆失败！')
            
    else:
        print('验证码校验失败，正在重新请求页面...')
        login()
    pass

    check_user_login()
    get_user_info()

def check_user_login():
    url = "https://kyfw.12306.cn/otn/login/checkUser"
    check_data = {
        "_json_att": ""
    }
    res = now_session.post(url, data=check_data, headers=head)
    print(res.content)
    if loads(res.content.decode("utf-8"))['data']['flag']:
        print("用户已经登录！")
    else:
        print("没有用户登录！")
        
def get_user_info():
    url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
    r = now_session.post(url, headers=head)
    #print (r.content)
    REPEAT_SUBMIT_TOKEN = re.findall("globalRepeatSubmitToken = '(.*?)';",r.text)[0]

    url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
    user_data = {
        "_json_att": "",
        'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN,
    }
    res = now_session.post(url, data=user_data, headers=head)
    #print(res.content)
    
    for i in loads(res.content.decode("utf-8"))['data']['normal_passengers']:
        print(i['code'], i['passenger_name'], i['sex_name'], i['born_date'])

if __name__ == '__main__':
    login()
