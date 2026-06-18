from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


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
    failed_login_attempts = models.IntegerField(default=0, verbose_name='连续登录失败次数')
    locked_until = models.DateTimeField(null=True, blank=True, verbose_name='锁定至')

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def is_locked(self):
        if self.locked_until and self.locked_until > timezone.now():
            return True
        return False
