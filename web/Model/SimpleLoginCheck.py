import functools

from flask import session, flash, redirect, url_for, abort
from web.Model.database import Members

from web.Model.RegChecks import check_acatvity


def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        act_name = kw.get('activity')
        act = check_acatvity(act_name)
        sid = session.get('{}_user'.format(act_name))
        if sid:
            member = Members.query.filter_by(sid=str(sid)).first()
            if act_name == member.get_act_name():

        return func(*args, current_user=member, act=act, **kw)
        # not logined
        flash('您还没加入活动或者登录呢~')
        return redirect(url_for('login', activity=act_name))

    return wrapper


def login_user(member):
    session['{}_user'.format(member.get_act_name())] = member.get_id()


def logout_user(member):
    session.pop('{}_user'.format(member.get_act_name()))


def is_authenticated(act_name):
    sid = session.get('{}_user'.format(act_name))
    if sid:
        return sid
    return None


def admin_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        isadmin = session.get('isadmin', False)
        if not isadmin:
            flash('请先登录')
            return redirect(url_for('admin_login'))
        return func(*args, **kw)
    return wrapper
