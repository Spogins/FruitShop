from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.all():
            admin = User.objects.create(
                username="admin",
                first_name="Admin",
                last_name="Admin",
                email="admin@admin.com",
                is_staff=True,
                is_superuser=True,
            )
            admin.set_password('fruit5231')
            admin.save()
            print('Admin created')
            
            user = User.objects.create(
                username="lastatar",
                first_name="Ostin",
                last_name="Pawers",
                email="user@user.com"
            )
            user.set_password('fruit5231')
            user.save()
            print('User created')

            jocker = User.objects.create(
                username="jocker",
                first_name="Jocker",
                last_name="Jocker",
                email="jocker@jocker.com"
            )
            jocker.set_password('fruit5231')
            jocker.save()
            print("Jocker created")
            print('Users created')