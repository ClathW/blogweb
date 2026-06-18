from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from articles.models import Article
from config.pagination import paginate_queryset, parse_pagination
from users.permissions import IsActiveAdmin, IsActiveAuthenticated
from .models import Comment
from .serializers import CommentCreateSerializer, CommentListSerializer, CommentSerializer


class ArticleCommentListView(APIView):
    """文章评论列表"""
    permission_classes = [AllowAny]

    def get(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id, status='published', is_deleted=False)
        # 获取顶层评论（无父评论），预加载回复
        comments = Comment.objects.filter(
            article=article, parent=None, is_deleted=False
        ).prefetch_related(
            Prefetch(
                'replies',
                queryset=Comment.objects.filter(is_deleted=False).order_by('created_at'),
                to_attr='prefetched_replies',
            )
        ).order_by('created_at')

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CommentCreateView(APIView):
    """发表评论"""
    permission_classes = [IsActiveAuthenticated]

    def post(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id, status='published', is_deleted=False)

        serializer = CommentCreateSerializer(
            data=request.data,
            context={'request': request, 'article': article}
        )
        if serializer.is_valid():
            comment = serializer.save()
            # 更新文章评论计数
            article.comment_count = Comment.objects.filter(
                article=article, is_deleted=False
            ).count()
            article.save(update_fields=['comment_count'])

            return Response({
                'message': '评论发表成功',
                'comment': CommentSerializer(comment).data,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': '请求参数有误',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


class CommentDeleteView(APIView):
    """删除评论（本人或管理员）"""
    permission_classes = [IsActiveAuthenticated]

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, is_deleted=False)

        # 权限检查：评论作者或管理员
        if request.user != comment.user and request.user.role != 'admin':
            return Response({'message': '无权删除此评论'}, status=status.HTTP_403_FORBIDDEN)

        comment.is_deleted = True
        comment.save(update_fields=['is_deleted'])

        # 更新文章评论计数
        article = comment.article
        article.comment_count = Comment.objects.filter(
            article=article, is_deleted=False
        ).count()
        article.save(update_fields=['comment_count'])

        return Response({'message': '评论已删除'})


# ===== 后台管理 Views =====

class AdminCommentListView(APIView):
    """后台评论管理列表"""
    permission_classes = [IsActiveAdmin]

    def get(self, request):
        page, page_size = parse_pagination(request.query_params)
        keyword = request.query_params.get('keyword', '')
        article_id = request.query_params.get('article_id', '')

        queryset = Comment.objects.filter(is_deleted=False).select_related('user', 'article')

        if keyword:
            queryset = queryset.filter(content__icontains=keyword)
        if article_id:
            queryset = queryset.filter(article_id=article_id)

        comments, pagination = paginate_queryset(queryset, page, page_size)

        serializer = CommentListSerializer(comments, many=True)
        return Response({**pagination, 'results': serializer.data})


class AdminCommentDeleteView(APIView):
    """后台强制删除评论"""
    permission_classes = [IsActiveAdmin]

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, is_deleted=False)
        comment.is_deleted = True
        comment.save(update_fields=['is_deleted'])

        # 更新文章评论计数
        article = comment.article
        article.comment_count = Comment.objects.filter(
            article=article, is_deleted=False
        ).count()
        article.save(update_fields=['comment_count'])

        return Response({'message': '评论已强制删除'})
