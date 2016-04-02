from web import app
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask import abort
import os.path as op

from flask.ext.login import  login_required, current_user
from web.database import db, User, Uploads


class UserView(ModelView):
    @login_required
    def is_accessible(self):
        if current_user.is_anonymous:
            abort(401)
        return current_user.is_admin()

    column_display_pk = True
    form_columns = ['user', 'pwd', 'admin']


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
