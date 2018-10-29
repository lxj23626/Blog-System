from django import template
from django.core.urlresolvers import reverse        # from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def article_type_all(kwargs_dict):
    article_type_id = kwargs_dict['article_type_id']
    tag__tid = kwargs_dict['tag__tid']
    # p = kwargs_dict['p']

    url = reverse('article', kwargs={'article_type_id':0, 'tag__tid':tag__tid})
    # print(1111,url)

    if article_type_id == '0':
        # temp = '<a href="%s?p=%s"><button class="btn btn-md btn-primary" type="submit">全部1</button></a>'%(url,p)  # 必须要a标签包含button标签才能跳转
        temp = '<a class="btn btn-primary btn-md" href="%s?p=%s">全部</a>'%(url,1)
    else:
        # temp = '<button class="btn btn-md" type="submit"><a href="%s?p=%s">全部1</a></button>'%(url,p)
        temp = '<a class="btn btn-md" href="%s?p=%s">全部</a>'%(url,1)

    return mark_safe(temp)

@register.simple_tag
def article_type_combine(article_type_list, kwargs_dict):
    li = []
    article_type_id = kwargs_dict['article_type_id']
    tag__tid = kwargs_dict['tag__tid']
    # p = kwargs_dict['p']

    for obj in article_type_list:   # [{'nid': 1, 'title': 'python'}, {'nid': 2, 'title': 'linux'}, {'nid': 3, 'title': 'OpenStack'}, {'nid': 4, 'title': 'GoLang'}]
        url = reverse('article',kwargs={'article_type_id':obj['nid'], 'tag__tid':tag__tid})

        if obj['nid'] == int(article_type_id):
            temp = '<div class="col-xs-1" style="text-align: center;"><a href="%s?p=%s"><button class="btn btn-md btn-primary" type="submit">%s</button></a></div>'%(url,1,obj['title'])
        else:
            temp = '<div class="col-xs-1" style="text-align: center;"><a href="%s?p=%s"><button class="btn btn-md" type="submit">%s</button></a></div>'%(url,1,obj['title'])

        li.append(temp)

    return mark_safe(''.join(li))


@register.simple_tag()
def tag_all(kwargs_dict):
    article_type_id = kwargs_dict['article_type_id']
    tag__tid = kwargs_dict['tag__tid']
    # p = kwargs_dict['p']

    url = reverse('article', kwargs={'article_type_id': article_type_id, 'tag__tid':0})

    if tag__tid == '0':
        temp = '<a class="btn btn-primary btn-md" href="%s?p=%s">全部</a>'%(url,1)
    else:
        temp = '<a class="btn btn-md" href="%s?p=%s">全部</a>'%(url,1)

    return mark_safe(temp)


@register.simple_tag()
def tag_combine(tag_list, kwargs_dict):
    li = []
    article_type_id = kwargs_dict['article_type_id']
    tag__tid = kwargs_dict['tag__tid']
    # p = kwargs_dict['p']

    # print(999,tag_list)
    for obj in tag_list:
        url = reverse('article', kwargs={'article_type_id': article_type_id, 'tag__tid':obj.tid})

        if obj.tid == int(tag__tid):
            temp = '<div class="col-xs-1" style="text-align: center;"><a href="%s?p=%s"><button class="btn btn-md btn-primary" type="submit">%s</button></a></div>'%(url,1,obj.title)
        else:
            temp = '<div class="col-xs-1" style="text-align: center;"><a href="%s?p=%s"><button class="btn btn-md" type="submit">%s</button></a></div>'%(url,1,obj.title)

        li.append(temp)
        # print('aa: ',''.join(li))
    return mark_safe(''.join(li))
