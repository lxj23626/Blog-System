from utils.baseform import BaseForm
from django import forms
from django.forms import fields
from django.core.exceptions import ValidationError
from repository import models


class LoginForm(BaseForm, forms.Form):
    username = fields.CharField(
        error_messages={
            'required': '用户名不能为空',
        }
    )
    
    password = fields.RegexField(
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        min_length= 8,
        max_length= 32,
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码不能小于8个字符',
            'max_length': '密码不能大于32个字符',
            'invalid': '密码必须包含字母，数字和特殊字符',
        }
    )

    rmb = fields.IntegerField(required=False)

    check_code = fields.CharField(
        error_messages={
            'required': '验证码不能为空',
        }
    )
    
    
    def clean_check_code(self):
        if self.request.session.get('CheckCode').upper() != self.cleaned_data.get('check_code').upper():
            raise ValidationError(message='验证码错误')

    def clean_rmb(self):
        if self.cleaned_data.get('rmb', None):
            # print(111,self.cleaned_data.get('rmb', None))
            self.rmb = True
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        userinfo = models.UserInfo.objects.filter(username=username, password=password).values(
            'uid',
            'nickname',
            'username',
            'email',
            'avatar',
            'blog__bid',
            'blog__site'
        ).first()

        if not userinfo:
            raise ValidationError(message='用户名或密码错误')
        self.userinfo = userinfo

        return self.cleaned_data
        