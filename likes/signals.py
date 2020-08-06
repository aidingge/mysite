from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from django.utils.html import strip_tags
from .models import LikeRecord

# 消息接收器
# 发送站内通知消息 sender发送者 instance实例（评论） LikeRecord保行为
@receiver(post_save, sender=LikeRecord)
def send_notification(sender, instance, **kwargs):
    # 点赞发送站内消息
    # # 博客/评论被点赞  接受者是博客/评论的作者
    recipient = instance.content_object.get_user()
    url = instance.content_object.get_url()
    verb = ''
    if instance.content_type.model == 'blog':
        # 博客被点赞
        blog = instance.content_object
        verb = '{0}点赞了你的博客《{1}》'.format(instance.user.get_nickname_or_username(), blog.title)
    elif instance.content_type.model == 'comment':
        # 评论被点赞
        comment = instance.content_object
        verb = '{0}点赞了你的评论"{1}"'.format(instance.user.get_nickname_or_username(),
                                        strip_tags(comment.text))
    '''
    其中的参数释义：
    actor：发送通知的对象 写评论/回复的人
    recipient：接收通知的对象 博客作者/回复的评论的作者
    verb：动词短语
    target：链接到动作的对象（可选）
    action_object：执行通知的对象（可选）
    '''
    notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance, url=url)

