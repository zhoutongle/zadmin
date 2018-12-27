import requests
import re
import urllib.parse
import json
import datetime
from collections import OrderedDict

'''a2OPMLooc5pB41P%2B7HZubzMGVGKTin8ro1zISEgUI9UBgI%2FjtkGl7SBnOncPduolmUJSLiXvGpv9%0AFXcvQAHOlhiju5ZAYErfKc0jhgHJhxPxvigRTjdaJVoHY7%2F4wNs
qjgBB%2FRj0cH0kCZx9GHMPe8A7%0ATyTGleZ%2BL1UyyjnO0Zk0JLhJ5eYWnDGFdV2stBr9GWuD9YVlrh8HvdEH9DOPlws7tFeaUEWbOntE%0AOWrLGuNgT2UtVOmB3UEMD9%2Fruy
2P|预订|26000K772635|K7727|HDP|QTP|BXP|TJP|00:42|02:33|01:51|Y|MY2Y5Z9kIWkxpjiGWUbLhYPHtDDoBIDfLdfNKo%2BsjcH5%2F4Eo|20181219|3|P2|09|10|0|0|
||||||有||有|有|||||103010|131|1'''

self=requests.session()
self.verify=False
self.headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Host':'kyfw.12306.cn',
    'Cache-Control':'no-cache',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
def dow():
    url='https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand'
    requests.packages.urllib3.disable_warnings()
    res=self.get(url)
    print(res.status_code)
    if res.status_code==200:
       with open('login.jpg','wb') as f:
          f.write(res.content)
    else:
        dow()
#验证
def yanzhengma():
     #获取验证码
     dow()
     # 1 2 3 4 5 6 7 8
     xylist=['35,35','105,35','175,35','245,35','35,105','105,105','175,105','245,105']
     print('请依次输入验证码的位置并换行,0表示结束')
     ilist=[]
     while True:
        i=input()
        if i=='0':
            break
        ilist.append(xylist[int(i)-1])
     xy=','.join(ilist)
     print(xy)

     data={
         'answer':xy,
         'login_site':'E',
         'rand':'sjrand'
     }
     url='https://kyfw.12306.cn/passport/captcha/captcha-check'
     requests.packages.urllib3.disable_warnings()
     res=self.post(url,data=data)
     print(res.url)
     print(res.text)
     code=re.search('_code.*?(\d)',res.text,re.S).group(1)

     print(code)

     # 成功返回True，失败递归调用
     if code=='4':
         print('验证成功，请登陆')

     elif code=='5':
         print('验证错误')
         yanzhengma()
     elif code=='7':
         print('验证超时')
         yanzhengma()
     else:
         print('验证失败')
         yanzhengma()
def login():
     yanzhengma()#验证码
     data={
         'username':'',#用户名
         'password':'',#密码
         'appid':'otn'
     }
     url='https://kyfw.12306.cn/passport/web/login'
     requests.packages.urllib3.disable_warnings()
     res=self.post(url,data=data)
     print(res.text)
     code=re.search('_code.*?(\d)',res.text,re.S).group(1)


     # 成功返回True，失败递归调用
     if code=='0':
         yzdata={
         'appid':'otn'
         }
         tk_url='https://kyfw.12306.cn/passport/web/auth/uamtk'
         resp3=self.post(tk_url,data=yzdata)
         print('-----------------第一次验证-----------------')
         print(resp3.text)
         login_message=resp3.json()['newapptk']
         print('loginMessage=',login_message)
         yz2data={
             'tk':login_message
         }
         client_url='https://kyfw.12306.cn/otn/uamauthclient'
         resp4=self.post(client_url,data=yz2data)
         print('-----------------第二次验证-----------------')
         print(resp4.text)
         print('登陆成功，可以开始购票')

     elif code=='1':
         print('密码输入错误。如果输错次数超过4次，用户将被锁定。')
         login()
     else:

         print('登录失败')
         login()
