from django import forms
from django.forms import fields, widgets
from repository import models


class Userinfo(forms.Form):
    username = fields.CharField(
        # label='用户名',
        widget = widgets.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名', 'readonly':'readonly'}),
        error_messages={
            'required':'用户名不能为空',
        }
    )

    email = fields.EmailField(
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}),

        error_messages={
            'required':'邮箱不能为空',
        }
    )

    nickname = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入昵称'}),

        required=False,
        error_messages={}
    )

    blog_title = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入博客名'}),

        required=False
    )

    blog_site = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入博客地址', 'readonly':'readonly'}),

        required=False
    )

    blog_theme = fields.CharField(
        widget=widgets.Select(attrs={'class': 'form-control',}, choices=((1,'主题1'),(2,'主题2')),),

        required=False
    )

    blog_motto = fields.CharField(
        widget = widgets.Textarea(attrs={'class':'form-control', 'placeholder':'来一杯鸡汤。。。'}),
    )

    avatar = fields.CharField(
        # required=False
    )

    def __init__(self, request, *args, **kwargs):
        super(Userinfo,self).__init__(*args, **kwargs)
        self.request = request



class AvatarForm(forms.Form):
    avatar = fields.FileField(
        widget = widgets.FileInput(attrs={'id':'avatarImg',}),
        # required=False
    )

    def __init__(self, request, *args, **kwargs):
        super(AvatarForm,self).__init__(*args, **kwargs)
        self.request = request
        # self.fields['avatar'].widget.choices = models.UserInfo.objects.values_list('avatar')
