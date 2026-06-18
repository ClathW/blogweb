from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('articles/', views.ArticleListView.as_view(), name='article-list'),
    path('articles/my/', views.MyArticlesView.as_view(), name='my-articles'),
    path('articles/create/', views.ArticleCreateView.as_view(), name='article-create'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('articles/<int:pk>/edit/', views.ArticleEditView.as_view(), name='article-edit'),
]
