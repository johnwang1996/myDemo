from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,ValidationError,BooleanField,FileField
from wtforms.validators import DataRequired,Email,Length,EqualTo
from flask_wtf.file import FileAllowed,FileRequired
from App.models import User
from App.extensions import file

class Register(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(message='用户名不能为空...'),Length(min=6,max=12,message='长度为6-12位')],render_kw={'placeholder':'请输入用户名...','maxlength':12})

    password = PasswordField('密码',validators=[DataRequired(message='密码不能为空'),Length(min=6,max=12,message='长度为6-12位'),EqualTo('confirm',message='俩次密码不一致')],render_kw={'placeholder':'请输入密码...','maxlength':12})

    confirm = PasswordField('密码',validators=[DataRequired(message='密码不能为空'),Length(min=6,max=12,message='长度为6-12位')],render_kw={'placeholder':'请输入确认密码...','maxlength':12})

    email = StringField('邮箱',validators=[Email(message='请输入正确的邮箱')],render_kw={'placeholder':'请输入邮箱...','maxlength':30})
    submit = SubmitField('注册')

    #自定义验证器 用户名是否存在
    def validate_username(self,field):
        if User.query.filter(User.username==field.data).first():
            raise ValidationError('该用户已注册!!!')

    #自定义验证器 邮箱是否存在
    def validate_email(self,field):
        if User.query.filter(User.email==field.data).first():
            raise ValidationError('该邮箱已注册!!!')


class Login(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(message='用户名不能为空...'), Length(min=6, max=12, message='长度为6-12位')],render_kw={'placeholder': '请输入用户名...', 'maxlength': 12})
    password = PasswordField('密码',validators=[DataRequired(message='密码不能为空'),Length(min=6, max=12, message='长度为6-12位')],render_kw={'placeholder': '请输入密码...', 'maxlength': 12})
    remember = BooleanField('记住我')
    submit = SubmitField('登录')



#配置更改头像
class Icon(FlaskForm):
    file = FileField('修改头像',validators=[FileAllowed(file,message='只允许上传图片'),FileRequired(message='文件不能为空')])
    submit = SubmitField('上传')
# 修改密码
class Change_password(FlaskForm):
    password = PasswordField('密码',validators=[DataRequired(message='密码不能为空'),Length(min=6,max=12,message='长度为6-12位'),EqualTo('confirm',message='俩次密码不一致')],render_kw={'placeholder':'请输入密码...','maxlength':12})

    confirm = PasswordField('密码',validators=[DataRequired(message='密码不能为空'),Length(min=6,max=12,message='长度为6-12位')],render_kw={'placeholder':'请输入确认密码...','maxlength':12})
    submit = SubmitField('上传')
#修改邮箱
class Change_email(FlaskForm):
    email = StringField('邮箱',validators=[Email(message='请输入正确的邮箱')],render_kw={'placeholder':'请输入邮箱...','maxlength':30})
    submit = SubmitField('上传')