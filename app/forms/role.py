"""
    role.py
    ~~~~~~~~
    views.role 数据校验

    :author: Fufu, 2019/12/5
"""
from wtforms import StringField
from wtforms.validators import ValidationError

from . import BaseForm, StripString, PositiveInteger
from ..models.user import TBRole


class RoleSearchForm(BaseForm):
    role = StringField('权限标识', validators=[StripString(plain_text=True, allow_none=True)])


class RoleForm(BaseForm):
    role = StringField('权限标识', validators=[StripString(plain_text=True)])


class RoleAddEditForm(RoleForm):
    role_id = StringField('权限ID', validators=[PositiveInteger(allow_0=True)])
    role_name = StringField('权限名称', validators=[StripString(plain_text=True)])
    role_allow = StringField('允许权限', validators=[StripString(plain_text=True)])
    role_deny = StringField('禁止权限', validators=[StripString(plain_text=True, allow_none=True)])

    def validate_role_id(self, field):
        if TBRole.query.filter(TBRole.role == self.role.data, TBRole.role_id != field.data).first():
            raise ValidationError('权限标识{}已存在'.format(self.role.data))
