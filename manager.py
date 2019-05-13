#!/usr/bin/env python
#-*- coding: utf-8 -*-

import traceback
import threadclass

from utils import settings
from flaskr import app, Alogger

if settings.PYTHON_VERSION == '2':
    from Queue import Queue
else:
    from queue import Queue

#-----------------------------------
#
#-----------------------------------
def main():
    try:
        #初始化队列
        settings.MONITORQUEUE = Queue(100)
        
        #启动线程
        threadclass.init_thread()
        
        app.run(debug=True)

    except Exception as e:
        Alogger.error(traceback.format_exc())    

#-----------------------------------
#
#-----------------------------------
if __name__ == '__main__':
    main()