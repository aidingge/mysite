"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import os
from .base import *


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%k7+phji7t0t)wa1^jq&($th=048v55me(+1%z^&!9q1cq6*sq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',  # 数据库主机
        'PORT': 3306,  # 数据库端口
        'USER': 'hjx',  # 数据库用户名python man
        'PASSWORD': '123456',  # 数据库用户密码
        'NAME': 'mysite_db',  # 数据库名字
    }
}

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # 数据库名字
    }
}
'''

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/


# 发送邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '2465541453@qq.com'
EMAIL_HOST_PASSWORD = 'psqhfoxoraipdifb'  # 授权码
EMAIL_SUBJECT_PREFIX = '[我的博客网站]'
# 这里为False
EMAIL_USE_TLS = False  # 与SMTP服务器通信时，是否启动TLS链接（安全连接）
EMAIL_FROM = '2465541453@qq.com'

