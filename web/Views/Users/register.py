from flask import render_template, flash, redirect, url_for, abort
from web.Model import Forms
from web.Model.SimpleLoginCheck import login_required, login_user, is_authenticated
from web.Model.database import db, Members

from web import app
from web import baseurl
from web.Model.RegChecks import check_acatvity, check_user_exist


@app.route(baseurl + '/<activity>/join', methods=['POST', 'GET'])
def reg(activity):
    act = check_acatvity(activity)

    if is_authenticated(activity):
        return redirect(url_for('register_success', activity=activity))

    if act.team_enable:
        form = Forms.RegWithTeam()
    else:
        form = Forms.Reg()

    if form.validate_on_submit():

        if not form.stucode.data.isdigit() or not form.qq.data.isdigit():
            flash('听说学号和QQ是数字组成的')
            return render_template('Joins/reg.html', form=form)

        if len(form.stucode.data) != 9 or len(form.qq.data) < 5 or len(form.phone.data) != 11:
            flash('感觉你填的资料有哪里不大对镜QAQ')
            return render_template('Joins/reg.html', form=form)

        if check_user_exist(form.stucode.data, activity):
            flash('您已经报名过辣~')
            return render_template('Joins/reg.html', form=form)

        # Make your own custom validator here
        # if custom_validator.valid_is_fzu(form.stucode.data, form.name.data) is False:
        #     flash('您填写的信息不正确/学号姓名不对应')
        #     return render_template('reg.html', form=form)

        try:
            new_member = Members(form.name.data, form.stucode.data, form.qq.data, form.phone.data, activity)
            if act.team_enable:
                new_member.team = form.team.data

            db.session.add(new_member)
            db.session.commit()
        except Exception as err:
            flash(str(err), 'error')

        else:
            login_user(new_member)

            return redirect(url_for('register_success', activity=activity))

    return render_template('Joins/reg.html', form=form, act=act)


@app.route(baseurl + '/<activity>/register_success')
@login_required
def register_success(activity, current_user, act):
    return render_template('Joins/regist_success.html', user=current_user, act=act)


@app.route(baseurl + '/<activity>/modify_team', methods=['GET', 'POST'])
@login_required
def modify_team(activity, current_user, act):
    if not act.team_enable:
        abort(404)
    form = Forms.TeamModify()
    if form.validate_on_submit():
        current_user.team = form.team.data
        db.session.commit()
        return redirect(url_for('register_success', activity=activity))
    form.team.data = current_user.team
    return render_template('Joins/modift_team.html', form=form, act=act)
