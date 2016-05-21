from web import app
from web import baseurl
from flask import render_template, flash, request, session, redirect, url_for, send_file
from ...Model.database import db, Activities, Members, UploadHistory, Admins
from ...Model import Forms
from ...Model.SimpleLoginCheck import admin_required
import xlwt
from io import BytesIO as StringIO


@app.route(baseurl + '/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = Forms.LoginAdmin()
    if form.validate_on_submit():
        user = Admins.query.filter_by(user=form.user.data).first()
        if user is not None and user.passwd == form.passwd.data:
            session['isadmin'] = True
            return redirect(url_for('admin_home'))
        flash('用户名或密码错误')
    return render_template('admin/login.html',form=form)


@app.route(baseurl + '/admin/home')
@admin_required
def admin_home():
    acts = Activities.query.order_by(Activities.rank).all()
    return render_template('admin/activities_list.html', activites=acts)


@app.route(baseurl + '/admin/edit_act/<activity>', methods=['GET', 'POST'])
@admin_required
def edit_activity(activity):
    act = Activities.query.filter_by(activity_name=activity).first()
    form = Forms.ActModify()

    if form.validate_on_submit():
        try:
            act.activity_name = form.name.data
            act.title = form.title.data
            act.team_enable = form.team_enable.data
            act.upload_enable = form.upload_enable.data
            act.reg_enable = form.reg_enable.data
            act.note = form.note.data
            act.rank = form.rank.data
            db.session.commit()
            flash("更新成功")
        except Exception as err:
            flash("失败  {}".format(str(err)))
    else:
        form.name.data = act.activity_name
        form.title.data = act.title
        form.team_enable.data = act.team_enable
        form.upload_enable.data = act.upload_enable
        form.reg_enable.data = act.reg_enable
        form.note.data = act.note
        form.rank.data = act.rank
    return render_template('admin/act_modify.html', form=form, act_name=act.title)


@app.route(baseurl + '/admin/add_act', methods=['GET', 'POST'])
@admin_required
def add_activity():
    form = Forms.ActModify()

    if form.validate_on_submit():
        try:
            act = Activities(form.name.data, form.title.data, form.reg_enable.data, form.team_enable.data,
                             form.upload_enable.data, form.note.data, form.rank.data)
            db.session.add(act)
            db.session.commit()
            flash("添加成功")
        except Exception as err:
            flash("失败  {}".format(str(err)))
    return render_template('admin/act_modify.html', form=form, act_name="(新增)")


@app.route(baseurl + '/admin/memberlist')
@admin_required
def memberlist():
    act_name = request.args.get('act')
    form = Forms.ActChosen()
    form.csrf_enabled = False
    if act_name:
        members = Members.query.order_by(Members.stu_code).filter_by(activity=act_name).all()
        form.act.data = act_name
    else:
        form.act.data = ''
        members = Members.query.order_by(Members.stu_code).all()
    return render_template('admin/member_list.html', form=form, member=members)


@app.route(baseurl + '/admin/submitlist')
@admin_required
def submitlist():
    act_name = request.args.get('act')
    form = Forms.ActChosen()
    form.csrf_enabled = False
    if act_name:
        his = UploadHistory.query.outerjoin(Members).add_columns(Members.name, Members.stu_code).filter_by(activity=act_name).all()
        form.act.data = act_name
    else:
        form.act.data = ''
        his = UploadHistory.query.outerjoin(Members).add_columns(Members.name, Members.stu_code).all()
    return render_template('admin/upload_history.html', data=his, form=form)


@app.route(baseurl + '/admin/logout')
@admin_required
def logout_admin():
    session.clear()
    return redirect((url_for('index')))


@app.route(baseurl + '/admin/export')
@admin_required
def generate_excel():
    act_name = request.args.get('act')
    if act_name:
        members = Members.query.filter_by(activity=act_name).all()
    else:
        members = Members.query.all()
        act_name = 'All'

    file = xlwt.Workbook()
    table = file.add_sheet(act_name)
    titleRow = ['姓名', '学号', 'qq', 'phone', '团队', '活动']
    for col in range(0, 6):
        table.write(0, col, titleRow[col])
    row = 0
    for person in members:
        row += 1
        table.write(row, 0, person.name)
        table.write(row, 1, person.stu_code)
        table.write(row, 2, person.qq)
        table.write(row, 3, person.phone)
        table.write(row, 4, person.team)
        table.write(row, 5, person.activity)

    sio = StringIO()
    file.save(sio)
    sio.seek(0)
    return send_file(sio,
                     attachment_filename="{}.xls".format(act_name),
                     as_attachment=True)


