from django.conf import settings
from django.db import models


class Comment(models.Model):
    content = models.TextField(max_length=1000, verbose_name='评论内容')
    article = models.ForeignKey(
        'articles.Article', on_delete=models.CASCADE, related_name='comments', verbose_name='所属文章'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', verbose_name='评论者'
    )
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='父评论'
    )
    is_deleted = models.BooleanField(default=False, verbose_name='已删除（软删除）')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'comments'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['article']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f'{self.user.username}: {self.content[:50]}'
