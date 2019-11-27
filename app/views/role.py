# -*- coding:utf-8 -*-
"""
    role.py
    ~~~~~~~~
    权限码表及权限设定

    :author: Fufu, 2019/9/17
"""
from flask import Blueprint, render_template

from ..services.role import RoleCharge
from ..services.auth import permission_required
from ..libs.exceptions import APISuccess, APIFailure

bp_role = Blueprint('role', __name__, url_prefix='/role')


@bp_role.route('')
@permission_required
def role_index():
    """主页"""
    return render_template('role/index.html')


@bp_role.route('/list', methods=['POST'])
@permission_required
def role_list():
    """权限列表"""
    data = RoleCharge.get_list()
    return APISuccess(data)


@bp_role.route('/data', methods=['POST'])
@permission_required
def role_data():
    """权限组数据(键值对)"""
    data = RoleCharge.get_role_data(as_kv=True)
    return APISuccess(data)


@bp_role.route('/delete', methods=['POST'])
@permission_required
def role_delete():
    """删除权限组"""
    return APIFailure('暂未开放删除操作')


@bp_role.route('/detail', methods=['POST'])
@permission_required
def role_detail(role):
    return 'role.detail' + type(role) + str(role)
