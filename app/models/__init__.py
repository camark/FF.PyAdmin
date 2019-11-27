"""
    __init__.py
    ~~~~~~~~
    模型基类

    :author: Fufu, 2019/9/2
"""
from collections import ChainMap
from contextlib import contextmanager

from flask import current_app
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery as _BaseQuery
from sqlalchemy import inspect, orm


class SQLAlchemy(_SQLAlchemy):
    """增加自动提交方法及异常处理"""

    @contextmanager
    def auto_commit(self, throw=True):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            current_app.logger.error('{0!r}'.format(e))
            if throw:
                raise e


class BaseQuery(_BaseQuery):
    """增加数据集转换, 更新删除自动提交"""

    @property
    def to_dicts(self):
        """
        将 .all() 转换为列表字典

        e.g.::

            asn_country = db.session.query(TBASNCountryCode, TBCountry). \
                join(TBCountry, and_(TBCountry.country_code == TBASNCountryCode.country_code,
                                     TBASNCountryCode.asn == 31001)).to_dicts

            asn_country = TBASNCountryCode.query.filter_by(asn=31001).to_dicts

        """
        try:
            res = self.all()
            if not res:
                return []
            if isinstance(res[0], tuple):
                rows = [dict(ChainMap(*[x.to_dict for x in row])) for row in res]
            else:
                rows = [x.to_dict for x in res]
            return rows
        except Exception:
            return []

    def update(self, values, synchronize_session="evaluate", update_args=None, throw=False):
        """
        增加自动提交和异常处理

        e.g.::

            TBUser.query.filter(TBUser.status < 2).update({'status': TBUser.status + 1})

            sess.query(User).filter(User.age == 25). \
                update({User.age: User.age - 10}, synchronize_session=False)

            sess.query(User).filter(User.age == 25). \
                update({"age": User.age - 10}, synchronize_session='evaluate')

            session.query(Engineer). \
                filter(Engineer.id == Employee.id). \
                filter(Employee.name == 'dilbert'). \
                update({"engineer_type": "programmer"})

        :param values: dict
        :param synchronize_session:
            ``'False'`` - 不修改当前 session 中的对象属性, 直接操作数据库.
            ``'fetch'`` - 修改前, 会先通过 select 查询条目的值, 数据库处理后再更新 session 中符合条件的条目.
            ``'evaluate'`` - 默认值, 会同时修改当前 session 中的对象属性.
        :param update_args: dict, 一些特殊参数, e.g. mysql_limit
        :param throw: bool, True 则抛出异常
        :return:
        """
        try:
            with db.auto_commit(True):
                return super(BaseQuery, self).update(values, synchronize_session=synchronize_session,
                                                     update_args=update_args)
        except Exception as e:
            if throw:
                raise e
            return False

    def delete(self, synchronize_session="evaluate", throw=False):
        """
        增加自动提交和异常处理

        e.g.::

            # 不能用 is None
            TBUser.query.filter(TBUser.status > 5, TBUser.mobile == None).delete(throw=True)
            TBUser.query.filter(TBUser.status < 2).delete()

            session.query(User).filter_by(username='abc').delete()

            user = session.query(User).filter_by(username='abc').first()
            session.delete(user)

            sess.query(User).filter(User.age == 25). \
                delete(synchronize_session=False)

            sess.query(User).filter(User.age == 25). \
                delete(synchronize_session='evaluate')

            session.query(Engineer). \
                filter(Engineer.id == Employee.id). \
                filter(Employee.name == 'dilbert'). \
                delete()

        :param synchronize_session:
            简单描述参考 update()
            ``'False'`` - 不同步 session, 如果被删除的 objects 已经在 session 中存在,
                          在 session commit 或者 expire_all 之前, 这些被删除的对象都存在 session 中.
                          不同步可能会导致获取被删除 objects 时出错.
            ``'fetch'`` - 删除之前从 db 中匹配被删除的对象并保存在 session 中, 然后再从 session 中删除,
                          这样做是为了让 session 的对象管理 identity_map 得知被删除的对象究竟是哪些以便更新引用关系.
            ``'evaluate'`` - 默认值. 根据当前的 query criteria 扫描 session 中的 objects, 如果不能正确执行则抛出错误,
                             即:
                             如果 session 中原本就没有这些被删除的 objects, 扫描当然不会发生匹配, 相当于匹配未正确执行.
                             这种报错只会在特定 query criteria 时报错, 比如 in 操作:
                             sess.query(Tag).filter(Tag.id.in_([1,2,3])).delete()
        :param throw: bool, True 则抛出异常
        :return:
        """
        try:
            with db.auto_commit(True):
                return super(BaseQuery, self).delete(synchronize_session=synchronize_session)
        except Exception as e:
            if throw:
                raise e
            return False


db = SQLAlchemy(query_class=BaseQuery)


