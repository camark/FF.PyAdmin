# -*- coding:utf-8 -*-
"""
    role.py
    ~~~~~~~~
    权限码表及权限设定

    :author: Fufu, 2019/9/17
"""
from flask import Blueprint, render_template
from flask_login import current_user

from ..forms.role import RoleSearchForm, RoleAddEditForm, RoleForm
from ..libs.exceptions import APISuccess, APIFailure
from ..services.role import RoleCharge
from ..services.auth import permission_required

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
    form = RoleSearchForm().check()
    data = RoleCharge.get_list(form.role.data)
    return APISuccess(data)


@bp_role.route('/data', methods=['POST'])
@permission_required
def role_data():
    """权限组数据(键值对)"""
    data = RoleCharge.get_role_data(as_kv=True)
    return APISuccess(data)


@bp_role.route('/add_edit', methods=['POST'])
@permission_required
def role_add_edit():
    """添加/修改权限组"""
    form = RoleAddEditForm().check()
    RoleCharge.save(form.data, as_api=True)
    return APISuccess()


@bp_role.route('/delete', methods=['POST'])
@permission_required
def role_delete():
    """删除权限组"""
    form = RoleForm().check()
    if current_user.role == form.role.data:
        return APIFailure('不能删除自己所在的权限组')
    RoleCharge.delete(form.role.data, as_api=True)

    return APISuccess()
