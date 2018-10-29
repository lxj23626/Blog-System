from django import template
from django.utils.safestring import mark_safe
from repository import models

register = template.Library()

@register.simple_tag()
def reply_func(article, reply_id):
    c_obj = models.Comment.objects.filter(article=article, cid=reply_id).first()
    reply_obj = models.UserInfo.objects.filter(uid=c_obj.commenter_id).first().nickname

    return mark_safe(reply_obj)