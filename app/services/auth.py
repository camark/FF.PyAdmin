# -*- coding:utf-8 -*-
"""
    auth.py
    ~~~~~~~~
    登录认证相关

    :author: Fufu, 2019/9/15
"""
import pickle
from functools import wraps

from flask import abort, current_app, request, session
from flask_login import LoginManager as _LoginManager, login_user, current_user
from authlib.integrations.flask_client import OAuth

from ..models.user import TBUser, TBRole
from ..models.bgp import TBBGP
from ..libs.exceptions import MsgException, APIFailure, APIForbidden, APIClosed
from ..libs.helper import is_accept_json
from ..services.log import LogCharge


class LoginManager(_LoginManager):
    """特定场景返回登录失效提示"""

    def unauthorized(self):
        if is_accept_json():
            raise APIFailure('登录状态过期, 请刷新')
        return super(LoginManager, self).unauthorized()


oauth = OAuth()
oauth.register('OA')

login_manager = LoginManager()
login_manager.login_view = 'web.web_login'
login_manager.login_message = '请先登录'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(job_number):
    """
    Flask-login 获取用户信息
    user = TBUser.query.get(int(job_number))

    :param job_number:
    :return:
    """
    try:
        user = pickle.loads(session['load_user'])
    except Exception:
        user = None

    return user


def chk_api_open():
    """检查 API 接口服务开关"""
    return True


def permission_required(fn):
    """
    校验登录状态
    检验权限
    日志记录

    e.g.::

        @web.route('/test')
        @permission_required
        def test():
            # 同时满足:
            # role_deny 不包含 web.test
            # role_allow 包含 web 或 web.test
            pass

    :param fn:
    :return:
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        # 校验登录状态
        if not current_user.is_authenticated or not session.get('role_allow'):
            return current_app.login_manager.unauthorized()

        # 校验权限(禁止优先)
        view_fn = request.endpoint
        bp = view_fn.split('.')[0]
        if view_fn in session['role_deny'] or bp not in session['role_allow'] and view_fn not in session['role_allow']:
            abort(403)

        # 记录日志
        LogCharge.to_db()

        return fn(*args, **kwargs)

    return wrapper


def bgp_required(fn):
    """
    校验来访是否为 BGP 服务器
    日志记录

    e.g.::

        @web.route('/test')
        @bgp_required
        def test():
            # 请求 IP 需要在 TBBGP.bgp_ip 中存在
            pass

    :param fn:
    :return: json
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        client_ip = request.remote_addr
        res = TBBGP.query.filter_by(bgp_ip=client_ip).first()
        if not res:
            raise APIForbidden('非法请求')

        if not chk_api_open():
            raise APIClosed()

        bgp_info = res.to_dict

        # 记录日志
        LogCharge.to_db({
            'log_operator': bgp_info['bgp_ip']
        })

        return fn(bgp_info, *args, **kwargs)

    return wrapper


def devops_required(fn):
    """
    校验来访是否为运维部(内网IP)

    e.g.::

        @web.route('/test')
        @devops_required
        def test():
            # 请求 IP 为 192.168.0.0/16
            pass

    :param fn:
    :return: json
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        client_ip = request.remote_addr
        if client_ip \
                and client_ip != current_app.config.get('LOCAL_GW') \
                and client_ip[0:8] not in ['192.168.', '127.0.0.']:
            abort(403)

        if not chk_api_open():
            raise MsgException('接口服务未开启', code=202)

        return fn(*args, **kwargs)

    return wrapper


def chk_user_login(token):
    """
    用户 OAuth 登录后检查

    :param token: OAuth2.token
    :return: bool
    """
    try:
        # 获取用户资料
        resp = oauth.OA.get('user/', token=token)
        user_info = resp.json()
    except Exception:
        raise MsgException('OA服务异常, 请重试')

    return set_user_login(user_info)


def set_user_login(user_info):
    """
    设置用户登录状态
    TODO: 单点登录限制

    :param user_info: dict, 用户资料
    :return:
    """
    # 更新 TBUser 表信息
    user = TBUser().replace({
        'job_number': user_info['job_number'],
        'realname': user_info['realname']
    }, skip=True)
    if user:
        if user.status != 1 or not user.role:
            raise MsgException('账号未激活', code=401)

        # 用户权限列表
        role = TBRole.query.filter_by(role=user.role).first()
        if not role or not role.role_allow:
            raise MsgException('账号未授权', code=401)

        # 登录成功
        login_user(user)
        session['load_user'] = pickle.dumps(user)
        session['role_allow'] = role.role_allow.split(',')
        session['role_deny'] = role.role_deny.split(',')
        session.permanent = True

        # 登录日志
        LogCharge.to_db()

        return True

    raise MsgException('登录失败, 请重试', code=401)


def is_can(allow):
    """
    检查是否有权限

    e.g.::

        if is_can('asn.add'):
            pass

    :param allow: str
    :return:
    """
    role_allow = session.get('role_allow')
    role_deny = session.get('role_deny')
    if not role_allow or not allow or not isinstance(allow, str):
        return False

    return allow not in role_deny and (allow in role_allow or allow.split('.')[0] in role_allow)
