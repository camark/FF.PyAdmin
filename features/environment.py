#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    environment.py
    ~~~~~~~~
    BDD 环境配置

    :author: Fufu, 2019/9/14
"""
from flask import session

from app import create_app
from app.services.auth import set_user_login


def before_all(ctx):
    ctx.config.setup_logging()
    app = create_app(config_name='testing')
    with app.test_request_context():
        # 测试专用账号(OA无法登录)
        set_user_login({
            'job_number': 9999,
            'realname': 'BDDTester'
        })
        # 构建客户端登录状态环境
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess.update(session)
            ctx.client = c


def after_all(ctx):
    del ctx.client
