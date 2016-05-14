from web.Views.Model.database import db, Activities, Members
from flask import abort


def check_acatvity(name):
    act = Activities.query.filter_by(activity_name=name).first()
    if not act:
        abort(404)
    return act


def check_user_exist(stucode, act_name):
    stu = Members.query.filter_by(stu_code=stucode, activity=act_name).first()
    if stu:
        return True
    else:
        return False
