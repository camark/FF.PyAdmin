"""
    log.py
    ~~~~~~~~
    views.log 数据校验

    :author: Fufu, 2019/9/21
"""
from wtforms import StringField

from . import BaseForm, StripString, PositiveInteger
from ..libs.helper import get_date


class LogSearchForm(BaseForm):
    # log_time = StringField('日志时间', validators=[StripString(allow_none=True)])
    log_operator = StringField('操作者', validators=[StripString(allow_none=True)])
    log_action = StringField('具体操作', validators=[StripString(allow_none=True)])
    log_status = StringField('操作结果', validators=[PositiveInteger(allow_none=True, allow_0=True)])

    # def validate_log_time(self, field):
    #     if field.data:
    #         self.log_time.data = get_date(field.data, out_fmt='%Y-%m-%d', default=False)


class LogReportForm(BaseForm):
    log_time = StringField('客户端操作时间', validators=[StripString(allow_none=True)])
    log_action = StringField('具体操作', validators=[StripString()])
    log_status = StringField('操作结果', validators=[PositiveInteger(allow_0=True)])

    def validate_log_time(self, field):
        self.log_time.data = get_date(field.data, in_fmt='%Y-%m-%d %H:%M:%S', out_fmt='%Y-%m-%d %H:%M:%S', default=True)

    def validate_log_status(self, field):
        self.log_status.data = 0 if field.data == 0 else 1
