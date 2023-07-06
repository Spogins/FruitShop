"""
ASGI config for fruit_shop project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from bank import routing as routing_bank
from fruits import routing as routing_fruit
from users import routing as routing_user

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fruit_shop.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(
            routing_user.websocket_urlpatterns
            + routing_fruit.websocket_urlpatterns
            + routing_bank.websocket_urlpatterns
        ))
    ),
})


