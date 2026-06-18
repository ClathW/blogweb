from django.urls import path
from . import views

urlpatterns = [
    path('articles/<int:article_id>/comments/', views.ArticleCommentListView.as_view(), name='article-comments'),
    path('articles/<int:article_id>/comments/create/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/', views.CommentDeleteView.as_view(), name='comment-delete'),
    # 后台管理
    path('admin/comments/', views.AdminCommentListView.as_view(), name='admin-comments'),
    path('admin/comments/<int:pk>/', views.AdminCommentDeleteView.as_view(), name='admin-comment-delete'),
]
