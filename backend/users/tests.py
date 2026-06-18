from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserModelTests(TestCase):
    """用户模型测试"""

    def test_create_user(self):
        user = User.objects.create_user(username='testuser', password='test123456', email='test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'user')
        self.assertEqual(user.status, 'active')
        self.assertTrue(user.check_password('test123456'))

    def test_create_superuser(self):
        user = User.objects.create_superuser(username='admin', password='admin123', email='admin@example.com')
        self.assertEqual(user.role, 'user')  # create_superuser doesn't auto-set role
        user.role = 'admin'
        user.save()
        self.assertEqual(user.role, 'admin')
        self.assertTrue(user.is_staff)

    def test_user_str(self):
        user = User.objects.create_user(username='testuser', password='test123456')
        self.assertEqual(str(user), 'testuser')

    def test_default_role(self):
        user = User.objects.create_user(username='user1', password='test123456')
        self.assertEqual(user.role, 'user')
        self.assertEqual(user.status, 'active')


class AuthAPITests(TestCase):
    """认证API测试"""

    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.logout_url = '/api/auth/logout/'
        self.check_url = '/api/auth/check/'
        self.profile_url = '/api/user/profile/'
        self.password_url = '/api/user/password/'

    def test_register_success(self):
        data = {
            'username': 'newuser',
            'password': 'test123456',
            'confirm_password': 'test123456',
            'email': 'new@example.com',
        }
        res = self.client.post(self.register_url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['message'], '注册成功')
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_duplicate_username(self):
        User.objects.create_user(username='existing', password='test123456')
        data = {
            'username': 'existing',
            'password': 'test123456',
            'confirm_password': 'test123456',
            'email': 'e@example.com',
        }
        res = self.client.post(self.register_url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_password_mismatch(self):
        data = {
            'username': 'user1',
            'password': 'abc123',
            'confirm_password': 'abc124',
            'email': 'u@example.com',
        }
        res = self.client.post(self.register_url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_short_username(self):
        data = {
            'username': 'ab',
            'password': 'test123456',
            'confirm_password': 'test123456',
            'email': 'u@example.com',
        }
        res = self.client.post(self.register_url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_short_password(self):
        data = {
            'username': 'validuser',
            'password': 'ab',
            'confirm_password': 'ab',
            'email': 'u@example.com',
        }
        res = self.client.post(self.register_url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success_with_username(self):
        User.objects.create_user(username='loginuser', password='test123456')
        res = self.client.post(self.login_url, {'username': 'loginuser', 'password': 'test123456'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['message'], '登录成功')

    def test_login_success_with_email(self):
        User.objects.create_user(username='loginuser', password='test123456', email='login@example.com')
        res = self.client.post(self.login_url, {'username': 'login@example.com', 'password': 'test123456'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_login_wrong_password(self):
        User.objects.create_user(username='loginuser', password='test123456')
        res = self.client.post(self.login_url, {'username': 'loginuser', 'password': 'wrongpass'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_disabled_user(self):
        user = User.objects.create_user(username='disabled', password='test123456', status='disabled')
        res = self.client.post(self.login_url, {'username': 'disabled', 'password': 'test123456'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_rate_limit_locks_after_5_failures(self):
        User.objects.create_user(username='locktest', password='rightpass')
        for _ in range(5):
            res = self.client.post(self.login_url, {'username': 'locktest', 'password': 'wrong'}, format='json')
            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # 6th attempt should say locked
        res = self.client.post(self.login_url, {'username': 'locktest', 'password': 'rightpass'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('锁定', res.data['message'])

    def test_login_rate_limit_resets_on_success(self):
        User.objects.create_user(username='resettest', password='rightpass')
        # Fail 3 times
        for _ in range(3):
            self.client.post(self.login_url, {'username': 'resettest', 'password': 'wrong'}, format='json')
        # Success resets counter
        res = self.client.post(self.login_url, {'username': 'resettest', 'password': 'rightpass'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_check_auth_authenticated(self):
        user = User.objects.create_user(username='authuser', password='test123456')
        self.client.force_authenticate(user=user)
        res = self.client.get(self.check_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data['is_authenticated'])

    def test_check_auth_unauthenticated(self):
        res = self.client.get(self.check_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_profile(self):
        user = User.objects.create_user(username='profileuser', password='test123456', email='p@example.com')
        self.client.force_authenticate(user=user)
        res = self.client.get(self.profile_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['username'], 'profileuser')

    def test_update_profile(self):
        user = User.objects.create_user(username='profileuser', password='test123456')
        self.client.force_authenticate(user=user)
        res = self.client.put(self.profile_url, {'bio': 'Hello World', 'avatar': 'https://example.com/avatar.jpg'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.bio, 'Hello World')

    def test_change_password_success(self):
        user = User.objects.create_user(username='pwuser', password='oldpass123')
        self.client.force_authenticate(user=user)
        res = self.client.put(self.password_url, {
            'old_password': 'oldpass123',
            'new_password': 'newpass456',
            'confirm_password': 'newpass456',
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.check_password('newpass456'))

    def test_change_password_wrong_old(self):
        user = User.objects.create_user(username='pwuser', password='oldpass123')
        self.client.force_authenticate(user=user)
        res = self.client.put(self.password_url, {
            'old_password': 'wrongpass',
            'new_password': 'newpass456',
            'confirm_password': 'newpass456',
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_mismatch(self):
        user = User.objects.create_user(username='pwuser', password='oldpass123')
        self.client.force_authenticate(user=user)
        res = self.client.put(self.password_url, {
            'old_password': 'oldpass123',
            'new_password': 'newpass456',
            'confirm_password': 'different',
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class AdminAPITests(TestCase):
    """后台管理API测试"""

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(username='admin', password='admin123', role='admin')
        self.normal_user = User.objects.create_user(username='normal', password='normal123', role='user')

    def test_admin_list_users(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.get('/api/admin/users/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(res.data['count'], 2)

    def test_admin_list_users_forbidden(self):
        self.client.force_authenticate(user=self.normal_user)
        res = self.client.get('/api/admin/users/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_update_user_status(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.put(
            f'/api/admin/users/{self.normal_user.id}/status/',
            {'status': 'disabled'}, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.normal_user.refresh_from_db()
        self.assertEqual(self.normal_user.status, 'disabled')

    def test_admin_cannot_disable_self(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.put(
            f'/api/admin/users/{self.admin.id}/status/',
            {'status': 'disabled'}, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_filter_users_by_keyword(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.get('/api/admin/users/?keyword=normal')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)

    def test_admin_filter_users_by_status(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.get('/api/admin/users/?status=active')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(res.data['count'], 2)
