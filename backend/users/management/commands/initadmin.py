from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = '创建默认管理员账号（如不存在）'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='admin', help='管理员用户名')
        parser.add_argument('--password', default='admin123', help='管理员密码')
        parser.add_argument('--email', default='admin@blogweb.com', help='管理员邮箱')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'用户 {username} 已存在，跳过创建'))
            return

        User.objects.create_superuser(username=username, password=password, email=email)
        self.stdout.write(self.style.SUCCESS(f'管理员已创建: {username} / {password}'))
