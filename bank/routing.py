from django.urls import re_path

from bank.consumers import BankConsumer

websocket_urlpatterns = [
    re_path(r"ws/fruit-shop/bank/$", BankConsumer.as_asgi()),
]