from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='分类名称')
    description = models.CharField(max_length=200, blank=True, default='', verbose_name='分类描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'categories'
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
        ('taken_down', '已下架'),
        ('archived', '已归档'),
    ]

    title = models.CharField(max_length=100, verbose_name='标题')
    content = models.TextField(max_length=50000, verbose_name='正文')
    summary = models.CharField(max_length=500, blank=True, default='', verbose_name='摘要')
    cover_image = models.URLField(max_length=255, blank=True, default='', verbose_name='封面图片URL')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='articles', verbose_name='分类'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles', verbose_name='作者'
    )
    view_count = models.IntegerField(default=0, verbose_name='浏览次数')
    comment_count = models.IntegerField(default=0, verbose_name='评论数')
    is_deleted = models.BooleanField(default=False, verbose_name='已删除（软删除）')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'articles'
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['category']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.title
