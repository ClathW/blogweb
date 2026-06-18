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

        existing_user = User.objects.filter(username=username).first()
        if existing_user:
            changed_fields = []
            if existing_user.role != 'admin':
                existing_user.role = 'admin'
                changed_fields.append('role')
            if not existing_user.is_staff:
                existing_user.is_staff = True
                changed_fields.append('is_staff')
            if not existing_user.is_superuser:
                existing_user.is_superuser = True
                changed_fields.append('is_superuser')
            if changed_fields:
                existing_user.save(update_fields=changed_fields)
                self.stdout.write(self.style.SUCCESS(f'用户 {username} 已提升为管理员'))
            else:
                self.stdout.write(self.style.WARNING(f'用户 {username} 已存在，跳过创建'))
            return

        User.objects.create_superuser(username=username, password=password, email=email, role='admin')
        self.stdout.write(self.style.SUCCESS(f'管理员已创建: {username} / {password}'))
