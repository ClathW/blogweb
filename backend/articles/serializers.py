import re

from rest_framework import serializers
from .models import Article, Category


def markdown_to_summary_text(content):
    text = re.sub(r'```[\s\S]*?```', ' ', content)
    text = re.sub(r'`([^`]*)`', r'\1', text)
    text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'(^|\n)\s{0,3}#{1,6}\s+', r'\1', text)
    text = re.sub(r'(^|\n)\s{0,3}>\s?', r'\1', text)
    text = re.sub(r'(^|\n)\s*[-*+]\s+', r'\1', text)
    text = re.sub(r'(^|\n)\s*\d+\.\s+', r'\1', text)
    text = re.sub(r'[*_~>#-]+', '', text)
    return re.sub(r'\s+', ' ', text).strip()


class CategorySerializer(serializers.ModelSerializer):
    article_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'article_count']

    def get_article_count(self, obj):
        return obj.articles.filter(status='published', is_deleted=False).count()


class ArticleListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True, default='')

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'summary', 'cover_image', 'status',
            'author', 'author_name', 'category', 'category_name',
            'view_count', 'comment_count', 'created_at', 'updated_at',
        ]


class ArticleDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.CharField(source='author.avatar', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True, default='')
    category_id = serializers.IntegerField(source='category.id', read_only=True, default=None)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'summary', 'cover_image', 'status',
            'author', 'author_name', 'author_avatar',
            'category', 'category_id', 'category_name',
            'view_count', 'comment_count', 'is_deleted',
            'created_at', 'updated_at',
        ]


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category']

    def validate_title(self, value):
        if len(value) < 1 or len(value) > 100:
            raise serializers.ValidationError('标题长度须为1-100个字符')
        return value

    def validate_content(self, value):
        if len(value) < 1 or len(value) > 50000:
            raise serializers.ValidationError('正文长度须为1-50000个字符')
        return value

    def validate_category(self, value):
        if value and not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError('所选分类不存在')
        return value

    def create(self, validated_data):
        author = self.context['request'].user
        # 自动生成摘要（从 Markdown 原文提取纯文本）
        summary = markdown_to_summary_text(validated_data.get('content', ''))[:200]
        validated_data['summary'] = summary
        validated_data['author'] = author
        validated_data['status'] = 'published'
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # 更新时重新生成摘要
        if 'content' in validated_data:
            validated_data['summary'] = markdown_to_summary_text(validated_data['content'])[:200]
        return super().update(instance, validated_data)
