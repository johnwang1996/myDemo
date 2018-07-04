from flask import Flask,render_template
from App.settings import config
from App.extensions import config_extensions
from App.views import config_blueprint

#初始化当期整个应用的函数
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    #给所有第三方扩展库初始化app的函数
    config_extensions(app)
    #注册所有蓝本的函数
    config_blueprint(app)
    errors(app)
    return app


#定制一个捕获错误的函数
def errors(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/error.html',error=e)
    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/error.html', error=e)
