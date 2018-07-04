from Api.utils import *


# 登录用户必须为卖家,只能在类中使用
def seller_required(func):
    def _wrapper(self,request, *args, **kwarg):
        if not request.user.is_authenticated:
            return not_authenticated()
        user = request.user
        if not hasattr(user, 'seller'):
            return permission_denied()
        return func(self,request, *args, **kwarg)
    return _wrapper


# 登录用户必须为卖家,只能在类中使用
def buyer_required(func):
    def _wrapper(self,request, *args, **kwarg):
        if not request.user.is_authenticated:
            return not_authenticated()
        user = request.user
        if not hasattr(user, 'buyer'):
            return permission_denied()
        return func(self,request, *args, **kwarg)
    return _wrapper

# 登录用户必须为超级用户,只能在类中使用
def superuser_required(func):
    def _wrapper(self,request, *args, **kwarg):
        if not request.user.is_superuser:
            return not_authenticated()
        return func(self,request, *args, **kwarg)
    return _wrapper
