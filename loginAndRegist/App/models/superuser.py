from App.extensions import db
from werkzeug.security import generate_password_hash,check_password_hash
#生成tooken模块
from itsdangerous import TimedJSONWebSignatureSerializer as Seralize 
from flask import current_app
from flask_login import UserMixin
from App.extensions import login_manager
from .posts import Posts
from .user import User

class Superuser(UserMixin,db.Model):
    __table__name='superuser'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(12),index=True)
    password_hash=db.Column(db.String(128))
    '''
    参数1模型名称。参数2 反响引用字段名称，参数3,加载方式，提供对象
    '''
    # users =db.relationship('User'，backref='stu111', lazy=True)
    # users = db.relationship('User',backref='superuser',lazy='dynamic')
    # uid = db.relationship('User',secondary='superanduser',backref=db.backref('superuser',lazy='dynamic'),lazy='dynamic')

    users = db.relationship('User',backref='superuser',lazy='dynamic')
    icon=db.Column(db.String(70),default='admin.jpg')
    

    #生成token的方法

    def generate_token(self):
        s = Seralize(current_app.config['SECRET_KEY'])
        return s.dumps({'id':self.id})
    @staticmethod
    def check_token(token):
        s=Seralize(current_app.config['SECRET_KEY'])
        #从当前token中拿出字典
        try:
            id=s.loads(token)['id']
        except:
            return False
        s=Superuser.query.get(id)
        if not s:
            return False
    def check_password_hash(self,password):
        return check_password_hash(self.password_hash,password)
    #定义一个删除电影的方法
    def remove_posts(self,pid):
        post=Posts.query.get(id=pid)
        if not post:
            return False
        #如果存在该电影信息
        #1.判断是否有user收藏该电影，将该post剔除收藏的posts
        # User.query.filter_by()
        # Users=User.query.filter(favorite.id=pid)
        # for i in users:
        db.session.delete(post)
        db.session.commit()

        #2.删除user关联的posts
        
        

#登录认证的回调  保持数据的一致性
@login_manager.user_loader
def user_loader(uid):
    return User.query.get(int(uid))         


