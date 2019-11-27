# -*- coding:utf-8 -*-
"""
    for asn.feature
    ~~~~~~~~

    :author: Fufu, 2019/10/9
"""
from behave import *
from flask import Response


@given('输入AS号和描述 "{asn}", "{asn_desc}"')
def step_impl(ctx, asn, asn_desc):
    ctx.asn = asn
    ctx.asn_desc = asn_desc


@given('仅输入AS号 "{asn}"')
def step_impl(ctx, asn):
    ctx.asn = asn
    ctx.asn_desc = None


@when('执行添加AS号')
def step_impl(ctx):
    ctx.resp = ctx.client.post('/asn/add', data={
        'asn': ctx.asn,
        'asn_desc': ctx.asn_desc
    })


@then('AS号添加成功')
def step_impl(ctx):
    assert isinstance(ctx.resp, Response)
    assert ctx.resp.status_code == 200
    res = ctx.resp.json
    print('asn_add: {}'.format(res))
    assert res['ok'] == 1


@then('AS号添加失败')
def step_impl(ctx):
    assert isinstance(ctx.resp, Response)
    assert ctx.resp.status_code == 200
    res = ctx.resp.json
    print('asn_add: {}'.format(res))
    assert res['ok'] == 0
    assert res['err_code'] > 0
    assert res['msg']
