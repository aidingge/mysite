from datetime import timedelta
from celery.schedules import crontab
import djcelery
# celery 设置
djcelery.setup_loader()
# 设置结果存储
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
# 使用django-celery默认的数据库调度模型
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# 设置代理人broker
BROKER_URL = 'redis://localhost:6379/2'
#导入指定的任务模块
CELERY_IMPORTS = (
    'celery_sendmail.tasks',
)
# 设置定时任务
'''
crontab时间参数设置
crontab()实例化的时候没设置任何参数，都是使用默认值。crontab一共有7个参数，常用有5个参数分别为：
minute：分钟，范围0-59；
hour：小时，范围0-23；
day_of_week：星期几，范围0-6。以星期天为开始，即0为星期天。这个星期几还可以使用英文缩写表示，例如“sun”表示星期天；
day_of_month：每月第几号，范围1-31；
month_of_year：月份，范围1-12。
'''
CELERYBEAT_SCHEDULE = {
    #定时任务1
    'send_mail_one_week': {  # 任务名
        "task": "celery_sendmail.tasks.send_mail_one_week",  # 执行任务的函数
        "schedule": crontab(hour=8, minute=30),  # 每天的8：30检查用户是否超过一周没登录
        "args": (),  # 参数
    },
    # 定时任务2
    'flush_cache_fixtime': {  # 任务名
        "task": "celery_sendmail.tasks.flush_cache_fixtime",  # 执行任务的函数
        "schedule": timedelta(hours=3),  # 每隔3小时刷新一次缓存
        "args": (),  # 参数
    },
}

