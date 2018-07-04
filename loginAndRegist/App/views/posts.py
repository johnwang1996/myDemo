from flask import Blueprint,render_template,flash,redirect,url_for,jsonify,request
from App.forms import Posts as PostsForm
from flask_login import current_user
from App.models import Posts
from App.extensions import db,file
import os
from .user import *

posts = Blueprint('posts',__name__)


#发表帖子的路由
@posts.route('/send_posts/',methods=['GET','POST'])
def send_posts():
    form= PostsForm()
    
    if form.validate_on_submit():
        if current_user.is_authenticated:
            shuffix = os.path.splitext(form.file.data.filename)[-1]
            #生成随机的图片名
            while True:
                newName = new_name(shuffix)
                if not os.path.exists(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],newName)):
                    break
            file.save(form.file.data,name=newName)
            #判断用户更改头像 原头像是否为默认 不是则将原图片删除
            
            #执行缩放
            img = Image.open(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],newName))
            img.thumbnail((300,300))
            #保存新的图片名称为新的图片的s_newname
            img.save(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],'s_'+newName))


            #拿到真正实例化的user对象
            u = current_user._get_current_object()
            file.save(form.file.data,name=newName)
            p = Posts(selfread=form.selfread.data,content=form.content.data,image=newName,
                user=u,title=form.title.data,director=form.director.data,characters=form.characters.data)
            db.session.add(p)
            flash('电影发表成功!!!')
            return redirect(url_for('main.index'))
        else:
            flash('您还没有登录 请前去登录在发表')
            return redirect(url_for('user.login'))
    return render_template('posts/send_posts.html',form=form)


#收藏 取消收藏
@posts.route('/favorite/<pid>')
def favorite(pid):
    try:
        if current_user.is_favorite(pid):
            print('取消收藏')
            current_user.remove_favorite(pid)
        else:
            print('添加收藏')
            current_user.add_favorite(pid)
        return jsonify({'res':200})
    except:
        return jsonify({'res':500})

@posts.route('/show_posts/<pid>')
def show_posts(pid):
    Post = Posts.query.filter_by(id=pid)[0]
    img=Post.image
    title=Post.title
    content=Post.content
    selfread=Post.selfread
    director=Post.director
    characters=Post.characters
    uid=Post.uid
    postUser=User.query.filter_by(id=uid)[0]
    icon=postUser.icon
    userName=postUser.username
    print(userName)
    # data =showPost.items #返回当前page的所有数据
    # print(pagination)
    return render_template('posts/show_posts.html',
        img=img,selfread=selfread
        ,title=title,content=content,userIcon=icon,username=userName,dirs=director,cha=characters)

# @posts.route('/search_posts/',methods=['POST','GET'])
# def search_posts():
#     if methods=='POST'
@posts.route('/search_posts/',methods=['GET','POST'])
def index():
    return redirect(url_for('posts.search_posts',page=1))

#搜索返回页
@posts.route('/search_posts/<int:page>',methods=['GET','POST'])
def search_posts(page):
    # print('能看到我几次')
    keyword=request.form.get('keyword')
    print(keyword)
    if keyword:
        keyword=str(keyword)
        pagination = Posts.query.filter(Posts.title.contains(keyword)).order_by(Posts.timestamp.desc()).paginate(page,current_app.config['PAGE_NUM'],False)
    else:
        pagination = Posts.query.filter_by(pid=0).order_by(Posts.timestamp.desc()).paginate(page,current_app.config['PAGE_NUM'],False)
        flash('未找到匹配项，您可以查看其他电影')
    data = pagination.items #返回当前page的所有数据
    print(pagination)
    return render_template('posts/search_posts.html',data=data,pagination=pagination,title='搜索结果为',keyword='关键词%s'%(keyword))
