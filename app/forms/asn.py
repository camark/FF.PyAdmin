"""
    asn.py
    ~~~~~~~~
    views.asn 数据校验

    :author: Fufu, 2019/9/19
"""
from wtforms import StringField
from wtforms.validators import ValidationError

from . import BaseForm, StripString, PositiveInteger
from ..models.bgp import TBASN


class ASNSearchForm(BaseForm):
    asn = StringField('AS 号', validators=[PositiveInteger(allow_none=True)])


class ASNForm(BaseForm):
    """AS 号必填正整数"""
    asn = StringField('AS 号', validators=[PositiveInteger()])


class ASNAddForm(ASNForm):
    asn_desc = StringField('AS 描述', validators=[StripString(plain_text=True)])

    def validate_asn(self, field):
        if TBASN.query.get(field.data):
            raise ValidationError('AS{}已存在'.format(field.data))


class ASNExistForm(ASNForm):
    """校验数据库是否有该 AS 号"""

    def validate_asn(self, field):
        if not TBASN.query.get(field.data):
            raise ValidationError('AS{}不存在'.format(field.data))
