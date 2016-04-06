import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from web import app


db = SQLAlchemy(app)


class User(db.Model):
    __bind_key__ = 'submiter'
    user = db.Column(db.VARCHAR, primary_key=True)
    pwd = db.Column(db.Text)
    admin = db.Column(db.Boolean, default=False)

    def is_admin(self):
        return self.admin

    def __init__(self, username, password, qq):
        self.user = username
        self.pwd = password
        self.qq = qq

    def get_id(self):
        return self.user

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __repr__(self):
            return "{0} {1}".format(self.user, self.pwd)


class Uploads(db.Model):
    __bind_key__ = 'submiter'
    user = db.Column(db.VARCHAR)
    time = db.Column(db.DateTime, default=datetime.datetime.now())
    size = db.Column(db.Text)
    fid = db.Column(db.Integer, primary_key=True)

    def __init__(self, user, size):
        self.user = user
        self.size = size
        self.time = datetime.datetime.now()
