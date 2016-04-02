from flask_bootstrap import Bootstrap
from flask import Flask, render_template

from flask_nav import Nav
from flask_nav.elements import Navbar, View

from web import Environment

from flask.ext.admin.contrib.sqla import ModelView


app = Flask(__name__)
app.secret_key = 'jhjhjgAWg;;fgsHH,jmN$*&hjksdfX/!?RT'

# BootStarp init
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['BOOTSTRAP_QUERYSTRING_REVVING'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
Bootstrap(app)

# Database Setting
app.config['databaseUser'] = Environment.mysql_user
app.config['databasePwd'] = Environment.mysql_passwd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_NATIVE_UNICODE'] = True

# app.config['SQLALCHEMY_ECHO']=True
mysql_url = 'mysql+pymysql://{0}:{1}@localhost:{2}/'.format(Environment.mysql_user, Environment.mysql_passwd,
                                                            Environment.mysql_port)
app.config['SQLALCHEMY_BINDS'] = {"submiter": mysql_url + 'homeworksubmit'
                                  }

import web.uploader
import web.index
import web.admin

nav = Nav()


@nav.navigation()
def nav_bar():
    return Navbar(
            '作品上传系统',
            View('上传', 'upload'),
            View('退出', 'logout')
    )


@nav.navigation()
def nav_bar_admin():
    return Navbar(
            '管理员',
            View('测试上传', 'upload'),
            View('上传清单', 'download_list'),
            View('情况总览', 'stu_list'),
            View('新版管理面版', 'admin.index'),
            View('退出', 'logout')

    )


nav.init_app(app)


@app.errorhandler(401)
def not_authed(err=None):
    return render_template('errors/401.html'), 401


@app.errorhandler(404)
def not_found(err=None):
    return render_template('errors/404.html', title='Page Not Found', code=404), 404


@app.errorhandler(500)
def inner_error(err=None):
    return render_template('errors/500.html', errors=err), 500

