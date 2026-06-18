from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, max_length=20, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, min_length=6, max_length=20)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'email']

    def validate_username(self, value):
        if len(value) < 3 or len(value) > 20:
            raise serializers.ValidationError('用户名长度须为3-20个字符')
        if not value.replace('_', '').isalnum():
            raise serializers.ValidationError('用户名仅支持字母、数字和下划线')
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('该用户名已被注册')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('该邮箱已被注册')
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': '两次密码输入不一致'})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=20)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError('用户名和密码不能为空')

        # 支持用户名或邮箱登录
        user = None
        if '@' in username:
            try:
                u = User.objects.get(email=username)
                user = authenticate(request=self.context.get('request'), username=u.username, password=password)
            except User.DoesNotExist:
                pass
        else:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

        if not user:
            raise serializers.ValidationError('用户名或密码错误')

        if user.status == 'disabled':
            raise serializers.ValidationError('账户已被禁用，请联系管理员')

        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'status', 'bio', 'avatar', 'date_joined']
        read_only_fields = ['id', 'username', 'email', 'role', 'status', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'avatar']
        read_only_fields = ['username', 'email']

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(id=user.id).filter(email=value).exists():
            raise serializers.ValidationError('该邮箱已被其他用户使用')
        return value


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, min_length=6, max_length=20)
    new_password = serializers.CharField(write_only=True, min_length=6, max_length=20)
    confirm_password = serializers.CharField(write_only=True, min_length=6, max_length=20)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': '两次密码输入不一致'})
        return data

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('原密码错误')
        return value
