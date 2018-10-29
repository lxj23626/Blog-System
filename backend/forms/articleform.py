from django import forms
from django.forms import fields, widgets
from django.core.exceptions import ValidationError
from repository import models

class ArticleForm(forms.Form):
    title = fields.CharField(
        widget = widgets.TextInput(attrs={'class':'form-control', 'placeholder':'文章标题'}),
        error_messages = {
            'required': '文章标题不能为空',
        }
    )

    summary = fields.CharField(
        widget = widgets.Textarea(attrs={'class': 'form-control', 'placeholder': '文章简介', 'rows': '3'}),
        error_messages={
            'required': '文章简介不能为空',
        }
    )

    content = fields.CharField(
        widget = widgets.Textarea(attrs={'class': 'kind-content'}),
        error_messages={
            'required': '文章内容不能为空',
        }
    )

    article_type_id = fields.IntegerField(
        widget = widgets.RadioSelect(choices=models.Article.article_type_choices),
        error_messages={
            'required': '文章分类不能为空',
        }
    )

    tag = fields.MultipleChoiceField(
        choices=[],
        widget = widgets.CheckboxSelectMultiple,
        error_messages={
            'required': '文章标签不能为空',
        }
    )

    def __init__(self, request, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.request = request
        self.blog_id = self.request.session['userinfo']['blog__bid']
        self.fields['tag'].choices = models.Tag.objects.filter(blog_id=self.blog_id).values_list('tid', 'title')










