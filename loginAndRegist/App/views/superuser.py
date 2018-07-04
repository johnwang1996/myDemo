from flask import Blueprint,render_template,flash,redirect,url_for,current_app
from App.models import Superuser
from App.forms import Login
from flask_login import login_user,logout_user,login_required,current_user


superuser=Blueprint('superuser',__name__)
#注册
@superuser.route('/register/',methods=['GET','POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        #实例化user模型类
        u = Superuser(username=form.username.data,password=form.password.data)
        db.session.add(u)
        db.session.commit()
        #生成token
        # token = u.generate_token()
        
    return render_template('superuser/login.html',form=form)


#登录
@superuser.route('/adminlogin/',methods=['GET','POST'])
def adminlogin():
    form = Login()
    if form.validate_on_submit():
        u=Superuser.query.filter_by(username=form.username.data)
        if not u:
            flash('管理员不存在')
        elif u.check_password_hash(form.password.data):
            flash('登录成功！')
            login_user(u,remember=form.remember.data)
        else:
            flash('请输入正确的密码')
    return render_template('superuser/login.html',form=form)