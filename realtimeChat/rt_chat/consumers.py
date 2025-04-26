import json

from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string

from .models import ChatRoom, RoomMessage

class ChatRoomConsumer(AsyncWebsocketConsumer):
    # connect method
    async def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room = await database_sync_to_async(get_object_or_404)(ChatRoom, room_name=self.room_name)

        await self.channel_layer.group_add(
            self.room_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name, self.channel_name
        )

    # get sent data from client here . text_data is in json format
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json["body"]
        message = await RoomMessage.objects.acreate(
            body=body,
            author=self.user,
            room=self.room
        )
        event = {
            "type": "message.handler",
            "message_id": message.id,
        }
        await self.channel_layer.group_send(
            self.room_name, event
        )

    async def message_handler(self, event):
        message_id = event["message_id"]
        message = await RoomMessage.objects.aget(id=message_id)
        context = {"message": message, "user": self.user}
        html = await database_sync_to_async(render_to_string)("rt_chat/partials/htmx_response_chat.html", context=context)
        await self.send(text_data=html)
