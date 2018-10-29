from django import forms as django_forms
from django.forms import fields
from django.core.exceptions import ValidationError

from repository import models
from utils.baseform import BaseForm



class RegisterForm(BaseForm, django_forms.Form):
    username = fields.CharField(
        # required= False,
        error_messages={
            'required':'用户名不能为空',
        }
    )

    email = fields.EmailField(
        error_messages={
            'required':'邮箱不能为空',
            'invalid':'邮箱格式不正确',
        }
    )
    
    password = fields.RegexField(
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        min_length=8,
        max_length=32,
        error_messages={
            'required':'密码不能为空',
            'invalid':'密码必须包含字母，数字，特殊字符',
            'min_length':"密码长度不能小于8个字符",
            'max_length':"密码长度不能大于32个字符",
        }
    )

    second_password = fields.RegexField(
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        min_length=8,
        max_length=32,
        error_messages={
            'required': '确认密码不能为空',
            'invalid': '确认密码必须包含字母，数字，特殊字符',
            'min_length': "确认密码长度不能小于8个字符",
            'max_length': "确认密码长度不能大于32个字符",
        }
    )

    check_code = fields.CharField(
        error_messages={
            'required':'验证码不能为空'
        }
    )


    def clean_username(self):
        v = self.cleaned_data.get('username')       # self.cleaned_data其实就是self.request.POST
        user_count = models.UserInfo.objects.filter(username=v).count()
        if user_count:
            raise ValidationError(message='用户名已存在')
        return v
    
    def clean_check_code(self):
        # if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
        if self.request.session.get('CheckCode').upper() != self.cleaned_data.get('check_code').upper():
            raise ValidationError(message='验证码错误', code='invalid')

    def clean(self):
        password = self.cleaned_data.get('password')
        sec_password = self.cleaned_data.get('second_password')

        if password != sec_password:
            raise ValidationError('两次密码不一致')
        return self.cleaned_data

            