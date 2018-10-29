from django import template
from django.utils.safestring import mark_safe
from repository import models

register = template.Library()

@register.simple_tag()
def articletype(num, blog):
    article_type_list = models.Article.objects.filter(blog=blog, article_type_id=num).count()

    return mark_safe(article_type_list)