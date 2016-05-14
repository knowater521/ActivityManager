import os

from flask import render_template, flash
from werkzeug import secure_filename

from web import app, baseurl
from web.Model import Forms
from web.Model.database import UploadHistory, db
from web.Model.SimpleLoginCheck import login_required


@app.route(baseurl + '/<activity>/uploadfile', methods=['POST', 'GET'])
@login_required
def upload(activity, act, current_user):
    form = Forms.UploadFile()
    filename = None
    if form.validate_on_submit():
        ext_name = secure_filename(form.works.data.filename).split('.')[-1]
        filename = "{}_{}_{}.{}".format(act.title, current_user.stu_code, current_user.name, ext_name)
        try:
            directory = 'uploads/{}/'.format(activity)
            if not os.path.exists(directory):
                os.makedirs(directory)

            form.works.data.save(directory + filename)
            file_size = "{0}k".format(os.path.getsize(directory + filename) / 1000)

            data = UploadHistory(current_user.sid, activity, file_size)
            db.session.add(data)
            db.session.commit()
        except Exception as err:
            flash("错误:" + str(err))
        flash("上传成功!", 'info')

    last_time = UploadHistory.query.filter_by(sid=current_user.sid, activity=activity).order_by(UploadHistory.fid.desc()
                                                                                                ).first()

    if not last_time:
        last_time_msg = '还未上传过文件'
    else:
        last_time_msg = '上次上传时间: {0} , 大小: {1}'.format(last_time.time[:-7], last_time.size)

    return render_template('upload.html', user=current_user, form=form, filename=filename, l_s_m=last_time_msg, act=act)