class DBModel(db.Model):
    """
    为 db.Model 增加通用方法
    """
    __abstract__ = True
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    @orm.reconstructor
    def __init__(self):
        self.__dict_keys = [c.name for c in self.__table__.columns]

    def __getitem__(self, item):
        return getattr(self, item)

    def set_attrs(self, attrs):
        """
        设置当前实例变量(字段)值
        插入, 更新时绑定数据

        e.g.::

            # {'job_number': 114, 'role': 'testAdmin', 'status': 1}
            dict(TBUser.query.get(114).set_attrs({'role': 'testAdmin'}))

            with db.auto_commit():
                User().set_attrs(form.data)
                db.session.add(user)

        :param attrs: dict
        :return:
        """
        for key, value in attrs.items():
            hasattr(self, key) and setattr(self, key, value)

        return self

    def replace(self, data, filter_by=None, skip=False, skip_add=False, throw=False):
        """
        单条记录, 存在则更新, 不存在则新增(自动提交, 屏蔽/抛出异常)

        e.g.::

            data = {'job_number': 21, 'realname': '书记'}
            TBUser().replace(data) or current_app.logger.error('数据入库失败: {}'.format(data))

            # 更新操作, 避免记录不存在时更新异常(存在时正常 update, 不存在时返回 None)
            data = {'bgp_update': '2019-10-07 10:00:00'}
            filter_by = {'bgp_ip': '192.168.1.100'}
            TBBGP().replace(data, filter_by=filter_by, skip_add=True)

        :param data: dict, 数据集
        :param filter_by: dict, 查询条件(优先)
        :param skip: bool, True 存在即跳过(只添加不更新), 此时返回原数据集
        :param skip_add: bool, True 不存在时也不新增, 相当于 update()
        :param throw: bool, True 则抛出异常
        :return: bool|DBModel
        """
        try:
            with db.auto_commit(True):
                if isinstance(filter_by, dict):
                    # 指定查询条件
                    row = self.query.filter_by(**filter_by).first()
                else:
                    # 主键查询
                    row = self.get_by_primary(data)
                if row:
                    # 更新数据(修改)
                    skip or row.set_attrs(data)
                else:
                    # 插入数据(新增)
                    skip_add or db.session.add(self.set_attrs(data))
            return row if row else self
        except Exception as e:
            if throw:
                raise e
            return False

    def insert(self, data, throw=False):
        """
        插入单条数据(自动提交, 屏蔽/抛出异常)

        e.g.::

            data = {'job_number': 114, 'realname': 'test'}
            TBUser().insert(data)

        :param data: dict
        :param throw: bool, True 则抛出异常
        :return: bool
        """
        try:
            with db.auto_commit(True):
                db.session.add(self.set_attrs(data))
            return self
        except Exception as e:
            if throw:
                raise e
            return False

    def bulk_insert(self, datas, throw=False):
        """
        批量插入数据(自动提交, 屏蔽/抛出异常)

        e.g.::

            datas = []
            for i in range(0, 5):
                datas.append({'job_number': 100 + i, 'realname': 'test_' + str(i)})
            TBUser().bulk_insert(datas)

        :param datas: list.dict
        :param throw: bool, True 则抛出异常
        :return: bool
        """
        try:
            with db.auto_commit(True):
                db.session.bulk_insert_mappings(self.__class__, datas)
            return True
        except Exception as e:
            if throw:
                raise e
            return False

    @classmethod
    def get_by_primary(cls, data=None):
        """
        根据主键获取该行数据
        或用于检查数据是否存在, 修改数据等

        e.g.::

            # 联合主键
            CNGameid.get_by_primary({'ctime': '2018-10-01', 'gameid': 1616})

            # 自增 ID
            TBUser.get_by_primary({'job_number': 114})
            TBUser.query.get(114)

        :return: DBModel
        """
        cls_primary_keys = tuple(k.name for k in inspect(cls).primary_key)
        if cls_primary_keys:
            # 主键:值字典
            primary_keys = cls_primary_keys if isinstance(cls_primary_keys, tuple) else (cls_primary_keys,)
            param = {field: data[field] for field in primary_keys if field in data}
            if len(param) == len(primary_keys):
                return cls.query.filter_by(**param).first()

        return None

    @property
    def to_dict(self):
        """
        (单条数据)得到完整表字段数据字典, 去除了 DBModel.__dict__ 中的额外元素

        e.g.::

            CNGameid.get_by_primary({'ctime': '2018-10-01', 'gameid': 1616}).to_dict
            TBUser.query.get(114).to_dict

            from app import JSONEncoder
            json.dumps(dict(TBUser.query.get(114)), cls=JSONEncoder, ensure_ascii=False)

        :return: dict
        """
        return dict(self)

    def keys(self):
        """
        为 to_dict 提供服务: keys, __getitem__

        e.g.::

            # {'job_number': 114, 'role': 'Admin', 'status': 1}
            return jsonify(TBUser.query.get(114))

            # 自定义返回字段
            class TBUser(DBModel):
                def keys(self):
                    return ['job_number', 'realname', 'last_login']

        """
        return self.__dict_keys

    def hide_keys(self, *keys):
        """
        隐藏不想输出的字段

        e.g.::

            # {'job_number': 114, 'status': 1}
            dict(TBUser.query.get(114).hide_keys('role'))

        :param keys:
        :return:
        """
        for key in keys:
            key in self.__dict_keys and self.__dict_keys.remove(key)

        return self

    def choose_keys(self, *keys):
        """
        仅选择需要的字段

        e.g.::

            # {'job_number': 114, 'status': 1}
            dict(TBUser.query.get(114).choose_keys('job_number', 'status'))

        :param keys:
        :return:
        """
        self.__dict_keys = keys
        return self

    def append_keys(self, *keys):
        """
        增加想输出的字段

        e.g.::

            # {'job_number': 114, 'status': 1}
            dict(TBUser.query.get(114).hide_keys('status').append_keys('status'))

        :param keys: str
        :return:
        """
        for key in keys:
            self.__dict_keys.append(key)

        return self
