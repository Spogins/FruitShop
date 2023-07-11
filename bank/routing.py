from django.urls import re_path

from bank.consumers import BankConsumer, DeclarationConsumer, AuditConsumer

websocket_urlpatterns = [
    re_path(r"ws/fruit-shop/declaration/$", DeclarationConsumer.as_asgi()),
    re_path(r"ws/fruit-shop/bank/$", BankConsumer.as_asgi()),
    re_path(r"ws/fruit-shop/(?P<room_name>\w+)/$", AuditConsumer.as_asgi()),
]