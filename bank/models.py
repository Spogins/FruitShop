from django.db import models


# Create your models here.
class Bank(models.Model):
    amount = models.IntegerField(verbose_name='Amount USD')

    class Meta:
        verbose_name = 'Банк'