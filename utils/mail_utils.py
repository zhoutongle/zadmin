#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
 
import poplib
import sys
import os
import traceback
 
# 输入邮件地址, 口令和POP3服务器地址:
# email = input('Email: ')
# password = input('Password: ')
# pop3_server = input('POP3 server: ')
 
# 新浪邮箱测试通过, 密码使用登陆密码
# email = "18937905850@sina.cn"
# password = "password"
# pop3_server = "pop.sina.cn"
 
 
# qq邮箱测试通过， 使用授权码， 使用ssl
# email = "343190282@qq.com"
# password = "16位授权码"
# pop3_server = "pop.qq.com"
email = '1140082051@qq.com'
password = 'trpoyjqnoqykgjha'
pop3_server = 'imap.qq.com'
 
def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset
 
 
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value
 
 
def print_info(msg, indent=0):
    try:
        #print "+++++++++++++ %s" % indent
        info = {}
        if indent == 0:
            for header in ['From', 'To', 'Subject']:
                value = msg.get(header, '')
                if value:
                    if header == 'Subject':
                        value = decode_str(value)
                    else:
                        hdr, addr = parseaddr(value)
                        name = decode_str(hdr)
                        value = u'%s <%s>' % (name, addr)
                print('%s%s: %s' % ('  ' * indent, header, value))
                info[header] = value
                
        #print msg.is_multipart()
        #if (msg.is_multipart()):
        parts = msg.get_payload()
        msg = parts[0]
        #for n, part in enumerate(parts):
        #    msg = part
        #        print('%spart %s' % ('  ' * indent, n))
        #        print('%s--------------------' % ('  ' * indent))
        #        print_info(part, indent + 1)
        #else:
        content_type = msg.get_content_type()
        print(content_type)
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
                info['content'] = content
            print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))
    except Exception as e:
        print(traceback.format_exc())
    return info
 

def get_mail():
    mail_info = []
    # 连接到POP3服务器:
    #server = poplib.POP3(pop3_server)
    # qq需要使用ssl
    # server = poplib.POP3_SSL(pop3_server)
    server = poplib.POP3_SSL(pop3_server,'995')
    # 可以打开或关闭调试信息:
    server.set_debuglevel(1)
    # 可选:打印POP3服务器的欢迎文字:
    print(server.getwelcome().decode('utf-8'))
    # 身份认证:
    server.user(email)
    server.pass_(password)
    # stat()返回邮件数量和占用空间:
    print('Messages: %s. Size: %s' % server.stat())
    # list()返回所有邮件的编号:
    resp, mails, octets = server.list()
    # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
    print(mails)
    # 获取最新一封邮件, 注意索引号从1开始:
    index = len(mails)
    print(index)
    try:
        for i in xrange(1, index):
            #print i
            print("*************************************************************************")
            resp, lines, octets = server.retr(i)
            # lines存储了邮件的原始文本的每一行,
            # 可以获得整个邮件的原始文本:
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            # 稍后解析出邮件:
            msg = Parser().parsestr(msg_content)
            info = print_info(msg)
            mail_info.append(info)
    except Exception as e:
        print(traceback.format_exc())
    print(len(mail_info))
    # 可以根据邮件索引号直接从服务器删除邮件:
    # server.dele(index)
    # 关闭连接:
    server.quit()
    return mail_info