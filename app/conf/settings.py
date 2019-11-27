"""
    settings.py
    ~~~~~~~~
    通用配置项(必须)

    :author: Fufu, 2019/9/2
"""
##########
# CORE
##########

DEBUG = False
TIME_ZONE = 'Asia/Shanghai'
EXCEPTION_DESC = {
    401: '未授权的请求',
    403: '请求权限不足',
    404: '页面未找到',
    405: '错误的请求方法',
    400: '错误的请求',
    500: '系统服务异常',
    'dbapi': '数据库操作失败',
}

##########
# LOG
##########

# logging.INFO = 20, CRITICAL = 50, ERROR = 40, WARNING = 30, DEBUG = 10
LOG_LEVEL = 20
# 单位 MB
LOG_MAXSIZE = 200
# 保留文件数
LOG_BACKUP = 30

##########
# APP
##########

# 可设置 APP_NAME 名称或 FLASK_CONFIG 环境变量值为: development / testing / production
APP_NAME = 'FF_PyAdmin'
# API 为 True 时所有请求都返回 JSON
API = False
# 保持键序
JSON_SORT_KEYS = False
# SESSION 和 CSRF 生命周期
PERMANENT_SESSION_LIFETIME = WTF_CSRF_TIME_LIMIT = 1440
# 运维接口白名单 IP
LOCAL_GW = ''
