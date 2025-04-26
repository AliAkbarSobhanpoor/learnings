from contextlib import nullcontext

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoom(models.Model):
    """
        the room for messages : can create in two ways:
            1. based on the room name
            2. based on the users (PV) : todo: implement this
        model include this fields:
            : room_name : the main room name . fill for private and protected rooms.
            : online_users : show the online users of the room
    """
    room_name = models.CharField(verbose_name="room_name", max_length=100)
    online_users = models.ManyToManyField(User, related_name="online_users", blank=True)

    def __str__(self):
        return self.room_name


class RoomMessage(models.Model):
    """
        user messages are saved here . each message has this property:
            : room : the instance of ChatRoom model . indicate to message room
            : author : the creator of the message
            : body : the message content
            : create_time : the time that this message was created
    """
    room = models.ForeignKey(to=ChatRoom, on_delete=models.CASCADE, related_name='room_chats')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    body = models.CharField(verbose_name="message", max_length=300)
    create_time = models.DateTimeField(verbose_name="create_time", auto_now_add=True)


    def __str__(self):
        return f'{self.room.room_name}: {self.author.username}: {self.body[:15]}'

    class Meta:
        ordering = ['-create_time']