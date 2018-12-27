#!/usr/bin/python
#coding=utf-8

import sys
import time
import threading
import traceback
import sqlite3_utils
from cpu_utils import *

python_version = sys.version.split(" ")[0].split(".")[0]
if python_version == '2':
    from Queue import Queue
else:
    from queue import Queue

def start_process():
    warn_info = []
    monitor_info_queue = Queue(1000)
    threads = []
    try:
        t1 = threading.Thread(name="get_cpu_mem", target=get_cpu_mem_info, args=(monitor_info_queue, ))
        threads.append(t1)
        
        for th in threads:
            th.setDaemon(True)
            th.start()
    except:
        print(traceback.format_exc())
     
    while True:
        try:
            monitor_info = monitor_info_queue.get()
            if monitor_info:
                #插入到数据库
                retcode = sqlite3_utils.insert_alarm_into_db(monitor_info)
        except:
            print(traceback.format_exc())
    
    for th in threads:
        th.join()
        
if __name__ == '__main__':
    start_process()