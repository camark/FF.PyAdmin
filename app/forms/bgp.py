"""
    bgp.py
    ~~~~~~~~
    views.bgp 数据校验

    :author: Fufu, 2019/9/21
"""
from wtforms import StringField
from wtforms.validators import ValidationError

from . import BaseForm, StripString, PositiveInteger
from ..models.bgp import TBBGP, TBASN
from ..libs.helper import get_ipv4_address


def validate_bgp_ip(form, field):
    if field.data:
        if not get_ipv4_address(field.data):
            raise ValidationError('BGP IP 不正确')


def validate_bgp_asn(form, field):
    if field.data:
        if not TBASN.query.get(field.data):
            raise ValidationError('AS{}不存在'.format(field.data))


class BGPSearchForm(BaseForm):
    bgp_ip = StringField('BGP-IP', validators=[StripString(allow_none=True), validate_bgp_ip])
    bgp_asn = StringField('所属ASN', validators=[PositiveInteger(allow_none=True), validate_bgp_asn])


class BGPListOrderByForm(BaseForm):
    """列表排序字段"""
    order__field = StringField(validators=[StripString(allow_none=True)])
    order__type = StringField(validators=[StripString(allow_none=True)])

    def validate_order_field(self, field):
        self.order__field.data = field.data.lower()

    def validate_order_type(self, field):
        self.order__type.data = 'desc' if field.data.lower() == 'desc' else 'asc'


class BGPIPForm(BaseForm):
    bgp_ip = StringField('BGP-IP', validators=[StripString(), validate_bgp_ip])


class BGPAddForm(BGPIPForm):
    bgp_asn = StringField('所属 ASN', validators=[PositiveInteger(), validate_bgp_asn])
    bgp_desc = StringField('BGP 描述', validators=[StripString(plain_text=True)])

    def validate_bgp_ip(self, field):
        if TBBGP.query.filter_by(bgp_ip=field.data).first():
            raise ValidationError('BGP{}已存在'.format(field.data))
