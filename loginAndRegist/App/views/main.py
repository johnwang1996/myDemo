from flask import Blueprint,render_template,request,current_app,redirect,url_for
from App.models import Posts,User,Superuser
from App.extensions import cache

main = Blueprint('main',__name__)

@main.route('/')
def index():
    return redirect(url_for('main.page_show',page=1))


@main.route('/page_show/<int:page>/')
# @cache.memoize(timeout=100)
# @cache.cached(timeout=100,key_prefix='index')
def page_show(page):
    print('能看到我几次')
    pagination = Posts.query.filter_by(pid=0).order_by(Posts.timestamp.desc()).paginate(page,current_app.config['PAGE_NUM'],False)
    
    data = pagination.items #返回当前page的所有数据
    print(pagination)
    return render_template('main/index.html',data=data,pagination=pagination)






#测试多对多的使用
@main.route('/test/')
def test():
    print('xxxxx')
    u = User.query.get(1)
    p = Posts.query.get(7)
    #id1用户收藏1号帖子
    # u.favorite.append(p)

    #查看用户1收藏了那些帖子
    # print(u.favorite.all())

    #1号帖子被哪些用户 收藏了
    # print(p.users.all())

    #取消收藏
    # u.favorite.remove(p)
    return '测试'