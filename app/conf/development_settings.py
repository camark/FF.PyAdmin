"""
    development_settings.py
    ~~~~~~~~
    开发环境配置项(最高优先级)

    先设置环境变量(FF_PyAdmin 是 settings.py 中设置的 APP_NAME):

    e.g.::

        1. Windows:
            set FF_PyAdmin=development
            echo %FF_PyAdmin%
        2. Linux:
            export FF_PyAdmin=development
            echo $FF_PyAdmin

    :author: Fufu, 2019/9/2
"""

##########
# CORE
##########

DEBUG = True
JSON_AS_ASCII = False
WTF_CSRF_ENABLED = True

# 域名访问, 写 HOSTS: 127.0.0.1 ff.pyadmin
# SERVER_NAME = 'ff.pyadmin:777'

##########
# OAuth2
##########

OA_CLIENT_ID = 'ffpy123glfxxxdabci3loln1xunyouff'
OA_CLIENT_SECRET = 'kkpy123glfxxxdabci3loln1xunyouok'
OA_API_BASE_URL = 'http://oa/oauth2/'
OA_AUTHORIZE_URL = 'http://oa/oauth2/authorize/'
OA_ACCESS_TOKEN_URL = 'http://oa/oauth2/access_token/'
OA_REFRESH_TOKEN_URL = 'http://oa/oauth2/refresh_token/'

##########
# DB
##########

SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://db_user_demo:db_pass_demo@127.0.0.1:3306' \
                          '/db_ff_pyadmin?charset=utf8mb4'
# 调试模式, 显示 SQL
SQLALCHEMY_ECHO = True
