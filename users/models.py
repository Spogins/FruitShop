import datetime


from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст')
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-date']