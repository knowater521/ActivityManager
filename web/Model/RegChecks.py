from flask import abort

from web.Model.database import Activities, Members


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
