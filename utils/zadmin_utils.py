#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
import os
import sys
import json
import time
import math
import psutil
import random
import hashlib
import requests
import datetime
import traceback
from PIL import Image
from json import loads
from time import ctime, sleep
from bs4 import BeautifulSoup
from collections import OrderedDict

python_version = sys.version.split(" ")[0].split(".")[0]
if python_version == '2':
    import pyttsx
    reload(sys)
    sys.setdefaultencoding('utf-8')
else:
    import imp
    imp.reload(sys)
    import pyttsx3
    from urllib import parse

currpath = os.path.join(os.getcwd(), os.path.dirname(__file__))
songs_path = os.path.join(currpath[:currpath.rfind('utils')], 'static\\song\\')
code_path = os.path.join(currpath[:currpath.rfind('utils')], 'static\\img\\auth_code.png')
song_list_path = os.path.join(currpath[:currpath.rfind('utils')], 'data\\song_list.json')
label_list_path = os.path.join(currpath[:currpath.rfind('utils')], 'data\\label_list.json')
article_list_path = os.path.join(currpath[:currpath.rfind('utils')], 'data\\article_list.json')
week = {0 : '星期日', 1 : '星期一', 2 : '星期二', 3 : '星期三', 4 : '星期四', 5 : '星期五', 6 : '星期六'}

def analysis_lrc(song_name):
    info = []
    song_name = songs_path + song_name +".lrc"
    if python_version == "2":
        with open(song_name, "r") as f:
            info = f.readlines()
    else:
        with open(song_name, "r", encoding="utf-8") as f:
            info = f.readlines()
        
    lrc = []
    for i in info:
        temp = {}
        if "[" in i and '.' in i:
           time = i.split("]")[0].split("[")[1]
           temp['time'] = float(time.split(":")[0])*60 + float(time.split(":")[1])
           temp['message'] = i.split(']')[1]
        if "[" in i and '.' not in i:
           time = i.split("]")[0].split("[")[1]
           temp['time'] = 0.0
           temp['message'] = time
        lrc.append(temp)

    return lrc
    
def get_song_list():
    song_list = []
    if python_version == "2":
        with open(song_list_path, "r") as f:
            song_list = json.load(f)
    else:
        with open(song_list_path, "r", encoding="utf-8") as f:
            song_list = json.load(f)

    return song_list
 
def read_content(content):
    if python_version == '2':
        engine = pyttsx.init()
        engine.say(content)
        engine.runAndWait()
    else:    #pip3 install pypiwin32
        engine = pyttsx3.init()    
        engine.say(content)
        engine.runAndWait()
    
    return '0'
    
def get_system_encoding():
    """
    The encoding of the default system locale but falls back to the given
    fallback encoding if the encoding is unsupported by python or could
    not be determined. See tickets #10335 and #5846
    """
    try:
        encoding = locale.getdefaultlocale()[1] or 'ascii'
        codecs.lookup(encoding)
    except Exception as e:
        encoding = 'ascii'
    return encoding
    
def is_win32():
    
    mswindows = (sys.platform == "win32")
    
    return mswindows
    
def is_linux2():

    linux = (sys.platform == "linux2")
    
    return linux
    
#-------------------------------------------------------#
'''
    get article from www.toutiao.com
'''
def getASCP():
    t = int(math.floor(time.time()))
    e = hex(t).upper()[2:]
    m = hashlib.md5()
    m.update(str(t).encode(encoding='utf-8'))
    i = m.hexdigest().upper()
    
    if len(e) != 8:
        AS = '479BB4B7254C150'
        CP = '7E0AC8874BB0985'
        return AS, CP
        
    n = i[0:5]
    a = i[-5:]
    s = ''
    r = ''
    for o in range(5):
        s += n[o] + e[o]
        r += e[o + 3] + a[o]
        
    AS = 'A1' +  s + e[-3:]
    CP = e[0:3] + r + 'E1'
    
    #print("AS : {}, CP: {}".format(AS, CP))
    
    return AS, CP
    
