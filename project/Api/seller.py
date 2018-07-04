"""
#卖家接口
"""
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
from django.utils import timezone
# from django.utl

from Mymall.models import *
from Api.resources import Resource
from Api.utils import *

from Api.decorators import *

#卖家商品信息
class SellerProductResource(Resource):
    @seller_required
    def get(self,request,*args,**kwargs):
        data=request.GET
        #每页分页限制
        limit=abs(int(data.get('limit',15)))
        #一对多，读取当前所有卖家的所有商品对象
        all_products=request.user.seller.product_set.all()
        # pages=math.ceil(all_products.count()/limit) or 1
        # if page>pages:
        #     page=pages
        # start=(page-1)*
        return json_response({
            'objs':all_products
        })



    @atomic
    @seller_required
    def put(self,request,*args,**kwargs):
        data=request.PUT 
        #错误字典
        errors={}
        #创建商品对象
        product=Product()
        product.seller=request.user.seller
        product.name=data.get('name','商品')
        #商品未分类为0
        product.category_id=data.get('category_id',0)
        product.number=data.get('number',0)
        product.price=data.get('price',-1)
        product.keywords=data.get('keywords','未分类')
        product.describe=data.get('describe','暂无详细描述信息')
        #一开始就存在一个id为1的商品信息模板
        product.product_info=ProductInfo.objects.get(pk=1)
        #创建时间为当前时间
        product.create_date=datetime.now()
        product.save()
        return json_response({
            'id':product.id
        })

    @atomic
    @seller_required
    def post(self,request,*args,**kwargs):
        data=request.POST
        product_id=data.get('product','')
        #商品id为空返回错误
        if not product_id:
            return params_error({
               'product_id':'找不到该商品，或者输入该商品id有误'
        }) 
        product_id=int(product_id)
        product=Product.objects.get(
            id=product_id,seller=request.user.seller
        )
        product.name=data.get('name','商品')
        #商品未分类为0
        product.category_id=data.get('category_id',0)
        product.number=data.get('number',0)
        product.price=data.get('price',-1)
        product.keywords=data.get('keywords','未分类')
        product.describe=data.get('describe','暂无详细描述信息')
        #创建时间为当前时间
        product.create_date=datetime.now()
        product.save()
        return json_response({
            'msg':'更新成功',
            'id':product.id
        })
    @seller_required
    def delete(self,request,*args,**kwargs):
        data=request.DELETE
        product_id=data.get('product_id','')
        if  product_id:
            product=Product.objects.filter(
                id=product_id,seller=request.user.seller
            )
            product.delete()
        else:
           return params_error({
               'product_id':'找不到该商品，或者输入该商品id有误'
        }) 
        return json_response({
            'delete_ids':product_id
        })

#卖家更新商品详细信息
class SellerChangeProductInfo(Resource):
    @atomic
    @seller_required
    def put(self,request,*args,**kwargs):
        data=request.PUT 
        product_id=data.get('product_id','')
        if  not product_id:
            return params_error({
                'msg':'找不到该商品，或者输入该商品id有误'
            })
        #建立商品详细信息对象
        productinfo=ProductInfo()
        productinfo.img=data.get('img','productdefault.jpg')
        productinfo.features=data.get('features','暂无特征描述')
        productinfo.modeltype=data.get('modeltype','暂无详细型号')
        productinfo.displaysize=data.get('displaysize','暂无显示屏尺寸')
        productinfo.dimensions=data.get('dimensions','暂无规格')
        #保存商品信息
        productinfo.save()
        product_id=int(product_id)
        product=Product.objects.filter(
            id=product_id,seller=request.user.seller
        )
        #和一对一商品关联
        product.product_info=productinfo
        return json_response({
            'id':product_id,
            'msg':'创建信息成功'
        })

    @atomic
    @seller_required
    def post(self,request,*args,**kwargs):
        data=request.POST
        product_id=data.get('product_id','')
        if  not product_id:
            return params_error({
                'msg':'找不到该商品，或者输入该商品id有误'
            })
        product_id=int(product_id)
        product=Product.objects.filter(
            id=product_id,seller=request.user.seller
        )
        productinfo=product.product_info
        productinfo.img=data.get('img','productdefault.jpg')
        productinfo.features=data.get('features','暂无特征描述')
        productinfo.modeltype=data.get('modeltype','暂无详细型号')
        productinfo.displaysize=data.get('displaysize','暂无显示屏尺寸')
        productinfo.dimensions=data.get('dimensions','暂无规格')
        #保存商品信息
        productinfo.save()

        return json_response({
            'id':product_id,
            'msg':'更新成功'
        })

    @atomic
    @seller_required
    def get(self,request,*args,**kwargs):
        data=request.GET
        product_id=data.get('product_id','')
        if  not product_id:
            return params_error({
                'msg':'找不到该商品，或者输入该商品id有误'
            })
        product=Product.objects.filter(
            id=product_id,seller=request.user.seller
        )
        productinfo=product.product_info
        #创建一个list存储数据
        data={}
        data['img']=productinfo.getattr('img','productdefault.jpg')
        data['features']=productinfo.get('features','暂无特征描述')
        data['modeltype']=productinfo.get('modeltype','暂无详细型号')
        data['displaysize']=productinfo.get('displaysize','暂无显示屏尺寸')
        data['dimensions']=productinfo.get('dimensions','暂无规格')
        return json_response({
            'data':data
        })