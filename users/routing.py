from django.urls import re_path

from users import consumers

websocket_urlpatterns = [
    re_path(r"ws/fruit-shop/chat/$", consumers.ChatConsumer.as_asgi()),
]
