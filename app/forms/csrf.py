# -*- coding:utf-8 -*-
"""
    csrf.py
    ~~~~~~~~
    修正 Flask-wtf 0.14.2 FlaskForm, @csrf.exempt 无效的问题
    后续版本有修复时直接使用 from flask_wtf.csrf import CSRFProtect 即可

    :author: Fufu, 2019/10/24
"""
from flask import request, g
from flask_wtf.csrf import generate_csrf, CSRFProtect as _CSRFProtect


class CSRFProtect(_CSRFProtect):
    """满足排除条件时设置 g.valid = True"""

    def init_app(self, app):
        app.extensions['csrf'] = self

        app.config.setdefault('WTF_CSRF_ENABLED', True)
        app.config.setdefault('WTF_CSRF_CHECK_DEFAULT', True)
        app.config['WTF_CSRF_METHODS'] = set(app.config.get(
            'WTF_CSRF_METHODS', ['POST', 'PUT', 'PATCH', 'DELETE']
        ))
        app.config.setdefault('WTF_CSRF_FIELD_NAME', 'csrf_token')
        app.config.setdefault(
            'WTF_CSRF_HEADERS', ['X-CSRFToken', 'X-CSRF-Token']
        )
        app.config.setdefault('WTF_CSRF_TIME_LIMIT', 3600)
        app.config.setdefault('WTF_CSRF_SSL_STRICT', True)

        app.jinja_env.globals['csrf_token'] = generate_csrf
        app.context_processor(lambda: {'csrf_token': generate_csrf})

        def _set_csrf_valid_true():
            """设置验证通过, 满足 _FlaskFormCSRF.validate_csrf_token 内判断"""
            g.csrf_valid = True
            return

        @app.before_request
        def csrf_protect():
            if not app.config['WTF_CSRF_ENABLED']:
                return _set_csrf_valid_true()

            if not app.config['WTF_CSRF_CHECK_DEFAULT']:
                return _set_csrf_valid_true()

            if request.method not in app.config['WTF_CSRF_METHODS']:
                return _set_csrf_valid_true()

            if not request.endpoint:
                return _set_csrf_valid_true()

            view = app.view_functions.get(request.endpoint)

            if not view:
                return _set_csrf_valid_true()

            if request.blueprint in self._exempt_blueprints:
                return _set_csrf_valid_true()

            dest = '%s.%s' % (view.__module__, view.__name__)

            if dest in self._exempt_views:
                return _set_csrf_valid_true()

            self.protect()
