import datetime

import channels.layers
from asgiref.sync import async_to_sync
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from bank.tasks import task_check_warehouse
from bank.models import Bank, Declaration



channel_layer = channels.layers.get_channel_layer()


# Create your views here.
def update_bank_account(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        bank = Bank.objects.first()
        if not request.GET.get('withdraw'):
            bank.amount += int(float(request.GET.get('amount')))
        else:
            bank.amount -= int(float(request.GET.get('amount')))
        bank.save()

        async_to_sync(channel_layer.group_send)(
            'shop_bank',
            {
                "type": "update.bank.account",
                "amount": bank.amount
            }
        )

        return JsonResponse({"updated_amount": bank.amount}, status=200)

def start_audit(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        user_id = request.GET.get('userId')
        if cache.get(f'user_{user_id}') is None:
            cache.set(f'user_{user_id}', 1)
            task_check_warehouse.delay(user_id)
            return JsonResponse({}, status=200)
        return JsonResponse({}, status=400)

def upload_declaration(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        Declaration.objects.create(file=request.FILES.get('file'), date=datetime.datetime.now())

        date = datetime.datetime.now()
        async_to_sync(channel_layer.group_send)(
            'shop_declaration',
            {
                "type": "upload.declaration",
                "count_docs": len(Declaration.objects.filter(
                    date__day=date.strftime('%d'),
                    date__month=date.strftime('%m'),
                    date__year=date.strftime('%Y'),
                ))
            }
        )
        return JsonResponse({}, status=200)
