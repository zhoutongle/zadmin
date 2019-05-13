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
CPUTHREAD = None #更新cpu信息线程
#-----------------------------------
# start thread
#-----------------------------------
def start():
    global CPUTHREAD
    try:
        if CPUTHREAD and isinstance(CPUTHREAD, CPUTHREAD) and CPUTHREAD.isAlive():
            if not CPUTHREAD._CPUTHREAD__running.isSet():
                CPUTHREAD._CPUTHREAD__running.set()
                CPUTHREAD.start()
        else:
            CPUTHREAD = CPUTHREAD('CPUTHREAD')
            CPUTHREAD.start()
    except:
       Alogger.error(traceback.format_exc())         
        
#-----------------------------------
# stop thread
#-----------------------------------
def stop():
    global CPUTHREAD
    try:
        if CPUTHREAD and isinstance(CPUTHREAD, CPUTHREAD):
            if CPUTHREAD._CPUTHREAD__running.isSet():
                CPUTHREAD._CPUTHREAD__running.clear()
    except:
        Alogger.error(traceback.format_exc())

#-----------------------------------
# 更新RAID信息线程
#-----------------------------------
class CPUTHREAD(threading.Thread):
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
                info = []
                temp = {}
                warn_info = []
                warn_temp = {}
                
                #获取CPU和内存信息
                timedata = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cpu_percent = psutil.cpu_percent(interval=2)
                mem_info = psutil.virtual_memory()
                mem_percent = mem_info.percent
                temp['time'] = timedata
                temp['cpu_percent'] = cpu_percent
                temp['mem_percent'] = mem_percent
                
                #插入到数据库
                retcode = sqlite3_utils.insert_cup_info_into_db(temp)
                
                #判断cpu使用率是否达到报警级别， 如果可以组装报警信息
                if cpu_percent > 90:
                    warn_temp['time'] = timedata
                    warn_temp['level'] = "warn"
                    warn_temp['serial'] = "1001"
                    warn_temp['message'] = "Cpu usage is too hight, cpu usage reached " + str(cpu_percent) + "%."
                    settings.MONITORQUEUE.put(warn_temp)


                #判断内存使用率是否达到报警级别， 如果可以组装报警信息
                warn_temp = []
                if mem_percent > 90:
                    warn_temp['time'] = timedata
                    warn_temp['level'] = "warn"
                    warn_temp['serial'] = "1002"
                    warn_temp['message'] = "Memory usage is too hight, memory usage reached " + str(mem_percent) + "%."
                    settings.MONITORQUEUE.put(warn_temp)
                
            except:
                Alogger.error(traceback.format_exc())
            time.sleep(settings.ALERT_SLEEP_TIME)
