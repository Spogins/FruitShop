from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from users import routing

# application = ProtocolTypeRouter({
#     "websocket": AllowedHostsOriginValidator(
#         AuthMiddlewareStack(URLRouter(routing))
#     ),
# })