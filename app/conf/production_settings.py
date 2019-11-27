"""
    production_settings.py
    ~~~~~~~~
    生产环境配置项(高优先级)

    先根据配置文件需要, 设置环境变量:

    e.g.::

        cp scripts/etc-profile.d-ffpyadmin.sh /etc/profile.d/ffpyadmin.sh
        chmod +x /etc/profile.d/ffpyadmin.sh
        source /etc/profile.d/ffpyadmin.sh

    :author: Fufu, 2019/9/2
"""

##########
# CORE
##########

# 根据需求, 指定正式环境的域名和端口
SERVER_NAME = 'pyadmin.xunyou.com:777'
