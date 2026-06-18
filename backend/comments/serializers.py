from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='user.username', read_only=True)
    author_avatar = serializers.CharField(source='user.avatar', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'article', 'user', 'author_name', 'author_avatar',
                  'parent', 'replies', 'created_at']
        read_only_fields = ['id', 'user', 'article', 'created_at']

    def get_replies(self, obj):
        if hasattr(obj, 'prefetched_replies'):
            replies = obj.prefetched_replies
        else:
            replies = Comment.objects.filter(parent=obj, is_deleted=False)
        return CommentSerializer(replies, many=True).data


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']

    def validate_content(self, value):
        if len(value) < 1 or len(value) > 1000:
            raise serializers.ValidationError('评论内容长度须为1-1000个字符')
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        article = self.context['article']
        parent = self.context.get('parent')
        validated_data['user'] = user
        validated_data['article'] = article
        validated_data['parent'] = parent
        return super().create(validated_data)


class CommentListSerializer(serializers.ModelSerializer):
    """用于后台管理的评论列表"""
    author_name = serializers.CharField(source='user.username', read_only=True)
    article_title = serializers.CharField(source='article.title', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'author_name', 'article', 'article_title',
                  'is_deleted', 'created_at']
