from django.shortcuts import render, HttpResponse, redirect
from utils.auth import check_login
from repository import models
from utils.pagination import Pagination
from django.core.urlresolvers import reverse    # from django.urls import reverse
from .forms.articleform import ArticleForm
from .forms.tagform import TagForm
from .forms.userinfo import Userinfo, AvatarForm

from django.db import transaction
from utils.xss import XSSFilter
import json, uuid, os


@check_login
def userinfo(request):
    blog_id = request.session['userinfo']['blog__bid']
    user_id = request.session['userinfo']['uid']
    username = request.session['userinfo']['username']
    email = request.session['userinfo']['email']
    nickname = request.session['userinfo']['nickname']
    blog_title = models.Blog.objects.filter(user_id=user_id).first().title
    blog_site = request.session['userinfo']['blog__site']
    blog_theme = models.Blog.objects.filter(user_id=user_id).first().theme
    blog_motto = models.Blog.objects.filter(user_id=user_id).first().motto
    avatar = models.UserInfo.objects.filter(uid=user_id).first().avatar

    if request.method == 'GET':
        request.session['temp_avatar'] = str(avatar)

        init_dict = {
            'username':username,
            'email':email,
            'nickname':nickname,
            'blog_title':blog_title,
            'blog_site':blog_site,
            'blog_theme':blog_theme,
            'blog_motto':blog_motto,
            # 'avatar':avatar
        }
        # print(1111,init_dict)
        userform = Userinfo(request, data=init_dict)
        avatarform = AvatarForm(request, data={'avatar':avatar})

        return render(request, 'backend/userinfo.html',{'userform':userform, 'avatar':avatar, 'avatarform':avatarform})

    elif request.method == 'POST':
        # print(7, request.session['temp_avatar'])
        dic = {}
        for k,v in request.POST.items():
            dic[k]=v
        dic['avatar'] = request.session.get('temp_avatar')
        # print(77,dic)

        userform = Userinfo(request, data=dic)
        # avatarform = AvatarForm(request, request.POST, request.FILES)
        # print(111, userform.errors)
        # print(222, form.cleaned_data)
        if userform.is_valid():
            # print(222,form.cleaned_data)
            blog_dic={}
            dic2={}
            for k,v in dic.items():
                if 'blog' in k:
                    # print(33,k)
                    keyname = k.split('_')[1]
                    blog_dic[keyname] = dic[k]
                elif 'csrf' in k:
                    pass
                else:
                    dic2[k] = dic[k]
            # print(11,dic2)
            # print(22,blog_dic)


            with transaction.atomic():
                models.UserInfo.objects.filter(uid=user_id).update(**dic2)
                models.Blog.objects.filter(bid=blog_id).update(**blog_dic)

            return redirect('/backend/article-0-0.html')
        return render(request, 'backend/userinfo.html',{'userform':userform, 'avatar':avatar})

@check_login
def upload_avatar(request):
    ret = {'status':False, 'data':None}

    if request.method == 'GET':
      if request.GET.get('retract'):
          request.session['temp_avatar'] = request.GET.get('retract').split('/')[-1]

    elif request.method == 'POST':
        # 更换头像图片
        file_obj = request.FILES.get('avatar')
        if file_obj:
            a = file_obj.name[-4:]
            file_name = str(uuid.uuid4())+a
            file_path = os.path.join('static/imgs/avatar', file_name)
            
            f = open(file_path,'wb')
            for chunk in file_obj.chunks():
                f.write(chunk)
            f.close()
            
            ret['status'] = True
            ret['data'] = file_path
            request.session['temp_avatar'] = file_name
    # print(666,request.session['temp_avatar'])
    return HttpResponse(json.dumps(ret))


@check_login
def article(request, *args, **kwargs):  # article_type_id, tag__tid
    blog_id = request.session['userinfo']['blog__bid']

    search_condition = {}
    for k, v in kwargs.items():
        if v != '0':
            search_condition[k] = v
    # print(55, search_condition)

    tag_list = models.Tag.objects.filter(blog_id=blog_id).all()

    article_type_choices = models.Article.article_type_choices      # [(1, 'python'), (2, 'linux'), (3, 'OpenStack'), (4, 'GoLang')]
    article_type_list = list(map(lambda x:{'nid':x[0],'title':x[1]}, article_type_choices))
    # print(article_type_list)    # [{'nid': 1, 'title': 'python'}, {'nid': 2, 'title': 'linux'}, {'nid': 3, 'title': 'OpenStack'}, {'nid': 4, 'title': 'GoLang'}]

    # article_obj2 = models.Article.objects.filter(blog_id=blog_id, tag__article2tag__).all()
    # print(333,article_obj2)

    article_obj = models.Article.objects.filter(blog_id=blog_id, **search_condition)
    data_count = article_obj.count()
    page_obj = Pagination(request.GET.get('p',1), data_count, per_page_article_num=10,)
    article_list = article_obj.order_by('-create_time')

    article_list2 = []
    for index, article in enumerate(article_list, 1):
        article_dict = {'index':index, 'article':article}
        article_list2.append(article_dict)

    # article_list2 = article_obj.order_by('-aid')[page_obj.start:page_obj.end]
    article_list3 = article_list2[page_obj.start:page_obj.end]

    page_str = page_obj.page_str(reverse('article', kwargs=kwargs))
    kwargs['p'] = page_obj.current_page

    return render(request, 'backend/article.html',
            {
                'article_type_list': article_type_list,
                'data_count': data_count,
                'article_list': article_list,
                'kwargs_dict':kwargs,
                'tag_list': tag_list,
                'page_str': page_str,
                'article_list3': article_list3,
            })

