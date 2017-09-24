from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField, StringField, validators, TextAreaField, BooleanField, SelectField, IntegerField, PasswordField
from .database import Activities


class Reg(Form):
    name = StringField('姓名', [validators.required()], description="你的姓名")
    stucode = StringField('学号', [validators.required()], description="你的学号")
    qq = StringField('QQ', [validators.required()], description="留下QQ便于我们联系")
    phone = StringField('手机', [validators.required()], description="我们将用短信通知您最新信息!")
    button = SubmitField('提交')


class RegWithTeam(Form):
    name = StringField('组长姓名', [validators.required()], description="你的姓名")
    stucode = StringField('组长学号', [validators.required()], description="你的学号")
    qq = StringField('组长QQ', [validators.required()], description="留下QQ便于我们联系")
    phone = StringField('组长手机', [validators.required()], description="我们将用短信通知您最新信息!")
    team = TextAreaField('队员信息', description="组队参加请按照\"姓名 学号\"一人一行填写在文本框内 如: 王尼玛 22150xxxx")
    button = SubmitField('提交')


class UploadFile(Form):
    works = FileField('你的作品', validators=[
        FileRequired(message='请选择文件'),
        FileAllowed(['zip', 'rar'], '请使用zip或rar压缩格式提交'),
    ],        
    description="文件请打包压缩后上传，推荐使用ZIP格式～～")
    button = SubmitField('提交')


class Login(Form):
    name = StringField('姓名', [validators.required()], description="就是你的名字")
    stucode = StringField('学号', [validators.required()], description="学号")
    button = SubmitField('提交')


class TeamModify(Form):
    team = TextAreaField('队员信息', description="组队参加请按照\"姓名 学号\"一人一行填写在文本框内 如: 王尼玛 22150xxxx")
    button = SubmitField('提交')


class ActModify(Form):
    name = StringField('活动名(网址)', [validators.required()], description="建议英文")
    title = StringField('活动Title', [validators.required()], description="显示标题")
    note = TextAreaField('Note', description="显示于活动页下方")
    rank = IntegerField('排序', [validators.NumberRange(min=0, max=10)], description="0在最上面")
    reg_enable = BooleanField('开放报名')
    team_enable = BooleanField('允许组队')
    upload_enable = BooleanField('开放上传')
    hide = BooleanField('隐藏显示')
    button = SubmitField('提交')

def getChoices():
    return list((o.activity_name, o.activity_name) for o in Activities.query.all())

class ActChosen(Form):
    act = SelectField('活动', choices=[])
    button = SubmitField('提交')


class LoginAdmin(Form):
    user = StringField('用户名', [validators.required()])
    passwd = PasswordField('密码', [validators.required()])
    button = SubmitField('提交')
