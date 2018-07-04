import os
base_path = os.path.abspath(os.path.dirname(__file__))
#所有环境配置的基类
class Config:
    SECRET_KEY = 'jiami'
    #数据库的配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    #邮箱的配置
    MAIL_SERVER =  os.environ.get('MAIL_SERVER','smtp.163.com')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME','13045454530@163.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD','wangyi163')
    #配置上传文件
    MAX_CONTENT_LENGTH = 1024*1024*64
    UPLOADED_PHOTOS_DEST = os.path.join(base_path,'static/upload')

    #配置每页显示数据的条数
    PAGE_NUM = 5

#测试配置
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/testing'

#开发配置
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123@127.0.0.1:3306/hz1802'

#生产配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/development'
#一个配置的字典
config = {
    'development':DevelopmentConfig,
    'production':ProductionConfig,
    'test':TestingConfig,
    'default':DevelopmentConfig
}


