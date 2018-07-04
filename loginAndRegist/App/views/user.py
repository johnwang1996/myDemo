from flask import Blueprint,render_template,flash,redirect,url_for,current_app
from App.models import User
from App.models import Superuser
from App.forms import Register,Login,Icon,Change_email,Change_password
from App.extensions import db,file
from App.email import send_mail
from flask_login import login_user,logout_user,login_required,current_user
import os
from PIL import Image


user = Blueprint('user',__name__)

#注册
@user.route('/register/',methods=['GET','POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        #实例化user模型类
        u = User(username=form.username.data,password=form.password.data,email=form.email.data)
        db.session.add(u)
        db.session.commit()
        #获取刚创建的user的id，并和superuser关联起来
        u=User.query.filter_by(username=form.username.data)[0]
        uid=u.id
        s=Superuser.query.filter_by(id=1)[0]
        s.users.append(u)
        # db.session.add(s)
        db.session.commit()
        #生成token
        token = u.generate_token()
        #发送邮件
        send_mail('邮件激活',form.email.data,'activate', username='zhangsan',token=token)
        #提示用户注册称该
        flash('注册成功请去邮箱中激活')
        #跳转到登录页面
        return redirect(url_for('user.login'))
    return render_template('user/register.html',form=form)

@user.route('/activate/<token>/')
def activate(token):
    if User.check_token(token):
        flash('激活成功 请登录')
        return redirect(url_for('user.login'))
    else:
        flash('激活失败')
        return redirect(url_for('main.index'))


#登录
#加一个时间的验证  如果输入错误超过三次  把激活改为False
@user.route('/login/',methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if not u:
            flash('该用户不存在')
        elif not u.confirm:
            flash('该用户还没激活！！！')
        elif u.check_password_hash(form.password.data):
            flash('登录成功！')
            login_user(u,remember=form.remember.data)
            return redirect(url_for('main.index'))
        else:
            flash('请输入正确的密码')
    return render_template('user/login.html',form=form)

#退出登录
@user.route('/logout/')
def logout():
    logout_user()
    flash('退出成功！')
    return redirect(url_for('main.index'))



"""
@user.route('/test/')
@login_required
def test():
    return '我必须登录以后才能访问'
    #需求  当用户反问了必须登录才能访问的路由的时候  在登录以后自动跳转到上次访问的路由地址
"""
#生成随机的名字的函数
def new_name(shuffix,length=32):
    import string,random
    myStr = string.ascii_letters+'0123456789'
    return ''.join(random.choice(myStr) for i in range(length))+shuffix

#修改头像
@user.route('/change_icon/',methods=['GET','POST'])
def change_icon():
    form = Icon()
    if form.validate_on_submit():
        shuffix = os.path.splitext(form.file.data.filename)[-1]
        #生成随机的图片名
        while True:
            newName = new_name(shuffix)
            if not os.path.exists(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],newName)):
                break
        file.save(form.file.data,name=newName)
        #判断用户更改头像 原头像是否为默认 不是则将原图片删除
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],current_user.icon))

        #执行缩放
        img = Image.open(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],newName))
        img.thumbnail((300,300))
        #保存新的图片名称为新的图片的s_newname
        img.save(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],'s_'+newName))

        current_user.icon = newName
        db.session.add(current_user)
        flash('头像上传成功')
    img_url = file.url(current_user.icon)
    return render_template('user/change_icon.html',form=form,img_url=img_url)
#修改邮箱
@user.route('/change_email/',methods=['GET','POST'])
@login_required
def change_email():
    form = Change_email()
    if form.validate_on_submit():
        newEmail=form.email.data
        #判断新旧邮箱是否想同
        if current_user.email !=newEmail:
            # send_mail('邮件激活',newEmail,'activate', username='zhangsan',token=token)
            current_user.email=newEmail
            db.session.commit()
        else:
            flash('新邮箱不能与就邮箱一致')
            return render_template('user/change_icon.html',form=form)
    return render_template('user/change_email.html',form=form)


@user.route('/change_password/',methods=['GET','POST'])
@login_required
def change_password():
    form = Icon()
    if form.validate_on_submit():
        shuffix = os.path.splitext(form.file.data.filename)[-1]
        #生成随机的图片名
        while True:
            newName = new_name(shuffix)
            if not os.path.exists(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],newName)):
                break
        file.save(form.file.data,name=newName)
        #判断用户更改头像 原头像是否为默认 不是则将原图片删除
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],current_user.icon))

        #执行缩放
        img = Image.open(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],newName))
        img.thumbnail((300,300))
        #保存新的图片名称为新的图片的s_newname
        img.save(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],'s_'+newName))

        current_user.icon = newName
        db.session.add(current_user)
        flash('头像上传成功')
    img_url = file.url(current_user.icon)
    return render_template('user/change_icon.html',form=form,img_url=img_url)