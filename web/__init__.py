from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap


from web import Environment

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
app.config['SQLALCHEMY_BINDS'] = {"submiter": mysql_url + 'homeworksubmit'}

baseurl = Environment.baseurl

import web.Views



@app.route('/upload/')
def goto_main_page():
    return redirect(url_for('reg'))


@app.errorhandler(401)
def not_authed(err=None):
    return render_template('errors/401.html'), 401


@app.errorhandler(404)
def not_found(err=None):
    return render_template('errors/404.html', title='Page Not Found', code=404), 404


@app.errorhandler(500)
def inner_error(err=None):
    return render_template('errors/500.html', errors=err), 500

