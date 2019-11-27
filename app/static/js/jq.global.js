var $ = layui.$, jQuery = layui.jquery, layer = layui.layer, form = layui.form, table = layui.table,
    element = layui.element, laydate = layui.laydate, fbody = $('body');

$(function () {
    /* 内容铺满屏 */
    $('#grid_main').height($(window).height() - $('.panel-title').outerHeight() - $('.header').outerHeight() - 70);

    /* 行点击底色 */
    fbody.on('click', '.layui-table-view table.layui-table tr', function (d) {
        var my = $(this);
        my.parent().find('tr').removeClass('tr-selected');
        my.addClass('tr-selected');
        if ($.isFunction($.trClick)) {
            //.行事件传参：当前选中的行索引号，当前表的id，当前行的dom
            var tbl_id = my.parent().parent().parent().parent().parent().prev().attr('id');
            $.trClick(my.data('index'), tbl_id, my);
        }
    });

    /* 点击文本框选中文本 */
    $('.txt-focus').focus(function () {
        this.select();
    });
});

/* 点击复制文本 */
$.extend({
    fcopy: function (dom) {
        let tmp = $('<input>');
        $('body').append(tmp);
        try {
            tmp.val(dom.text()).select();
            if (document.execCommand('copy')) {
                layer.msg('已复制');
            } else {
                layer.msg('复制失败, 请手动复制')
            }
        } catch (e) {
            layer.msg('复制错误, 请手动复制')
        }
        tmp.remove();
    }
});

