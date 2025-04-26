from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path("ws/chatroom/<room_name>/", ChatRoomConsumer.as_asgi()),
]