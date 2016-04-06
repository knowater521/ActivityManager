from web import app
from flask import render_template, flash ,redirect ,url_for
from flask_wtf import Form
from wtforms import SubmitField, StringField, PasswordField, validators

from web.database import db, User
from web import custom_validator
from flask.ext.login import LoginManager,login_required,login_user,logout_user,current_user


class RegForm(Form):
    user = StringField('姓名', [validators.required()], description="你的姓名")
    pwd =StringField('学号', [validators.required()], description="你的学号")
    qq=StringField('QQ',[validators.required()],description="留下QQ便于我们联系")
    button = SubmitField('提交')


@app.route('/upload/register', methods=['POST', 'GET'])
def reg():
    if current_user.is_authenticated :
        return redirect(url_for('register_success'))

    form = RegForm()
    if form.validate_on_submit():
        if User.query.filter_by(user=form.user.data).first() is not None:
            flash('您已经报名过辣~')
            return render_template('reg.html', form=form)

        # Make your own custom validator here
        if custom_validator.valid_is_fzu(form.pwd.data, form.user.data) is False:
            flash('您填写的信息不正确/学号姓名不对应')
            return render_template('reg.html', form=form)

        try:
            new_user = User(form.user.data, form.pwd.data, form.qq.data)
            db.session.add(new_user)
            db.session.commit()
        except Exception as err:
            flash(str(err), 'error')

        else:
            login_user(new_user)
            return redirect(url_for('register_success'))

    return render_template('reg.html', form=form)

@app.route('/upload/register_success')
@login_required
def register_success():
    return render_template('regist_success.html',user=current_user.user,stu_id=current_user.pwd)