def get_url(max_behot_time, AS, CP, signature):
    url = ('https://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1'
           '&max_behot_time={0}'
           '&max_behot_time_tmp={0}' 
           '&tadrequire=true'
           '&as={1}'
           '&cp={2}'
           '&_signature={3}'.format(0, AS, CP, signature))
           
    #print(url)
    return url
    
def get_item(url):
    try:
        cookies = {"tt_webid" : "6628718188178507272"}
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"}
        wbdata = requests.get(url, headers = headers, cookies = cookies).text
        #print wbdata
        wbdata2 = json.loads(wbdata)
        
        data = wbdata2['data']
       
        info_list = []
        for news in data:
            #for i in news.keys():
            #    print i," :: ", news[i]
            #print "-----------------------------------"
            tag = "chinese_tag" in news and news['chinese_tag'] or '-'
            title = news['title']
            table = 'label' in news and news['label'] or '-'
            source = 'source' in news and news['source'] or '-' 
            comments = "comments_count" in news and news['comments_count'] or 0
            news_url = news['source_url']
            news_url = "https://www.toutiao.com" + news_url

            info_list.append({"title": title, "url": news_url, 'tag': tag, 'table': table, 'source': source, 'comments': comments})
            #print(title, news_url)

        new_data = wbdata2['next']
        next_max_behot_time = new_data['max_behot_time']
    
        #print("next_max_behot_time: {0}".format(next_max_behot_time))
        return next_max_behot_time, info_list
    except Exception as e:
        pass

def article_main():
    refresh = 5
    signature = 'vwnxGwAA4w4u8jivctQIIL8J8Q'
    next_max_behot_time = 0

    article_list = []


    for x in range(refresh):
        #temp = {}
        #print(u"第{0}次：".format(x))
        if x == 0:
            max_behot_time = 0
        else:
            max_behot_time = next_max_behot_time
            #print(max_behot_time)
        
        AS, CP = getASCP()
        url = get_url(max_behot_time, AS, CP, signature)
        
        info = get_item(url)
        #next_max_behot_time = info[0]
        #temp['title'] = info[1]
        #temp['url'] = info[2]
        article_list.extend(info[1])
        #print article_list
    try:
        with open(article_list_path, "r+") as f:
            article = json.load(f)
            article.extend(article_list)
            f.seek(0)
            json.dump(article, f)
    except Exception as e:
        print(traceback.format_exc())
    #return article_list
    return article
    
    
def get_article_info(url):
    print(url)
    source = ''
    time = ''
    comments_count = ''
    try:
        headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"}
        session = requests.Session()
        response = session.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        html = soup.select("script")
        for i in  html[6].get_text().split(','):
            if "source" in i:
                i = i.encode('raw_unicode_escape')
                source = i.split(": ")[1]
                #print "source: {}".format(i.split(": ")[1])
            elif "time" in i:
                time = i.split(": ")[1].split('}')[0]
                #print "time: {}".format(i.split(": ")[1].split('}')[0])
            elif "comments_count" in i:
                comments_count = i.split(": ")[1]
                #print "comments_count: {}".format(i.split(": ")[1])
                break    
        return source, time, comments_count
    except Exception as e:
        return '', '', ''
#-------------------------------------------------------#
'''
    get picture
'''
def get_index(offset, keyword):
    '''
       今日头条网页涉及json动态加载
    '''
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3,
        'from': 'search_tab',
        'pd': ''
    }
    url = 'http://www.toutiao.com/search_content/?' + urllib.urlencode(data)
    response = requests.get(url)
    try:
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print(u'请求索引页出错')
    return None
    
def download_picture(file, name, html):
    #r = requests.get(html, stream=True)
    filename = os.path.join(file, name + '.jpg')
    #with open(filename, 'wb') as f:
    #    f.write(r.content)
    res = urllib2.Request(html)
    r = urllib2.urlopen(res)
    with open(filename, 'wb') as f:
        f.write(r.read())    
    
        
