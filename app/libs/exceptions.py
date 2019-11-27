"""
    exceptions.py
    ~~~~~~~~
    通用 HTTP 错误页
    API 各类异常处理
    API 通用返回值处理
    注: 为适应内部各系统和前端, 并非标准 RESTful (兼容)

    :author: Fufu, 2019/8/15
"""
from flask import json
from werkzeug.exceptions import HTTPException


class MsgException(HTTPException):
    """通用的消息页面"""

    description = '发生错误, 请重试'
    code = 406

    def __init__(self, description=None, response=None, code=None):
        if not description is None:
            try:
                # form.errors, dict, 返回第一个错误消息
                self.description = list(description.values())[0][0]
            except Exception:
                self.description = str(description)
        if not code is None:
            self.code = code

        super(MsgException, self).__init__(response=response)


class APIException(HTTPException):
    """
    API 接口异常处理
    Flask 中异常处理字段不变
        description: 自定义消息 / 系统异常消息 / form.errors
        err_code: 0 正常, 自定义的字段, [关键属性] 决定 ret 返回成功还是失败. == ret['err_code']
        code: HTTP Status Code
    API 请求始终返回固定的 6 个字段(ret):
        ok: 0 失败, 1 成功 (前端 js 常用)
        msg: 错误消息, 成功时必定为空
        code: 0 成功, 1 失败 (前端框架使用方便)
        data: 各类型数据或数据集, 默认为列表
        count: 总记录数 (数据分页时可用)
        err_code: 接口自定义的错误码
            0 成功
            < 1000 程序内部错误
            >= 1000 请求类错误

    e.g.::

        # 异常
        raise APIException('非法请求')

        # 指定 HTTP Status Code
        raise APIException('拒绝请求', code=521, err_code=1234)

        # Form
        raise APIException(form.errors)
        raise APIParameterError(form.errors)

        # 成功
        ret = {'data': [1, 2]}
        return APIException(ret=ret, code=200, err_code=0)
        return APISuccess(ret=ret)
        return APISuccess([1, 2])

        # 失败
        return APIFailure()
        return APIFailure('错误消息')
    """
    description = '接口异常'
    err_code = 400
    code = 400

    def __init__(self, description=None, response=None, ret=None, code=None, err_code=None, headers=None):
        """同 HTTPException, 增加 ret 属性"""
        self.ret = {
            'ok': 0,
            'msg': '',
            'data': [],
            'code': 1,
            'count': 0,
            'err_code': 400
        }
        if ret and isinstance(ret, dict):
            self.ret.update(ret)

        if not code is None:
            self.code = code
        if not err_code is None:
            self.err_code = err_code
        if not description is None:
            self.description = description

        # 自定义响应头 e.g. [('xunyou', 'xxx')]
        self.headers = headers if headers and isinstance(headers, list) else []

        # 根据 err_code 重新整理返回值
        if self.err_code:
            self.ret.update({
                'ok': 0,
                'code': 1,
                'err_code': self.err_code
            })

            # 错误消息
            if not self.ret['msg']:
                if isinstance(self.description, str):
                    self.ret['msg'] = self.description
                else:
                    try:
                        # form.errors, dict, 返回第一个错误消息
                        self.ret['msg'] = list(self.description.values())[0][0]
                    except Exception:
                        self.ret['msg'] = str(self.description)
        else:
            self.ret.update({
                'ok': 1,
                'msg': '',
                'code': 0,
                'err_code': 0
            })

        super(APIException, self).__init__(response=response)

    def get_body(self, environ=None):
        """Get the JSON body"""
        return json.dumps(self.ret)

    def get_headers(self, environ=None):
        """JSON headers"""
        return [('Content-Type', 'application/json')] + self.headers


class APISuccess(APIException):
    """
    API 请求成功通用返回

    e.g.::

        return APISuccess([1])

    """
    code = 200
    err_code = 0
    description = 'OK'

    def __init__(self, data=None, count=0, response=None, headers=None):
        super(APISuccess, self).__init__(ret={'data': data, 'count': count}, response=response, headers=headers)


class APIFailure(APIException):
    """
    API 请求失败通用返回
    HTTP 状态码同样为 200, 前端 ajax 方便接收和显示错误消息
    """
    code = 200
    err_code = 1000
    description = '接口请求失败'


class APIParameterError(APIFailure):
    err_code = 1001
    description = '请求参数错误'


class APIServerError(APIException):
    code = 500
    err_code = 500
    description = '接口服务异常'


class APINotFound(APIException):
    code = 404
    err_code = 404
    description = '未知接口请求'


class APIAuthFailed(APIException):
    code = 401
    err_code = 401
    description = '接口鉴权失败'


class APIForbidden(APIException):
    code = 403
    err_code = 403
    description = '拒绝访问接口'


class APIClosed(APIException):
    code = 202
    err_code = 202
    description = '接口服务未开启'
