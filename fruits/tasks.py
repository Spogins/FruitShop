import datetime
import random

import channels.layers
from asgiref.sync import async_to_sync
from django_celery_beat.models import IntervalSchedule, PeriodicTask, PeriodicTasks

from bank.models import Bank
from fruit_shop.celery import app
from fruits.models import Fruit, Log, Status, Operation

channel_layer = channels.layers.get_channel_layer()


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(6, task_buy_fruits.s(1))
    sender.add_periodic_task(9, task_buy_fruits.s(2))
    sender.add_periodic_task(12, task_buy_fruits.s(3))
    sender.add_periodic_task(15, task_buy_fruits.s(4))
    sender.add_periodic_task(15, task_sell_fruits.s(1))
    sender.add_periodic_task(12, task_sell_fruits.s(2))
    sender.add_periodic_task(9, task_sell_fruits.s(3))
    sender.add_periodic_task(6, task_sell_fruits.s(4))



@app.task
def task_buy_fruits(fruit_id, amount=None, cost_for_unit=None):
    amounts = [random.randint(1, 10), random.randint(10, 20), random.randint(1, 10), random.randint(5, 15)]
    price = [4, 1, 3, 2]
    fruit = Fruit.objects.get(pk=fruit_id)
    cost_for_unit = price[fruit_id-1] if cost_for_unit is None else cost_for_unit
    amount = amounts[fruit_id-1] if amount is None else amount
    bank = Bank.objects.first()
    usd = cost_for_unit * amount

    log = Log.objects.create(
        fruit=fruit,
        status=Status.ERROR if usd > bank.amount else Status.SUCCESS,
        date=datetime.datetime.now(),
        amount=amount,
        usd=usd,
        operation=Operation.BUY
    )

    async_to_sync(channel_layer.group_send)(
        'shop_fruit',
        {
            "type": "update.fruit",
            "status": log.get_status_display(),
            "fruit_id": fruit.id,
            "fruit_name": fruit.name,
            "date": log.date.strftime('%d.%m.%Y %H:%M'),
            "amount": amount,
            "usd": usd,
            "operation": log.get_operation_display()
        }
    )

    fruit.amount += amount
    bank.amount -= usd
    fruit.save()
    bank.save()

    async_to_sync(channel_layer.group_send)(
        'shop_bank',
        {
            "type": "update.bank.account",
            "amount": bank.amount
        }
    )
    return 'ok buy'


@app.task
def task_sell_fruits(fruit_id, amount=None, cost_for_unit=None):
    amounts = [random.randint(1, 10), random.randint(1, 30), random.randint(1, 10), random.randint(1, 20)]
    price = [5, 2, 4, 3]
    fruit = Fruit.objects.get(pk=fruit_id)
    cost_for_unit = price[fruit_id-1] if cost_for_unit is None else cost_for_unit
    amount = amounts[fruit_id-1] if amount is None else amount
    bank = Bank.objects.first()
    usd = cost_for_unit * amount

    log = Log.objects.create(
        fruit=fruit,
        status=Status.ERROR if amount > fruit.amount else Status.SUCCESS,
        date=datetime.datetime.now(),
        amount=amount,
        usd=usd,
        operation=Operation.SELL
    )

    async_to_sync(channel_layer.group_send)(
        'shop_fruit',
        {
            "type": "update.fruit",
            "status": log.get_status_display(),
            "fruit_id": fruit.id,
            "fruit_name": fruit.name,
            "date": log.date.strftime('%d.%m.%Y %H:%M'),
            "amount": amount,
            "usd": usd,
            "operation": log.get_operation_display()
        }
    )
    if not log.get_status_display() == 'ERROR':
        fruit.amount -= amount
        bank.amount += usd
    fruit.save()
    bank.save()

    async_to_sync(channel_layer.group_send)(
        'shop_bank',
        {
            "type": "update.bank.account",
            "amount": bank.amount
        }
    )

    return 'ok sell'

