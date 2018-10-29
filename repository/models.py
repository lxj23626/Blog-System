from django.db import models

# Create your models here.

class UserInfo(models.Model):
    uid = models.AutoField(primary_key=True, verbose_name='用户ID')
    username = models.CharField(max_length=32, verbose_name='用户名', unique=True)
    password = models.CharField(max_length=32, verbose_name='密码')
    nickname = models.CharField(max_length=8, verbose_name='昵称')
    email = models.EmailField(verbose_name='邮箱', unique=True)
    avatar = models.ImageField(verbose_name='头像')
    create_time = models.DateField(verbose_name='创建用户时间', auto_now_add=True)

    # 通过多对多自关联，粉丝可以粉多个明星，所以fan不在UserInfo表中显示，在第三张表UserFans里体现
    fan = models.ManyToManyField(
        to='UserInfo',
        through='UserFans',
        through_fields=('user', 'follower'),
        related_name='fans',
        verbose_name='粉丝'
    )

    def __str__(self):
        return self.username


class UserFans(models.Model):
    '''自建第三张表：互粉表'''
    user = models.ForeignKey(to='UserInfo', to_field='uid', related_name='users', verbose_name='博主')
    follower = models.ForeignKey(to='UserInfo', to_field='uid', related_name='followers', verbose_name='粉丝')

    class Meta:
        unique_together = [
            'user', 'follower',
        ]


class Blog(models.Model):
    bid = models.AutoField(primary_key=True, verbose_name='博客ID')
    title = models.CharField(max_length=32, verbose_name='博客标题')
    site = models.CharField(max_length=32, verbose_name='博客地址', unique=True)
    motto = models.CharField(max_length=64, verbose_name='博客座右铭')
    theme = models.CharField(max_length=16, verbose_name='博客主题')
    user = models.OneToOneField(to='UserInfo', to_field='uid')

    def __str__(self):
        return self.title


class Article(models.Model):
    aid = models.AutoField(primary_key=True, verbose_name='文章ID')
    title = models.CharField(max_length=32, verbose_name='文章标题')
    summary = models.CharField(max_length=64, verbose_name='文章简介')

    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)

    create_time = models.DateTimeField(verbose_name='创建文章时间', auto_now_add=True)
    blog = models.ForeignKey(to='Blog', to_field='bid', verbose_name='所属博客')

    article_type_choices = [
        (1, 'python'),
        (2, 'linux'),
        (3, 'OpenStack'),
        (4, 'GoLang'),
    ]
    article_type_id = models.IntegerField(choices=article_type_choices, default=None)
    tag = models.ManyToManyField(
        to='Tag',
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )

    def __str__(self):
        return self.title


class Tag(models.Model):
    tid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=16, verbose_name='标签名')
    blog = models.ForeignKey(to='Blog', to_field='bid')

    def __str__(self):
        return self.title


class Article2Tag(models.Model):
    '''自定义第三张表'''
    article = models.ForeignKey(to='Article', to_field='aid', verbose_name='文章')
    tag = models.ForeignKey(to='Tag', to_field='tid', verbose_name='标签')

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]


class Article_detail(models.Model):
    adid = models.AutoField(primary_key=True, verbose_name='文章详情ID')
    content = models.TextField(verbose_name='文章内容')
    article = models.OneToOneField(to='Article', to_field='aid', verbose_name='所属文章')

    def __str__(self):
        return '%s_%s' %(self.article.title, 'detail')


class Comment(models.Model):
    cid = models.AutoField(primary_key=True, verbose_name='评论ID')
    commenter = models.ForeignKey(to='UserInfo', to_field='uid', verbose_name='评论者')
    content = models.CharField(max_length=255, verbose_name='评论内容')
    article = models.ForeignKey(to='Article', to_field='aid')

    # 通过一对多自关联，区别在于一条评论只能回复一条原评论，而一个粉丝可以粉多个明星，reply在Comment表显示
    reply = models.ForeignKey(
        to='self',
        to_field='cid',
        related_name='back',
        verbose_name='回复评论',
        null=True,
        blank=True
    )

    create_time = models.DateTimeField(verbose_name='创建评论时间', auto_now_add=True)

    def __str__(self):
        return '%s收到的评论%s' % (self.article, self.cid)


class Like_or_Not(models.Model):
    article = models.ForeignKey(to='Article', to_field='aid', verbose_name='文章')
    commenter = models.ForeignKey(to='UserInfo', to_field='uid', verbose_name='点赞者')
    if_like = models.BooleanField(verbose_name='是否点赞')

    class Meta:
        unique_together = [
            ('article', 'commenter'),
        ]