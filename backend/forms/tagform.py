from django import forms
from django.forms import fields, widgets
from repository import models
from django.core.exceptions import ValidationError

class TagForm(forms.Form):
    title = fields.CharField(
        widget = widgets.TextInput(attrs={'class':'form-control', 'placeholder':'请输入标签名'}),
        error_messages={
            'required':'标签名不能为空'
        }
    )

    def __init__(self, request, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        self.blog_id = request.session['userinfo']['blog__bid']
        self.request = request

    def clean(self):
        v = self.cleaned_data.get('title')
        if models.Tag.objects.filter(blog_id=self.blog_id, title=v).count():
            raise ValidationError(message='标签名已存在')     # 在'__all__'键里
        return self.cleaned_data
        # return v        # 返回获取的值v，自动放入clean_data