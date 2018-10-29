from django import template
from repository import models
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag()
def like(uid, article):
    like_count = models.Like_or_Not.objects.filter(article=article, if_like=1).count()
    dislike_count = models.Like_or_Not.objects.filter(article=article, if_like=0).count()

    if_clicked = models.Like_or_Not.objects.filter(article=article, commenter_id=uid).first()   # 该用户是否按下了赞或踩的按钮

    if if_clicked:
        if if_clicked.if_like:
            temp = '''
                <div class="up" style="display: inline-block; padding: 5px 15px;border: 1px solid #3ca22c; text-align: center;">
                    <i class="fa fa-thumbs-up fa-3" aria-hidden="true" style="font-size: 25px"></i>
    
                    <div>%s</div>
                </div>
                <div class="down" style="margin: 5px 30px 5px 10px;display: inline-block;padding: 5px 15px;border: 1px solid #dddddd; text-align: center;">
                    <i class="fa fa-thumbs-o-down fa-3" aria-hidden="true" style="font-size: 25px"></i>
    
                    <div>%s</div>
                </div>
            '''%(like_count, dislike_count)
        else:
            temp = '''
                <div class="up" style="display: inline-block; padding: 5px 15px;border: 1px solid #dddddd;text-align: center;">
                    <i class="fa fa-thumbs-o-up fa-3" aria-hidden="true" style="font-size: 25px"></i>

                    <div>%s</div>
                </div>
                <div class="down" style="margin: 5px 30px 5px 10px;display: inline-block;padding: 5px 15px;border: 1px solid red ;text-align: center;">
                    <i class="fa fa-thumbs-down fa-3" aria-hidden="true" style="font-size: 25px"></i>

                    <div>%s</div>
                </div>
            ''' % (like_count, dislike_count)
    else:
        temp = '''
            <div class="up" style="display: inline-block; padding: 5px 15px;border: 1px solid #dddddd; text-align: center;">
                <i class="fa fa-thumbs-o-up fa-3" aria-hidden="true" style="font-size: 25px"></i>

                <div>%s</div>
            </div>
            <div class="down" style="margin: 5px 30px 5px 10px;display: inline-block;padding: 5px 15px;border: 1px solid #dddddd; text-align: center;">
                <i class="fa fa-thumbs-o-down fa-3" aria-hidden="true" style="font-size: 25px"></i>

                <div>%s</div>
            </div>
        '''%(like_count, dislike_count)

    return mark_safe(temp)