from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.shortcuts import get_object_or_404

from config.pagination import paginate_queryset, parse_pagination
from users.permissions import IsActiveAdmin, IsActiveAuthenticated
from .models import Article, Category
from .serializers import (
    ArticleCreateSerializer,
    ArticleDetailSerializer,
    ArticleListSerializer,
    CategorySerializer,
)


class CategoryListView(APIView):
    """文章分类列表"""
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ArticleListView(APIView):
    """文章列表（分页 + 分类筛选）"""
    permission_classes = [AllowAny]

    def get(self, request):
        page, page_size = parse_pagination(request.query_params)
        category_id = request.query_params.get('category')

        queryset = Article.objects.filter(status='published', is_deleted=False)

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        articles, pagination = paginate_queryset(queryset, page, page_size)

        serializer = ArticleListSerializer(articles, many=True)
        return Response({**pagination, 'results': serializer.data})


class ArticleDetailView(APIView):
    """文章详情"""
    permission_classes = [AllowAny]

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk, status='published', is_deleted=False)
        # 增加浏览次数
        article.view_count += 1
        article.save(update_fields=['view_count'])
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)


class ArticleCreateView(APIView):
    """发布文章"""
    permission_classes = [IsActiveAuthenticated]

    def post(self, request):
        serializer = ArticleCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            article = serializer.save()
            return Response({
                'message': '文章发布成功',
                'article': ArticleDetailSerializer(article).data,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': '文章发布失败',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


class ArticleEditView(APIView):
    """编辑与删除文章（作者或管理员）"""
    permission_classes = [IsActiveAuthenticated]

    def _check_permission(self, article, user):
        return user == article.author or user.role == 'admin'

    def put(self, request, pk):
        article = get_object_or_404(Article, pk=pk, is_deleted=False)
        if not self._check_permission(article, request.user):
            return Response({'message': '无权编辑此文章'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ArticleCreateSerializer(article, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            article = serializer.save()
            return Response({
                'message': '文章更新成功',
                'article': ArticleDetailSerializer(article).data,
            })
        return Response({
            'message': '请求参数有误',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk, is_deleted=False)
        if not self._check_permission(article, request.user):
            return Response({'message': '无权删除此文章'}, status=status.HTTP_403_FORBIDDEN)

        article.is_deleted = True
        article.save(update_fields=['is_deleted'])
        return Response({'message': '文章已删除'})


class MyArticlesView(APIView):
    """当前用户的文章列表"""
    permission_classes = [IsActiveAuthenticated]

    def get(self, request):
        page, page_size = parse_pagination(request.query_params)

        queryset = Article.objects.filter(author=request.user, is_deleted=False)
        articles, pagination = paginate_queryset(queryset, page, page_size)

        serializer = ArticleListSerializer(articles, many=True)
        return Response({**pagination, 'results': serializer.data})


# ===== 后台管理 Views =====

class AdminArticleListView(APIView):
    """后台文章管理列表"""
    permission_classes = [IsActiveAdmin]

    def get(self, request):
        page, page_size = parse_pagination(request.query_params)
        keyword = request.query_params.get('keyword', '')
        category_id = request.query_params.get('category', '')

        queryset = Article.objects.filter(is_deleted=False).select_related('author', 'category')

        if keyword:
            queryset = queryset.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword))
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        articles, pagination = paginate_queryset(queryset, page, page_size)

        serializer = ArticleListSerializer(articles, many=True)
        return Response({**pagination, 'results': serializer.data})


class AdminArticleDeleteView(APIView):
    """后台强制删除文章"""
    permission_classes = [IsActiveAdmin]

    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk, is_deleted=False)
        article.is_deleted = True
        article.save(update_fields=['is_deleted'])
        return Response({'message': '文章已强制删除'})
