import json

from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string

from .models import ChatRoom, RoomMessage

class ChatRoomConsumer(AsyncWebsocketConsumer):
    """
        the main socket consumer for chat rooms
        structer is this way:
            - main setting of the code like connection and disconnect and receive and ....
            - handlers that send data back with websocket
            - database function calls . are the database ORMs that are capsuled in functions because of the
                async structure of the code.
    """

    # | ----------------------------------------------------------------------------------------------------------- | #
    # |                                               mains                                                         | #
    # | ----------------------------------------------------------------------------------------------------------- | #

    async def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room = await database_sync_to_async(get_object_or_404)(ChatRoom, room_name=self.room_name)
        await self.channel_layer.group_add(self.room_name, self.channel_name)

        # implementation of the update online users : add
        if not await self.is_user_online():
            await self.add_user_to_online_users()
            await self.update_online_user_count()

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        # implementation of the update online users : remove
        if await self.is_user_online():
            await self.remove_user_from_online_users()
            await self.update_online_user_count()

    async def receive(self, text_data):
        # get sent data from client here . text_data is in json format
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
        await self.channel_layer.group_send(self.room_name, event)

    async def update_online_user_count(self):
        online_count = await self.get_online_user_count()
        event = {
            "type": "online.count.handler",
            "online_count": online_count,
        }
        await self.channel_layer.group_send(
            self.room_name, event
        )

    # | ----------------------------------------------------------------------------------------------------------- | #
    # |                                               handlers                                                      | #
    # | ----------------------------------------------------------------------------------------------------------- | #

    async def message_handler(self, event):
        message_id = event["message_id"]
        message = await RoomMessage.objects.aget(id=message_id)
        context = {"message": message, "user": self.user}
        html = await self.render_partial("rt_chat/partials/htmx_response_chat.html", context)
        await self.send(text_data=html)

    async def online_count_handler(self, event):
        context = {"online_count": event["online_count"] }
        html = await self.render_partial("rt_chat/partials/online_count.html", context)
        await self.send(text_data=html)

    # | ----------------------------------------------------------------------------------------------------------- | #
    # |                                              ORM cals                                                       | #
    # | ----------------------------------------------------------------------------------------------------------- | #

    @database_sync_to_async
    def is_user_online(self):
        return self.room.online_users.filter(id=self.user.id).exists()

    @database_sync_to_async
    def add_user_to_online_users(self):
        self.room.online_users.add(self.user)

    @database_sync_to_async
    def remove_user_from_online_users(self):
        self.room.online_users.remove(self.user)

    @database_sync_to_async
    def get_online_user_count(self):
        return self.room.online_users.count() - 1

    @database_sync_to_async
    def render_partial(self, partial_dir, context):
        return render_to_string(partial_dir, context=context)
