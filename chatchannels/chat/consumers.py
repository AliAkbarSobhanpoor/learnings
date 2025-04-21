import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from . import models

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # get the received data here and. send it to type model to send the data one by one.
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        user = self.scope['user']
        real_user = user if user.is_authenticated else None
        print(user)
        room = self.room_name
        print(room)
        time = datetime.now().isoformat()
        print(time)
        await self.save_message(real_user, room, message, time)
        await self.channel_layer.group_send(self.room_group_name, {"type": "chat.message", "message": message, "user": user.username if user.is_authenticated else "Anonymous", "time":time},)

    # this is the model that send data to all consumers the data that is send come from group send
    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        time = event['time']
        await self.send(text_data=json.dumps({"message": message, "user": user, "time": time}))

    @database_sync_to_async
    def save_message(self, user, room, message, time):
        if user:
            models.ChatMessage.objects.create(user=user, room=room, message=message, timestamp=time)
        else:
            models.ChatMessage.objects.create(room=room, message=message, timestamp=time)

# sync version of the django channels channel work.
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'
#
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, self.channel_name
#         )
#         self.accept()
#
#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )
#
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name, {
#                 'type': 'chat_message',
#                 'message': message,
#             }
#         )
#
#     def chat_message(self, event):
#         message = event['message']
#         self.send(text_data=json.dumps({"message": message,}))
