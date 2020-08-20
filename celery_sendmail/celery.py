from django.conf import settings
from celery import Celery
import os

# 为celery设置环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.production")
# 创建celery app
app = Celery('celery_sendmail')
# 从单独的配置模块中加载配置
app.config_from_object("celery_sendmail.celeryconfig")
# 设置app自动加载任务
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

