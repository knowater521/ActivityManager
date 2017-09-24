from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import json

app = Flask(__name__)

# BootStarp init
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['BOOTSTRAP_QUERYSTRING_REVVING'] = False
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
Bootstrap(app)

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
        app.secret_key = config["secret_key"]
        app.config['databaseUser'] = config["mysql_user"]
        app.config['databasePwd'] = config["mysql_passwd"]
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_NATIVE_UNICODE'] = True
        if config["Test_Mode"]:
            app.config['SQLALCHEMY_ECHO'] = True

        mysql_url = 'mysql+pymysql://{0}:{1}@localhost:{2}/'.format(config["mysql_user"], config["mysql_passwd"],
                                                                    config["mysql_port"])
        app.config['SQLALCHEMY_BINDS'] = {"activity": mysql_url + config["database"]}
        baseurl = config["baseurl"]

except:
    print("Config File Open Fail!")
    exit(-1)

import web.Views


@app.errorhandler(401)
def not_authed(err=None):
    return render_template('errors/401.html'), 401


@app.errorhandler(404)
def not_found(err=None):
    return render_template('errors/404.html', title='Page Not Found', code=404), 404


@app.errorhandler(500)
def inner_error(err=None):
    return render_template('errors/500.html', errors=err), 500
