import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from web import app


db = SQLAlchemy(app)


class Members(db.Model):
    __bind_key__ = 'activity'
    sid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    stu_code = db.Column(db.Text)
    qq = db.Column(db.Text)
    phone = db.Column(db.Text)
    team = db.Column(db.Text, default="")
    activity = db.Column(db.VARCHAR(10))
    admin = db.Column(db.Boolean, default=False)

    def is_admin(self):
        return self.admin

    def __init__(self, name, stu_code, qq, phone, activity):
        self.name = name
        self.stu_code = stu_code
        self.qq = qq
        self.phone = phone
        self.activity = activity

    def get_id(self):
        return self.sid

    def get_act_name(self):
        return self.activity

    @property
    def is_authenticated(self, act):
        if act == self.activity:
            return True
        else:
            return False

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __repr__(self):
            return "{0} {1}".format(self.name, self.stu_code)


class Activities(db.Model):
    __bind_key__ = 'activity'
    activity_name = db.Column(db.VARCHAR(10), primary_key=True, unique=True)
    title = db.Column(db.Text)
    team_enable = db.Column(db.Boolean, default=False)
    upload_enable = db.Column(db.Boolean, default=False)
    note = db.Column(db.Text, default="")

    def __init__(self, activity_name, title, team_enable, upload_enable, note):
        self.activity_name = activity_name
        self.title = title
        self.team_enable = team_enable
        self.upload_enable = upload_enable
        self.note = note

    def __repr__(self):
        return "{0} {1} {2}".format(self.activity_name, self.team_enable, self.upload_enable)


class UploadHistory(db.Model):
    __bind_key__ = 'activity'
    sid = db.Column(db.Integer)
    activity = db.Column(db.VARCHAR)
    time = db.Column(db.DateTime, default=datetime.datetime.now())
    size = db.Column(db.Text)
    fid = db.Column(db.Integer, primary_key=True)

    def __init__(self, sid, activity, size):
        self.sid = sid
        self.size = size
        self.time = datetime.datetime.now()
        self.activity = activity


