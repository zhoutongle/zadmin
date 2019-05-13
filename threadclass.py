#-*- coding: utf-8 -*-

import os
import re
import sys
import json
import threading

from flaskr import Alogger

#-----------------------------------
# global
#-----------------------------------
currpath = os.path.join(os.getcwd(),os.path.dirname(__file__))
THREADCLASS_PATH_NAME = 'threadclassd'
THREADCLASS_FILE_PATH = os.path.join(currpath, THREADCLASS_PATH_NAME) #子线程目录
THREADS = set() #现有已启动的线程
#-----------------------------------
# 加载所有的线程任务
# threadclassd目录下脚本命名规则Xthreadclass.py，X为线程名，代表线程要实现的主要功能。
#-----------------------------------
def init_thread():
    global THREADS
    CURR_THREADS = set() #存放当前扫描到的线程列表，和THREADS比较，THREADS没有的则启动，THREADS有但CURR_THREADS没有的则停止
    try:
        #如果有license控制，筛选列表
        if os.path.exists(THREADCLASS_FILE_PATH):
            items = os.listdir(THREADCLASS_FILE_PATH)
            for item in items:
                im = re.match('((\S+thread)class)\.py*',item)
                itempath = os.path.join(THREADCLASS_FILE_PATH,item)
                if os.path.isfile(itempath) and im:
                    module_name = im.group(1)
                    try:
                        module = '%s.%s' % (THREADCLASS_PATH_NAME,module_name)
                        #不在现有线程列表里的开启
                        if not module in THREADS:
                            __import__(module)
                            if hasattr(sys.modules[module],"start"):
                                sys.modules[module].start()
                                Alogger.error("Start thread %s" % module)
                        else:
                            #已在现有线程列表的重载
                            if hasattr(sys.modules[module],"stop"):
                                sys.modules[module].stop()
                                reload(sys.modules[module])
                                sys.modules[module].start()
                                Alogger.error("Reload thread %s" % module)
                        CURR_THREADS.add(module)
                    except:
                        Alogger.error(traceback.format_exc())
            THREADS_TO_STOP = THREADS - CURR_THREADS
            for module in THREADS_TO_STOP:
                if hasattr(sys.modules[module], "stop"):
                    sys.modules[module].stop()
            THREADS = CURR_THREADS
    except:
        Alogger.error(traceback.format_exc())
