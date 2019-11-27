# -*- coding:utf-8 -*-
"""
    log.py
    ~~~~~~~~
    日志相关服务

    :author: Fufu, 2019/9/16
"""
from flask import request
from flask_login import current_user
from sqlalchemy import desc

from ..models.user import TBLog
from ..models.bgp import TBBGP
from ..libs.exceptions import APIFailure


class LogCharge:
    """日志数据表相关操作"""

    @staticmethod
    def to_db(data=None, as_api=False):
        """
        记录日志到数据库
        客户端上报日志

        :param data: dict
        :param as_api:
        :return:
        """
        log = {
            'log_action': request.endpoint,
            'log_operator': getattr(current_user, 'realname', request.remote_addr)
        }
        isinstance(data, dict) and log.update(data)
        res = TBLog().insert(log)
        if not res and as_api:
            raise APIFailure('日志入库失败')

        # BGP 最后更新时间
        res and log.get('log_status') and log['log_action'] == 'update' and LogCharge.update_bgp(log)

        return res

    @staticmethod
    def get_list(where=None, limit=200):
        """
        获取日志列表(暂未分页)

        :param where: dict
        :param limit: int
        :return: list
        """
        where = dict(filter(lambda x: tuple(x)[1] not in [None, ''], where.items())) if where else {}
        return TBLog.query.filter_by(**where).order_by(desc('log_id')).limit(limit).to_dicts

    @staticmethod
    def update_bgp(log):
        """
        更新 BGP 最后更新时间

        :param log: dict
        :return:
        """
        data = {'bgp_update': log['log_time']}
        filter_by = {'bgp_ip': log['log_operator']}
        res = TBBGP().replace(data, filter_by=filter_by, skip_add=True)

        return res
