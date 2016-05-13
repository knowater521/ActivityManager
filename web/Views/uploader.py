import os
import zipfile

from flask import render_template, flash, redirect, url_for
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user


from web import app
from web.Views.Model.database import User, Uploads, db

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "此页需要登录"


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user




@app.route('/upload/uploadfile/', methods=['POST', 'GET'])
@login_required
def upload():
    form = HomeworkForm()
    filename = None
    if form.validate_on_submit():
        if not zipfile.is_zipfile(form.homework.data):
            flash("你上传的不是标准ZIP文件哦~")
        else:
            filename = "{}.zip".format(current_user.user)
            try:
                form.homework.data.save('uploads/' + filename)
                file_size = "{0}m".format(os.path.getsize('uploads/'+filename)/1000000)
                data = Uploads(current_user.user, file_size)
                db.session.add(data)
                db.session.commit()
            except Exception as err:
                flash("错误:" + str(err))
            flash("上传成功!", 'info')

    last_time = Uploads.query.filter_by(user=current_user.user).order_by(Uploads.fid.desc()).first()

    if not last_time:
        last_time_msg = '还未上传过文件'
    else:
        last_time_msg = '上次上传时间: {0} , 大小: {1}'.format(last_time.time[:-7], last_time.size)

    return render_template('upload.html',user=current_user,form=form,filename=filename,l_s_m=last_time_msg)


@app.route('/upload/login', methods=['GET', "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user=form.user.data).first()
        if user is not None and user.pwd == form.pwd.data:
            login_user(user)
            return redirect(url_for('upload'))
        flash('用户名或密码错误', 'error')
    return render_template('login.html',form=form)


@app.route('/upload/logout', methods=['GET', "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

