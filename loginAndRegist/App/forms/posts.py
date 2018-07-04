from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField,FileField
from wtforms.validators import DataRequired,Length
from flask_wtf.file import FileAllowed,FileRequired
from App.extensions import file
# class Posts(FlaskForm):
#     content = TextAreaField('发表博客',validators=[DataRequired(message='帖子不可以为空'),Length(min=6,max=100,message='帖子内容为6-100个字')],render_kw={'placeholder':'发表你此刻的感想...','style':'resize:none;'})
#     # submit = SubmitField('发表')

class Posts(FlaskForm):
    title = TextAreaField('电影名称',validators=[DataRequired(message='名称不可以为空'),Length(min=1,max=100,message='帖子内容为6-100个字')],render_kw={'placeholder':'请输入电影名称...','style':'resize:none;'})
    #演员名称
    characters=TextAreaField('演员名称',validators=[DataRequired(message='名称不可以为空'),Length(min=1,max=100,message='帖子内容为6-100个字')],render_kw={'placeholder':'请输入演员信息','style':'resize:none;'})
    director=TextAreaField('导演名称',validators=[DataRequired(message='名称不可以为空'),Length(min=1,max=100,message='帖子内容为6-100个字')],render_kw={'placeholder':'请输入导演名字','style':'resize:none;'})
    # category=TextAreaField('电影分类',validators=[DataRequired(message='名称不可以为空'),Length(min=1,max=100,message='帖子内容为6-100个字')],render_kw={'placeholder':'请填写分类，例如','style':'resize:none;'})#分类
    content = TextAreaField('电影简介',validators=[DataRequired(message='内容不可以为空'),Length(min=100,max=200,message='帖子内容为100-200个字')],render_kw={'placeholder':'请输入电影简介...','style':'resize:none;'})
    selfread=TextAreaField('电影观后感',validators=[DataRequired(message='内容不可以为空'),Length(min=100,max=200,message='帖子内容为100-200个字')],render_kw={'placeholder':'发表你此刻的感想...','style':'resize:none;'})
    file = FileField('上传电影海报',validators=[FileAllowed(file,message='只允许上传图片'),FileRequired(message='文件不能为空')])
    submit = SubmitField('上传')