"""
    bp_web.py
    ~~~~~~~~
    主页

    :author: Fufu, 2019/9/2
"""
import os

from authlib.common.errors import AuthlibBaseError
from flask import (Blueprint, current_app, send_from_directory, redirect, url_for,
                   render_template, session)
from flask_login import logout_user, login_required
from requests.exceptions import RequestException

from ..forms import csrf
from ..services.auth import oauth, chk_user_login, set_user_login

bp_web = Blueprint('web', __name__)
csrf.exempt(bp_web)


@bp_web.route('/')
@login_required
def web_index():
    """主页"""
    return render_template('index.html')


@bp_web.route('/login')
def web_login():
    """登录页"""
    return render_template('login.html')


@bp_web.route('/authorize')
def web_authorize():
    """OAuth 登录跳转"""

    # TODO: (演示使用, 自动登录), 请删除并配置自己的认证方式, OAuth2或账密系统
    set_user_login({
        'job_number': 7777,
        'realname': 'Fufu'
    })
    return redirect(url_for('web.web_index'))

    # OAuth 认证
    redirect_uri = url_for('web.web_authorized', _external=True)
    return oauth.OA.authorize_redirect(redirect_uri)


@bp_web.route('/authorized')
def web_authorized():
    """OAuth 登录认证"""
    try:
        token = oauth.OA.authorize_access_token()
    except (AuthlibBaseError, RequestException):
        return redirect(url_for('web.web_authorize'))

    # 用户身份校验
    chk_user_login(token)

    return redirect(url_for('web.web_index'))


@bp_web.route('/logout')
@login_required
def web_logout():
    """退出登录"""
    logout_user()
    session.clear()

    return redirect(url_for('web.web_index'))


@bp_web.route('/favicon.ico')
def web_favicon():
    """浏览器地址栏图标"""
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')
