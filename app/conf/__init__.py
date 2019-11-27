"""
    __init__.py
    ~~~~~~~~
    配置项

    :author: Fufu, 2019/9/2
"""
import os
import xxtea

from flask import current_app, json


def get_conf_json(path, file):
    """
    通用: 获取 JSON 配置文件

    :param path: 相对于 conf, e.g. bgp
    :param file: 文件名, 不带扩展名, e.g. as-name
    :return: dict，e.g. {'123': '成都'}
    """
    ret = {}
    file = os.path.join(current_app.root_path, 'conf', path, file + '.json')

    try:
        with open(file, 'r', encoding='utf-8') as f:
            ret = json.load(f)
    except Exception as e:
        current_app.logger.error('{0!r} {1}'.format(e, file))

    return ret


def get_environ(varname='', default='', key=None):
    """
    获取环境变量值(解密数据)

    :param varname: str, 环境变量名称
    :param default: 缺省值
    :param key: 加密的 key
    :return: str
    """
    data = os.getenv(varname, default)
    if key:
        try:
            data = xxtea.decrypt_hex(data.encode('utf-8'), key).decode('utf-8')
        except Exception:
            data = default

    return data


def set_environ(varname='', data='', key=None):
    """
    设置环境变量值(加密数据)

    :param varname: str, 环境变量名称
    :param data: 值
    :param key: 加密的 key
    :return: str
    """
    if key:
        try:
            data = xxtea.encrypt_hex(data, key).decode('utf-8')
        except Exception:
            data = ''

    os.environ[varname] = data

    return data