def shoppiao():

    data={
       'leftTicketDTO.train_date':'2018-10-15',#时间
        'leftTicketDTO.from_station':'BJQ',#出发站码
        'leftTicketDTO.to_station':'CBN',#目的地码
        'purpose_codes':'ADULT'#票类型ADULT成人，STUDENT学生
    }
    url='https://kyfw.12306.cn/otn/leftTicket/query?'
    requests.packages.urllib3.disable_warnings()
    res=self.get(url,params=data)
    print(res.status_code)
    print(res.text)
    dictr=json.loads(res.text)
    pklist=dictr.get('data').get('result')
    for item in pklist:
        sp_item = item.split('|')
        for index, item in enumerate(sp_item,0):

            print('{}:\t{}'.format(index, item))
        '''
        通过分析
        0：列车信息（订票时候需要） 1：信息 2：火车编号
        3：列车号 4：始发站   5：终点站   6：起始站  7：目标站    8：出发时间       9：到达时间
        10：行车时间
        11：有3种状态：Y, N, IS_TIME_NOT_BUY 分别对应，可以预定，不可以预定，其他原因----对应的是第1项
        12：参数leftTicket
        13：日期
        14：
        15：参数train_location
        21：高级动卧   22：        23：软卧 24：软座  25：特等座  26：无座 28：硬卧  29：硬座  30：二等座  31：一等座  32：商务座 33：动卧
       '''
        if sp_item[11]=='Y':#可以买票，开始订票
            if sp_item[30]!='无':#买二等座
                print(sp_item[30])
                if vel_longin_2():#验证登陆
                   print('已经登陆可以开始下单')
                   self.headers['X-Requested-With']='XMLHttpRequest'
                   secretStr=urllib.parse.unquote(sp_item[0])


                   self.headers['Referer'] = 'https://kyfw.12306.cn/otn/leftTicket/init'

                   submitOrderRequest(secretStr)

                   data = OrderedDict()
                   data["_json_att"] =''
                   data["fromStationTelecode"] =sp_item[6]
                   data["leftTicket"] = sp_item[12]
                   data['purpose_codes']='00'
                   data['REPEAT_SUBMIT_TOKEN']=''
                   data["seatType"] = 'O'
                   data["stationTrainCode"] = sp_item[3]
                   data["toStationTelecode"] =sp_item[7]
                   data["train_date"] = str(datetime.datetime.strptime(sp_item[13], '%Y%m%d').strftime('%a %b %d %Y %H:%M:%S GMT+0800'))
                   data["train_location"] = sp_item[15]
                   data["train_no"] =sp_item[2]

                   '''
                   data={
                        'train_date':str(datetime.datetime.strptime(sp_item[13], '%Y%m%d').strftime('%a %b %d %Y %H:%M:%S GMT+0800')),
                        'train_no':sp_item[2],#火车编号
                        'stationTrainCode':sp_item[3],#列车号
                        'seatType':'O',#座位类型 1是硬座(无座)，2是软座，3是硬卧，4是软卧,  O 大写字母  是高铁二等座，M是高铁一等座，商务座(9),特等座(P),高级软卧(6)
                       'fromStationTelecode':sp_item[6],#起始站编号
                        'toStationTelecode':sp_item[7],#目标站编号
                        'leftTicket':sp_item[12],
                        'train_location':sp_item[15],#15项Q6
                   }
                '''
                   shopdin(data)

                else:
                    login()
                    shoppiao()
        break

def submitOrderRequest(secretStr):
    data = OrderedDict()
    data["secretStr"] = secretStr
    data["train_date"] = '2018-09-20'
    data["tour_flag"] = "dc"
    data["purpose_codes"] = "ADULT"
    data["query_from_station_name"] ='深圳'
    data["query_to_station_name"] = '赤壁'
    data["undefined"] = ''
    url='https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
    res=self.post(url,data=data)
    print(res.text)
