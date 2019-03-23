#!/usr/bin/python
#coding=utf8

import os
import psutil
import datetime
import traceback
from time import sleep

import settings
import sqlite3_utils
from logger_utils import AppLogger

#sleep_time = 8
#unit_list = ['B', 'KB', "MB", "GB", "PB"]
Alogger = AppLogger()._getHandler()

#合并信息
def get_cpu_mem_info(queue):
    while True:
        try:
            info = []
            temp = {}
            warn_info = []
            warn_temp = {}
            
            #获取CPU和内存信息
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cpu_percent = psutil.cpu_percent(interval=2)
            mem_info = psutil.virtual_memory()
            mem_percent = mem_info.percent
            temp['time'] = time
            temp['cpu_percent'] = cpu_percent
            temp['mem_percent'] = mem_percent
            
            #插入到数据库
            retcode = sqlite3_utils.insert_cup_info_into_db(temp)
            
            #判断cpu使用率是否达到报警级别， 如果可以组装报警信息
            if cpu_percent > 90:
                warn_temp['time'] = time
                warn_temp['level'] = "warn"
                warn_temp['serial'] = "1001"
                warn_temp['message'] = "Cpu usage is too hight, cpu usage reached " + str(cpu_percent) + "%."
                Alogger.error(warn_temp)
                queue.put(warn_temp)


            #判断内存使用率是否达到报警级别， 如果可以组装报警信息
            warn_temp = []
            if mem_percent > 90:
                warn_temp['time'] = time
                warn_temp['level'] = "warn"
                warn_temp['serial'] = "1002"
                warn_temp['message'] = "Memory usage is too hight, memory usage reached " + str(mem_percent) + "%."
                queue.put(warn_temp)

            sleep(settings.ALERT_SLEEP_TIME)
        except Exception as e:
            Alogger.error(traceback.format_exc())