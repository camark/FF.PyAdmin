# -*- coding:utf-8 -*-
"""
    role.py
    ~~~~~~~~
    权限组及权限明细管理

    :author: Fufu, 2019/9/21
"""
from ..models import db
from ..models.user import TBRole
from ..libs.helper import list2dict


class RoleCharge:
    """Role 相关数据表操作"""

    @staticmethod
    def get_list(role=''):
        """
        获取权限列表(暂未分页)

        :param role: str
        :return: list
        """
        if role:
            return TBRole.query.filter_by(role=role).to_dicts

        return TBRole.query.to_dicts

    @staticmethod
    def get_role_data(as_dict=False, as_kv=False):
        """
        获取权限组数据

        :param as_dict:
        :param as_kv: True 时返回前端下拉框键值对
        :return: list
        """
        data = db.session.query(TBRole.role, TBRole.role_name).all()

        if as_kv:
            return list2dict(('Key', 'Value'), data)

        if as_dict:
            return list2dict(('role', 'role_name'), data)

        return data
