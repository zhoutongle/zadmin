#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-

import os
import sys
import uuid
import codecs
import locale
import socket
import getpass
import platform
import traceback
import subprocess
if sys.version.split(" ")[0].split(".")[0] == '2':
    import _winreg
    import netifaces
else:
    import winreg
 
'''
    python中，platform模块给我们提供了很多方法去获取操作系统的信息
    如：
        import platform
        platform.platform()   #获取操作系统名称及版本号，'Windows-7-6.1.7601-SP1'
        platform.version()    #获取操作系统版本号，'6.1.7601'
        platform.architecture()   #获取操作系统的位数，('32bit', 'WindowsPE')
        platform.machine()    #计算机类型，'x86'
        platform.node()       #计算机的网络名称，'hongjie-PC'
        platform.processor()  #计算机处理器信息，'x86 Family 16 Model 6 Stepping 3, AuthenticAMD'
        platform.uname()      #包含上面所有的信息汇总，uname_result(system='Windows', node='hongjie-PC',
                               release='7', version='6.1.7601', machine='x86', processor='x86 Family
                               16 Model 6 Stepping 3, AuthenticAMD')

        还可以获得计算机中python的一些信息：
        import platform
        platform.python_build()
        platform.python_compiler()
        platform.python_branch()
        platform.python_implementation()
        platform.python_revision()
        platform.python_version()
        platform.python_version_tuple()
'''

#global var
#是否显示日志信息
SHOW_LOG = True

def get_platform():
    '''获取操作系统名称及版本号'''
    return platform.platform()

def get_version():
    '''获取操作系统版本号'''
    return platform.version()

def get_architecture():
    '''获取操作系统的位数'''
    return platform.architecture()

def get_machine():
    '''计算机类型'''
    return platform.machine()

def get_node():
    '''计算机的网络名称'''
    return platform.node()

def get_processor():
    '''计算机处理器信息'''
    return platform.processor()

def get_system():
    '''获取操作系统类型'''
    return platform.system()

def get_uname():
    '''汇总信息'''
    return platform.uname()

def get_python_build():
    ''' the Python build number and date as strings'''
    return platform.python_build()

def get_python_compiler():
    '''Returns a string identifying the compiler used for compiling Python'''
    return platform.python_compiler()

def get_python_branch():
    '''Returns a string identifying the Python implementation SCM branch'''
    return platform.python_branch()

def get_python_implementation():
    '''Returns a string identifying the Python implementation. Possible return values are: ‘CPython’, ‘IronPython’, ‘Jython’, ‘PyPy’.'''
    return platform.python_implementation()

def get_python_version():
    '''Returns the Python version as string 'major.minor.patchlevel'
    '''
    return platform.python_version()

def get_python_revision():
    '''Returns a string identifying the Python implementation SCM revision.'''
    return platform.python_revision()

def get_python_version_tuple():
    '''Returns the Python version as tuple (major, minor, patchlevel) of strings'''
    return platform.python_version_tuple()

def show_python_all_info():
    '''打印python的全部信息'''
    print('The Python build number and date as strings : [{}]'.format(get_python_build()))
    print('Returns a string identifying the compiler used for compiling Python : [{}]'.format(get_python_compiler()))
    print('Returns a string identifying the Python implementation SCM branch : [{}]'.format(get_python_branch()))
    print('Returns a string identifying the Python implementation : [{}]'.format(get_python_implementation()))
    print('The version of Python ： [{}]'.format(get_python_version()))
    print('Python implementation SCM revision : [{}]'.format(get_python_revision()))
    print('Python version as tuple : [{}]'.format(get_python_version_tuple()))

def show_python_info():
    '''只打印python的信息，没有解释部分'''
    print(get_python_build())
    print(get_python_compiler())
    print(get_python_branch())
    print(get_python_implementation())
    print(get_python_version())
    print(get_python_revision())
    print(get_python_version_tuple())

def show_os_all_info():
    '''打印os的全部信息'''
    print('获取操作系统名称及版本号 : [{}]'.format(get_platform()))
    print('获取操作系统版本号 : [{}]'.format(get_version()))
    print('获取操作系统的位数 : [{}]'.format(get_architecture()))
    print('计算机类型 : [{}]'.format(get_machine()))
    print('计算机的网络名称 : [{}]'.format(get_node()))
    print('计算机处理器信息 : [{}]'.format(get_processor()))
    print('获取操作系统类型 : [{}]'.format(get_system()))
    print('汇总信息 : [{}]'.format(get_uname()))

def show_os_info():
    '''只打印os的信息，没有解释部分'''
    print(get_platform())
    print(get_version())
    print(get_architecture())
    print(get_machine())
    print(get_node())
    print(get_processor())
    print(get_system())
    print(get_uname())

