# Generated by Django 4.2.2 on 2023-07-03 11:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fruit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Название')),
                ('amount', models.IntegerField(verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Фрукт',
                'verbose_name_plural': 'Фрукты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('SS', 'SUCCESS'), ('ER', 'ERROR')], default='SS', max_length=2, verbose_name='Статус')),
                ('date', models.DateTimeField(default=datetime.datetime(2023, 7, 3, 11, 37, 28, 943492), verbose_name='Дата')),
                ('amount', models.IntegerField(verbose_name='Кол-во фруктов')),
                ('usd', models.IntegerField(verbose_name='Сумма USD')),
                ('operation', models.CharField(choices=[('B', 'BUY'), ('S', 'SELL')], default='B', max_length=1)),
                ('fruit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='fruits.fruit', verbose_name='Фрукт')),
            ],
            options={
                'verbose_name': 'Лог',
                'verbose_name_plural': 'Логи',
                'ordering': ['date'],
            },
        ),
    ]
