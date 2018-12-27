#!/usr/bin/python
#-*- coding:utf-8 -*-

import os
import re
import json
import time
import urllib
import urllib2
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

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
        print u'请求索引页出错'
    return None
    
def parse_page_index(html):
    #将json格式的字符串转化成python对象，对象转换成json用 json.dumps()
    data=json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
        #yield 是url生成器 即取出article_url并生成url
            yield item.get('article_url')

def get_page_detail(url):
    response = requests.get(url)
    try:
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print '请求详情页出错'
    return None

def parse_page_detail(html,url):
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('title')[0].get_text()
    images_pattern= re.compile('var gallery = (.*?);',re.S)
    result = re.search(images_pattern,html)
    if result:
        data = json.loads(result.group(1))
        sub_images = data.get('sub_images')
        images = [item.get('url') for item in sub_images]
        
    return {'title' :title, 'url':url, 'images':images}

def main():
    html = get_index(0,'街拍')
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html, url)
            print result['title']

#----------------------------------------------------------------#

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
        print i['title']
        new_path = file_path + '\\' + i['title']
        if not os.path.isdir(new_path):
            os.makedirs(new_path)
        for p in i['image_list']:
            print p['url']
            name = p['url'].split('/')[-1]
            print name
            picture_url = p['url'].replace("list", "large")
            download_picture(new_path, name, "http:" + picture_url)
            
def main_picture():
    for i in xrange(5):
        html = get_index(i*20, '校花')
        get_picture(html)

#--------------------------------------------------------------------#
'''
    煎蛋网不是json动态加载，直接用beacutifulsoup
'''
def get_url(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    data = soup.select('div.text > p > img')

    for i in data:
        s = i.attrs['src'][2:]
        file_path = os.getcwd() + '\image1'
        print file_path
        name = i.attrs['src'].split('/')[-1]
        download_picture(file_path, name, 'http://' + s)
        
def main_jiandan():
    for i in reversed(range(236)):
        url = 'http://jandan.net/ooxx/page-'+str(i)+'#comments'  
        if requests.get(url).status_code == 200:
            get_url(url)
        time.sleep(5)

        
if __name__ == '__main__':
    #main_picture()
    #main_jiandan()
    res = requests.get('https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-12-11&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=SHH&purpose_codes=ADULT')
    soup = BeautifulSoup(res.text, 'html.parser')
    s = str(soup)
    s = s.replace("true", "'true'")
    s = eval(s)
    print s['data']['result'][0].split("|")[0]