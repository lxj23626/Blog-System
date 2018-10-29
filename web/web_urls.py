from django.conf.urls import url
from .views import home, account

urlpatterns = [
    url(r'^register.html', account.register),
    url(r'^article_type/(?P<article_type_id>\d+).html', home.index, name='index'),  # 首页
    url(r'^check_code.html$', account.check_code),
    url(r'^login.html', account.login),
    url(r'^logout.html', account.logout),
    url(r'^send.html', home.send),

    url(r'^(?P<site>\w+)/(?P<condition>((tag)|(type)|(date)))/(?P<val>\d+-*\d*).html', home.myblog, name='myblog'),
    url(r'^(?P<site>\w+).html', home.myblog, name='myblog'),
    url(r'^(?P<site>\w+)/(?P<aid>\d+).html', home.detail, name='detail'),

    url(r'', home.index),    # 首页
]
