import random
import json
import math
from datetime import datetime,timedelta

from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.db.transaction import atomic
from django.db.models import Q
from django.utils import timezone


from Mymall.models import *
from Api.resources import Resource
from Api.utils import *
# from Api.decorators import userinfo_required, customer_required, superuser_required


#获取验证麻
class RegistCodeResource(Resource):
    def get(self,request,*args,**kwargs):
        regist_code=random.randint(1000,10000)
        request.session['regist_code']=regist_code
        return json_response({
            'regist_code':regist_code
        })

#买家信息
class UserResource(Resource):
    #获取用户信息
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            user=request.user
            #判断是否是买家登录身份
            if hasattr(user,'buyer'):
                buyer=user.buyer
                #构建json字典
                data=dict()
                data['user']=user.id
                data['age']=getattr(buyer,'age','')
                data['name']=getattr(buyer,'name','')
                data['gender']=getattr(buyer,'gender','')
                data['phone']=getattr(buyer,'phone','')
                data['address']=getattr(buyer,'address','')
                data['email']=getattr(buyer,'email','')
                data['birthday']=getattr(buyer,'birthday','')
                data['qq'] = getattr(buyer, 'qq', '')
                data['wechat'] = getattr(buyer, 'wechat', '')
                #用json将data转化成字符串，返回给客户端
                return json_response(data)
            elif hasattr(user,'seller'):
                seller=user.seller
                data=dict()
                data['user']=user.id
                data['age']=getattr(seller,'age','')
                data['name']=getattr(seller,'name','')
                data['gender']=getattr(seller,'gender','')
                data['phone']=getattr(seller,'phone','')
                data['qq'] = getattr(seller, 'qq', '')
                data['wechat'] = getattr(seller, 'wechat', '')
                #用json将data转化成字符串，返回给客户端
                return json_response(data)
            else:
                #没有相关用户信息，返回空
                return json_response({})
        #用户为登录，不允许查看信息                
        return not_authenticated()

    #注册用户
    def put(self,request,*args,**kwargs):
        data=request.PUT 
        username=data.get('username','')
        password=data.get('password','')
        regist_code=data.get('regist_code','')
        session_regist_code=request.session.get('regist_code',11111)
        category=data.get('category','buyer')
        ensure_password=data.get('ensure_password','')

        #构建错误信息字典
        errors=dict()
        if not username:
            errors['username'] = '没有提供用户名'
        elif User.objects.filter(username=username):
            errors['username'] = '用户名已存在'
        if len(password) < 6:
            errors['password'] = '密码长度不够'
        if password != ensure_password:
            errors['ensure_password'] = '密码不一样'
        if regist_code != str(session_regist_code):
            errors['regist_code'] = '验证码不对'
        if errors:
            return params_error(errors)

        user=User()
        user.username=username
        #设置密码
        user.set_password(password)
        user.save()

        #根据用户类型创建买家或卖家
        if category=='buyer':
            buyer=Buyer()
            buyer.user=user
            buyer.name='姓名'
            buyer.save()
        else:
            seller=Seller()
            seller.name='卖家名称'
            seller.user=user
            seller.save()
        return json_response({
            'id':user.id
        })

    #更新用户
    def post(self,request,*args,**kwargs):
        data=request.POST
        user=request.user
        if user.is_authenticated:
            #判断是否是买家
            if hasattr(user,'buyer'):
                buyer=user.buyer
                buyer.name = data.get('name', '姓名')
                buyer.age = data.get('age', '')
                buyer.gender = data.get('gender', '')
                buyer.phone = data.get('phone', '')
                buyer.email = data.get('email', '')
                buyer.address = data.get('address', '')
                buyer.birthday = data.get('birthday', '')

                buyer.qq = data.get('qq', '')
                buyer.wechat = data.get('wechat', '')
                buyer.job = data.get('job', '')
                buyer.salary = data.get('salary', '')
                buyer.save()

            elif hasattr(user,'seller'):
                seller = user.seller
                seller.name = data.get('name', '客户名称')
                seller.email = data.get('email', '') 
                seller.address = data.get('address', '')
                seller.phone = data.get('phone', '')
                seller.qq = data.get('qq', '')
                seller.wechat = data.get('wechat', '')    
                seller.save()
            return json_response({
                'msg': '更新成功'
            })
        return not_authenticated()

#用户登录和退出
class SessionResource(Resource):
    #获取登录状态
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return json_response({
                'msg':'已经登陆'
            })
        return not_authenticated()
    #登录
    def put(self,request,*args,**kwargs):
        data=request.PUT 
        username=data.get('username','')
        password=data.get('password','')
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return json_response({
                
                'msg':'登录成功'
            })
        return params_error({
            'msg':'用户名或密码错误'
        })
    #退出
    def delete(self,request,*args,**kwargs):
        logout(request)
        return json_response({
            'msg':'退出成功'
        })


# 密码
class PasswordResource(Resource):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return not_authenticated()
        data = request.POST
        password = data.get('password', '')
        ensure_password = data.get('ensure_password', '')
        error = dict()
        if len(password) < 6:
            error['password'] = "密码长度不小于6位"
        if password != ensure_password:
            error['ensure_password'] = "密码不匹配"
        if error:
            return params_error(error)
        user = request.user
        user.set_password(password)
        user.save()
        login(request, user)
        return json_response({
            "msg": "密码更新成功"
        })