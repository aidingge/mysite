from celery_sendmail.celery import app as celery_app  # 导入创建好的celery应用
from django.core.mail import send_mail  # 使用django内置函数发送邮件
from django.conf import settings  # 导入django配置
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from datetime import datetime
from dateutil import rrule
import pytz
from mysite.cache import caches

utc = pytz.UTC
from celery import shared_task


# 添加需要执行的任务，这里是发邮件 注册这个任务 有评论回复和点赞时给用户发邮件
@celery_app.task
def send_mail_task(subject, text, email, fail_silently=False):
    # 使用django内置函数发邮件
    send_mail(subject, '', settings.EMAIL_HOST_USER, [email, ],
              fail_silently=fail_silently, html_message=text)


# 每天检查用户距上次登录时间间隔是不是超过一周了，当用户超过1周没有登录网站时发邮件提醒用户，该阅读博客写博客开始学习了
@shared_task
def send_mail_one_week():
    print('send_mail_one_week start')
    # 使用django内置函数发邮件
    users = User.objects.all()
    email_list = []
    for user in users:
        # 获取当前日期并格式化
        now = datetime.now()
        today = datetime(now.year, now.month, now.day)
        # 获取该用户上次登录的日期
        last = user.last_login
        lastday = datetime(last.year, last.month, last.day)
        # 计算时间差 天数
        days = rrule.rrule(freq=rrule.DAILY, dtstart=lastday, until=today)
        # 分钟时间间隔
        #start_time = last.replace(tzinfo=utc)
        #end_time = now.replace(tzinfo=utc)
        #minutes = (start_time - end_time).seconds
        if days.count() >= 7:
            # 超过7天未登录将邮件加入邮件列表
            email_list.append(user.email)
    # 发送邮件
    subject = "学习提醒"
    msg = "hello~您已经超过7天没有登录博客网站更新博客了哦，最近是不是懒惰了，快快登录博客网站学习吧！\n"
    context = {}
    context['url'] = ''
    context['comment_text'] = msg
    text = render_to_string('comment/send_mail.html', context)

    send_mail(subject, '', settings.EMAIL_HOST_USER, email_list,
              fail_silently=False, html_message=text)
    print('send_mail_one_week end')


# 定时刷新缓存
@shared_task
def flush_cache_fixtime():
    for cache in caches:
        cache.set_cache()

