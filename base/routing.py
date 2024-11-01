from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/sc/<str:roomCode>', consumers.MySyncConsumer.as_asgi())
]