#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import os
import sys
import base64
import hashlib
import tkinter as tk

'''
　　总结如下：
　　sticky:默认的控件在窗口中的对齐方式是居中
　　sticky=N/S/E/W:顶端对齐/底端对齐/右对齐/左对齐
　　sticky=N+S:拉伸高度，使其在水平方向上顶端和底端都对齐
　　sticky=E+W:拉伸宽度，使其在垂直方向上左边界和右边界都对齐
　　sticky=N+S+E:拉伸高度，使其在水平方向上对齐，并将控件放在右边（当两个控件放在同一行同一列时效果明显）
　　.......
　　还有诸如此类的组合方式根据需要调整。
　　在Tkinter模块中，各种控件的大小计量单位并不尽相同，可能需要反复调整才能达到最佳效果。
'''
#pyinstaller --onefile --nowindowed -w --icon="E:\zadmin\static\img\img\favicon.ico" base64.py  打包成exe可执行文件

def main():
    root = tk.Tk()
    root.minsize(390, 530)
    root.maxsize(390, 530)
    root.title('I`am a book')
    text = edit(root)
    button(root, text)
    root.mainloop()

def edit(root):
    edit = tk.Text(root, fg='black', bg='white', font='微软雅黑', width=30, height=10)
    edit.grid(sticky = tk.N + tk.E + tk.W)

    clear = tk.Button(root, text="clear", width=28, bg='yellow', font='微软雅黑', command=lambda :edit.delete(1.0, tk.END))
    clear.grid(sticky = tk.W)

    result = tk.Text(root, fg='black', bg='white', font='微软雅黑', width=30, height=10)
    result.grid(sticky = tk.N + tk.E + tk.W)

    clear = tk.Button(root, text="clear", width=28, bg='yellow', font='微软雅黑', command=lambda :result.delete(1.0, tk.END))
    clear.grid(sticky = tk.W)

    l = tk.Label(root, text='I`am a book', fg='white', bg='black', width=30)
    l.grid(sticky=tk.E + tk.W + tk.S + tk.N)

    text = [edit, result]
    return text

def button(root, text):
    num = 0
    b64en = tk.Button(root, text='Base64 Encode', fg='white', bg='green', command=lambda :b64encode(text))
    b64de = tk.Button(root, text='Base64 Decode', fg='white', bg='green', command=lambda :b64decode(text))
    b32en = tk.Button(root, text='Base32 Encode', fg='white', bg='green', command=lambda :b32encode(text))
    b32de = tk.Button(root, text='Base32 Decode', fg='white', bg='green', command=lambda :b32decode(text))
    md5do = tk.Button(root, text='-Md5  Creator-', fg='white', bg='green', command=lambda :md5create(text))
    buttons = [b64en, b64de, b32en, b32de, md5do]
    for button in buttons:
        button.grid(row=num, column=1, sticky = tk.N + tk.S + tk.W)
        num += 1
    return buttons

def b64encode(text):
    edit, result = text[0], text[1]
    content = edit.get(1.0, tk.END)
    result.delete(1.0, tk.END)
    try:
        ret = base64.b64encode(content[0:-1].encode('ascii'))
    except Exception as e:
        result.insert(1.0, 'error!!!\n')
        return False
    result.insert(1.0, ret.decode('ascii'))
    return True

def b64decode(text):
    edit, result = text[0], text[1]
    content = edit.get(1.0, tk.END)
    result.delete(1.0, tk.END)
    try:
        ret = base64.b64decode(content[0:-1].encode('ascii'))
    except Exception as e:
        result.insert(1.0, 'error!!!')
        return False
    result.insert(1.0, ret.decode('ascii'))
    return True

def b32encode(text):
    edit, result = text[0], text[1]
    content = edit.get(1.0, tk.END)
    result.delete(1.0, tk.END)
    try:
        ret = base64.b32encode(content[0:-1].encode('ascii'))
    except Exception as e:
        result.insert(1.0, 'error!!!')
        return False
    result.insert(1.0, ret.decode('ascii'))
    return True
    
def b32decode(text):
    edit, result = text[0], text[1]
    content = edit.get(1.0, tk.END)
    result.delete(1.0, tk.END)
    try:
        ret = base64.b32decode(content[0:-1].encode('ascii'))
    except Exception as e:
        result.insert(1.0, 'error!!!')
        return False
    result.insert(1.0, ret.decode('ascii'))
    return True

def md5create(text):
    edit, result = text[0], text[1]
    content = edit.get(1.0, tk.END)
    result.delete(1.0, tk.END)
    ret = hashlib.md5()
    try:
        ret.update(content[0:-1].encode('ascii'))
    except Exception as e:
        result.insert(1.0, 'error!!!')
        return False
    result.insert(1.0, ret.hexdigest())

if __name__ == '__main__':
    main()