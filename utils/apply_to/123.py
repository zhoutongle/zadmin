#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time
import random
import datetime
import traceback
import requests
from urllib import parse
from PIL import Image
from json import loads
from collections import OrderedDict

'''
    1.确认用户信息                  https://kyfw.12306.cn/otn/login/checkUser
    2.提交预定请求                  https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest
    3.确认乘客信息                  https://kyfw.12306.cn/otn/confirmPassenger/initDc
    4.获取乘客信息                  https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs
    5.确认订单信息                  https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo
    6.提交预定请求                  https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount
    7.确认配置信息                  https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue
    8.排队等待                      https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime
    9.请求预定结果                  https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue
'''

'''
    EB0%2BaDn17za4TqqV4QYoCPeq3exXyBSax9%2FxTBH0sf8kR71V3nJBGwJwiIohTLYMng2pt2BRKnTK%0AOEX%2BIC6RLqZFA32lUiOTO4yR%2BkOiESssS64MfWkzB0NWWM
    HrteO16sORxZPEv4aZQKWrzNmEb045%0AZ6%2FnNM0UMZZ6NRhlBMDmdgTD9NmqSedBchmTSdmyGekxy%2B3vgLd4cr3eO%2F4hoUTKwYVFtCiCzcPT%0AU65dIZGxXjXNQuE
    vHw8uP9i%2BMq69|预订|26000K772635|K7727|HDP|QTP|BXP|TJP|00:42|02:33|01:51|Y|hQLU3ok%2BUlNDhHsvlccX%2F4xv%2FKFDVwqi5lhtd8g2s5SiC%2BMn|
    20181221|3|P2|09|10|0|0|||||||无||有|有|||||101030|113|1

    通过分析
    0：列车信息（订票时候需要） 
    1：信息 
    2：火车编号
    3：列车号 
    4：始发站   
    5：终点站   
    6：起始站  
    7：目标站    
    8：出发时间       
    9：到达时间
    10：行车时间
    11：有3种状态：Y, N, IS_TIME_NOT_BUY 分别对应，可以预定，不可以预定，其他原因----对应的是第1项
    12：参数leftTicket
    13：日期
    14：
    15：参数train_location
    21：高级动卧   
    22：        
    23：软卧 
    24：软座  
    25：特等座  
    26：无座 
    28：硬卧  
    29：硬座  
    30：二等座  
    31：一等座  
    32：商务座 
    33：动卧
'''
'''用户信息
    {
        "code":"5",
        "passenger_name":"周同乐",
        "sex_code":"M",
        "sex_name":"男",
        "born_date":"****-**-** 00:00:00",
        "country_code":"CN",
        "passenger_id_type_code":"1",
        "passenger_id_type_name":"中国居民身份证",
        "passenger_id_no":"4****************4",
        "passenger_type":"1",
        "passenger_flag":"0",
        "passenger_type_name":"成人",
        "mobile_no":"183********",
        "phone_no":"",
        "email":"1********1@qq.com",
        "address":"",
        "postalcode":"",
        "first_letter":"",
        "recordCount":"5",
        "total_times":"99",
        "index_id":"0",
        "gat_born_date":"",
        "gat_valid_date_start":"",
        "gat_valid_date_end":"",
        "gat_version":""
    }
'''

DEFAULT_HEADERS = {
    'Host':'kyfw.12306.cn',
    'Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer':'https://kyfw.12306.cn/otn/index/init',
    'Accept-Language':'zh-CN,zh;q=0.9',
}

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

def get_random():
    return str(random.random())     #生产一个18位的随机数
    
def get_13_time():          #一个十三位的时间戳
    return str(int(time.time()*1000))
    
