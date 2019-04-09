#!/usr/bin/env python
#-*- coding: utf-8 -*-
#Auth : ztl
#time : 2019-4-9
#python_version : 3.6

import requests
import re,json,os
from hashlib import md5
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from requests.exceptions import RequestException
#引入模块config中所有变量

import settings

def get_page_index(offset, keyword):
    # 获取页面的HTML
    data = {
        'aid': 24,
        'app_name': 'web_search',
        'en_qc': '1',
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1,
        'from':'search_tab',
        'pd': 'synthesis'
    }
    try:
        url = 'https://www.toutiao.com/api/search/content?' + urlencode(data)
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求失败')
        return None

def get_page_detial(url):
    #请求详情页的url
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4882.400 QQBrowser/9.7.13039.400'}
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页失败')
        return None

def parse_page_index(data):
    # 获取所有详情页的url
    if data and 'data' in data.keys():
        info = data['data']
        for sub in info:
            if sub and 'share_url' in sub.keys():
                yield sub['share_url']

def parse_page_detial(html):
    #获取详情页的标题和图片地址url
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    new_path = settings.PICTURE_PATH + title
    if not os.path.isdir(new_path):
        os.makedirs(new_path)

    #利用正则提取图片地址
    info = re.findall('http://(.*?)&quot', html)
    images = ['http://' + sub for sub in info]
    for image in images:
        download_image(image, title)

def save_image(result, title):
    file_path = '{0}{1}\\{2}{3}'.format(settings.PICTURE_PATH, title, md5(result).hexdigest(), '.jpg')
    file_path = file_path.replace("\\", "/")
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(result)

def download_image(url, title):
    try:
        print('正在下载',url)
        r = requests.get(url)
        if r.status_code == 200:
            save_image(r.content, title)
        return False
    except RequestException:
        print('请求图片出错')
        return False
        
def main(offset, KEY_WORD):
    # 调用函数
    html = get_page_index(offset,KEY_WORD)
    html = html.encode('utf-8').decode()
    html = html.replace("false", "'false'").replace("true", "'true'").replace("null", "'null'")
    html = eval(html)

    for url in parse_page_index(html):
        html = get_page_detial(url)
        if html:
            result = parse_page_detial(html)

if __name__ == '__main__':
    main(0, '演员')