#开始下单
def shopdin(data1):
    #获取1个参数
    liop=initDc()
     #改变Headers
    self.headers['Referer'] = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
    self.headers['Origin']='https://kyfw.12306.cn'
    print(self.headers)
    #请求并获取联系人参数
    pasdir=PassengerDTOs(liop[0])
    print(type(pasdir))
    # 二等座 0  (车票类型:ticket_type_codes 成人票1)      ,1,张三(passenger_name),   1(证件类型:passenger_id_type_code),320xxxxxx(passenger_id_no),151xxxx(mobile_no),N
    passengerTicketStr=data1['seatType']+ ',0,'+pasdir['passenger_type']+','+pasdir['passenger_name']+','+pasdir['passenger_id_type_code']+','+pasdir['passenger_id_no']+','+pasdir['mobile_no']+',N'
    #张三(passenger_name),1(证件类型:passenger_id_type_code),320xxxxxx(passenger_id_no),1(passenger_type)_
    oldPassengerStr=pasdir['passenger_name']+','+pasdir['passenger_id_type_code']+','+pasdir['passenger_id_no']+','+pasdir['passenger_type']+'_'
    data = OrderedDict()
    data["_json_att"] =''
    data["ed_level_order_num"] ='000000000000000000000000000000'
    data["cancel_flag"] ='2'
    data["oldPassengerStr"] = oldPassengerStr
    data["passengerTicketStr"] = passengerTicketStr
    data["randCode"] =''
    data["tour_flag"] ='dc'
    data["whatsSelect"] ='1'
    '''
    data={
        'cancel_flag':'2',#固定
        'ed_level_order_num':'000000000000000000000000000000',#固定
        'passengerTicketStr':passengerTicketStr,#联系人
        'oldPassengerStr':oldPassengerStr,#联系人
        'tour_flag':'dc',#单程
        'randCode':'',#空
        'whatsSelect':'1',#是否选择了联系人,
    }
    '''
    OrderInfo(data)
    data1['REPEAT_SUBMIT_TOKEN']=liop[0]
    #提交订单
    getQueueCount(data1)
    data2= OrderedDict()
    data2["_json_att"] =''#空
    data2["choose_seats"] =''#空
    data2["dwAll"] ='N'#固定
    data2["key_check_isChange"] =liop[1]#页面找
    data2["leftTicketStr"] = data1['leftTicket']#列车
    data2["oldPassengerStr"] =oldPassengerStr#联系人
    data2["passengerTicketStr"] =passengerTicketStr#联系人
    data2["purpose_codes"] ='00'#
    data2["randCode"] =''#随机数 空
    data2["REPEAT_SUBMIT_TOKEN"] =liop[0]
    data2["roomType"] ='00'#固定
    data2["seatDetailType"] ='000'#选铺 暂不支持 默认参数
    data2["train_location"] = data1['train_location']#q6
    data2["whatsSelect"] ='1'#固定
    tijiao(data2)
def tijiao(data):
    url='https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
    res=self.post(url,data=data)
    print(res.status_code)
    print(res.text)
#获取联系人
def PassengerDTOs(REPEAT_SUBMIT_TOKEN):
    data={
        '_json_att':'',#空
        'REPEAT_SUBMIT_TOKEN':REPEAT_SUBMIT_TOKEN#页面找
    }
    url='https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
    res=self.post(url,data=data)
    #print(res.text)
    passen=res.json().get('data').get('normal_passengers')[1]
    print(passen)
    return passen

#订单页面----获取参数
def initDc():
    url='https://kyfw.12306.cn/otn/confirmPassenger/initDc'
    res=self.post(url,data={'_json_att':''})
    REPEAT_SUBMIT_TOKEN=re.search('globalRepeatSubmitToken = .(.*?).;',res.text,re.S).group(1)
    ticketInfoForPassengerForm_name = re.compile(r'var ticketInfoForPassengerForm=(\{.+\})?')
    order_request_params_name = re.compile(r'var orderRequestDTO=(\{.+\})?')
    re_tfpf = re.findall(ticketInfoForPassengerForm_name, res.text)
    re_orp = re.findall(order_request_params_name, res.text)
    key_check_isChange=re.search('key_check_isChange.:.(.*?).,',res.text,re.S).group(1)
    return [REPEAT_SUBMIT_TOKEN,key_check_isChange]
 #选乘客票种提交
def OrderInfo(data):
    url='https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
    res=self.post(url,data=data)
    print(res.status_code)
    print(res.text)
#提交订单列车余票。
def getQueueCount(data):
    url='https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
    res=self.post(url,data=data)
    print(res.status_code)
    print(res.text)
def vel_longin_2():
    url='https://kyfw.12306.cn/otn/login/checkUser'
    requests.packages.urllib3.disable_warnings()
    res=self.post(url,data={'_json_att':''})
    login_vel=res.json().get('data')['flag']

    return login_vel
if __name__ == '__main__':
    #yanzhengma()
    shoppiao()
    vel_longin_2()