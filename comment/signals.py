import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from .models import Comment
from celery_sendmail.tasks import send_mail_task  # 导入celery任务

# 消息接收器
# 发送站内通知消息 sender发送者 instance实例（评论）
@receiver(post_save, sender=Comment)
def send_notification(sender, instance, **kwargs):
    # 发送站内消息
    if instance.reply_to is None:
        # 评论
        recipient = instance.content_object.get_user()
        if instance.content_type.model == 'blog':
            blog = instance.content_object
            verb = '{0} 评论了你的《{1}》'.format(instance.user.get_nickname_or_username(), blog.title)
        else:
            raise Exception('unknown comment object type')
    else:
        # 回复
        recipient = instance.reply_to
        verb = '{0}回复了你的评论"{1}"'.format(instance.user.get_nickname_or_username(),
                                        strip_tags(instance.parent.text))
        # instance.content_object评论的具体实体
    url = instance.content_object.get_url()+"#comment_"+str(instance.pk)
    '''
    其中的参数释义：
    actor：发送通知的对象 写评论/回复的人
    recipient：接收通知的对象 博客作者/回复的评论的作者
    verb：动词短语
    target：链接到动作的对象（可选）
    action_object：执行通知的对象（可选）
    '''
    notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance, url=url)


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


# 当有博客保存时，就通知这个接收器执行该方法
@receiver(post_save, sender=Comment)
def send_mail(sender, instance, **kwargs):
    # 发送邮件通知
    # 发送邮件通知 判断是评论还是回复  开销大，有停顿，等发送完成之后才执行后面的评论
    if instance.parent is None:
        # 评论我的博客
        subject = '有人评论你的博客'
        email = instance.content_object.get_email()
        print('email:%s' % email)
    else:
        # 回复评论
        subject = '有人回复你的评论'
        email = instance.reply_to.email
    if email != '':
        # 评论内容+博客链接
        context = {}
        context['comment_text'] = instance.text
        context['url'] = instance.content_object.get_url()
        text = render_to_string('comment/send_mail.html', context)
        # 发送邮件 另一个线程执行
        '''
        send_mail = SendMail(subject, text, email)
        send_mail.start()
        '''
        # 使用delay异步调用发邮件的任务
        send_mail_task.delay(subject, text, email)
        print('celery异步发送邮件成功：%s' + text)

