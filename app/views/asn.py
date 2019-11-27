# -*- coding:utf-8 -*-
"""
    asn.py
    ~~~~~~~~
    ASN 码表及关系关联

    :author: Fufu, 2019/9/17
"""
from flask import Blueprint, render_template
from flask_login import login_required

from ..forms.asn import ASNSearchForm, ASNAddForm
from ..libs.exceptions import APISuccess, APIFailure
from ..services.asn import ASNCharge
from ..services.auth import permission_required

bp_asn = Blueprint('asn', __name__, url_prefix='/asn')


@bp_asn.route('')
@login_required
def asn_index():
    """主页"""
    return render_template('asn/index.html')


@bp_asn.route('/list', methods=['POST'])
@login_required
def asn_list():
    """主页 ASN 列表"""
    form = ASNSearchForm().check()
    data = ASNCharge.get_list(form.asn.data)
    return APISuccess(data)


@bp_asn.route('/add', methods=['POST'])
@permission_required
def asn_add():
    """新增 AS 号"""
    form = ASNAddForm().check()
    ASNCharge.add(form.data, as_api=True)
    return APISuccess()


@bp_asn.route('/delete', methods=['POST'])
@permission_required
def asn_delete():
    """删除 AS 号"""
    return APIFailure('暂未开放删除操作')
