
from django.conf.urls import url, include
from django.contrib import admin
from backend import views

urlpatterns = [
    url(r'^userinfo.html', views.userinfo),
    url(r'^upload-avatar.html', views.upload_avatar),

    url(r'^article-(?P<article_type_id>\d+)-(?P<tag__tid>\d+).html', views.article, name='article'),
    url(r'^edit-article-(?P<aid>\d+).html', views.edit_article),
    url(r'^create-article.html', views.create_article),
    url(r'^delete-article.html', views.delete_article),

    url(r'^tag.html', views.tag, name='tag'),
    url(r'^edit-tag-(?P<tid>\d+).html', views.edit_tag),
    url(r'^delete-tag.html', views.delete_tag,),

]
