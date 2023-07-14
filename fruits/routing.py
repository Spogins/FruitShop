from django.urls import re_path

from fruits.consumers import FruitConsumer, TestConsumer

websocket_urlpatterns = [
    re_path(r"ws/fruit-shop/fruit/$", FruitConsumer.as_asgi()),
]