# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('aid', models.AutoField(verbose_name='文章ID', primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='文章标题', max_length=32)),
                ('summary', models.CharField(verbose_name='文章简介', max_length=64)),
                ('read_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('down_count', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(verbose_name='创建文章时间', auto_now_add=True)),
                ('article_type_id', models.IntegerField(default=None, choices=[(1, 'python'), (2, 'linux'), (3, 'OpenStack'), (4, 'GoLang')])),
            ],
        ),
        migrations.CreateModel(
            name='Article2Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('article', models.ForeignKey(verbose_name='文章', to='repository.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Article_detail',
            fields=[
                ('adid', models.AutoField(verbose_name='文章详情ID', primary_key=True, serialize=False)),
                ('content', models.TextField(verbose_name='文章内容')),
                ('article', models.OneToOneField(verbose_name='所属文章', to='repository.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('bid', models.AutoField(verbose_name='博客ID', primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='博客标题', max_length=32)),
                ('site', models.CharField(verbose_name='博客地址', max_length=32, unique=True)),
                ('motto', models.CharField(verbose_name='博客座右铭', max_length=64)),
                ('theme', models.CharField(verbose_name='博客主题', max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('cid', models.AutoField(verbose_name='评论ID', primary_key=True, serialize=False)),
                ('content', models.CharField(verbose_name='评论内容', max_length=255)),
                ('create_time', models.DateTimeField(verbose_name='创建评论时间', auto_now_add=True)),
                ('article', models.ForeignKey(to='repository.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Like_or_Not',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('if_like', models.BooleanField(verbose_name='是否点赞')),
                ('article', models.ForeignKey(verbose_name='文章', to='repository.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='标签名', max_length=16)),
                ('blog', models.ForeignKey(to='repository.Blog')),
            ],
        ),
        migrations.CreateModel(
            name='UserFans',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('uid', models.AutoField(verbose_name='用户ID', primary_key=True, serialize=False)),
                ('username', models.CharField(verbose_name='用户名', max_length=32, unique=True)),
                ('password', models.CharField(verbose_name='密码', max_length=32)),
                ('nickname', models.CharField(verbose_name='昵称', max_length=8)),
                ('email', models.EmailField(verbose_name='邮箱', max_length=254, unique=True)),
                ('avatar', models.ImageField(verbose_name='头像', upload_to='')),
                ('create_time', models.DateField(verbose_name='创建用户时间', auto_now_add=True)),
                ('fan', models.ManyToManyField(verbose_name='粉丝', related_name='fans', to='repository.UserInfo', through='repository.UserFans')),
            ],
        ),
        migrations.AddField(
            model_name='userfans',
            name='follower',
            field=models.ForeignKey(verbose_name='粉丝', related_name='followers', to='repository.UserInfo'),
        ),
        migrations.AddField(
            model_name='userfans',
            name='user',
            field=models.ForeignKey(verbose_name='博主', related_name='users', to='repository.UserInfo'),
        ),
        migrations.AddField(
            model_name='like_or_not',
            name='commenter',
            field=models.ForeignKey(verbose_name='点赞者', to='repository.UserInfo'),
        ),
        migrations.AddField(
            model_name='comment',
            name='commenter',
            field=models.ForeignKey(verbose_name='评论者', to='repository.UserInfo'),
        ),
        migrations.AddField(
            model_name='comment',
            name='reply',
            field=models.ForeignKey(verbose_name='回复评论', blank=True, null=True, related_name='back', to='repository.Comment'),
        ),
        migrations.AddField(
            model_name='blog',
            name='user',
            field=models.OneToOneField(to='repository.UserInfo'),
        ),
        migrations.AddField(
            model_name='article2tag',
            name='tag',
            field=models.ForeignKey(verbose_name='标签', to='repository.Tag'),
        ),
        migrations.AddField(
            model_name='article',
            name='blog',
            field=models.ForeignKey(verbose_name='所属博客', to='repository.Blog'),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(to='repository.Tag', through='repository.Article2Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='userfans',
            unique_together=set([('user', 'follower')]),
        ),
        migrations.AlterUniqueTogether(
            name='like_or_not',
            unique_together=set([('article', 'commenter')]),
        ),
        migrations.AlterUniqueTogether(
            name='article2tag',
            unique_together=set([('article', 'tag')]),
        ),
    ]
