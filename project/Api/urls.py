from django.conf.urls import url

from Api.common import RegistCodeResource,UserResource,SessionResource
# from Api.user import *
# from Api.admin import *
# from Api.customer import *
# from Api.payment_callback import *

from Api.resources import Register
# from Api.view import *
api=Register()

api.regist(RegistCodeResource('regist_code'))
api.regist(UserResource('user'))
api.regist(SessionResource('session'))
# # api.regist(QuestionnaireResource('questionnaire'))
# api.regist(PasswordResource('password'))