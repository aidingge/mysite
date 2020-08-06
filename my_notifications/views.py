from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from notifications.models import Notification
# Create your views here.
def my_notifications(request):
    context = {}
    return render(request, 'my_notifications.html', context)

def my_notification(request, my_notification_pk):
    # 得到消息通知 将这条通知的状态变为已读并保存
    my_notification = get_object_or_404(Notification, pk=my_notification_pk)
    my_notification.unread = False
    my_notification.save()
    # 跳转到通知的具体url
    return redirect(my_notification.data['url'])


# 删除已读消息
def delete_my_read_notifications(request):
    # 将已读消息找出来，调用delete方法
    notifications = request.user.notifications.read()
    notifications.delete()
    return redirect(reverse('my_notifications'))