#!/usr/bin/python
#-*- coding:utf-8 -*-

import requests
import json
import time
import math
import hashlib

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
    cookies = {"tt_webid" : "6628718188178507272"}
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"}
    wbdata = requests.get(url, headers = headers, cookies = cookies).text
    #print wbdata
    wbdata2 = json.loads(wbdata)
    
    data = wbdata2['data']
    
    
    for news in data:
        title = news['title']
        news_url = news['source_url']
        news_url = "https://www.toutiao.com" + news_url

        #print(title, news_url)

    new_data = wbdata2['next']
    next_max_behot_time = new_data['max_behot_time']
    
    #print("next_max_behot_time: {0}".format(next_max_behot_time))
    return next_max_behot_time
        
refresh = 50
signature = 'vwnxGwAA4w4u8jivctQIIL8J8Q'
next_max_behot_time = 0

for x in range(5):
    print(u"第{0}次：".format(x))
    if x == 0:
        max_behot_time = 0
    else:
        max_behot_time = next_max_behot_time
        print(max_behot_time)
    
    AS, CP = getASCP()
    url = get_url(max_behot_time, AS, CP, signature)
    next_max_behot_time = get_item(url)
    
    time.sleep(5)