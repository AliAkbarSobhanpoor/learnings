from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoom(models.Model):
    room_name = models.CharField(verbose_name="room_name", max_length=100)

    def __str__(self):
        return self.room_name


class RoomMessage(models.Model):
    room = models.ForeignKey(to=ChatRoom, on_delete=models.CASCADE, related_name='room_chats')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    body = models.CharField(verbose_name="message", max_length=300)
    create_time = models.DateTimeField(verbose_name="create_time", auto_now_add=True)


    def __str__(self):
        return f'{self.room.room_name}: {self.author.username}: {self.body[:15]}'

    class Meta:
        ordering = ['-create_time']