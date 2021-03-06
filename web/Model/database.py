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
    activity = db.Column(db.VARCHAR(10), db.ForeignKey('activities.activity_name'))

    __has_submitted = None

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
    def team_str(self):
        if self.team is None:
            return ""
        return self.team

    @property
    def has_submit(self):
        if self.__has_submitted is None:
            member_submit_his = UploadHistory.query.filter_by(activity=self.activity, sid=self.sid).first()
            self.__has_submitted = member_submit_his is not None
        return self.__has_submitted

    def __repr__(self):
        return "{0} {1}".format(self.name, self.stu_code)


class Activities(db.Model):
    __bind_key__ = 'activity'
    activity_name = db.Column(db.VARCHAR(10), primary_key=True, unique=True)
    title = db.Column(db.Text)
    reg_enable = db.Column(db.Boolean, default=True)
    team_enable = db.Column(db.Boolean, default=False)
    upload_enable = db.Column(db.Boolean, default=False)
    note = db.Column(db.Text, default="")
    rank = db.Column(db.Integer, default=0)
    hide = db.Column(db.Boolean, default=False)

    def __init__(self, activity_name, title, reg_enable, team_enable, upload_enable, note, rank):
        self.activity_name = activity_name
        self.title = title
        self.team_enable = team_enable
        self.upload_enable = upload_enable
        self.reg_enable = reg_enable
        self.note = note
        self.rank = rank
        self.hide = False

    def __repr__(self):
        return "{0} {1} {2}".format(self.activity_name, self.team_enable, self.upload_enable)


class UploadHistory(db.Model):
    __bind_key__ = 'activity'
    sid = db.Column(db.Integer, db.ForeignKey('members.sid'))
    activity = db.Column(db.VARCHAR, db.ForeignKey('activities.activity_name'))
    time = db.Column(db.DateTime, default=datetime.datetime.now())
    size = db.Column(db.Text)
    fid = db.Column(db.Integer, primary_key=True)

    def __init__(self, sid, activity, size):
        self.sid = sid
        self.size = size
        self.time = datetime.datetime.now()
        self.activity = activity


class Admins(db.Model):
    __bind_key__ = 'activity'
    user = db.Column(db.VARCHAR, primary_key=True)
    passwd = db.Column(db.Text)
