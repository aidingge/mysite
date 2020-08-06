from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail


class BlogType(models.Model):
    type_name = models.CharField(max_length=15, verbose_name='分类')

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50, verbose_name='标题')
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE, verbose_name='分类')
    content = RichTextUploadingField(verbose_name='内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_updated_time = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')

    # 返回该博客的作者
    def get_user(self):
        return self.author

    # 获取当前页面链接
    def get_url(self):
        # 根据当前博客反向解析出页面链接 第一个参数当前页面的别名
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    # 获取当前博客作者的Email
    def get_email(self):
        return self.author.email

    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-created_time']
