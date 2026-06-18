from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import (
    LoginSerializer,
    PasswordChangeSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    UserSerializer,
)


class RegisterView(APIView):
    """用户注册"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': '注册成功',
                'user': UserSerializer(user).data,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': '请求参数有误',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """用户登录"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({
                'message': '登录成功',
                'user': UserSerializer(user).data,
            })
        return Response({
            'message': '用户名或密码错误',
            'errors': serializer.errors,
        }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """用户登出"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': '已登出'})


class UserProfileView(APIView):
    """个人信息查看与修改"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': '个人信息更新成功',
                'user': UserSerializer(request.user).data,
            })
        return Response({
            'message': '请求参数有误',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    """修改密码"""
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': '密码修改成功'})
        return Response({
            'message': '请求参数有误',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


class UserCheckView(APIView):
    """检查当前登录状态"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'is_authenticated': True,
            'user': UserSerializer(request.user).data,
        })
