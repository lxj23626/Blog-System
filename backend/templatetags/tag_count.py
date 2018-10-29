from django import template
from django.utils.safestring import mark_safe
from repository import models

register = template.Library()

@register.simple_tag()
def tag_num(tag):
    article_count = models.Article.objects.filter(tag=tag).count()

    return mark_safe(article_count)