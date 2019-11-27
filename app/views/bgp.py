"""
    bgp.py
    ~~~~~~~~
    BGP 码表操作

    :author: Fufu, 2019/9/17
"""
from flask import Blueprint, render_template
from flask_login import login_required

from ..libs.exceptions import APISuccess, APIFailure
from ..services.auth import permission_required
from ..services.bgp import BGPCharge
from ..forms.bgp import BGPSearchForm, BGPAddForm, BGPListOrderByForm

bp_bgp = Blueprint('bgp', __name__, url_prefix='/bgp')


@bp_bgp.route('')
@login_required
def bgp_index():
    """主页"""
    return render_template('bgp/index.html')


@bp_bgp.route('/list', methods=['POST'])
@login_required
def bgp_list():
    """BGP 列表"""
    form_search = BGPSearchForm().check()
    form_order = BGPListOrderByForm().check()
    order_by = {form_order.order__field.data: form_order.order__type.data} if form_order.order__field.data else {}
    data = BGPCharge.get_list(form_search.data, order_by)

    return APISuccess(data)


@bp_bgp.route('/add', methods=['POST'])
@permission_required
def bgp_add():
    """新增 BGP"""
    form = BGPAddForm().check()
    BGPCharge.add(form.data, as_api=True)
    return APISuccess()


@bp_bgp.route('/delete', methods=['POST'])
@permission_required
def bgp_delete():
    """删除特殊路由表"""
    return APIFailure('暂未开放删除操作')
