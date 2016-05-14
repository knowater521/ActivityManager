import functools
from flask import session, flash,redirect
from web.Views.Model.database import db, Activities, Members
from web.Views.Model.RegChecks import check_acatvity


def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        act_name = kw.get('activity')
        act = check_acatvity(act_name)
        sid = session.get('{}_user'.format(act_name))
        if sid:
            member = Members.query.filter_by(sid=str(sid)).first()
            if act_name == member.get_act_name():
                return func(*args, **kw, current_user=member, act=act)
        # not logined
        flash('您还没加入活动或者登录呢~')
        return redirect('/upload/{}/join'.format(act_name))

    return wrapper


def login_user(member):
    session['{}_user'.format(member.get_act_name())] = member.get_id()


def is_authenticated(act_name):
    sid = session.get('{}_user'.format(act_name))
    if sid:
        return sid
    return None
