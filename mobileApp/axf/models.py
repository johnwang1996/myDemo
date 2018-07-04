from django.db import models

# Create your models here.


class SliderShow(models.Model):
    name=models.CharField(max_length=40)
    img=models.CharField(max_length=200)
    sort=models.IntegerField()
    trackid=models.CharField(max_length=20)
    class Meta:
        db_table="slidershows"

'''
商品表    products
name            商品名
long_name       商品名+规格
product_id      商品id
store_nums      库存
specifics       规格
sort            排序   
market_price    超市价格  
price           价格     
category_id     分组id
child_cid       子组id
img             商品图片
keywords        搜索关键字
brand_id        品牌id
brand_name      品牌名称
safe_day        保质期长度
safe_unit       保质期单位模式
safe_unit_desc  保质期单位 
'''
class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager,self).get_queryset().filter(isDelete=False)

class Product(models.Model):
    objects=ProductManager()
    name=models.CharField(max_length=100)
    long_name=models.CharField(max_length=150)
    product_id=models.CharField(max_length=20)
    store_nums=models.IntegerField()
    specifics=models.CharField(max_length=20)
    sort=models.IntegerField()
    market_price=models.FloatField()
    price=models.FloatField()
    category_id=models.CharField(max_length=20)
    child_cid=models.CharField(max_length=20)
    img=models.CharField(max_length=200)
    keywords=models.CharField(max_length=200)
    brand_name=models.CharField(max_length=200)
    safe_unit=models.CharField(max_length=20)
    safe_unit_desc=models.CharField(max_length=20)
    isDelete=models.BooleanField(default=False)
    class Meta:
        db_table='products'
        