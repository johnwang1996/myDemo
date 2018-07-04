from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,ValidationError,BooleanField,FileField
from wtforms.validators import DataRequired,Email,Length
from App.models import User
# from App.extensions import file


class Login(FlaskForm):
    supername=StringField('用户名',validators=[DataRequired(message='用户名不能为空。。。'),Length(min=6,max=12,message='长度为6-12位')],render_kw={'placeholder':'请输入用户名...','maxlength':12})
    password = PasswordField('密码',validators=[DataRequired(message='密码不能为空'),Length(min=6, max=12, message='长度为6-12位')],render_kw={'placeholder': '请输入密码...', 'maxlength': 12})
    remember = BooleanField('记住我')
    submit = SubmitField('登录')