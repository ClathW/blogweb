from django.urls import path
from . import views

urlpatterns = [
    # 认证
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/check/', views.UserCheckView.as_view(), name='auth-check'),
    # 个人信息
    path('user/profile/', views.UserProfileView.as_view(), name='profile'),
    path('user/password/', views.PasswordChangeView.as_view(), name='password-change'),
    # 后台管理
    path('admin/users/', views.AdminUserListView.as_view(), name='admin-users'),
    path('admin/users/<int:pk>/status/', views.AdminUserStatusView.as_view(), name='admin-user-status'),
]
