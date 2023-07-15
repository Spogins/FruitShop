from django.core.management.base import BaseCommand

from fruits.models import Fruit


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Fruit.objects.all():
            apple = Fruit.objects.create(
                name='Яблоки',
                amount=100
            )
            apple.save()
            print('Apple created')
            banana = Fruit.objects.create(
                name='Бананы',
                amount=100
            )
            banana.save()
            print('Banana created')
            pineapple = Fruit.objects.create(
                name='Ананасы',
                amount=100
            )
            pineapple.save()
            print('Pineapple created')
            peach = Fruit.objects.create(
                name='Персики',
                amount=100
            )
            peach.save()
            print('Peach created')
            print('Fruit created')