def get_picture(html):
    #url = 'http://www.toutiao.com/search_content/?offset=0&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=1'
    #res = requests.get(url)
    #json_data = json.loads(res.text)
    json_data = json.loads(html)
    data = json_data['data']
    
    temp = os.getcwd().split("\\")[:-1]
    temp.append("static")
    temp.append("img")
    temp.append("image1")
    file_path = "\\".join(temp)
    #print file_path  
   
    for i in data:
        print(i['title'])
        new_path = file_path + '\\' + i['title']
        if not os.path.isdir(new_path):
            os.makedirs(new_path)
        for p in i['image_list']:
            #print p['url']
            name = p['url'].split('/')[-1]
            #print name
            picture_url = p['url'].replace("list", "large")
            download_picture(new_path, name, "http:" + picture_url)
            
def main_picture():
    html = get_index(0, '校花')
    get_picture(html)
    
#----------------------------------------------------------------#
def test(qq):
    return unicode(qq, "utf-8").encode('gbk')
    
def get_train_ticket(from_station, to_station, train_time):
    print("-----------------------------------")
    print(from_station, to_station, train_time)
    kv = {'user-agent': 'Mozilla/5.0'}
    train_info = []
    break_flag = False
    url1 = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9006'
    response1 = requests.get(url1, headers=kv)
    stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response1.text)
    sta_cod = dict(stations)                        # 车站名称对应的代码
    cod_sta = {v : k for k, v in sta_cod.items()}    # 代码对应的车站名称

    while 1:    # 多次查询
        k = [0, 0, 0]
        if break_flag:
            break
        while sum(k) != 3:
            # train_data = raw_input(test("请输入出发时间(格式:20180131):"))
            # from_station = raw_input(test("请输入出发站:"))
            # to_station = raw_input(test("请输入到达站:"))
            #train_time = '2018-12-25'
            #from_station = '北京'
            #to_station = '郑州'
            if len(train_time) == 10:
                year  = train_time.split('-')[0] 
                month = train_time.split('-')[1] 
                day   = train_time.split('-')[2]
                year  = eval(year)
                if eval(month[0]) != 0:
                    month = eval(month)
                else:
                    month = eval(month[1])
                if eval(day[0]) != 0:
                    day = eval(day)
                else:
                    day = eval(day[1])
                if month < 1 or month > 12 or day < 0 or day > 31:
                    print('1,出发日期输入错误！')
                    break_flag = True
                    break
                elif month in [1, 3, 5, 7, 8, 10, 12]:
                    k[0] = 1
                elif month in [4, 6, 9, 11]:
                    if day < 31:
                        k[0] = 1
                    else:
                        print('2,出发日期输入错误！')
                        break_flag = True
                        break
                else:
                    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
                        if day < 30:
                            k[0] = 1
                        else:
                            print('3,出发日期输入错误！')
                            break_flag = True
                            break
                    else:
                        if day < 29:
                            k[0] = 1
                        else:
                            print('4,出发日期输入错误！')
                            break_flag = True
                            break
            else:
                print('5,出发日期输入错误！')
                break_flag = True
                break
     
            if from_station.find('站') == -1:
                k[1] = 1
                #python2 or python3 
                if python_version == '2':
                    from_station = sta_cod[from_station.decode('utf-8')]
                else:
                    from_station = sta_cod[from_station]
            elif from_station.find('站') != -1:
                k[1] = 1
                from_station = sta_cod[from_station[0:(len(from_station) - 1)]]
            else:
                print(test('出发站输入错误！'))
                break_flag = True
                break
     
            if to_station.find('站') == -1:
                k[2] = 1
                #python2 or python3
                if python_version == '2':
                    to_station = sta_cod[to_station.decode('utf-8')]
                else:
                    to_station = sta_cod[to_station]
            elif to_station.find('站') != -1:
                k[2] = 1
                to_station = sta_cod[to_station[0:(len(to_station) - 1)]]
            else:
                print(test('到达站输入错误！'))
                break_flag = True
                break
        # 火车票信息查询接口
               #https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2018-12-26        &leftTicketDTO.from_station=BJP                 &leftTicketDTO.to_station=SHH               &purpose_codes=ADULT
        url2 = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=' + train_time + '&leftTicketDTO.from_station=' + from_station + '&leftTicketDTO.to_station=' + to_station + '&purpose_codes=ADULT'
        print(url2)
        response2 = requests.get(url2, headers=kv)
        #soup2 = BeautifulSoup(response2.text, 'html.parser')
        #Str_tmp = str(soup2)    # 将获得的网页源码转换成字符串
        
        #Str = Str_tmp.replace("true", "'true'")
        k = []
        k_tmp = -1
        #print(Str)
        #Mes = eval(Str)         # 字符串转换成字典
        Mes = response2.json()
        if Mes['messages']:
            print(test('选择的查询日期不在预售日期范围内！\n'))
            break_flag = True
            break
        elif Mes['data']['result'] == [] and Mes['messages'] ==[]:
            print('很抱歉，按您的查询条件，当前未找到从 {:} 到 {:} 的列车！\n'.format(cod_sta[from_station], cod_sta[to_station]))
            break_flag = True
            break
        else:
            mes = Mes['data']['result']
            tra_cod = []  # 车次
            sta_beg = []  # 始发站
            sta_end = []  # 终到站
            sta_lea = []  # 起始站
            sta_arr = []  # 终点站
            t_lea = []    # 出发时间
            t_arr = []    # 到达时间
            t_dur = []    # 历时
            t_dat = []    # 出发日期
            tic = []      # 是否有票
            gr = []       # 高级软卧
            rw = []       # 软卧
            rz = []       # 软座
            wz = []       # 无座
            yw = []       # 硬卧
            yz = []       # 硬座
            edz = []      # 二等座
            ydz = []      # 一等座
            swz = []      # 商务座
            dw = []       # 动卧
     
            for i in range(0, len(mes)):    # 根据字符串特征提取相关信息
                for j in range(0, len(mes[i])):
                    k_tmp = mes[i].find('|', k_tmp + 1)
                    if k_tmp == -1:
                        break
                    k.append(k_tmp)
                tra_cod.append(mes[i][(k[2] + 1):k[3]])
                sta_beg.append(cod_sta[mes[i][(k[3] + 1):k[4]]])
                sta_end.append(cod_sta[mes[i][(k[4] + 1):k[5]]])
                sta_lea.append(cod_sta[mes[i][(k[5] + 1):k[6]]])
                sta_arr.append(cod_sta[mes[i][(k[6] + 1):k[7]]])
                t_lea.append(mes[i][(k[7] + 1):k[8]])
                t_arr.append(mes[i][(k[8] + 1):k[9]])
                t_dur.append(mes[i][(k[9] + 1):k[10]])
                tic.append(mes[i][(k[10] + 1):k[11]])
                t_dat.append(mes[i][(k[12] + 1):k[13]])
                gr.append(mes[i][(k[20] + 1):k[21]])
                rw.append(mes[i][(k[22] + 1):k[23]])
                rz.append(mes[i][(k[23] + 1):k[24]])
                wz.append(mes[i][(k[25] + 1):k[26]])
                yw.append(mes[i][(k[27] + 1):k[28]])
                yz.append(mes[i][(k[28] + 1):k[29]])
                edz.append(mes[i][(k[29] + 1):k[30]])
                ydz.append(mes[i][(k[30] + 1):k[31]])
                swz.append(mes[i][(k[31] + 1):k[32]])
                dw.append(mes[i][(k[32] + 1):k[33]])
                for h in range(0, len(gr)):     # 表示列车不存在相关票种
                    if gr[h].strip() == '':
                        gr[h] = '--'
                    if rw[h].strip() == '':
                        rw[h] = '--'
                    if rz[h].strip() == '':
                        rz[h] = '--'
                    if wz[h].strip() == '':
                        wz[h] = '--'
                    if yw[h].strip() == '':
                        yw[h] = '--'
                    if yz[h].strip() == '':
                        yz[h] = '--'
                    if edz[h].strip() == '':
                        edz[h] = '--'
                    if ydz[h].strip() == '':
                        ydz[h] = '--'
                    if swz[h].strip() == '':
                        swz[h] = '--'
                    if dw[h].strip() == '':
                        dw[h] = '--'
                k_tmp = -1
                del k[0:(len(k) + 1)]
            #输出格式统一
            tplt = "{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}"
            #print(tplt.format(test("车次"), test("车站"), test("时间"), test("历时"), test("商务座"), test("一等座"), test("二等座"), test("高级软卧"), test("软卧"), test("动卧"), test("硬卧"), test("软座"), test("硬座"), test("无座")))
            #for i in range(0, len(mes)):
                #print(tplt.format(tra_cod[i], sta_lea[i], t_lea[i], t_dur[i], swz[i], ydz[i], edz[i], gr[i], rw[i], dw[i], yw[i], rz[i], yz[i], wz[i]))
                #print(tplt.format("", sta_arr[i], t_arr[i], "", "", "", "", "", "", "", "", "", "", ""))
                #print("")
            for i in range(0, len(mes)):
                temp = {}
                temp['tra_cod'] = tra_cod[i]
                temp['sta_lea'] = sta_lea[i]
                temp['t_lea'] = t_lea[i]
                temp['t_dur'] = t_dur[i]
                temp['swz'] = swz[i]
                temp['ydz'] = ydz[i]
                temp['edz'] = edz[i]
                temp['gr'] = gr[i]
                temp['rw'] = rw[i]
                temp['dw'] = dw[i]
                temp['yw'] = yw[i]
                temp['rz'] = rz[i]
                temp['yz'] = yz[i]
                temp['wz'] = wz[i]
                train_info.append(temp)

            return train_info

