#*- coding: utf-8 -*-

import os
import sys

currpath = os.path.join(os.getcwd(),os.path.dirname(__file__))
if currpath not in sys.path:
    sys.path.append(currpath)

admin_menu = [
    {'name' : u'管理系统', 'label' : 'fa fa fa-cog',
     'sub' : [{'name' : u'用户管理', 'label' : 'fa fa-user', 'func' : 'user_manager()'}, 
              {'name' : u'修改密码', 'label' : 'fa fa-pencil', 'func' : 'modify_password()'},
              {'name' : u'查看日志', 'label' : 'fa fa-eye', 'func' : 'view_log()'},
              {'name' : u'系统信息', 'label' : 'fa fa-info-circle', 'func' : 'system_info("system_info")'},
              {'name' : u'退出系统', 'label' : 'fa fa-sign-out', 'func' : 'logout()'}]
    },
    {'name' : u'图标统计', 'label' : 'fa fa-bar-chart-o',
     'sub' : [{'name' : u'磁盘使用率', 'label': 'fa fa-pie-chart', 'func' : 'disk_usage()'},
              {'name' : u'CPU使用率', 'label': 'fa fa-line-chart', 'func' : 'cpu_usage()'},
              {'name' : u'地图', 'label': 'fa fa-map', 'func' : 'china_map()'},]
    },
    {'name' : u'多媒体', 'label' : 'fa fa-video-camera',
     'sub' : [{'name' : u'音频', 'label': 'fa fa-music', 'func' : 'show_audio()'},
              {'name' : u'视频', 'label': 'fa fa-film', 'func' : 'show_video()'},
              {'name' : u'语音', 'label': 'fa fa-microphone', 'func' : 'show_voice()'}]
    },
    {'name' : u'日常', 'label' : 'fa fa-list-alt',
     'sub' : [{'name' : u'标签墙', 'label': 'fa fa-tag', 'func' : 'label_wall()'},
              {'name' : u'日历', 'label': 'fa fa-tag', 'func' : 'get_calendar()'},
              {'name' : u'图片', 'label': 'fa fa-tag', 'func' : 'get_picture()'},
              {'name' : u'文章', 'label': 'fa fa-tag', 'func' : 'get_article()'},
              {'name' : u'火车票', 'label': 'fa fa-tag', 'func' : 'get_train_ticket()'},
              {'name' : u'购票', 'label': 'fa fa-tag', 'func' : 'book_ticket()'}]
    },
    {'name' : u'邮箱', 'label' : 'fa fa-list-alt',
     'sub' : [{'name' : u'收件箱', 'label': 'fa fa-tag', 'func' : 'receive_mail()'}]
    }
]

admin_menu2 = [
    {'name' : u'统计图表', 'label' : 'fa fa fa-bar-chart-o',
     'sub' : [{'name' : u'百度ECharts', 'label' : 'fa fa-user', 'func' : 'graph_echarts()'}, 
              {'name' : u'Flot', 'label' : 'fa fa-pencil', 'func' : 'graph_flot()'},
              {'name' : u'Morris.js', 'label' : 'fa fa-eye', 'func' : 'view_log()'},
              {'name' : u'Rickshaw', 'label' : 'fa fa-info-circle', 'func' : 'system_info()'},
              {'name' : u'Peity', 'label' : 'fa fa-info-circle', 'func' : 'system_info()'},
              {'name' : u'Sparkline', 'label' : 'fa fa-info-circle', 'func' : 'system_info()'},
              {'name' : u'图表组合', 'label' : 'fa fa-info-circle', 'func' : 'system_info()'}]
    }    
]