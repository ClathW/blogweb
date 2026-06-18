from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', '普通用户'),
        ('admin', '管理员'),
    ]
    STATUS_CHOICES = [
        ('active', '正常'),
        ('disabled', '已禁用'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name='角色')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name='状态')
    bio = models.TextField(max_length=200, blank=True, default='', verbose_name='个人简介')
    avatar = models.URLField(max_length=255, blank=True, default='', verbose_name='头像URL')

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