def getLocalIP():

    routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]
    for interface in netifaces.interfaces():
        if interface == routingNicName:
            try:
                routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
                return interface, routingIPAddr
            except KeyError:
                pass
                
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
    
def get_AddressIp():
    '''获取本机IP'''
    return socket.gethostbyname(socket.gethostname())

def get_Mac():
    '''获取MAC地址'''
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ':'.join(mac[e:e+2].upper() for e in range(0,11,2))

def get_localDataPath():
    '''当前用户路径'''
    return os.path.expanduser('~')

def get_UserName():
    '''当前用户名'''
    return getpass.getuser()
#################################################################################################################### 
def get_system_encoding():
    """
    The encoding of the default system locale but falls back to the given
    fallback encoding if the encoding is unsupported by python or could
    not be determined. See tickets #10335 and #5846
    """
    try:
    	encoding = locale.getdefaultlocale()[1] or 'ascii'
    	codecs.lookup(encoding)
    except Exception:
    	encoding = 'ascii'
    return encoding
 
 
DEFAULT_LOCALE_ENCODING = get_system_encoding()
 
def get_system_info():
    '''
        获得机器的基本信息
    '''
    mswindows = (sys.platform == "win32") # learning from 'subprocess' module
    linux = (sys.platform == "linux2")
     
    hidden_hostname = True
    system_info = {}
    all_ip = ''
    if get_host_ip() not in all_ip:
        all_ip = all_ip + " " + get_host_ip()
    if get_AddressIp() not in all_ip:
        all_ip = all_ip + " " + get_AddressIp()
     
    if mswindows:
        #uname = list(platform.uname())
        #if hidden_hostname:
        #    uname[1] = "hidden_hostname"

        try:
            '''
            判断是Python2.x还是Python3.x
            if sys.version.split(" ")[0].split(".")[0] == '2':
                reg_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion")
                if reg_key:
                    ProductName  = _winreg.QueryValueEx(reg_key, "ProductName")[0] or None
                    EditionId    = _winreg.QueryValueEx(reg_key, "EditionId")[0] or None
                    ReleaseId    = _winreg.QueryValueEx(reg_key, "ReleaseId")[0] or None
                    CurrentBuild = _winreg.QueryValueEx(reg_key, "CurrentBuild")[0] or None
                    BuildLabEx   = _winreg.QueryValueEx(reg_key, "BuildLabEx")[0][:9] or None
                    system_info['ProductName'] = ProductName
                    system_info['EditionId'] = EditionId
                    system_info['ReleaseId'] = ReleaseId
                    system_info['CurrentBuild'] = CurrentBuild
                    system_info['BuildLabEx'] = BuildLabEx
                    system_info['Ipaddr'] = getLocalIP()[1]
                    print (ProductName, EditionId, ReleaseId, CurrentBuild, BuildLabEx)
            else:
                reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion")
                if reg_key:
                    ProductName  = winreg.QueryValueEx(reg_key, "ProductName")[0] or None
                    EditionId    = winreg.QueryValueEx(reg_key, "EditionId")[0] or None
                    ReleaseId    = winreg.QueryValueEx(reg_key, "ReleaseId")[0] or None
                    CurrentBuild = winreg.QueryValueEx(reg_key, "CurrentBuild")[0] or None
                    BuildLabEx   = winreg.QueryValueEx(reg_key, "BuildLabEx")[0][:9] or None
                    system_info['ProductName'] = ProductName
                    system_info['EditionId'] = EditionId
                    system_info['ReleaseId'] = ReleaseId
                    system_info['CurrentBuild'] = CurrentBuild
                    system_info['BuildLabEx'] = BuildLabEx
                    system_info['Ipaddr'] = getLocalIP()[1]
                    print (ProductName, EditionId, ReleaseId, CurrentBuild, BuildLabEx)
                '''
            system_info['system_name'] = get_platform() or None
            system_info['system_version'] = get_version() or None
            system_info['system_sum'] = get_architecture() or None
            system_info['computer_type'] = get_machine() or None
            system_info['computer_network_name'] = get_node() or None
            system_info['computer_cpu_info'] = get_processor() or None
            system_info['system_type'] = get_system() or None
            system_info['local_ip'] = all_ip or None
            system_info['mac_address'] = get_Mac() or None
            system_info['username'] = get_UserName() or None
            system_info['userpath'] = get_localDataPath() or None
        except Exception as e:
            print(traceback.format_exc())

     
    if linux:
        system_info['system_name'] = get_platform() or None
        system_info['system_version'] = get_version() or None
        system_info['system_sum'] = get_architecture() or None
        system_info['computer_type'] = get_machine() or None
        system_info['computer_network_name'] = get_node() or None
        system_info['computer_cpu_info'] = get_processor() or None
        system_info['system_type'] = get_system() or None
        system_info['local_ip'] = all_ip or None
        system_info['mac_address'] = get_Mac() or None
        system_info['username'] = get_UserName() or None
        system_info['userpath'] = get_localDataPath() or None
    return system_info
    
