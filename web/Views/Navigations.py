from web import app
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask import request,session
from web.Model.database import Activities
from web.Model.SimpleLoginCheck import is_authenticated
nav = Nav()


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
        items.append(View('登录', 'login', activity=act_name))

    return Navbar('作品上传系统', *items)


@nav.navigation()
def nav_bar_admin():

    return Navbar(
        '管理员',
        # View('测试上传', 'upload'),
        # View('上传清单', 'download_list'),
        # View('情况总览', 'stu_list'),
        # View('新版管理面版', 'admin.index'),
        # View('退出', 'logout')

    )


nav.init_app(app)
