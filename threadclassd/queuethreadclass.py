#-*- coding: utf-8 -*-

import os
import sys
import time
import psutil
import datetime
import traceback
import threading

currpath = os.path.join(os.getcwd(), os.path.dirname(__file__))
utilspath = os.path.join(currpath, 'utils')
if not utilspath in sys.path:
    sys.path.append(utilspath)

from flaskr import Alogger
from utils import settings
from utils import sqlite3_utils

#-----------------------------------
#
#-----------------------------------
QUEUETHREAD = None #从队列中获得报警信息线程
#-----------------------------------
# start thread
#-----------------------------------
def start():
    global QUEUETHREAD
    try:
        if QUEUETHREAD and isinstance(QUEUETHREAD, QUEUETHREAD) and QUEUETHREAD.isAlive():
            if not QUEUETHREAD._QUEUETHREAD__running.isSet():
                QUEUETHREAD._QUEUETHREAD__running.set()
                QUEUETHREAD.start()
        else:
            QUEUETHREAD = QUEUETHREAD('QUEUETHREAD')
            QUEUETHREAD.start()
    except:
       Alogger.error(traceback.format_exc())         
        
#-----------------------------------
# stop thread
#-----------------------------------
def stop():
    global QUEUETHREAD
    try:
        if QUEUETHREAD and isinstance(QUEUETHREAD, QUEUETHREAD):
            if QUEUETHREAD._QUEUETHREAD__running.isSet():
                QUEUETHREAD._QUEUETHREAD__running.clear()
    except:
        Alogger.error(traceback.format_exc())

#-----------------------------------
# 更新RAID信息线程
#-----------------------------------
class QUEUETHREAD(threading.Thread):
    def __init__ (self, threadname):
        try:
            threading.Thread.__init__(self, name=threadname)
            self.__running = threading.Event()
            self.__running.set()
        except:
            Alogger.error(traceback.format_exc())

    def run(self):
        while self.__running.isSet():
            try:
                warningdata = []
                while True:
                    warningdata.append(settings.MONITORQUEUE.get())
                    if settings.MONITORQUEUE.empty():
                        break

                if warningdata:
                    for warn_data in warningdata:
                        #插入到数据库
                        Alogger.error(warn_data)
                        sqlite3_utils.insert_alarm_into_db(warn_data)
            except:
                Alogger.error(traceback.format_exc())
            time.sleep(settings.ALERT_SLEEP_TIME)