#---------------------------------------------------------------------#
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
        "born_date":"1993-08-09 00:00:00",
        "country_code":"CN",
        "passenger_id_type_code":"1",
        "passenger_id_type_name":"中国居民身份证",
        "passenger_id_no":"411528199308093314",
        "passenger_type":"1",
        "passenger_flag":"0",
        "passenger_type_name":"成人",
        "mobile_no":"18301049957",
        "phone_no":"",
        "email":"1140082051@qq.com",
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

#生产一个18位的随机数
def get_random():
    return str(random.random())
 
#一个十三位的时间戳    
def get_13_time():
    return str(int(time.time()*1000))

    
class CN12306(object):
    def __init__(self):
    
        self.default_headers = {
            'Host':'kyfw.12306.cn',
            'Connection':'keep-alive',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer':'https://kyfw.12306.cn/otn/index/init',
            'Accept-Language':'zh-CN,zh;q=0.9',
        }
        self.locate = {
            '1':'44,44,',
            '2':'114,44,',
            '3':'185,44,',
            '4':'254,44,',
            '5':'44,124,',
            '6':'114,124,',
            '7':'185,124,',
            '8':'254,124,',
        }
        self.train_time = ''
        self.s        = requests.session()
        self.s.verify = False        #忽略https 证书验证
        self.codes    = ''
        self.username = ''
        self.password = ''
        self.train_info = []
        self.user_info  = {}
        self.passenger_ticket = ''
        self.old_passenger    = ''     
        self.user_name        = ''     #登陆者（买票者）
        self.from_station     = ''     #出发地（北京）
        self.to_station       = ''     #目的地（郑州）
        self.station_code     = {}     #车站名称对应的代码  {'北京' : BJP'}
        self.seattype         = ''     #座位的类型（无座，硬座...）


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
        with open(code_path, 'wb') as f:
            f.write(r.content)
    
    #验证验证码是否正确提交方式post
    def auth_auth_code(self):
        url  = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
        print(type(self.codes))
        data = {
            'answer' : self.codes,
            'login_site' : 'E',
            'rand' : 'sjrand',
        }
        r = self.s.post(url=url,data=data)
        #result = loads(r.content.decode("utf-8"))     #result = r.json()
        #{'result_code': '8', 'result_message': '验证码校验失败,信息为空'}
        #{'result_code': '4', 'result_message': '验证码校验成功'}
        #{'result_code': '5', 'result_message': '验证码校验失败'}
        #print(r.json())
        return r.json()
 
    def login(self, username, password):
        print(username, password)
        url  = 'https://kyfw.12306.cn/passport/web/login'
        data = {
            'username' : username,
            'password' : password,
            'appid' : 'otn',
        }
        r = self.s.post(url=url,data=data)
        self.uamtk = r.json()["uamtk"]
     
        print(r.text)
 
    def userLogin(self):
        url = 'https://kyfw.12306.cn/otn/login/userLogin'
        r   = self.s.post(url=url)
        
    #不知道是干啥的，但是也提交吧        
    def getjs(self):  
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
        r.encoding = 'utf-8'
        self.apptk = r.json()["apptk"]
        self.user_name = r.json()["username"]
        print(r.text)
        return r.json()
        
    def get_userLogin(self):
        url = 'https://kyfw.12306.cn/otn/login/userLogin'
        r   = self.s.get(url)
        r.encoding = 'utf-8'
        
    def get_leftTicket(self):
        url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        r   = self.s.get(url)
        r.encoding = 'utf-8'
        
    def get_GetJS(self):
        url = 'https://kyfw.12306.cn/otn/HttpZF/GetJS'
        self.s.get(url)
     
    def get_qufzjql(self):
        url = 'https://kyfw.12306.cn/otn/dynamicJs/qufzjql'
        self.s.get(url)
 
    def get_queryZ(self):
        try:
            url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes={}'.format(self.train_time, self.from_station, self.to_station,'ADULT')
            print(url)
            r = self.s.get(url)
            r.encoding='utf-8'
            cheliang = r.json()["data"]["result"]
            print(r.json().keys())
        except Exception as e:
            print(traceback.format_exc())
            cheliang = []
            
        try:
            while True:
                for i in cheliang[::]:
                    dandulist = str(i).split('|')
                    self.train_info = dandulist
                    if len(str(dandulist[0])) >= 100:
                        self.secretStr = parse.unquote(dandulist[0])
                        train_index  = str(dandulist[3])  #车次 = str(dandulist[3])
                        start_time   = str(dandulist[8])  #出发时间 = str(dandulist[8])
                        to_time      = str(dandulist[9])  #到达时间 = str(dandulist[9])
                        process_time = str(dandulist[10]) #历时 = str(dandulist[10])
                        soft_wo      = str(dandulist[23]) #软卧 = str(dandulist[23])
                        hard_wo      = str(dandulist[28]) #硬卧 = str(dandulist[28])
                        hard_zuo     = str(dandulist[29]) #硬卧 = str(dandulist[28])
                        print('可预订车次列表，','车次：', train_index,'出发时间：', start_time,'到达时间：', to_time,'历时：', process_time,'软卧剩余： ',soft_wo,' 硬卧剩余： ',hard_wo, '硬座剩余：',hard_zuo)
                        #if (soft_wo != '' and soft_wo != '0' and soft_wo != '无' and soft_wo != '空') or \
                        #   (hard_wo != '' and hard_wo != '0' and hard_wo != '无' and hard_wo != '空'):
                        #if hard_wo != '' and hard_wo != '0' and hard_wo != '无' and hard_wo != '空' and train_index == 'T289':
                        if hard_zuo != '' and hard_zuo != '0' and hard_zuo != '无' and hard_zuo != '空':
                            print("可以预定！")
                            #执行下单操作
                            print("############### 提交预定请求 ###############")
                            self.post_submitOrderRequest()
                            print("############### 确认乘客信息 ###############")
                            self.post_initDc()
                            print("############### 获取乘客信息 ###############")
                            self.post_getPassengerDTOs()
                            print("############### 确认订单信息 ###############")
                            self.post_checkOrderInfo()
                            print("############### 提交预定请求 ###############")
                            self.post_getQueueCount()
                            print("############### 确认配置信息 ###############")
                            result = self.post_confirmSingleForQueue()
                            print(result)
                            if result["data"]["errMsg"] == "系统繁忙，请稍后重试！":
                                print("error!!!!!!!!!")
                                sleep(3)
                                self.get_queryZ()
                            #return True
                                   
                        print('*****************************************************')
                        sleep(3)
        except Exception as e:
            print(traceback.format_exc())
        return "0"
 
    # 点击预定下单
    def post_submitOrderRequest(self):
        url  = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        data = {
            'secretStr':self.secretStr,
            'train_date':self.train_time,         #出发时间
            'back_train_date':self.train_time ,   #返回时间
            'tour_flag':'dc',                     #固定
            'purpose_codes':'ADULT',
            'query_from_station_name':self.from_station,
            'query_to_station_name':self.to_station,
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
        for passenger in r.json()["data"]["normal_passengers"]:
            if passenger["passenger_name"] == self.user_name:
                print(passenger)
                self.user_info = passenger
            print("{} : {}".format(passenger["code"], passenger['passenger_name']))
        
        self.passenger_ticket = '{},0,{},{},{},{},{},N'.format(self.seattype, self.user_info['passenger_type'], self.user_info['passenger_name'], self.user_info['passenger_id_type_code'], self.user_info['passenger_id_no'], self.user_info['mobile_no']) #'3,0,1,周同乐,1,411528199308093314,18301049957,N' , (车票类型，0， 姓名， 证件类型，证件号， 手机号，N)
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
            "seatType": self.seattype,                           #座位类型 1是硬座(无座)，2是软座，3是硬卧，4是软卧,  O 大写字母  是高铁二等座，M是高铁一等座，商务座(9),特等座(P),高级软卧(6)
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
        res.encoding = 'utf-8'
        return res.json()

    def sta_code(self, from_station, to_station, train_time, seattype):
        url1 = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9006'
        res = self.s.get(url1, headers={'user-agent': 'Mozilla/5.0'})
        stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', res.text)
        sta_cod = dict(stations)                                        # 车站名称对应的代码
        self.station_code = sta_cod
        self.from_station = sta_cod[from_station]
        self.to_station = sta_cod[to_station]
        self.train_time = train_time
        self.seattype = seattype

#--------------------------------------------------------------------------------------#
'''
获得磁盘的使用情况
'''

def get_disk_info():
    unit_list = ['B', 'KB', "MB", "GB", "PB"]
    disk = []
    for id in psutil.disk_partitions():
        temp = {}
        if 'cdrom' in id.opts or id.fstype == '':  
            continue  
        disk_name = id.device.split(':')  
        disk_info = psutil.disk_usage(id.device)  
        temp['id']    = disk_name[0]
        #temp['info']  = psutil.disk_usage(id.mountpoint)
        if disk_info.used > disk_info.free:
            free = disk_info.free
            used = disk_info.used
            total = disk_info.total
            unit_num = 0
            while free > 1024:
                free = free/1024
                unit_num += 1

            temp['unit'] = unit_list[unit_num]
            while unit_num > 0:
                used = used/1024
                total = total/1024
                unit_num -= 1
            if python_version == '2':                           #python2 or python3
                temp['free'] = int(str(free).split("L")[0])
                temp['used']  = int(str(used).split("L")[0])
                temp['total']  = int(str(total).split("L")[0])
            else:
                temp['free'] = int(free)
                temp['used'] = int(used)               
                temp['total'] = int(total)
        else:
            used = disk_info.used
            free = disk_info.free
            total = disk_info.total
            unit_num = 0
            while used > 1024:
                used = used/1024
                unit_num += 1
            temp['unit'] = unit_list[unit_num]
            while unit_num > 0:
                free = free/1024
                total = total/1024
                unit_num -= 1
            if python_version == '2':                           #python2 or python3
                temp['free'] = int(str(free).split("L")[0])
                temp['used']  = int(str(used).split("L")[0])
                temp['total']  = int(str(total).split("L")[0])
            else:
                temp['free'] = int(free)
                temp['used'] = int(used)               
                temp['total'] = int(total)
        temp['percent'] = disk_info.percent
        disk.append(temp)
    return disk
