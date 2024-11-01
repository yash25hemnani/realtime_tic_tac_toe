import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tic_Tac_Toe.settings')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tic_Tac_Toe.settings')
django.setup()

django_asgi_app = get_asgi_application()

import base.routing

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    raise Exception("DJANGO_SETTINGS_MODULE not set")

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(URLRouter(
        base.routing.websocket_urlpatterns
    ))
})