class CN12306(object):
    def __init__(self):
        self.chufa    = '2018-12-20'
        self.s        = requests.session()
        self.s.verify = False        #忽略https 证书验证
        self.codes    = ''
        self.username = '***********'
        self.password = '***********'
        self.train_info = []
        self.user_info  = {}
        self.passenger_ticket = ''
        self.old_passenger = ''

    #请求了一个首页   
    def get_init(self): 
        url = 'https://kyfw.12306.cn/otn/login/init'
        r   = self.s.get(url)
        print('首页获取成功，状态码：',r)
 
    #这个页面不知道是干啥的，但是12306 请求了，咱们为了模仿的像一点也去请求
    def get_newpasscode(self): 
        url = 'https://kyfw.12306.cn/otn/resources/js/newpasscode/captcha_js.js?_={}'.format(get_13_time())
        r   = self.s.get(url)
        print('newpasscode获取成功，状态码：',r)
 
    #获取验证码
    def get_auth_code(self):
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&{}'.format(get_random())
        r = self.s.post(url=url)
        with open('auth_code.png','wb') as f:
            f.write(r.content)
        try:
            im = Image.open('auth_code.png')    # 展示验证码图片，会调用系统自带的图片浏览器打开图片，线程阻塞
            im.show()                           # 关闭，只是代码关闭，实际上图片浏览器没有关闭，但是终端已经可以进行交互了(结束阻塞)
            im.close()
        except:
            print ('请输入验证码')
            
        print('请输入验证码坐标代号, 以","分割[例如2,5]:')
        self.codes = ''
        write = input().split(',')
        for i in write:
            self.codes += locate[i]

    
    #验证验证码是否正确提交方式post
    def auth_auth_code(self):
        self.get_auth_code()    #获取验证码
        print(self.codes)
        url  = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
        data = {
            'answer' : self.codes,
            'login_site' : 'E',
            'rand' : 'sjrand',
        }
        r = self.s.post(url=url,data=data)
        result = loads(r.content.decode("utf-8"))     #result = r.json()
        if result['result_code'] == "4":
            print("messages: {}, code: {}".format(result['result_message'], result['result_code']))
            return True
        else: #如果验证码校验失败
            print('验证码错误，刷新验证码，重新提交! messages: {}, code: {}'.format(result['result_message'], result['result_code']))
            self.auth_auth_code()      #重新校验验证码
 
    def login(self):
        url  = 'https://kyfw.12306.cn/passport/web/login'
        data = {
            'username' : self.username,
            'password' : self.password,
            'appid' : 'otn',
        }
        r = self.s.post(url=url,data=data)
        self.uamtk = r.json()["uamtk"]
     
        print(r.text)
 
    def userLogin(self):
        url = 'https://kyfw.12306.cn/otn/login/userLogin'
        r   = self.s.post(url=url)
        #print(r.text)
        
    def getjs(self):  #不知道是干啥的，但是也提交吧
        url = 'https://kyfw.12306.cn/otn/HttpZF/GetJS'
        r   = self.s.get(url)
        
    def post_uamtk(self):
        url  = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        data = { 'appid':'otn'}
        r    = self.s.post(url=url,data=data,allow_redirects=False)
        self.newapptk = r.json()["newapptk"]
        r.encoding    = 'utf-8'
        print(r.text)
        
    def post_uamauthclient(self):
        url  = 'https://kyfw.12306.cn/otn/uamauthclient'
        data = {
          'tk':self.newapptk
        }
        r = self.s.post(url=url,data=data)
        self.apptk = r.json()["apptk"]
        r.encoding = 'utf-8'
        print(r.text)
        
    def get_userLogin(self):
        url = 'https://kyfw.12306.cn/otn/login/userLogin'
        r   = self.s.get(url)
        r.encoding = 'utf-8'
        #print(r.text)
        
    def get_leftTicket(self):
        url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        r   = self.s.get(url)
        r.encoding = 'utf-8'
        #print(r.text)
        
    def get_GetJS(self):
        url = 'https://kyfw.12306.cn/otn/HttpZF/GetJS'
        self.s.get(url)
     
    def get_qufzjql(self):
        url = 'https://kyfw.12306.cn/otn/dynamicJs/qufzjql'
        self.s.get(url)
 
    def get_queryZ(self):
        try:
            url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes={}'.format(self.chufa,'BJP','TBP','ADULT')
            r = self.s.get(url)
            r.encoding='utf-8'
            cheliang = r.json()["data"]["result"]
            print(r.json().keys())
        except Exception as e:
            print(traceback.format_exc())
            cheliang = []
            
        try:
            for i in cheliang[:1]:
                print(i)
                dandulist = str(i).split('|')
                self.train_info = dandulist
                if len(str(dandulist[0])) >= 100:
                    self.secretStr = parse.unquote(dandulist[0])
                    车次 = str(dandulist[3])
                    出发时间 = str(dandulist[8])
                    到达时间 = str(dandulist[9])
                    历时 = str(dandulist[10])
                    软卧 = str(dandulist[23])
                    硬卧 = str(dandulist[28])               
                    print('可预订车次列表，','车次：',车次,'出发时间：', 出发时间,'到达时间：', 到达时间,'历时：', 历时,'软卧剩余： ',软卧,' 硬卧剩余： ',硬卧)
                    if (软卧 != '' and 软卧 != '0' and 软卧 != '无' and 软卧 != '空') or (硬卧 != '' and 硬卧 != '0' and 硬卧 != '无' and 硬卧 != '空'):
                        #执行下单操作
                        print("############### 提交预定请求 ###############")
                        # self.post_submitOrderRequest()
                        # print("############### 确认乘客信息 ###############")
                        # self.post_initDc()
                        # print("############### 获取乘客信息 ###############")
                        # self.post_getPassengerDTOs()
                        # print("############### 确认订单信息 ###############")
                        # self.post_checkOrderInfo()
                        # print("############### 提交预定请求 ###############")
                        # self.post_getQueueCount()
                        # print("############### 确认配置信息 ###############")
                        # self.post_confirmSingleForQueue()
                        return False
                               
                    print('*****************************************************')
        except Exception as e:
            print(traceback.format_exc())
        return True

 
    # 点击预定下单
    def post_submitOrderRequest(self):
        url  = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        data = {
            'secretStr':self.secretStr,
            'train_date':self.chufa,         #出发时间
            'back_train_date':self.chufa ,   #返回时间
            'tour_flag':'dc',                #固定
            'purpose_codes':'ADULT',
            'query_from_station_name':'BXP',
            'query_to_station_name':'TJP',
            'undefined':''
        }
        r = self.s.post(url=url,data=data)
        r.encoding='utf-8'
        print(r.json())
        return r.json()['status']
        
    def post_initDc(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        r   = self.s.post(url, data={'_json_att':''})
        self.REPEAT_SUBMIT_TOKEN = re.findall("globalRepeatSubmitToken = '(.*?)';",r.text)[0]
        self.key_check_isChange = re.findall("'key_check_isChange':'(.*?)'",r.text)[0]
        print(self.REPEAT_SUBMIT_TOKEN)
        print(self.key_check_isChange)

    def post_getPassengerDTOs(self): 
        url  ='https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        data = {
           'REPEAT_SUBMIT_TOKEN':self.REPEAT_SUBMIT_TOKEN,
           '_json_att':''
        }
        r = self.s.post(url=url,data=data)
        r.encoding = 'utf-8'
        #print(r.text)
        for passenger in r.json()["data"]["normal_passengers"]:
            if passenger["code"] == "5":
                print(passenger)
                self.user_info = passenger
            print("{} : {}".format(passenger["code"], passenger['passenger_name']))
        
        self.passenger_ticket = '3,0,{},{},{},{},{},N'.format(self.user_info['passenger_type'], self.user_info['passenger_name'], self.user_info['passenger_id_type_code'], self.user_info['passenger_id_no'], self.user_info['mobile_no']) #'3,0,1,周同乐,1,411528199308093314,18301049957,N' , (车票类型，0， 姓名， 证件类型，证件号， 手机号，N)
        self.old_passenger = '{},{},{},{}_'.format(self.user_info['passenger_name'], self.user_info['passenger_id_type_code'], self.user_info['passenger_id_no'], self.user_info['passenger_type']) #'周同乐,1,411528199308093314,1_'
        
        print(self.passenger_ticket)
        print(self.old_passenger)
        
    #确认订单信息
    def post_checkOrderInfo(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        data = {
            'cancel_flag': '2',
            'randCode': '',
            'whatsSelect': '1',
            'tour_flag': 'dc',
            'ed_level_order_num': '000000000000000000000000000000',
            'passengerTicketStr': self.passenger_ticket,        
            'oldPassengerStr': self.old_passenger
        }
        res = self.s.post(url,data=data)
        print(res.status_code)
        print(res.text)
        
    #提交预定请求    
    def post_getQueueCount(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        data = {
            "_json_att": "",
            "fromStationTelecode": self.train_info[6],           #起始站编号 'BXP' 6项
            "leftTicket": self.train_info[12],                   #12项
            "purpose_codes": '00',
            "REPEAT_SUBMIT_TOKEN": self.REPEAT_SUBMIT_TOKEN,
            "seatType": "3",                                     #座位类型 1是硬座(无座)，2是软座，3是硬卧，4是软卧,  O 大写字母  是高铁二等座，M是高铁一等座，商务座(9),特等座(P),高级软卧(6)
            "stationTrainCode": self.train_info[3],              #列车号   3项
            "toStationTelecode": self.train_info[6],             #目标站编号 "TJP"  7项
            "train_date": datetime.datetime.strptime(self.train_info[13], '%Y%m%d').strftime('%a %b %d %Y %H:%M:%S GMT+0800'),     #'Sat Dec 22 2018 00:00:00 GMT+0800'
            "train_location": self.train_info[15],               #15项  "P2"
            "train_no": self.train_info[2]                       #火车编号 2项
        }
        res = self.s.post(url,data=data)
        print(res.status_code)
        print(res.text)
        
    #确认配置信息
    def post_confirmSingleForQueue(self):
        url='https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        data = {
            "_json_att": "",
            "choose_seats": "",
            "dwAll": "N",
            "key_check_isChange": self.key_check_isChange,
            "leftTicketStr": self.train_info[12],
            "oldPassengerStr": self.old_passenger,
            "passengerTicketStr": self.passenger_ticket,
            "purpose_codes": '00',
            "randCode": "",
            "REPEAT_SUBMIT_TOKEN": self.REPEAT_SUBMIT_TOKEN,
            "roomType": '000',
            "whatsSelect": '1',
            "train_location": self.train_info[15]
        }
        res = self.s.post(url,data=data)
        print(res.status_code)
        print(res.text)
     
if __name__ == '__main__':
    cn = CN12306()
    cn.get_init()
    cn.get_newpasscode()
    if cn.auth_auth_code(): #验证验证码是否正确
        cn.login()
        print("####################  login  ###########")
        cn.userLogin()
        print("####################  userlogin  ###########")
        cn.getjs()
        print("####################  getjs  ###########")
        cn.post_uamtk()
        print("####################  post_uamtk  ###########")
        cn.post_uamauthclient()
        print("####################  post_uamauthclient  ###########")
        cn.get_userLogin()
        print("####################  get_userLogin ###########")
        cn.get_leftTicket()
        print("####################  get_leftTicket  ###########")
        cn.get_GetJS()
        print("####################  GetJS  ###########")
        cn.get_qufzjql()
        print("####################  get_queryZ  ###########")

        while cn.get_queryZ():
           print("####################  123  ###########")
           time.sleep(3)
      
