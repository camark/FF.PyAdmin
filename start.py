#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    start.py
    ~~~~~~~~
    环网自动路由表
    启动服务：python3 start.py

    :author: Fufu, 2019/9/2
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
