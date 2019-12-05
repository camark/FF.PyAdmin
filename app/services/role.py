# -*- coding:utf-8 -*-
"""
    role.py
    ~~~~~~~~
    权限组及权限明细管理

    :author: Fufu, 2019/9/21
"""
from flask import current_app

from ..models import db
from ..models.user import TBRole, TBUser
from ..libs.exceptions import APIFailure
from ..libs.helper import list2dict


class RoleCharge:
    """Role 相关数据表操作"""

    @staticmethod
    def save(data, as_api=False):
        """
        新增/修改权限组

        :param data: dict
        :param as_api: True 入库失败返回 APIException
        :return:
        """
        res = TBRole().replace(data)
        current_app.logger.info('{}, {}'.format(res, data))
        if not res and as_api:
            raise APIFailure('权限组保存失败')

        return res

    @staticmethod
    def delete(role, as_api=False):
        """
        删除权限组
        禁用该权限组所有用户

        :param role: 权限标识
        :param as_api: True 入库失败返回 APIException
        :return:
        """
        # 禁用该权限组的用户
        deny = TBUser.query.filter_by(role=role).update({
            'role': '',
            'status': 0,
        })
        if deny is False:
            if as_api:
                raise APIFailure('权限组用户禁用失败')
            return False

        # 删除权限组
        res = TBRole.query.filter_by(role=role).delete()
        current_app.logger.info('{}, {}'.format(res, role))
        if not res and as_api:
            raise APIFailure('权限组删除失败')

        return res

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
