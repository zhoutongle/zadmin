#*- coding: utf-8 -*-

import os
import sys

currpath = os.path.join(os.getcwd(),os.path.dirname(__file__))
if currpath not in sys.path:
    sys.path.append(currpath)

admin_menu = [
    {'name' : u'管理系统', 'label' : 'fa fa fa-cog',
     'sub' : [{'name' : u'用户管理', 'label' : 'fa fa-user',        'url' : '/user_manager'}, 
              {'name' : u'修改密码', 'label' : 'fa fa-pencil',      'url' : '/modify_password'},
              {'name' : u'查看日志', 'label' : 'fa fa-eye',         'url' : '/view_log'},
              {'name' : u'系统目录', 'label' : 'fa fa-info-circle', 'url' : '/show_directory'},
              {'name' : u'系统信息', 'label' : 'fa fa-info-circle', 'url' : '/system_info'},
              {'name' : u'退出系统', 'label' : 'fa fa-sign-out',    'url' : '/logout'}]
    },
    {'name' : u'图标统计', 'label' : 'fa fa-bar-chart-o',
     'sub' : [{'name' : u'磁盘使用率', 'label': 'fa fa-pie-chart',  'url' : '/disk_usage'},
              {'name' : u'CPU使用率',  'label': 'fa fa-line-chart', 'url' : '/cpu_usage'},
              {'name' : u'地图',       'label': 'fa fa-map',        'url' : '/china_map'}]
    },
    {'name' : u'多媒体', 'label' : 'fa fa-video-camera',
     'sub' : [{'name' : u'音频', 'label': 'fa fa-music',      'url' : '/show_audio'},
              {'name' : u'视频', 'label': 'fa fa-film',       'url' : '/show_video'},
              {'name' : u'语音', 'label': 'fa fa-microphone', 'url' : '/show_voice'}]
    },
    {'name' : u'日常', 'label' : 'fa fa-list-alt',
     'sub' : [{'name' : u'标签墙', 'label': 'fa fa-tag', 'url' : '/label_wall'},
              {'name' : u'日记',   'label': 'fa fa-tag', 'url' : '/editor_article'},
              {'name' : u'日历',   'label': 'fa fa-tag', 'url' : '/get_calendar'},
              {'name' : u'图片',   'label': 'fa fa-tag', 'url' : '/get_picture'},
              {'name' : u'文章',   'label': 'fa fa-tag', 'url' : '/get_article'},
              {'name' : u'火车票', 'label': 'fa fa-tag', 'url' : '/get_train_ticket'},
              {'name' : u'购票',   'label': 'fa fa-tag', 'url' : '/book_ticket'}]
    },
    {'name' : u'工具', 'label' : 'fa fa-list-alt',
     'sub' : [{'name' : u'base64转换', 'label': 'fa fa-tag', 'url' : '/base64_transition'},
              {'name' : u'聊天', 'label': 'fa fa-tag', 'url' : '/chat_other'},
              {'name' : u'图片剪裁', 'label': 'fa fa-tag', 'url' : '/image_cropper'},
              {'name' : u'系统工具', 'label': 'fa fa-tag', 'url' : '/system_tool'}]
    },
    {'name' : u'邮箱', 'label' : 'fa fa-list-alt',
     'sub' : [{'name' : u'收件箱', 'label': 'fa fa-tag', 'url' : '/receive_mail'},
              {'name' : u'查看邮件', 'label': 'fa fa-tag', 'url' : '/mail_detail'},
              {'name' : u'写件箱', 'label': 'fa fa-tag', 'url' : '/write_mail'}]
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