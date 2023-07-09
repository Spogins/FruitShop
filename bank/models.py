from django.db import models


# Create your models here.
class Bank(models.Model):
    amount = models.IntegerField(verbose_name='Amount USD')

    class Meta:
        verbose_name = 'Банк'


class Declaration(models.Model):
    file = models.FileField(upload_to='files/', verbose_name='Декларация')
    date = models.DateTimeField(verbose_name='Дата')

    class Meta:
        verbose_name = 'Декларация'
        verbose_name_plural = 'Декларации'
        ordering = ['-date']