# -*- coding:utf-8 -*-
"""
    user.py
    ~~~~~~~~
    用户管理和用户权限分配

    :author: Fufu, 2019/9/21
"""
from flask import current_app

from ..models.user import TBUser
from ..libs.exceptions import APIFailure


class UserCharge:
    """User 相关数据表操作"""

    @staticmethod
    def get_list(job_number=0, realname=''):
        """
        获取用户列表(暂未分页)

        :param job_number: int
        :param realname: str
        :return: list
        """
        where = {}
        if job_number:
            where['job_number'] = job_number
        if realname:
            where['realname'] = realname
        if where:
            return TBUser.query.filter_by(**where).to_dicts

        return TBUser.query.to_dicts

    @staticmethod
    def authorize(data, as_api=False):
        """
        更新用户数据

        :param data: dict
        :param as_api: bool, True 入库失败返回 APIException
        :return:
        """
        res = TBUser().replace(data)
        current_app.logger.info('{}, {}'.format(res, data))
        if not res and as_api:
            raise APIFailure('用户授权失败')

        return res

    @staticmethod
    def deny(job_number, as_api=False):
        """
        禁用用户

        :param job_number: int
        :param as_api: bool
        :return:
        """
        data = {
            'job_number': job_number,
            'status': 0,
            'role': ''
        }
        res = TBUser().replace(data)
        current_app.logger.info('{}, {}'.format(res, data))
        if not res and as_api:
            raise APIFailure('禁用用户失败')

        return res
