# -*- coding:utf-8 -*-
"""
    user.py
    ~~~~~~~~
    用户管理和权限分配

    :author: Fufu, 2019/9/17
"""
from flask import Blueprint, render_template
from flask_login import current_user

from ..services.user import UserCharge
from ..services.auth import permission_required
from ..forms.user import UserAuthorizeForm, UserJobNumberForm, UserSearchForm
from ..libs.exceptions import APISuccess, APIFailure

bp_user = Blueprint('user', __name__, url_prefix='/user')


@bp_user.route('')
@permission_required
def user_index():
    return render_template('user/index.html')


@bp_user.route('/list', methods=['POST'])
@permission_required
def user_list():
    form = UserSearchForm().check()
    data = UserCharge.get_list(form.job_number.data, form.realname.data)
    return APISuccess(data)


@bp_user.route('/authorize', methods=['POST'])
@permission_required
def user_authorize():
    form = UserAuthorizeForm().check()
    UserCharge.authorize(form.data)
    return APISuccess()


@bp_user.route('/deny', methods=['POST'])
@permission_required
def user_deny():
    form = UserJobNumberForm().check()
    if current_user.job_number == form.job_number.data:
        return APIFailure('不能禁用自己的账号')
    UserCharge.deny(form.job_number.data)
    return APISuccess()
