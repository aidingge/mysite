from django.db import models
import threading
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Create your models here.

# 多线程异步发送通知邮件
class SendMail(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject,
                  '',
                  settings.EMAIL_HOST_USER,
                  [self.email],
                  fail_silently=self.fail_silently,
                  html_message=self.text)


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    # 这条评论是谁写的
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    # 每条回复的顶级评论是哪条，为了方便获取这条评论下的所有回复
    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    # 回复的是哪条评论，外键指向自己
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE)
    # 指向用户，回复谁
    reply_to = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.CASCADE)

    # 评论或回复评论时发送邮件通知用户
    def send_mail(self):
        # 发送邮件通知 判断是评论还是回复  开销大，有停顿，等发送完成之后才执行后面的评论
        if self.parent is None:
            # 评论我的博客
            subject = '有人评论你的博客'
            email = self.content_object.get_email()
            print('email:%s' % email)
        else:
            # 回复评论
            subject = '有人回复你的评论'
            email = self.reply_to.email
        if email != '':
            # 评论内容+博客链接
            context = {}
            context['comment_text'] = self.text
            context['url'] = self.content_object.get_url()
            text = render_to_string('comment/send_mail.html', context)
            # 发送邮件 另一个线程执行
            send_mail = SendMail(subject, text, email)
            send_mail.start()


    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']
