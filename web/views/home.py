from django.shortcuts import render, HttpResponse, redirect
# from django.urls import reverse
from django.core.urlresolvers import reverse
from repository import models
from utils.pagination import Pagination
from django.db.models import Count, QuerySet
import json,re
from utils.xss import XSSFilter
from django.db import transaction


def index(request, *args, **kwargs):
    article_type_list = models.Article.article_type_choices     # [(1, 'python'), (2, 'linux'), (3, 'OpenStack'), (4, 'GoLang')]

    if kwargs:
        article_type_id = int(kwargs['article_type_id'])
        base_url = reverse('index', kwargs=kwargs)              # /article_type/1.html
    else:
        article_type_id = None
        base_url = '/'                                          # /

    data_count = models.Article.objects.filter(**kwargs).count()# 根据文章标签搜索到的数据库里一共存有多少篇该标签下的文章

    page_obj = Pagination(
        request.GET.get('p', 1),
        data_count,
        per_page_article_num=5,
        pager_num=7
    )     # 为了获取start和end

    article_list = models.Article.objects.filter(**kwargs).order_by('-aid')[page_obj.start : page_obj.end]  # 从数据库获取要显示的文章
    # print(111, article_list)

    page_str = page_obj.page_str(base_url)

    return render(request, 'web/index.html',
                  {
                      'article_type_list':article_type_list,
                      'article_type_id':article_type_id,
                      'article_list':article_list,
                      'page_str':page_str,
                   })



def myblog(request, *args, **kwargs):
    # site, condition, val
    # 对应两种链接，一种是点进‘我的博客’首页/superoot.html，一种是分类文章页面/superoot/tag/1.html，/superoot/type/1.html，/superoot/date/2018-06.html

    base_url = reverse('myblog', kwargs=kwargs)

    blog = models.Blog.objects.filter(site=kwargs['site']).select_related('user').first()      # 根据site条件筛选blog和user
    if not blog:
        return redirect('/')

    tag_list = models.Tag.objects.filter(blog=blog).all()   # 找到这个博客下所有文章的标签
    article_type = models.Article.article_type_choices      # 找到所有文章类型

    date_list = models.Article.objects.raw(
        'SELECT aid, COUNT(aid) AS count, strftime("%%Y-%%m", create_time) AS ctime FROM repository_article WHERE blog_id=%s GROUP BY strftime("%%Y-%%m", create_time)',
        params=[blog.bid,]
    )
    '''
        aid    count    ctime
        
    '''

    # date_list = models.Article.objects.extra(
    #     select={"create_date": "strftime('%%Y-%%m',create_time)"}).values_list('aid', 'create_date', )
    # print(555,date_list)        # <RawQuerySet: SELECT aid, COUNT(aid) AS count, strftime("%Y-%m", create_time) AS ctime FROM repository_article WHERE blog_id=1 GROUP BY strftime("%Y-%m", create_time)>
    # for date in date_list:
    #     print(111, date, date.ctime, date.count)    # 找到的是Article，根据Article.ctime才能找到时间，结果：python002 2018-06 7, dfjlakjsdflka 2018-07 1


    #### 页码
    if kwargs.get('condition'):
        if kwargs['condition'] == 'tag':
            article_obj = models.Article.objects.filter(blog=blog, tag=kwargs['val'])
            data_count = article_obj.count()
            article_list = article_obj.order_by('-create_time')
        elif kwargs['condition'] == 'type':
            article_obj = models.Article.objects.filter(blog=blog, article_type_id=kwargs['val'])
            article_list = article_obj.order_by('-create_time')
            data_count = article_obj.count()
        elif kwargs['condition'] == 'date':
            article_obj = models.Article.objects.filter(blog=blog).extra(
                where=['strftime("%%Y-%%m", create_time)=%s'], params=[kwargs['val'],]
            )
            # 相当于：select * from tb where blog_id=1 and strftime('%Y-%m',create_time)=2018-01

            article_list = article_obj.order_by('-create_time')
            data_count = article_obj.count()
        else:
            # article_list = []
            # data_count = models.Article.objects.filter(blog=blog).count()
            # print(111, data_count)
            pass
    else:
        article_list = models.Article.objects.filter(blog=blog).order_by('-create_time')
        data_count = models.Article.objects.filter(blog=blog).count()

    pager_obj = Pagination(request.GET.get('p'), data_count, per_page_article_num=3)
    article_list = article_list[pager_obj.start:pager_obj.end]

    page_str = pager_obj.page_str(base_url)


    #### 关注数，粉丝数
    # fans_count = models.UserInfo.objects.filter(uid=request.session['userinfo']['uid'], fan=3).all()    # 找uid=1，拥有粉丝uid=3的用户
    # fans_count2 = models.UserInfo.objects.filter(uid=request.session['userinfo']['uid'], fans=3).all()  # 找uid=1，且关注了uid=3的用户
    # fans_count = models.UserInfo.objects.filter(fans=1).count()      # 找关注了uid=1的用户(uid=1用户的粉丝)，用这种方式，当去到别人的博客时，显示的粉丝数还是自己的
    # follows_count = models.UserInfo.objects.filter(fan=1).count()
    # print(111, fans_count)

    fans_count = models.UserInfo.objects.filter(blog=blog).first().fan.count()   # 通过博客地址找到博主的粉丝数量
    follows_count = models.UserInfo.objects.filter(blog=blog).first().fans.count()

    return render(request, 'web/myblog.html',
                  {
                      'blog':blog,
                      'tag_list':tag_list,
                      'article_type':article_type,
                      'date_list':date_list,
                      'article_list':article_list,
                      'data_count':data_count,
                      'page_str':page_str,
                      'fans_count':fans_count,
                      'follows_count':follows_count,
                  })


