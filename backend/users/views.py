from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Q

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


# ===== 后台管理 Views =====

class AdminUserListView(APIView):
    """后台用户列表"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin':
            return Response({'message': '无权访问'}, status=status.HTTP_403_FORBIDDEN)

        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        keyword = request.query_params.get('keyword', '')
        user_status = request.query_params.get('status', '')

        queryset = User.objects.all().order_by('-date_joined')

        if keyword:
            queryset = queryset.filter(Q(username__icontains=keyword) | Q(email__icontains=keyword))
        if user_status:
            queryset = queryset.filter(status=user_status)

        total = queryset.count()
        total_pages = max(1, (total + page_size - 1) // page_size)

        start = (page - 1) * page_size
        end = start + page_size

        serializer = UserSerializer(queryset[start:end], many=True)
        return Response({
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'results': serializer.data,
        })


class AdminUserStatusView(APIView):
    """后台用户状态变更"""
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        if request.user.role != 'admin':
            return Response({'message': '无权操作'}, status=status.HTTP_403_FORBIDDEN)
        if str(request.user.id) == str(pk):
            return Response({'message': '不能禁用自己的账户'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, pk=pk)
        new_status = request.data.get('status')
        if new_status not in ('active', 'disabled'):
            return Response({'message': '无效的状态值'}, status=status.HTTP_400_BAD_REQUEST)

        user.status = new_status
        user.save(update_fields=['status'])
        return Response({'message': '用户状态更新成功'})