'''    
import sys    
import os    
    
import atexit    
import time    
import psutil    
    
#print "Welcome,current system is",os.name," 3 seconds late start to get data..."    
time.sleep(3)    
     
line_num = 1    
    
#function of Get CPU State    
def getCPUstate(interval=1):    
    return (" CPU: " + str(psutil.cpu_percent(interval)) + "%")    
#function of Get Memory    
def getMemorystate():    
    phymem = psutil.phymem_usage()    
    buffers = getattr(psutil, 'phymem_buffers', lambda: 0)()    
    cached = getattr(psutil, 'cached_phymem', lambda: 0)()    
    used = phymem.total - (phymem.free + buffers + cached)    
    line = " Memory: %5s%% %6s/%s" % (    
        phymem.percent,    
        str(int(used / 1024 / 1024)) + "M",    
        str(int(phymem.total / 1024 / 1024)) + "M"    
    )       
    return line    
def bytes2human(n):    
    """  
    >>> bytes2human(10000)  
    '9.8 K'  
    >>> bytes2human(100001221)  
    '95.4 M'  
    """    
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')    
    prefix = {}    
    for i, s in enumerate(symbols):    
        prefix[s] = 1 << (i+1)*10    
    for s in reversed(symbols):    
        if n >= prefix[s]:    
            value = float(n) / prefix[s]    
            return '%.2f %s' % (value, s)    
    return '%.2f B' % (n)    
    
    
def poll(interval):    
    """Retrieve raw stats within an interval window."""    
    tot_before = psutil.net_io_counters()    
    pnic_before = psutil.net_io_counters(pernic=True)    
    # sleep some time    
    time.sleep(interval)    
    tot_after = psutil.net_io_counters()    
    pnic_after = psutil.net_io_counters(pernic=True)    
    # get cpu state    
    cpu_state = getCPUstate(interval)    
    # get memory    
    memory_state = getMemorystate()    
    return (tot_before, tot_after, pnic_before, pnic_after,cpu_state,memory_state)    
    
def refresh_window(tot_before, tot_after, pnic_before, pnic_after,cpu_state,memory_state):    
    os.system("cls")    
    """Print stats on screen."""    
    
    
    #print current time #cpu state #memory    
    print(time.asctime()+" | "+cpu_state+" | "+memory_state)    
        
    # totals    
    print(" NetStates:")    
    print("total bytes:           sent: %-10s   received: %s" % (bytes2human(tot_after.bytes_sent),    
                                                                      bytes2human(tot_after.bytes_recv))    
    )    
    print("total packets:         sent: %-10s   received: %s" % (tot_after.packets_sent,   
                                                                      tot_after.packets_recv)    
    )  
    # per-network interface details: let's sort network interfaces so    
    # that the ones which generated more traffic are shown first    
    print("")    
    nic_names = pnic_after.keys()    
    #nic_names.sort(key=lambda x: sum(pnic_after[x]), reverse=True)    
    for name in nic_names:    
        stats_before = pnic_before[name]    
        stats_after = pnic_after[name]    
        templ = "%-15s %15s %15s"    
        print(templ % (name, "TOTAL", "PER-SEC"))    
        print(templ % (    
            "bytes-sent",    
            bytes2human(stats_after.bytes_sent),    
            bytes2human(stats_after.bytes_sent - stats_before.bytes_sent) + '/s',    
        ))    
        print(templ % (    
            "bytes-recv",    
            bytes2human(stats_after.bytes_recv),    
            bytes2human(stats_after.bytes_recv - stats_before.bytes_recv) + '/s',    
        ))    
        print(templ % (    
            "pkts-sent",    
            stats_after.packets_sent,    
            stats_after.packets_sent - stats_before.packets_sent,    
        ))    
        print(templ % (    
            "pkts-recv",    
            stats_after.packets_recv,    
            stats_after.packets_recv - stats_before.packets_recv,    
        ))    
        print("")    
    
try:    
    interval = 0    
    while 1:    
        args = poll(interval)    
        refresh_window(*args)  
        interval = 1    
except (KeyboardInterrupt, SystemExit):    
    pass
''' 
if __name__ == '__main__':
    system_info = get_system_info()
    print(system_info)