# -*- coding:utf-8 -*-
"""
    bgp.py
    ~~~~~~~~
    BGP 管理

    :author: Fufu, 2019/9/21
"""
from flask import current_app
from sqlalchemy import desc

from ..models.bgp import TBBGP
from ..libs.exceptions import APIFailure


class BGPCharge:
    """BGP 相关数据表操作"""

    @staticmethod
    def add(data, as_api=False):
        """
        新增 BGP

        :param data: dict
        :param as_api: True 入库失败返回 APIException
        :return:
        """
        res = TBBGP().insert(data)
        current_app.logger.info('{}, {}'.format(res, data))
        if not res and as_api:
            raise APIFailure('BGP 入库失败')

        return res

    @staticmethod
    def get_list(where=None, order_by=None):
        """
        获取 BGP 列表(暂未分页)

        :param where: dict
        :param order_by: dict, 排序字段 e.g. {'bgp_update'} {'bgp_update': 'desc'}
        :return: list
        """
        where = dict(filter(lambda x: tuple(x)[1], where.items())) if where else {}
        q = TBBGP.query.filter_by(**where)

        if order_by and isinstance(order_by, dict):
            for field, order_type in order_by.items():
                q = q.order_by(desc(field) if order_type == 'desc' else field)
        else:
            # 默认 BGP 最后更新时间升序
            q = q.order_by('bgp_update')

        return q.to_dicts
