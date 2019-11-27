"""
    __init__.py
    ~~~~~~~~
    初始化蓝图：web(公用/单蓝图)...

    :author: Fufu, 2019/9/2
"""
from .web import bp_web
from .bgp import bp_bgp
from .asn import bp_asn
from .log import bp_log
from .user import bp_user
from .role import bp_role
from ..services.auth import is_can


def init_blueprint(app):
    """
    初始化蓝图

    :param app: Flask
    :return:
    """
    app.register_blueprint(bp_web)
    app.register_blueprint(bp_bgp)
    app.register_blueprint(bp_asn)
    app.register_blueprint(bp_log)
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_role)


def init_template_global(app):
    """模板全局函数"""
    app.add_template_global(is_can)
    # 清除空行
    app.jinja_env.trim_blocks = app.config.get('JINJA_ENV_TRIM_BLOCKS', True)
    app.jinja_env.lstrip_blocks = app.config.get('JINJA_ENV_LSTRIP_BLOCKS', True)