/* js.htmlspecialchars，默认不处理单引号，直接显示输入的代码或插入表单使用, b == true: onclick=open(var) */
$.extend({
    ftohtml: function (a, b) {
        a = a || "";
        a && (a = a.toString().replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"));
        b && (a = a.replace(/'/g, "\\'"));
        return a;
    }
});

/* freload */
$.extend({
    freload: function (a, b) {
        a = a || location.href;
        b = b || 500;
        setTimeout(function () {
            location.replace(a);
            return !0
        }, b)
    }
});

/* fgourl */
$.extend({
    fgourl: function (a) {
        a = a || location.href;
        location.href = a;
        return !1
    }
});

/* selectLinkage，联动下拉菜单 */
$.extend({
    fselect: function (a, b, cfg) {
        b = b || "";
        cfg = cfg || {};
        var c = $("#" + a);
        if (c.length > 0) {
            c.empty();
            c.append('<option value="">加载中..</option>');
            form.render("select");
            $.ajax({
                url: c.data("fjson"),
                type: "POST",
                data: {x: c.data("fx"), v: b},
                dataType: "json",
                beforeSend: function (xhr, settings) {
                    let csrf_token = $('meta[name=csrf-token]').attr('content');
                    if (csrf_token && !/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader('X-CSRFToken', csrf_token);
                    }
                }
            }).done(function (b) {
                //.请求失败或登录失效的情况
                if (b['msg'] && b['ok'] == 0) {
                    layer.msg(b['msg']);
                    return false;
                }
                if (b['data'] && b['ok'] == 1) {
                    b = b['data']
                }
                var d = c.data("fvalue");
                //.数据请求完毕时回调
                var mySuccess = c.data("fsuccess");
                cfg[mySuccess] && typeof cfg[mySuccess] === 'function' && (b = cfg[mySuccess](b, d));
                var fval = '';
                var e, selected;
                c.empty();
                $.each(b, function (a, b) {
                    if (d == b["Key"]) {
                        selected = ' selected="selected"';
                        fval = b["Key"];
                    } else {
                        selected = '';
                        fval = fval || b["Key"];
                    }
                    c.append('<option value="' + b["Key"] + '"' + selected + ">" + b["Value"] + "</option>")
                });
                form.render("select");
                //.渲染完成时回调
                var myDone = c.data("fdone");
                cfg[myDone] && typeof cfg[myDone] === 'function' && cfg[myDone](b, fval);
                e = c.data("fchange");
                var myOn = c.data("fon");
                cfg[myOn] && typeof cfg[myOn] === 'function' || (cfg[myOn] = false);
                if (e || cfg[myOn]) {
                    //.渲染下级菜单
                    e && $.fselect(e, c.val(), cfg);
                    //.有下级菜单或指定了监听回调时，需要 form.on()
                    form.on("select(" + a + ")", function (a) {
                        e && $.fselect(e, a.value, cfg);
                        cfg[myOn] && cfg[myOn](a);
                    })
                }
            }).fail(function () {
                c.empty();
                c.append('<option value="">加载失败</option>');
                form.render("select");
            })
        }
    }
});

/* 通用 ajax 请求, kw['sync'] == true 为同步 */
$.extend({
    mkAjax: function (d, url, title, callBack, btn, type, kw) {
        kw = kw || {};
        btn && btn.prop('disabled', true).addClass('layui-btn-disabled');
        var msg = '错误: ' + (title || '操作') + '失败';
        var icon = {icon: 5, anim: 6};
        var idx = kw['noload'] || layer.load();
        //.{done: func, fail: func, always: func}; func == {done: func}
        var func = 'function' == typeof callBack ? {done: callBack} : callBack || {};
        $.ajax({
            url: url,
            type: type || 'POST',
            data: d || {},
            dataType: 'json',
            async: !kw['sync'],
            cache: false,
            beforeSend: function (xhr, settings) {
                let csrf_token = $('meta[name=csrf-token]').attr('content');
                if (csrf_token && !/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', csrf_token);
                }
            }
        }).done(function (r, textStatus, jqXHR) {
            if (!$.isEmptyObject(r)) {
                msg = r['msg'] || (title || '操作') + '成功';
                if (r['ok'] == 1) {
                    icon = {icon: 1};
                    func['done'] && typeof func['done'] === 'function' && func['done'](r, d, textStatus, jqXHR);
                }
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            func['fail'] && typeof func['fail'] === 'function' && func['fail'](d, jqXHR, textStatus, errorThrown);
        }).always(function (obj, textStatus) {
            btn && btn.prop('disabled', false).removeClass('layui-btn-disabled');
            kw['noload'] || layer.close(idx);
            if (func['always'] && typeof func['always'] === 'function') {
                //.always: return true && show msg
                func['always'](d, obj, textStatus) && layer.msg(msg, icon);
            } else {
                msg && layer.msg(msg, icon);
            }
        });
        return false;
    }
});

/* 按数据集字段渲染表格 */
$.extend({
    autoTbl: function (cfg, def) {
        cfg = cfg || {};
        def = def || {};
        //.CSRF 保护
        let csrf_token = $('meta[name=csrf-token]').attr('content');
        cfg["headers"] || (cfg["headers"] = {});
        var o_ins;
        //.PS：请用标准的 {code: 0, msg: '', count: 0, data: []}，该函数未做自定义参数兼容
        //.必须要有数据集，才开始渲染表格
        if (cfg["r"]) {
            var cols = [[]];
            //.单元格宽度，默认自适应，2.2.0 新增，还是手动强
            cfg["w"] = cfg["w"] || null;
            if (cfg["cols"]) {
                //.优先使用传参中的列配置
                cols = cfg["cols"];
            } else {
                //.附加的表头, 前置: [{cols},{cols}]
                $.each(def["before"], function (k, v) {
                    cols[0].push(v);
                });
                //.提取数据集中的字段
                if ($.isEmptyObject(cfg["r"]["data"][0])) {
                    //.数据集为空时的默认列配置
                    cols = [[{
                        field: "null",
                        title: "无数据",
                        width: cfg["w"]
                    }]];
                } else {
                    $.each(cfg["r"]["data"][0], function (field) {
                        var col = {
                            field: field,
                            title: $.fxmlchars(field)
                        };
                        cfg["w"] && (col['width'] = cfg["w"]);
                        //.优先使用传参中的字段配置: {field: {cols.option}}
                        def["main"] && def["main"][field] && $.each(def["main"][field], function (k, v) {
                            col[k] = v;
                        });
                        cols[0].push(col);
                        //.字段的附加字段, 如计算的%, 可以是多个, 单个值为完整字段配置: {field: [{cols},{cols}]}
                        def["main_add"] && def["main_add"][field] && $.each(def["main_add"][field], function (k, v) {
                            v && cols[0].push(v);
                        });
                    });
                }
                //.附加的表头, 后置: [{cols},{cols}]
                $.each(def["after"], function (k, v) {
                    cols[0].push(v);
                });
            }
            if (cfg["t"]) {
                //.静态表格，非数据表格
                var colgroup = "";
                var thead = "";
                var tbody = "";
                //.数据请求完成表格渲染前时回调
                typeof cfg["parseData"] === "function" && (cfg["r"] = cfg["parseData"](cfg["r"]));
                //.表格配置及表头
                $.each(cols[0], function (k, v) {
                    colgroup += v["width"] ? '<col width="' + v["width"] + '">' : '<col>';
                    thead += "<th>" + v["title"] + "</th>";
                });
                //.表格数据
                $.each(cfg["r"]["data"], function (i, row) {
                    tbody += "<tr>";
                    //.表格行数据，按表头字段取值
                    $.each(cols[0], function (k, v) {
                        tbody += "<td>" + (row[v["field"]] === undefined ? "" : row[v["field"]]) + "</td>";
                    });
                    tbody += "</tr>";
                });
                //.其他配置项
                var css = "layui-table" + (cfg["css"] ? " " + cfg["css"] : "");
                var add = cfg["add"] ? " " + cfg["add"] : "";
                var size = cfg["size"] ? ' lay-size="' + cfg["size"] + '"' : "";
                //.返回静态表格 HTML
                var tbl = '<table class="' + css + '"' + size + add + ">" + "<colgroup>" + colgroup + "</colgroup>" + "<thead>" + thead + "</thead>" + "<tbody>" + tbody + "</tbody>" + "</table>";
                //.完成时回调
                typeof cfg["done"] === "function" && cfg["done"](tbl, cfg["r"]);
                return tbl;
            } else {
                //.数据表格渲染参数集
                var option = {};
                //.配置参数
                $.each(cfg, function (k, v) {
                    //.表格类型，结果集，请求参数，表格列默认宽度，这四个参数特殊用途（避免后期与官方参数冲突，用单字母）
                    k == "t" || k == "r" || k == "d" || k == "w" || (option[k] = v);
                });
                //.必要的参数处理
                option["elem"] || (option["elem"] = cfg["elem"] ? cfg["elem"] : cfg["id"] ? "#" + cfg["id"] : "#tbl_main");
                option["id"] || (option["id"] = cfg["id"] ? cfg["id"] : cfg["elem"] ? cfg["elem"].replace("#", "").replace(".", "") : "tbl_main");
                //.2.1.7 非异步数据时不分页这参数也会生效，修正
                option["limit"] = option["limit"] || cfg["limit"] || (cfg["page"] ? 60 : 99999);
                option["data"] = cfg["r"]["data"] || []; //.data 为了进入已知数据渲染
                option["setRes"] = cfg["r"]; //.用原始数据集进入渲染，为了回调时可使用原始数据集
                option["setCount"] = option["setCount"] || cfg["r"]["count"];  //.记录总数
                option["cols"] = cols;
                //.需要分页且不是已知数据分页时的处理
                if (option["page"] && !option["dataPage"]) {
                    //.在得到 cols 后，以下二个参数将写入当前实例参数中，后续由实例自身的 laypage 接管请求
                    option["setUrl"] = cfg["d"]["url"];
                    option["setWhere"] = cfg["d"]["where"];
                }
                //.请求状态及消息，以下两个参数用于模拟 Ajax 请求后表格主体上显示的错误消息
                option["firstCode"] = cfg["r"]["code"];
                option["firstMsg"] = cfg["r"]["msg"];
                //.表格翻页时回调，可动态附加请求参数，第一页除外，默认会附加 总页数 count 字段，需要返回 obj
                option["myJump"] = cfg["myJump"] || null;
                //.自动宽度时全局最小列宽（系统默认 60）
                option["cellMinWidth"] = option["cellMinWidth"] || 110;
                //.请求头
                option["headers"] = cfg["headers"];
                //.返回方法级渲染实例
                o_ins = table.render(option);
                typeof option["myIns"] === 'function' && option["myIns"](o_ins);
                return o_ins;
            }
        } else {
            //.先呈现一个带加载图标的占位表格
            var tmp = {
                elem: cfg["elem"],
                id: cfg["id"],
                size: cfg["size"],
                height: cfg["height"],
                loading: true,
                autoSort: false,
                data: [],
                cols: cfg["cols"] || [[{title: "..."}]],
                text: {none: '<i class="layui-icon layui-icon-loading layui-anim layui-anim-rotate layui-anim-loop f32 p20"></i>'}
            };
            o_ins = table.render(tmp);
            //.异步请求数据（最后使用回调取得结果）
            var ret = null;
            $.ajax({
                url: cfg["d"]["url"],
                type: cfg["method"] || "POST",
                data: cfg["d"]["where"],
                dataType: cfg["dataType"] || "json",
                headers: cfg["headers"],
                beforeSend: function (xhr, settings) {
                    if (csrf_token && !/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrf_token);
                        cfg["headers"]["X-CSRFToken"] = csrf_token;
                    }
                }
            }).done(function (r) {
                if ($.isEmptyObject(r["data"]) || $.isEmptyObject(r["data"][0]) || r["code"] > 1) {
                    //.0 和 1 由表格显示消息或渲染数据，否则中止渲染弹出消息层
                    //.initSort 存在时, 默认的 无数据 提示将无效, 故统一判断数据集是否为空
                    o_ins.reload({
                        data: [],
                        cols: [[{title: ""}]],
                        text: {none: r["msg"] || "暂无相关数据"}
                    });
                } else {
                    //.用已知数据渲染表格
                    cfg["r"] = r;
                    ret = $.autoTbl(cfg, def);
                }
            }).fail(function (jqXHR, textStatus) {
                o_ins.reload({
                    autoSort: false,
                    data: [],
                    cols: [[{title: ""}]],
                    text: {none: "数据加载失败, 请稍后重试"}
                });
            });

            return ret;
        }
    }
});

/* $('form').serializeJson(); */
$.fn.serializeJson = function () {
    let a = {}, b = this.serializeArray();
    $.each(b, function () {
        if (a[this.name]) {
            a[this.name].push || (a[this.name] = [a[this.name]]);
            a[this.name].push(this.value || "")
        } else a[this.name] = this.value || ""
    });
    return a
};
