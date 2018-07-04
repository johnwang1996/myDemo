from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Seller(models.Model):
    """
    #卖家信息
    """
    user=models.OneToOneField(User)
    name=models.CharField(default='卖家名称',max_length=32,)
    age = models.IntegerField(default=1, help_text="年龄")
    gender = models.CharField(max_length=8, default="male", help_text="性别")
    email=models.EmailField(default='',null=True,blank=True)
    # store=models.ForeginKey('Store',help_text='店铺')
    phone = models.CharField(default='', max_length=16,
                             blank=True, null=True, help_text="手机号码")
    
    qq = models.CharField(default='', max_length=16,
                          null=True, blank=True, help_text="QQ")
    wechat = models.CharField(
        default='', max_length=64, null=True, blank=True, help_text="微信号")
    
    product=models.ForeignKey('Product',help_text='商品')

    

class Buyer(models.Model):
    """
    #买家用户信息
    """
    user=models.OneToOneField(User)
    name=models.CharField(default='用户名称',max_length=32)
    age = models.IntegerField(default=1, help_text="年龄")
    gender = models.CharField(max_length=8, default="male", help_text="性别")
    email=models.EmailField(default='',null=True,
                            blank=True,)
    birthday =models.CharField(default='暂无详细生日信息',max_length=128)
    # address=models.ForeignKey('Address',help_text="地址，多对一")
    address=models.CharField(default='暂无详细地址',max_length=128,help_text="地址，多对一")

    phone=models.CharField(default='',max_length=16,
                            blank=True,null=True,help_text='电话')
    qq=models.CharField(
        default='',blank=True,max_length=16,null=True,
    )              
    wechat=models.CharField(
        default='',max_length=64,null=True,blank=True,
    ) 
    
    @classmethod
    def create_Buyer(cls,user,**kwargs)         :
        buyer=Buyer.objects.create(user=user,**kwargs)
        wallet=Wallet.objects.create(buyer=buyer,balace=0)

class Order(models.Model):
    """
    #订单
    """
    seller=models.ForeignKey('Seller',help_text='订单')
    buyer=models.ForeignKey('Buyer',help_text='订单')
    address=models.CharField(default='',max_length=128,help_text='地址')
    product_id=models.CharField(default='',max_length=128,help_text='商品id')
    total_moeny=models.FloatField(default=0,help_text='订单价格')


    
class Product(models.Model):
    """
    #商品类
    """
    seller=models.ForeignKey('Seller',help_text='卖家')
    name=models.CharField(default='商品名称',max_length=64)
    category_id=models.CharField(max_length=20)
    number=models.IntegerField(default=0,help_text='商品数量')
    product_info=models.OneToOneField('ProductInfo',help_text='商品详细信息')
    price=models.FloatField(help_text='商品价钱')
    keywords=models.CharField(default='',max_length=20,help_text='搜索关键字')
    describe=models.TextField(default='暂无描述信息',help_text='描述信息')
    create_date=models.DateTimeField(auto_now=True,help_text='发布时间')


class ProductInfo(models.Model):
    """
    #商品详细信息
    """
    # product=models.OneToOneField('Product',help_text='商品类')
    img=models.CharField(max_length=20)
    features=models.TextField(default='暂无特征描述')
    modeltype=models.CharField(default='暂无详细型号',max_length=64)
    displaysize=models.CharField(default='',blank=True,max_length=32,help_text='显示屏尺寸')
    dimensions=models.CharField(default='',max_length=64,help_text='规格')



class Wallet(models.Model):
    """
    #客户钱包
    # """
    buyer=models.OneToOneField('Buyer',help_text='买家用户')
    balance=models.FloatField(default=0,help_text='余额')


    #更新钱包金额
    @classmethod
    def update_wallet(cls,buyer,amount=0,reason='未提供'):
        """
        customer: 客户对象
        amount: 金额变动数量
        """
        #更新金额
        wallet=buyer.wallet
        balance=wallet.balance+amount
        if balance>0:
            wallet.balace=balance
        else:
            return False
        wallet.save()
        #保存历史记录
        WalletFlow.objects.create(wallet=wallet,
                                    amount=amount, reason=reason, direction=True if amount > 0 else False)


class WalletFlow(models.Model):
    """
    #钱包流水明细
    # """
    wallet=models.ForeignKey('Wallet',help_text='钱包')
    amount=models.FloatField(default=0,help_text='差额')
    direction=models.BooleanField(
        default=True,help_text='方向,增加为True,减少为False'
    )
    create_date=models.DateTimeField(auto_now=True, help_text="发生时间")
    reason = models.CharField(max_length=32, help_text="变动原因")
    done = models.BooleanField(default=False, help_text="是否已完成")
    payment = models.CharField(max_length=32, choices=[(
        'alipay', '支付宝'), ('wechat', '微信')], help_text="支付方式")
    paymentid = models.CharField(max_length=128, help_text="第三方支付id")