def detail(request, site, aid):
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        return redirect('/')

    tag_list = models.Tag.objects.filter(blog=blog).all()

    article_type = models.Article.article_type_choices

    date_list = models.Article.objects.raw(
        'SELECT aid, COUNT(aid) AS count, strftime("%%Y-%%m", create_time) AS ctime FROM repository_article WHERE blog_id=%s GROUP BY strftime("%%Y-%%m", create_time)',
        params=[blog.bid, ]
    )

    article = models.Article.objects.filter(blog=blog, aid=aid).select_related('article_detail').first()
    fans_count = models.UserInfo.objects.filter(blog=blog).first().fan.count()  # 通过博客地址找到博主的粉丝数量
    follows_count = models.UserInfo.objects.filter(blog=blog).first().fans.count()

    # like_count = models.Like_or_Not.objects.filter(article=article, if_like=1).count()
    # dislike_count = models.Like_or_Not.objects.filter(article=article, if_like=0).count()

    # if_liked = models.Like_or_Not.objects.filter(article=article, commenter_id=request.session['userinfo']['uid']).first()
    # print(111,if_liked.if_like)

    comment_obj = models.Comment.objects.filter(article=article).all()
    # print(111,comment_obj.content)
    # for i in comment_obj:
    #     print(222,i.create_time,)
    comment_list =[]
    for index, comment in enumerate(comment_obj, 1):
        comment_list.append({'index':index, 'comments':comment})
    # print(100,comment_list)

    uid = int()
    if request.session.get('userinfo'):
        uid = request.session['userinfo']['uid']


    if request.method == 'GET':

        return render(request, 'web/article_detail.html',
                      {
                          'blog': blog,
                          'tag_list': tag_list,
                          'article_type': article_type,
                          'date_list': date_list,
                          'article': article,
                          # 'like_count':like_count,
                          # 'dislike_count':dislike_count,
                          'fans_count': fans_count,
                          'follows_count': follows_count,
                          'comment_list': comment_list,
                          'uid': uid,
                          'req': request,
                      })

    elif request.method == 'POST':
        create_dict = {}
        del_dict = {}
        ret = {'msg':None, 'code':100, 'status':False}

        data = request.POST.get('thumbs')

        if not request.session.get('userinfo'):
            ret['code'] = 4001
            ret['msg'] = '请登录后再点赞'
            return HttpResponse(json.dumps(ret))
        else:
            like_obj = models.Like_or_Not.objects.filter(article=article.aid, commenter_id=request.session['userinfo']['uid']).first()
            if not like_obj:
                if data == 'up':
                    ret['msg'] = '点赞'
                    ret['code'] = 2001
                    create_dict = {'article': article, 'commenter_id': request.session['userinfo']['uid'], 'if_like': 1}
                elif data == 'down':
                    ret['msg'] = '点踩'
                    ret['code'] = 2002
                    create_dict = {'article': article, 'commenter_id': request.session['userinfo']['uid'], 'if_like': 0}
            else:
                if like_obj.if_like == 1:
                    if data == 'up':
                        ret['msg'] = '赞过'
                        ret['code'] = 2003
                        del_dict = {'article': article, 'commenter_id': request.session['userinfo']['uid']}
                    elif data == 'down':
                        ret['msg'] = '已经赞过不能踩'
                        ret['code'] = 4002
                elif like_obj.if_like == 0:
                    if data == 'up':
                        ret['msg'] = '已经踩过不能赞'
                        ret['code'] = 4003
                    elif data == 'down':
                        ret['msg'] = '踩过'
                        ret['code'] = 2004
                        del_dict = {'article': article, 'commenter_id': request.session['userinfo']['uid']}

        if create_dict:
            models.Like_or_Not.objects.create(**create_dict)
        elif del_dict:
            models.Like_or_Not.objects.filter(**del_dict).delete()

        return HttpResponse(json.dumps(ret))


from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
def send(request):
    ret = {'status':False}
    if request.method == 'POST':
        html = request.POST.get('html')
        aid = request.POST.get('article')
        uid = request.session['userinfo']['uid']
        reply_id = request.POST.get('reply_id')
        # print(111,reply_id)
        html = XSSFilter().process(html)

        if html:
            create_dict = {'article_id':aid, 'commenter_id':uid}
            if '@' in html:
                a = re.search('\w+',html).group()
                html = html.replace('@ '+a+':','')

                # print(111,a)
                # print(123,b)
                create_dict['content']=html
                create_dict['reply_id'] = reply_id
            else:
                create_dict['content'] = html
            # print(12345,create_dict)

            models.Comment.objects.create(**create_dict)

            ret['status']=True

    return HttpResponse(json.dumps(ret))
