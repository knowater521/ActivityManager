from web import app
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask import request,session
from web.Model.database import Activities
from web.Model.SimpleLoginCheck import is_authenticated
nav = Nav()
nav.init_app(app)


@nav.navigation()
def nav_bar():
    nav.renderer()
    act_name = request.base_url.split('/')[-2]
    act = Activities.query.filter_by(activity_name=act_name).first()
    items = [View('首页', 'index')]
    if is_authenticated(act_name):
        items.append(View('报名查询', 'register_success', activity=act_name))
        if act.upload_enable:
            items.append(View('作品上传', 'upload', activity=act_name))
        if session.get('isadmin', False):
            items.append(View('管理中心', 'admin_home', activity=act_name))
        items.append(View('登出', 'logout', activity=act_name))
    else:
        items.append(View('报名', 'reg', activity=act_name))
        items.append(View('报名查询', 'login', activity=act_name))

    return Navbar('作品上传系统', *items)


@nav.navigation()
def nav_bar_admin():
    act_name = request.args.get('act')
    return Navbar(
        '管理员',
        View('活动管理', 'admin_home'),
        View('活动成员', 'memberlist', act=act_name),
        View('提交情况', 'submitlist', act=act_name),
        View('退出', 'logout_admin'),
        # View('新版管理面版', 'admin.index'),
        # View('退出', 'logout')

    )


