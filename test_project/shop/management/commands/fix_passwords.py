from django.core.management.base import BaseCommand
from shop.models import User

class Command(BaseCommand):
    help = 'Хеширует сырые пароли у пользователей, созданных через seed.sql'

    def handle(self, *args, **options):
        for user in User.objects.all():
            # Если пароль не начинается с хеша Django
            if not user.password.startswith('pbkdf2_'):
                raw = user.password
                user.set_password(raw)
                user.save()
                self.stdout.write(f'Исправлен пароль для {user.username}')