"""
    user.py
    ~~~~~~~~
    views.user 数据校验

    :author: Fufu, 2019/9/21
"""
from wtforms import StringField
from wtforms.validators import ValidationError, Regexp

from . import BaseForm, StripString, PositiveInteger
from ..models.user import TBUser, TBRole


class UserSearchForm(BaseForm):
    job_number = StringField('工号', validators=[PositiveInteger(allow_none=True)])
    realname = StringField('姓名', validators=[StripString(allow_none=True)])


class UserJobNumberForm(BaseForm):
    job_number = StringField('工号', validators=[PositiveInteger()])

    def validate_job_number(self, field):
        if not TBUser.query.get(field.data):
            raise ValidationError('工号{}不存在'.format(field.data))


class UserAuthorizeForm(UserJobNumberForm):
    role = StringField('权限组', validators=[StripString()])
    mobile = StringField('手机号', validators=[StripString(), Regexp(r'^1\d{10}$', message='手机号不正确')])
    status = StringField('状态', default=1, validators=[PositiveInteger()])

    def validate_role(self, field):
        if not TBRole.query.filter_by(role=field.data).first():
            raise ValidationError('权限组{}不存在'.format(field.data))