@check_login
def edit_article(request, aid):
    blog_id = request.session['userinfo']['blog__bid']

    if request.method == 'GET':
        article_obj = models.Article.objects.filter(blog_id=blog_id, aid=aid).first()
        if not article_obj:
            return HttpResponse('not Found')
        article_tag = article_obj.tag.values_list('tid')    # <QuerySet [(2,)]>

        if article_tag:
            article_tag = list(zip(*article_tag))[0]

        try:
            content = article_obj.article_detail.content
        except Exception as e:
            return HttpResponse('not Found')

        init_dict = {
            'aid':article_obj.aid,
            'title':article_obj.title,
            'summary':article_obj.summary,
            'content':content,
            'article_type_id':article_obj.article_type_id,
            'tag':article_tag,
        }
        form = ArticleForm(request, data=init_dict)     # 把数据库的内容展现到get页面上
        # print(111,init_dict)

        return render(request, 'backend/edit_article.html', {'form':form, 'aid':aid})

    elif request.method == 'POST':
        form = ArticleForm(request, data=request.POST)
        if form.is_valid():
            article_obj = models.Article.objects.filter(blog_id=blog_id, aid=aid).first()
            if not article_obj:
                return HttpResponse('Not Found')
            with transaction.atomic():
                # print(222222,form.cleaned_data)
                content = form.cleaned_data.pop('content')
                content = XSSFilter().process(content)

                tag = form.cleaned_data.pop('tag')
                # print(777,tag)

                models.Article.objects.filter(aid=article_obj.aid).update(**form.cleaned_data)
                models.Article_detail.objects.filter(article=article_obj).update(content=content)

                models.Article2Tag.objects.filter(article=article_obj).delete()

                tag_list = []
                for tag_id in tag:
                    # tag_list.append(models.Article2Tag.objects.filter(article=article_obj, tag_id=int(tag_id)))    # [<QuerySet []>]，不能用这个，被删了找不到了
                    tag_list.append(models.Article2Tag(article=article_obj, tag_id=int(tag_id)))    # [<Article2Tag: Article2Tag object>, <Article2Tag: Article2Tag object>]
                print(5555,tag_list)
                models.Article2Tag.objects.bulk_create(tag_list)

            return redirect('/backend/article-0-0.html')
        else:
            return render(request, 'backend/edit_article.html', {'form':form, 'aid':aid})

@check_login
def create_article(request):
    blog_id = request.session['userinfo']['blog__bid']

    if request.method == 'GET':
        form = ArticleForm(request)
        return render(request, 'backend/create_article.html', {'form':form})

    elif request.method == 'POST':
        form = ArticleForm(request, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                content = form.cleaned_data.pop('content')
                tag = form.cleaned_data.pop('tag')
                content = XSSFilter().process(content)

                form.cleaned_data['blog_id'] = blog_id
                article_obj = models.Article.objects.create(**form.cleaned_data)
                models.Article_detail.objects.create(article=article_obj, content=content)

                tag_list = []
                for tag_id in tag:
                    tag_id = int(tag_id)
                    tag_list.append(models.Article2Tag(article=article_obj, tag_id=tag_id))
                models.Article2Tag.objects.bulk_create(tag_list)

            return redirect('/backend/article-0-0.html')
        return render(request, 'backend/create_article.html', {'form': form})

@check_login
def delete_article(request):
    result = {'status':False}
    try:
        aid = request.GET.get('aid')
        models.Article.objects.filter(aid=aid).delete()
        result['status'] = True
    except Exception as e:
        pass
    return HttpResponse(json.dumps(result))

@check_login
def tag(request):
    blog_id = request.session['userinfo']['blog__bid']

    tag_obj = models.Tag.objects.filter(blog_id=blog_id)
    tag_list = tag_obj.all()
    tag_count = tag_obj.count()
    # print(111,tag_list)
    page = Pagination(request.GET.get('p',1), tag_count, per_page_article_num=2)

    tag_list2 = []
    for index, tag in enumerate(tag_list,1):
        tag_dict = {'index':index, 'tag':tag}
        tag_list2.append(tag_dict)
    tag_list3 = tag_list2[page.start:page.end]
    page_str = page.page_str(reverse('tag'))

    if request.method == 'GET':
        form = TagForm(request)

        return render(request, 'backend/tag.html',{'tag_list3':tag_list3, 'page_str':page_str, 'form':form})

    elif request.method == 'POST':
        form = TagForm(request, data=request.POST)

        if form.is_valid():
            models.Tag.objects.create(blog_id=blog_id, **form.cleaned_data)

            return redirect('/backend/tag.html')
        return render(request, 'backend/tag.html', {'tag_list3':tag_list3, 'page_str':page_str, 'form':form})

@check_login
def edit_tag(request, tid):
    blog_id = request.session['userinfo']['blog__bid']

    if request.method == 'GET':
        tag_obj = models.Tag.objects.filter(blog_id=blog_id, tid=tid).first()
        if not tag_obj:
            return HttpResponse('Not Found')
        init_dict = {'title': tag_obj.title}

        form = TagForm(request, initial=init_dict)

        return render(request, 'backend/edit_tag.html',{'form':form, 'tid':tid})

    elif request.method == 'POST':
        form = TagForm(request, data=request.POST)

        if form.is_valid():
            models.Tag.objects.filter(blog_id=blog_id,tid=tid).update(**form.cleaned_data)
            return redirect('/backend/tag.html')
        return render(request, 'backend/edit_tag.html', {'form': form, 'tid': tid})

@check_login
def delete_tag(request):
    result = {'status':False}
    try:
        tid = request.GET.get('tid')
        models.Tag.objects.filter(tid=tid).delete()
        result['status'] = True
    except Exception as e:
        pass

    return HttpResponse(json.dumps(result))

