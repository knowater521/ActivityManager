from web import app
from flask_nav import Nav
from flask_nav.elements import Navbar, View

nav = Nav()


@nav.navigation()
def nav_bar():
    return Navbar(
        '作品上传系统',
        # View('报名', 'reg'),
        # View('上传', 'upload'),
        # View('退出', 'logout')
    )


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
