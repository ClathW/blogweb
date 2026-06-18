from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'article', 'content_preview', 'is_deleted', 'created_at']
    list_filter = ['is_deleted']
    search_fields = ['content']

    def content_preview(self, obj):
        return obj.content[:50]
    content_preview.short_description = '评论内容'
