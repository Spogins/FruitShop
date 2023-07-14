from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.all():
            jocker = User.objects.create(
                username="jocker",
                first_name="Jocker",
                last_name="Jocker",
                email="jocker@jocker.com"
            )
            jocker.set_password('523164')
            jocker.save()
            print("jocker created")