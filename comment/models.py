from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


# Create your models here.



class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField(verbose_name='评论内容')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    # 这条评论是谁写的
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE, verbose_name='用户')
    # 每条回复的顶级评论是哪条，为了方便获取这条评论下的所有回复
    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    # 回复的是哪条评论，外键指向自己
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE)
    # 指向用户，回复谁
    reply_to = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.CASCADE)

    def get_url(self):
        return self.content_object.get_url()

    def get_user(self):
        return self.user

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']
