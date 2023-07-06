import datetime
import random

import channels.layers
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from django.shortcuts import render
from fruits.tasks import task_buy_fruits, task_sell_fruits
from bank.models import Bank
from fruits.models import Operation, Status, Log, Fruit

# Create your views here.
channel_layer = channels.layers.get_channel_layer()


def buy_or_sell_fruits(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        cost_for_unit = random.choice(range(1, 5))
        fruit = Fruit.objects.get(pk=request.GET.get('fruit_id'))
        amount = int(request.GET.get('amount'))
        bank = Bank.objects.first()
        usd = cost_for_unit * amount

        if usd > bank.amount and request.GET.get('type') == 'buy':
            log = Log.objects.create(
                fruit=fruit,
                status=Status.ERROR if usd > bank.amount or amount > fruit.amount else Status.SUCCESS,
                date=datetime.datetime.now(),
                amount=amount,
                usd=usd,
                operation=Operation.BUY if request.GET.get('type') == 'buy' else Operation.SELL
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
            return JsonResponse(
                {"message": "Недостаточно средств на счету, закупка отменена." if request.GET.get('type') == 'buy' else
                            "Недостаточно товара на складе, продажа отменена."},
                status=400
            )

        if request.GET.get('type') == 'buy':
            task_buy_fruits.delay(fruit.id, amount, cost_for_unit)
        else:
            task_sell_fruits.delay(fruit.id, amount, cost_for_unit)

        return JsonResponse(
            {'message': 'Покупка успешна' if request.GET.get('type') == 'buy' else 'Продажа успешна'},
            status=200
        )