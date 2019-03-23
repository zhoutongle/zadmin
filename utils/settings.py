import os
import sys

CN = None         # 用作登陆12306的句柄
USER_NAME = None  # 记录登陆的用户名

###########各个文件的路径
currpath = os.path.join(os.getcwd(), os.path.dirname(__file__))    #settings.py所在路径
if sys.platform == "win32":
    DATA_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'data\\db\\data.db')
    LOG_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'conf\\log.conf')
    APP_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'conf\\app.log')
    OPERATION_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'conf\\aperation.log')
    CONF_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'conf')
    MONITOR_PATH = os.path.join(currpath, 'monitor_reporter.py')
    SESSION_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'session')
    BACKGROUND_PICTURE_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'static\\img\\background\\')
    SONG_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'static\\song\\')
    CODE_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'static\\img\\auth_code.png')
    SONG_LIST_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'data\\song_list.json')
    PICTURE_PATH = os.path.join(currpath[:currpath.rfind('utils')], "static\\img\\image1\\")
    ARTICLE_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'data\\article_list.json')

if sys.platform == "linux2":
    DATA_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'data/db/data.db')
    LOG_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'conf/log.conf')
    APP_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'conf/app.log')
    OPERATION_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'conf/aperation.log')
    CONF_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'conf')
    MONITOR_PATH = os.path.join(currpath, 'monitor_reporter.py')
    SESSION_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'session')
    BACKGROUND_PICTURE_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'static/img/background/')
    SONG_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'static/song/')
    CODE_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'static/img/auth_code.png')
    SONG_LIST_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'data/song_list.json')
    PICTURE_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'static/img/image1/')
    ARTICLE_PATH = os.path.join(currpath[:currpath.rfind('utils')], 'data/article_list.json')

############规定的常量

PYTHON_VERSION = sys.version.split(" ")[0].split(".")[0]       #python的版本（只区分Python2和Python3）
SYSTEM_TYPE = sys.platform                                     #系统的环境（win32还是linux2）
ALERT_SLEEP_TIME = 8                                           #监控时间间隔
UNIT_LIST = ['B', 'KB', "MB", "GB", "PB"]                      #数据大小的单位
TABLE_INFO = {
    'cpu'       : 'create table cpu(time varchar(20), cpu integer, mem integer)',
    'user'      : 'create table user(id integer primary key autoincrement, name varchar(20), mail varchar(50), password varchar(20))', 
    'alarm'     : 'create table alarm(id integer primary key autoincrement, time varchar(20), level varchar(10), message varchar(50))', 
    'label'     : 'create table label(id integer primary key autoincrement, time varchar(20), title varchar(30), content varchar(200))', 
    'event'     : 'create table event(id integer primary key autoincrement, start varchar(20), end varchar(20), title varchar(200))',
    'background': 'create table background(style varchar(20), imgsrc varchar(50)'
    }  #数据库中所有的table, 目前有（用户，内存和CPU【保存20条】，报警信息，标签，日历中的事件，登陆背景）
WEEK_INFO = {0 : '星期日', 1 : '星期一', 2 : '星期二', 3 : '星期三', 4 : '星期四', 5 : '星期五', 6 : '星期六'} #用于标签上的日期星期几
EMAIL = '1140082051@qq.com'
PASSWORD = 'trpoyjqnoqykgjha'
POP3_SERVER = 'imap.qq.com'