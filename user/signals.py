from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from django.contrib.auth.models import User
from django.urls import reverse

# 消息接收器
# 发送站内通知消息 sender发送者 instance实例（评论） LikeRecord保行为
@receiver(post_save, sender=User)
def send_notification(sender, instance, **kwargs):
    # 注册成功发送站内信 判断是否是第一次创建用户
    if kwargs['created']:
        verb = "注册成功，更多精彩内容等你发现"
        url = reverse('user_info')
        notify.send(instance, recipient=instance, verb=verb, action_object=instance, url=url)
    '''
    其中的参数释义：
    actor：发送通知的对象 写评论/回复的人
    recipient：接收通知的对象 博客作者/回复的评论的作者
    verb：动词短语
    target：链接到动作的对象（可选）
    action_object：执行通知的对象（可选）
    '''

