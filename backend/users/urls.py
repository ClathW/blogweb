from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/check/', views.UserCheckView.as_view(), name='auth-check'),
    path('user/profile/', views.UserProfileView.as_view(), name='profile'),
    path('user/password/', views.PasswordChangeView.as_view(), name='password-change'),
]
