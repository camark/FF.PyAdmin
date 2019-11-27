# -*- coding:utf-8 -*-
"""
    asn.py
    ~~~~~~~~
    ASN 相关服务

    :author: Fufu, 2019/9/18
"""
from flask import current_app

from ..models.bgp import *
from ..libs.exceptions import APIFailure


class ASNCharge:
    """ASN 相关数据表操作"""

    @staticmethod
    def add(data, as_api=False):
        """
        新增 ASN

        :param data: dict
        :param as_api: True 入库失败返回 APIException
        :return:
        """
        res = TBASN().insert(data)
        current_app.logger.info('{}, {}'.format(res, data))
        if not res and as_api:
            raise APIFailure('ASN 入库失败')

        return res

    @staticmethod
    def get_list(asn=None):
        """
        获取 ASN 列表(暂未分页)

        e.g.::

            ASNCharge.get_list(31001)
            ASNCharge.get_list()

        :return: list
        """
        if asn:
            return TBASN.query.filter_by(asn=asn).to_dicts

        return TBASN.query.to_dicts
