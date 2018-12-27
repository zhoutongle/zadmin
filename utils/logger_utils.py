#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import logging
import logging.config
if sys.version.split(" ")[0].split(".")[0] == '2':
    import ConfigParser
else:
    import configparser

currpath = os.path.join(os.getcwd(),os.path.dirname(__file__))
if not currpath in sys.path:
    sys.path.append(currpath)
homepath = currpath[:currpath.find('utils')]
if not homepath in sys.path:
    sys.path.append(homepath)

conf_path = os.path.join(currpath[:currpath.rfind('utils')], 'conf')
log_path = os.path.join(currpath[:currpath.rfind('utils')], 'conf\\log.conf')
app_path = os.path.join(currpath[:currpath.rfind('utils')], 'conf\\app.log')
oper_path = os.path.join(currpath[:currpath.rfind('utils')], 'conf\\aperation.log')

class AppLogger:
    """
        Application log
    """
    def __init__(self):
        if not os.path.exists(conf_path):
            os.makedirs(conf_path)
        if not os.path.exists(app_path):
            course = open(app_path, 'w')
            course.close()          
        logging.config.fileConfig(log_path)
        
    def _getHandler(self):
        Alogger = logging.getLogger('App')
        return Alogger



class OperationLogger:
    """
        Operation log
    """
    def __init__(self):
        if not os.path.exists(conf_path):
            os.makedirs(conf_path)
        if not os.path.exists(oper_path):
            course = open(oper_path, 'w')
            course.close()     
        logging.config.fileConfig(log_path)
        
    def _getHandler(self):
        Ologger = logging.getLogger('Operation')
        return Ologger
