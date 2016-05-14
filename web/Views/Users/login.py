from web import app, baseurl
from web.Views.Model import Forms
from web.Views.Model.database import Members
from web.Views.Model.SimpleLoginCheck import login_user, logout_user
from web.Views.Model.RegChecks import check_acatvity
from web.Views.Model.SimpleLoginCheck import login_required
from flask import render_template, flash, url_for, redirect


@app.route(baseurl + '/<activity>/login', methods=['GET', "POST"])
def login(activity):
    act = check_acatvity(activity)
    form = Forms.Login()
    if form.validate_on_submit():
        user = Members.query.filter_by(stu_code=form.name.data, activity=act.activity_name).first()
        if user is not None and user.stu_code == form.stucode.data:
            login_user(user)
            if act.upload_enable:
                return redirect(url_for('upload', activity=activity))
            else:
                return redirect(url_for('register_success', activity=activity))

        flash('用户名或密码错误', 'error')
    return render_template('Joins/login.html', form=form, act=act)


@app.route(baseurl + '/<activity>/logout', methods=['GET', "POST"])
@login_required
def logout(activity, current_user, act):
    logout_user(current_user)
    return redirect(url_for('login', activity=activity))

