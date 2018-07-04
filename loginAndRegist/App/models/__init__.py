from .user import User
from .posts import Posts
from .superuser import Superuser
from App.extensions import db

#创建一个收藏的中间表
collections = db.Table('collections',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('posts_id',db.Integer,db.ForeignKey('posts.id')))

superanduser = db.Table('superanduser',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('superuser_id',db.Integer,db.ForeignKey('superuser.id')))

