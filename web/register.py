from web import app
from flask import render_template, flash
from flask_wtf import Form
from wtforms import SubmitField, StringField, PasswordField, validators

from web.database import db, User
from web import custom_validator


class RegForm(Form):
    user = StringField('姓名', [validators.required()], description="你的姓名")
    pwd = PasswordField('学号', [validators.required()], description="你的学号")
    button = SubmitField('提交')


@app.route('/upload/register', methods=['POST', 'GET'])
def reg():
    form = RegForm()
    if form.validate_on_submit():
        if User.query.filter_by(user=form.user.data).first() is not None:
            flash('您已经报名过辣~')
            return render_template('reg.html', form=form)

        # Make your own custom validator here
        if custom_validator.valid_is_fzu(form.pwd.data, form.user.data) is False:
            flash('您填写的信息不正确')
            return render_template('reg.html', form=form)

        try:
            new_user = User(form.user.data, form.pwd.data)
            db.session.add(new_user)
            db.session.commit()
        except Exception as err:
            flash(str(err), 'error')

        else:
            flash("报名成功!", 'info')

    return render_template('reg.html', form=form)

