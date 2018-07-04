from App.extensions import db
from datetime import datetime



class Posts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text)
    title=db.Column(db.String(50),default='电影名称')
    pid = db.Column(db.Integer,default=0)
    image = db.Column(db.String(255),default='defaultImage,')
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    uid = db.Column(db.Integer,db.ForeignKey('user.id'))
    characters=db.Column(db.String(255),default='暂无详细演员信息')#演员名称
    director=db.Column(db.String(255),default="暂无详细导演信息")
    selfread=db.Column(db.Text,default="暂无作者观后感")
    # category=db.Column(db.String(255),default='暂未分类')#分类