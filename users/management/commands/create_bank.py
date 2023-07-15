from django.core.management.base import BaseCommand

from bank.models import Bank


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Bank.objects.all():
            bank = Bank.objects.create(
                amount=5000
            )
            bank.save()
            print('Bank created')
