#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import logging
import settings
import logging.config

if settings.PYTHON_VERSION == '2':
    import ConfigParser
else:
    import configparser
# if sys.version.split(" ")[0].split(".")[0] == '2':
    # import ConfigParser
# else:
    # import configparser

# currpath = os.path.join(os.getcwd(),os.path.dirname(__file__))
# if not currpath in sys.path:
    # sys.path.append(currpath)
# homepath = currpath[:currpath.find('utils')]
# if not homepath in sys.path:
    # sys.path.append(homepath)

# conf_path = os.path.join(currpath[:currpath.rfind('utils')], 'conf')
# log_path = os.path.join(currpath[:currpath.rfind('utils')], 'conf\\log.conf')
# app_path = os.path.join(currpath[:currpath.rfind('utils')], 'conf\\app.log')
# oper_path = os.path.join(currpath[:currpath.rfind('utils')], 'conf\\aperation.log')

class AppLogger:
    """
        Application log
    """
    def __init__(self):
        if not os.path.exists(settings.CONF_PATH):
            os.makedirs(settings.CONF_PATH)
        if not os.path.exists(settings.APP_PATH):
            course = open(settings.APP_PATH, 'w')
            course.close()
        logging.config.fileConfig(settings.LOG_PATH)
        
    def _getHandler(self):
        Alogger = logging.getLogger('App')
        return Alogger



class OperationLogger:
    """
        Operation log
    """
    def __init__(self):
        if not os.path.exists(settings.CONF_PATH):
            os.makedirs(settings.CONF_PATH)
        if not os.path.exists(settings.OPERATION_PATH):
            course = open(settings.OPERATION_PATH, 'w')
            course.close()     
        logging.config.fileConfig(settings.LOG_PATH)
        
    def _getHandler(self):
        Ologger = logging.getLogger('Operation')
        return Ologger
