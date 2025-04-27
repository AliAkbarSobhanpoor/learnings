from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path("ws/chat/room/<room_name>/", ChatRoomConsumer.as_asgi()),
]