#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    manage.py
    ~~~~~~~~
    启动服务(测试使用)：python3 manage.py runserver

    :author: Fufu, 2019/9/2
"""
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import xxtea
from start import app
from app.models import db
from app.libs.helper import debug
from app.models.user import TBUser
from app.models.bgp import TBBGP

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def runserver():
    """Start Flask’s built-in server"""
    app.run()


@manager.option('-d', '--data', dest='data', help="待加密内容")
def encrypt(data=None):
    """
    根据 SECRET_KEY 加密
    用于生成加密环境变量值, 如 secret_settings.py 中的 PYADMIN_OAUTH_SECRET, PYADMIN_DBPASS

    e.g.::

        # 3e8cf54cd043920f
        python3 manage.py encrypt -d Fufu

    :param data:
    :return:
    """
    debug(data, xxtea.encrypt_hex(data, app.secret_key).decode('utf-8'))


if __name__ == '__main__':
    manager.run()
