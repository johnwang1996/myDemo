from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager #处理用户登录的模块
from flask_uploads import UploadSet,IMAGES,patch_request_class,configure_uploads
from flask_moment import Moment
#导入缓存模块
from flask_cache import Cache

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate(db=db)
mail = Mail()
login_manager = LoginManager()
file = UploadSet('photos',IMAGES)
moment = Moment()
#simple 简单的缓存
# cache = Cache(config={"CACHE_TYPE":"simple"})
#使用redis进行缓存
cache = Cache(config={"CACHE_TYPE":"redis"})

#初始化当期整个应用的函数
def config_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app=app)
    mail.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    cache.init_app(app=app)

    #需要指定登录端点
    login_manager.login_view = 'user.login'
    #提示信息
    login_manager.login_message = '请登录在访问'
    #设置当前session的保护级别 basic最基础的 None没有 strong最强的 如果当期登录有任何异常 都会自动退出登录
    login_manager.session_protection = 'strong'
    #配置文件上传
    configure_uploads(app,file)
    patch_request_class(app,size=None)