"""
    __init__.py
    ~~~~~~~~
    初始化 app
    注册蓝图到 app
    日志及环境配置

    :author: Fufu, 2019/9/2
"""
import os
import logging
from datetime import datetime, date
from collections import namedtuple

from flask import Flask as _Flask, render_template
from flask.json import JSONEncoder as _JSONEncoder, jsonify
from concurrent_log_handler import ConcurrentRotatingFileHandler

from .services.auth import oauth, login_manager
from .models import db, DBModel
from .forms import csrf
from .views import init_blueprint, init_template_global
from .libs.exceptions import APIException, APIServerError, APIFailure
from .libs.helper import is_accept_json


class JSONEncoder(_JSONEncoder):
    """重写 Flask JSON encoder"""

    def default(self, o):
        """
        支持 DBModel 和日期时间. (注: ``UUID``, ``dataclasses`` 等未继承)

        e.g.::

            # {job_number: 114, mobile: "13880010809", last_login: "2019-09-10 09:04:59", status: 1}
            return jsonify(TBUser.query.get(114).hide_keys('realname', 'role'))

        :param o:
        :return:
        """
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        raise APIServerError()


class Flask(_Flask):
    json_encoder = JSONEncoder

    def make_response(self, rv):
        """
        支持视图函数直接返回 DBModel, list, dict(1.1.0+官方支持)

        e.g.::

            # {job_number: 114, mobile: "13880010809", last_login: "2019-09-10 09:04:59", status: 1}
            return TBUser.query.get(114).hide_keys('realname', 'role')

        :param rv:
        :return:
        """
        if isinstance(rv, (list, dict, DBModel)):
            rv = jsonify(rv)
        return super(Flask, self).make_response(rv=rv)


def init_config(app, config_name=None, config=None):
    """
    加载各类环境配置

    :param app: Flask
    :param config_name: str, 指定配置文件名或环境变量配置名 e.g. development / testing / production
    :param config: str / dict 最高优先级配置, 字典或文件名
    :return: None
    """
    # 加载生产环境配置
    app.config.from_object('app.conf.secret_settings')
    app.config.from_object('app.conf.settings')

    # 加载指定名称的文件配置
    if not config_name:
        config_name = os.getenv(app.config.get('APP_NAME', 'FLASK_CONFIG'))
    if config_name:
        try:
            app.config.from_object('app.conf.{}_settings'.format(config_name))
        except ImportError:
            pass

    # 加载指定的参数配置
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config, silent=True)


def init_logger(app):
    """
    初始化日志(按大小滚动)

    :param app: Flask
    :return: None
    """
    log_maxsize = app.config.get('LOG_MAXSIZE', 100)
    log_backup = app.config.get('LOG_BACKUP', 20)
    log_level = app.config.get('LOG_LEVEL', logging.INFO)
    app_log = app.config.get('LOG_FILE')
    if not app_log:
        app_log = os.path.join(os.path.dirname(app.root_path), 'logs', 'app.log')
    fh = ConcurrentRotatingFileHandler(app_log, maxBytes=log_maxsize * 1024 * 1024, backupCount=log_backup,
                                       encoding='utf-8', use_gzip=True)
    fh.setLevel(log_level)
    fh.setFormatter(logging.Formatter(
        app.config.get('LOG_FORMAT', '%(asctime)s %(levelname)s %(module)s.%(funcName)s: %(message)s')))
    app.logger.addHandler(fh)


def init_error(app):
    """
    全局异常处理

    :param app: Flask
    :return: None
    """

    @app.errorhandler(Exception)
    def global_exception_handler(e):
        # 500 错误时记录日志
        code = getattr(e, 'code', 500)
        code == 500 and app.logger.error(e)

        if isinstance(e, APIException):
            return e

        # 自定义异常描述
        err = namedtuple('MyError', ['code', 'description'])(
            code, app.config.get('EXCEPTION_DESC', {}).get(code, getattr(e, 'description', str(e)))
        )

        if app.config.get('API') or is_accept_json():
            return APIFailure(description=err.description)
        if app.config['DEBUG']:
            raise e

        return render_template('base-error.html', e=err), code


def create_app(config_name=None, config=None):
    """
    初始化 Flask 应用

    :param config_name: str
    :param config: str / dict 扩展配置或配置文件
    :return: Flask
    """
    app = Flask(__name__)

    # 加载环境配置
    init_config(app, config_name=config_name, config=config)

    # 日志配置
    init_logger(app)

    # 自定义错误页
    init_error(app)

    # 注册蓝图
    init_blueprint(app)

    # 注册 OAuth2
    oauth.init_app(app)

    # 注册 flask_login
    login_manager.init_app(app)

    # CSRF 保护
    csrf.init_app(app)

    # 注册模板全局函数
    init_template_global(app)

    # 初始化数据库配置
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app
