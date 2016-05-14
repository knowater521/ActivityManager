import os
import os.path as op

from flask import render_template, send_file, abort
from flask.ext.admin import Admin
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import  login_required, current_user

from web import app
from web.Model import db


class UserView(ModelView):
    @login_required
    def is_accessible(self):
        if current_user.is_anonymous:
            abort(401)
        return current_user.is_admin()

    column_display_pk = True
    form_columns = ['name', 'stucode', 'admin']

    def __init__(self, session, **kwargs):
        super(UserView, self).__init__(User, session, **kwargs)


class FileView(ModelView):
    def is_accessible(self):
        if current_user.is_anonymous:
            abort(401)
        return current_user.is_admin()

    can_create = False
    can_edit = False
    can_delete = False

    def __init__(self, session, **kwargs):
        super(FileView, self).__init__(Uploads, session, **kwargs)


class FileDownload(FileAdmin):
    def is_accessible(self):
        if current_user.is_anonymous:
            abort(401)
        return current_user.is_admin()

    def __init__(self, place, download_url, **kwargs):
        super(FileDownload, self).__init__(place, download_url, **kwargs)

path = op.join(op.dirname(__file__), 'uploads')
admin = Admin(name='管理面板',template_mode='bootstrap3', url='/upload/admin')
admin.init_app(app)

admin.add_view(UserView(db.session, name='用户管理'))
admin.add_view(FileView(db.session, name='上传列表'))
admin.add_view(FileDownload('uploads/', '/upload/download/', name='文件下载'))


# Old Methods

@app.route('/upload/download/list')
@login_required
def download_list():
    if not current_user.is_admin():
        return render_template('errors/402.html'),401

    x = Uploads.query.all()
    return render_template('download.html',data=x)


@app.route('/upload/download/<filename>')
@login_required
def download_file(filename):
    if not current_user.is_admin():
        return render_template('errors/402.html'),401
    # 判断合法性
    if not User.query.filter_by(user=filename).first():
        abort(404)
    if os.path.exists('./uploads/{}.zip'.format(filename)):
        return send_file('../uploads/{}.zip'.format(filename))
    abort(404)


@app.route('/upload/stulist')
@login_required
def stu_list():
    if not current_user.is_admin():
        return render_template('errors/402.html'),401
    has_uploads = Uploads.query.all()
    has_uploads_usernames = []
    for one in has_uploads:
        has_uploads_usernames.append(one.user)
    all_users = User.query.all()
    res_set = []
    for one in all_users:
        if one.user in has_uploads_usernames:
            res_set.append({'name': one.user, 'has': True})
        else:
            res_set.append({'name': one.user, 'has': False})
    return render_template('stu_list.html',data=res_set)
