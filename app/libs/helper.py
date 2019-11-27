"""
    helper.py
    ~~~~~~~~
    助手函数集

    :author: Fufu, 2019/9/9
"""
import hashlib
import re
import sys
import time
import ipaddress
from functools import wraps
from itertools import chain
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from flask import request


def run_perf(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = fn(*args, **kwargs)
        end = time.perf_counter()
        print('\n~~~~~~\n{}.{} : {}\n~~~~~~\n'.format(fn.__module__, fn.__name__, end - start))
        return res

    return wrapper


def debug(*data, end='------\n', die=False):
    """输出调试信息"""
    from pprint import pprint
    for x in data:
        pprint(x)
    print('', end=end)
    die and sys.exit(1)


def get_plain_text(s):
    """
    获取纯文本内容
    清除 html 标签, 空白字符替换为一个空格, 去除首尾空白

    :param s: str
    :return: str
    """
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()


def get_uniq_list(data):
    """
    列表去重并保持顺序(数据量大时效率不高)

    :param data: list
    :return: list
    """
    ret = list(set(data))
    ret.sort(key=data.index)
    return ret


def list2dict(key, *value):
    """
    列表转换列表.字典(用于数据记录转字典列表)

    e.g.::

        list2dict(('a', 'b'), [(1, 2), (3, 4)], [('x', 22)])

    :param key: tuple, list, 元组或列表, 与每行数据元素个数相同
    :param value: list.tuple, 一组元组数据
    :return: list.dict
    """
    try:
        return [dict(zip(key, x)) for x in chain(*value)]
    except Exception:
        return []


def get_int(s=None, default=None, sep=None):
    """
    检查是否为整数, 转换并返回 int 或 列表

    e.g.::

        # None
        get_int('1a')

        # 0
        get_int('1a', 0)

        # 123
        get_int(' 123   ')

        # [123, 456, 7]
        get_int('123, 456,, 7,, ,')

    :param s: str, 整数值或字符串
    :param default: 转换整数失败时的默认值(列表转换时无效)
    :param sep: str, 指定分隔符时返回 list, e.g. [1, 7]
    :return: int / list / default
    """
    if isinstance(s, int):
        return int(s)
    elif isinstance(s, str):
        s = s.strip()
        try:
            if sep:
                ret = [int(x) for x in s.split(sep) if x.strip() != '']
                ret = get_uniq_list(ret)
            else:
                ret = int(s)
        except ValueError:
            ret = [] if sep else default
    else:
        ret = [] if sep else default

    return ret


def get_ipv4(ip=None, sep=None, fn='IPv4Address'):
    """
    检查是否为 IP 地址/网段/接口, 清除每个 IP 的空白, 返回 IP 字符串或 IP 列表

    e.g.::

        # 127.0.0.1
        get_ipv4(' 127.0.0.1   ')

        # 127.0.0.1
        get_ipv4(0x7f000001)

        # ['127.0.0.1', '8.8.8.8', '0.0.0.7']
        get_ipv4('127.0.0.1, 8.8.8.8,, 10a, 7,,127.0.0.1,::1 ', ',')

        # 0.0.0.10
        get_ipv4(10)

        # 172.16.0.0/12
        get_ipv4('172.16.0.0/12', fn='IPv4Network')

        # 172.16.0.1/12
        get_ipv4('172.16.0.1/12', fn='IPv4Interface')

        # ['127.0.0.1/31', '8.8.8.8/24', '0.0.0.7/32', '127.0.1.0/24']
        get_ipv4('127.0.0.1/31, 8.8.8.8/24,, 10a, 7,,127.0.1.0/24,::1 ', ',' , fn='IPv4Interface')

    :param ip: str, IP 地址
    :param sep: str, 指定分隔符时返回 list
    :param fn: str, ip_address / ip_network / ip_interface
    :return: str / list
    """
    if not ip:
        return None

    if sep:
        ret = []
        for x in ip.split(sep):
            ipv4 = get_ipv4(x, fn=fn)
            if ipv4 and not ipv4 in ret:
                ret.append(ipv4)
    else:
        if isinstance(ip, str):
            ip = ip.strip()
            if ip.count('.') != 3:
                return None
        try:
            ret = str(getattr(ipaddress, fn)(ip))
        except Exception:
            ret = None

    return ret


def get_ipv4_address(ip=None, sep=None):
    """
    检查是否为 IP 地址, 清除每个 IP 的空白, 返回 IP 字符串或 IP 列表

    e.g.::

        # 127.0.0.1
        get_ipv4_address(' 127.0.0.1   ')

        # 127.0.0.1
        get_ipv4_address(0x7f000001)

        # ['127.0.0.1', '8.8.8.8', '0.0.0.7']
        get_ipv4_address('127.0.0.1, 8.8.8.8,, 10a, 7,,127.0.0.1,::1 ', ',')

        # 0.0.0.10
        get_ipv4_address(10)

    :param ip: str, IP 地址
    :param sep: str, 指定分隔符时返回 list
    :return: str / list
    """
    return get_ipv4(ip, sep, fn='IPv4Address')


def get_ipv4_network(ip=None, sep=None):
    """
    检查是否为 IP 网段, 清除每个 IP 的空白, 返回 IP 字符串或 IP 列表

    e.g.::

        # 172.16.0.0/12
        get_ipv4_network('172.16.0.0/12')

        # ['127.0.0.1/32', '8.8.8.8/32', '127.0.1.0/24']
        get_ipv4_network('127.0.0.1/32, 8.8.8.8,, 10a, 7,,127.0.1.0/24,::1 ', ',')

    :param ip: str, IP 地址
    :param sep: str, 指定分隔符时返回 list
    :return: str / list
    """
    return get_ipv4(ip, sep, fn='IPv4Network')


def get_ipv4_interface(ip=None, sep=None):
    """
    检查是否为 IP 接口, 清除每个 IP 的空白, 返回 IP 字符串或 IP 列表

    e.g.::

        # 172.16.0.1/12
        get_ipv4_interface('172.16.0.1/12')

        # ['127.0.0.1/31', '8.8.8.8/24', '0.0.0.7/32', '127.0.1.0/24']
        get_ipv4_interface('127.0.0.1/31, 8.8.8.8/24,, 10a, 7,,127.0.1.0/24,::1 ', ',')

    :param ip: str, IP 地址
    :param sep: str, 指定分隔符时返回 list
    :return: str / list
    """
    return get_ipv4(ip, sep, fn='IPv4Interface')


def get_date(dt=None, in_fmt='%Y-%m-%d', out_fmt='', default=True):
    """
    检查日期是否正确并返回日期

    e.g.::

        get_date('2018-10-10')
        get_date('2018-10-10 12:00:00', '%Y-%m-%d %H:%M:%S')

    :param dt: mixed, 输入的日期, 空/日期字符串/日期对象
    :param in_fmt: str, 源日期格式
    :param out_fmt: str, 返回的日期格式, 默认返回日期对象
    :param default: bool, True 源日期格式不正确时返回今天
    :return: datetime|None|str
    """
    if not isinstance(dt, datetime):
        try:
            dt = datetime.strptime(dt, in_fmt)
        except Exception:
            dt = datetime.now() if default else None

    return (datetime.strftime(dt, out_fmt) if out_fmt else dt) if dt else None


def get_hash(data=None, hash_name='md5', salt=''):
    """
    获取数据的摘要信息

    :param data: str, list, dict...
    :param hash_name: str, e.g. 'md5', 'sha1', 'sha224', 'sha256'...
    :param salt: str
    :return:
    """
    try:
        m = getattr(hashlib, hash_name)(salt if isinstance(salt, bytes) else bytes(str(salt), 'utf-8'))
        m.update(data if isinstance(data, bytes) else bytes(str(data), 'utf-8'))
        return m.hexdigest()
    except Exception:
        return ''


def is_accept_json(or_post=True):
    """
    用于确定是否返回 JSON 响应体
    替代 request.xhr

    :type or_post: bool, True 时 POST 请求也返回真
    :return: bool
    """
    return 'application/json' in str(request.accept_mimetypes) or \
           request.environ.get('HTTP_X_REQUESTED_WITH', '').lower() == 'xmlhttprequest' or \
           or_post and request.method == 'POST'


def get_large_file(url, file=None, chunk_size=4096, retries=3, timeout=(30, 30), throw=False, **kwargs):
    """
    下载大文件(流), 默认重试 3 次
    保存到文件或返回 requests 对象

    :param url: str, 下载链接
    :param file: str, 结果保存文件
    :param chunk_size: int, 文件保存时的块大小
    :param retries: int, 重试次数
    :param timeout: int | tuple 连接超时和读取超时
    :param throw: bool, 是否抛出异常
    :param kwargs: dict, requests 自定义参数
    :return: bool | requests
    """
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        r = s.get(url, stream=True, timeout=timeout, **kwargs)
        if file:
            try:
                with open(file, 'wb+') as f:
                    for chunk in r.iter_content(chunk_size):
                        f.write(chunk)
                return True
            except Exception as e:
                if throw:
                    raise e
                return False
        return r
    except requests.exceptions.RequestException as e:
        if throw:
            raise e
        return False
